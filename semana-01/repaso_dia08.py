import json
from pathlib import Path
from tempfile import NamedTemporaryFile


ARCHIVO_SESIONES = Path(__file__).resolve().with_name("sesiones.json")


def cargar_sesiones():
    try:
        with ARCHIVO_SESIONES.open("r", encoding="utf-8") as archivo:
            sesiones = json.load(archivo)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError(
            f"El archivo {ARCHIVO_SESIONES} no contiene JSON válido en UTF-8."
        ) from error

    if not isinstance(sesiones, list):
        raise ValueError("El historial debe ser una lista de sesiones.")

    for numero, sesion in enumerate(sesiones, start=1):
        if not isinstance(sesion, dict):
            raise ValueError(f"La sesión {numero} debe ser un diccionario.")

        asignatura = sesion.get("asignatura")
        minutos = sesion.get("minutos")
        if not isinstance(asignatura, str) or not asignatura.strip():
            raise ValueError(f"La sesión {numero} debe tener una asignatura no vacía.")

        # bool también es un tipo de entero en Python; exigimos el tipo int exacto.
        if type(minutos) is not int or minutos <= 0:
            raise ValueError(f"La sesión {numero} debe tener minutos enteros positivos.")

    return sesiones


def guardar_sesiones(sesiones):
    ruta_temporal = None
    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=ARCHIVO_SESIONES.parent,
            prefix=".sesiones-",
            suffix=".tmp",
            delete=False,
        ) as archivo:
            ruta_temporal = Path(archivo.name)
            json.dump(sesiones, archivo, ensure_ascii=False, indent=4)
            archivo.write("\n")

        # El temporal está cerrado y completo antes de reemplazar el historial.
        ruta_temporal.replace(ARCHIVO_SESIONES)
    finally:
        if ruta_temporal is not None:
            ruta_temporal.unlink(missing_ok=True)


def pedir_numero(mensaje):
    while True:
        try:
            numero = int(input(mensaje))
        except ValueError:
            print("Introduce un numero, por favor")
        else:
            if numero > 0:
                return numero
            else:
                print("Introduce un numero positivo")


def registrar_sesiones(sesiones):
    cantidad_sesiones = pedir_numero("¿Cuantas sesiones de estudio vas a realizar?")
    sesion_actual = 1

    while sesion_actual <= cantidad_sesiones:
        print("Sesion:", sesion_actual)
        asignatura = input("¿Que asignatura estudiaste en la sesion?").strip()
        while not asignatura:
            print("Introduce una asignatura que no este vacia")
            asignatura = input("¿Que asignatura estudiaste en la sesion?").strip()

        minutos = pedir_numero("¿Cuantos minutos estudiaste en la sesion?")
        sesiones.append({"asignatura": asignatura, "minutos": minutos})
        guardar_sesiones(sesiones)

        sesion_actual = sesion_actual + 1


def mostrar_resumen(sesiones):
    if not sesiones:
        print("No hay sesiones")
        print("El total de minutos estudiados es de:", 0)
        return

    sesiones_cortas = 0
    duraciones = []
    for sesion in sesiones:
        duraciones.append(sesion["minutos"])
        if sesion["minutos"] < 30:
            sesiones_cortas = sesiones_cortas + 1

    minutos_totales = sum(duraciones)
    print("El total de minutos estudiados es de:", minutos_totales)
    print("Usted ha estudiado:", sesiones_cortas, "de menos de 30 minutos")
    print("Duraciones:", duraciones)
    print("Duracion media:", minutos_totales / len(duraciones), "minutos")
    print("Detalle de las sesiones:")

    sesiones_completas = 0
    for sesion in sesiones:
        print("Asignatura:", sesion["asignatura"])
        print("Duracion:", sesion["minutos"], "minutos")

        if sesion["minutos"] < 30:
            print("Sesion corta")
        else:
            print("Sesion completa")
            sesiones_completas = sesiones_completas + 1

    print("Ha realizado:", sesiones_completas, "sesiones completas")

    print("Sesion mas larga:", max(duraciones), "minutos")
    print("Sesion mas corta:", min(duraciones), "minutos")


def main():
    try:
        sesiones = cargar_sesiones()
    except ValueError as error:
        print(f"Error en {ARCHIVO_SESIONES}: {error}")
        print("El programa termina sin modificar el historial.")
        raise SystemExit(1)
    except OSError as error:
        print(f"No se pudo leer {ARCHIVO_SESIONES}: {error}")
        print("El programa termina sin modificar el historial.")
        raise SystemExit(1)

    while True:
        print("\n1. Registrar sesiones.")
        print("2. Consultar historial y resumen.")
        print("3. Salir.")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            try:
                registrar_sesiones(sesiones)
            except OSError as error:
                print(f"No se pudo guardar la nueva sesión en {ARCHIVO_SESIONES}: {error}")
                raise SystemExit(1)
            mostrar_resumen(sesiones)
        elif opcion == "2":
            mostrar_resumen(sesiones)
        elif opcion == "3":
            break
        else:
            print("Opción inválida. Elige 1, 2 o 3.")


if __name__ == "__main__":
    main()
