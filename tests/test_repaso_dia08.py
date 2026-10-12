import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


RUTA_SCRIPT = Path(__file__).resolve().parents[1] / "semana-01" / "repaso_dia08.py"
ESPECIFICACION = importlib.util.spec_from_file_location("repaso_dia08", RUTA_SCRIPT)
registro = importlib.util.module_from_spec(ESPECIFICACION)
ESPECIFICACION.loader.exec_module(registro)


class PruebasRegistro(unittest.TestCase):
    def setUp(self):
        temporal = tempfile.TemporaryDirectory(prefix="pruebas-registro-")
        self.addCleanup(temporal.cleanup)
        self.carpeta = Path(temporal.name)
        self.archivo = self.carpeta / "sesiones.json"

        # Todas las funciones usan el JSON temporal, nunca el historial personal.
        ruta_temporal = patch.object(registro, "ARCHIVO_SESIONES", self.archivo)
        ruta_temporal.start()
        self.addCleanup(ruta_temporal.stop)

        self.sesiones = [
            {"asignatura": "Matemáticas", "minutos": 20},
            {"asignatura": "Programación", "minutos": 35},
        ]

    def ejecutar_menu(self, respuestas):
        salida = io.StringIO()
        with patch("builtins.input", side_effect=respuestas):
            with contextlib.redirect_stdout(salida):
                registro.main()
        return salida.getvalue()

    def comprobar_error_inicio(self, mensaje):
        salida = io.StringIO()
        with patch("builtins.input") as entrada:
            with patch.object(registro, "guardar_sesiones") as guardar:
                with contextlib.redirect_stdout(salida):
                    with self.assertRaises(SystemExit) as error:
                        registro.main()
        self.assertEqual(error.exception.code, 1)
        self.assertIn(mensaje, salida.getvalue())
        self.assertIn("sin modificar el historial", salida.getvalue())
        entrada.assert_not_called()
        guardar.assert_not_called()

    def comprobar_sin_temporales(self):
        self.assertEqual(list(self.carpeta.glob(".sesiones-*.tmp")), [])

    def test_cargar_sin_archivo(self):
        self.assertEqual(registro.cargar_sesiones(), [])
        self.assertFalse(self.archivo.exists())

    def test_guardar_y_recuperar_sesiones(self):
        registro.guardar_sesiones(self.sesiones)
        self.assertEqual(registro.cargar_sesiones(), self.sesiones)
        self.comprobar_sin_temporales()

    def test_registrar_conserva_sesiones_anteriores(self):
        registro.guardar_sesiones(self.sesiones)
        salida = self.ejecutar_menu(["1", "1", "Historia", "10", "2", "3"])
        esperadas = self.sesiones + [{"asignatura": "Historia", "minutos": 10}]
        self.assertEqual(registro.cargar_sesiones(), esperadas)
        for mensaje in (
            "El total de minutos estudiados es de: 65",
            "Usted ha estudiado: 2 de menos de 30 minutos",
            "Ha realizado: 1 sesiones completas",
            "Duraciones: [20, 35, 10]",
            "Duracion media: 21.666666666666668 minutos",
            "Sesion mas larga: 35 minutos",
            "Sesion mas corta: 10 minutos",
            "Asignatura: Matemáticas\nDuracion: 20 minutos\nSesion corta",
            "Asignatura: Programación\nDuracion: 35 minutos\nSesion completa",
            "Asignatura: Historia\nDuracion: 10 minutos\nSesion corta",
        ):
            # Se muestra al acabar el registro y al elegir consultar.
            self.assertEqual(salida.count(mensaje), 2)

    def test_guarda_despues_de_cada_sesion(self):
        historiales_guardados = []
        guardar_original = registro.guardar_sesiones

        def guardar_y_comprobar(sesiones):
            guardar_original(sesiones)
            historiales_guardados.append(registro.cargar_sesiones())

        with patch.object(registro, "guardar_sesiones", side_effect=guardar_y_comprobar):
            self.ejecutar_menu(["1", "2", "Matemáticas", "20", "Programación", "35", "3"])
        self.assertEqual(historiales_guardados, [self.sesiones[:1], self.sesiones])

    def test_rechaza_historial_invalido_sin_modificarlo(self):
        invalidos = [None, {}, "texto", [1], [[]], [{}]]
        invalidos += [
            [{"asignatura": asignatura, "minutos": 20}]
            for asignatura in ("", "   ", "\t\n", None, 123, True)
        ]
        invalidos += [
            [{"asignatura": "Python", "minutos": minutos}]
            for minutos in (0, -1, 20.0, "20", None, True, False)
        ]
        invalidos += [[{"asignatura": "Python"}], [{"minutos": 20}]]
        invalidos += [self.sesiones + [{"asignatura": "Python", "minutos": True}]]
        contenidos = [b'{"sesiones": roto\r\n', b"", b"\xff\xfe\x00"]
        contenidos += [json.dumps(valor).encode("utf-8") for valor in invalidos]

        for contenido in contenidos:
            with self.subTest(contenido=contenido):
                self.archivo.write_bytes(contenido)
                modificacion = self.archivo.stat().st_mtime_ns
                self.comprobar_error_inicio("Error en")
                self.assertEqual(self.archivo.read_bytes(), contenido)
                self.assertEqual(self.archivo.stat().st_mtime_ns, modificacion)
                self.comprobar_sin_temporales()

    def test_consultar_historial_vacio_sin_crear_archivo(self):
        with patch.object(registro, "guardar_sesiones") as guardar:
            salida = self.ejecutar_menu(["2", "3"])
        guardar.assert_not_called()
        self.assertIn("No hay sesiones", salida)
        self.assertIn("El total de minutos estudiados es de: 0", salida)
        self.assertNotIn("Duracion media:", salida)
        self.assertNotIn("Sesion mas larga:", salida)
        self.assertNotIn("Sesion mas corta:", salida)
        self.assertFalse(self.archivo.exists())

    def test_consultar_lista_vacia_existente_no_escribe(self):
        contenido = b"  [ ]\n"
        self.archivo.write_bytes(contenido)
        modificacion = self.archivo.stat().st_mtime_ns
        with patch.object(registro, "guardar_sesiones") as guardar:
            salida = self.ejecutar_menu(["2", "3"])
        guardar.assert_not_called()
        self.assertIn("No hay sesiones", salida)
        self.assertIn("El total de minutos estudiados es de: 0", salida)
        self.assertEqual(self.archivo.read_bytes(), contenido)
        self.assertEqual(self.archivo.stat().st_mtime_ns, modificacion)

    def test_consultar_historial_completo_no_escribe(self):
        contenido = ("  " + json.dumps(self.sesiones, ensure_ascii=False) + "\n").encode("utf-8")
        self.archivo.write_bytes(contenido)
        modificacion = self.archivo.stat().st_mtime_ns
        with patch.object(registro, "guardar_sesiones") as guardar:
            salida = self.ejecutar_menu(["2", "2", "3"])
        guardar.assert_not_called()
        for mensaje in (
            "El total de minutos estudiados es de: 55",
            "Asignatura: Matemáticas\nDuracion: 20 minutos\nSesion corta",
            "Asignatura: Programación\nDuracion: 35 minutos\nSesion completa",
        ):
            self.assertEqual(salida.count(mensaje), 2)
        self.assertEqual(self.archivo.read_bytes(), contenido)
        self.assertEqual(self.archivo.stat().st_mtime_ns, modificacion)

    def test_opcion_invalida_vuelve_a_pedir_opcion(self):
        salida = self.ejecutar_menu(["", "texto", "0", "4", "1.5", " 2 ", "3"])
        self.assertEqual(salida.count("Opción inválida. Elige 1, 2 o 3."), 5)
        self.assertEqual(salida.count("No hay sesiones"), 1)
        self.assertFalse(self.archivo.exists())

    def test_validaciones_de_registro_y_limite_de_30_minutos(self):
        salida = self.ejecutar_menu([
            "1", "0", "texto", "1", "", "   ", "  Python  ",
            "", "texto", "3.5", "0", "-5", "30", "3",
        ])
        self.assertEqual(registro.cargar_sesiones(), [{"asignatura": "Python", "minutos": 30}])
        self.assertEqual(salida.count("Introduce una asignatura que no este vacia"), 2)
        self.assertEqual(salida.count("Introduce un numero, por favor"), 4)
        self.assertEqual(salida.count("Introduce un numero positivo"), 3)
        self.assertIn("Usted ha estudiado: 0 de menos de 30 minutos", salida)
        self.assertIn("Ha realizado: 1 sesiones completas", salida)

    def test_error_de_lectura_no_es_historial_inexistente(self):
        self.archivo.mkdir()
        self.comprobar_error_inicio("No se pudo leer")
        self.assertTrue(self.archivo.is_dir())
        self.assertEqual(list(self.archivo.iterdir()), [])

    def test_permiso_de_lectura_denegado_simulado(self):
        with patch.object(Path, "open", side_effect=PermissionError("permiso denegado")):
            self.comprobar_error_inicio("No se pudo leer")
        self.assertFalse(self.archivo.exists())

    def test_fallo_de_escritura_conserva_original(self):
        registro.guardar_sesiones(self.sesiones)
        contenido = self.archivo.read_bytes()

        def escribir_parcial(sesiones, archivo, **opciones):
            self.assertEqual(Path(archivo.name).parent, self.carpeta)
            archivo.write('[{"asignatura":')
            raise OSError("fallo de escritura simulado")

        with patch.object(registro.json, "dump", side_effect=escribir_parcial):
            with self.assertRaises(OSError):
                registro.guardar_sesiones(self.sesiones + [{"asignatura": "Historia", "minutos": 10}])
        self.assertEqual(self.archivo.read_bytes(), contenido)
        self.comprobar_sin_temporales()

    def test_fallo_de_reemplazo_conserva_original(self):
        registro.guardar_sesiones(self.sesiones)
        contenido = self.archivo.read_bytes()
        with patch.object(Path, "replace", side_effect=PermissionError("reemplazo denegado")):
            with self.assertRaises(PermissionError):
                registro.guardar_sesiones(self.sesiones + [{"asignatura": "Historia", "minutos": 10}])
        self.assertEqual(self.archivo.read_bytes(), contenido)
        self.comprobar_sin_temporales()

    def test_menu_termina_si_falla_el_guardado(self):
        registro.guardar_sesiones(self.sesiones)
        contenido = self.archivo.read_bytes()
        salida = io.StringIO()
        with patch.object(registro, "guardar_sesiones", side_effect=OSError("sin espacio")):
            with contextlib.redirect_stdout(salida):
                with patch("builtins.input", side_effect=["1", "1", "Historia", "10"]):
                    with self.assertRaises(SystemExit) as error:
                        registro.main()
        self.assertEqual(error.exception.code, 1)
        self.assertIn("No se pudo guardar la nueva sesión", salida.getvalue())
        self.assertEqual(self.archivo.read_bytes(), contenido)

    def test_reinicio_desde_otra_carpeta_usa_el_mismo_json(self):
        carpeta_script = self.carpeta / "ejercicios"
        carpeta_script.mkdir()
        script = carpeta_script / RUTA_SCRIPT.name
        shutil.copy2(RUTA_SCRIPT, script)
        otra_carpeta = self.carpeta / "otra-carpeta"
        otra_carpeta.mkdir()

        primero = subprocess.run(
            [sys.executable, "-B", str(script)],
            input="1\n2\nMatemáticas\n20\nProgramación\n35\n3\n",
            text=True, encoding="utf-8", capture_output=True,
            cwd=carpeta_script, timeout=5,
        )
        self.assertEqual(primero.returncode, 0, primero.stderr)
        segundo = subprocess.run(
            [sys.executable, "-B", str(script)],
            input="1\n1\nHistoria\n10\n2\n3\n",
            text=True, encoding="utf-8", capture_output=True,
            cwd=otra_carpeta, timeout=5,
        )
        self.assertEqual(segundo.returncode, 0, segundo.stderr)
        historial = json.loads((carpeta_script / "sesiones.json").read_text(encoding="utf-8"))
        self.assertEqual(historial, self.sesiones + [{"asignatura": "Historia", "minutos": 10}])
        self.assertIn("El total de minutos estudiados es de: 65", segundo.stdout)
        self.assertFalse((otra_carpeta / "sesiones.json").exists())


if __name__ == "__main__":
    unittest.main()
