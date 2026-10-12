# Carrera Tech - Fundamentos de programación

Repositorio de ejercicios con los que voy aprendiendo Python. Cada programa amplía
lo practicado anteriormente: pedir datos, tomar decisiones, repetir operaciones y
resumir sesiones de estudio.

Para ejecutar los ejercicios necesitas Python 3. Los comandos siguientes se
ejecutan en una terminal, desde la carpeta `carrera-tech`.

**[registro.py](semana-01/registro.py) — Una sesión con un objetivo de 60 minutos.**

Pide la asignatura y los minutos estudiados. Si se alcanzan o superan los 60 minutos,
muestra que la sesión se ha completado; si faltan minutos, indica cuántos quedan
para llegar al objetivo. Por ejemplo, con 45 minutos indica que faltan 15.

Acepta minutos enteros mayores o iguales que cero. Ante texto, decimales o números
negativos, muestra un aviso y vuelve a pedir los minutos. La asignatura se recoge
como dato de entrada, pero el mensaje final informa únicamente del objetivo.

Aquí practico `input()` para pedir datos, `int()` para convertir texto en un entero
y condiciones con `if` y `else` para decidir qué mensaje mostrar. También uso un
bucle `while`, que repite instrucciones, y `try`/`except` para gestionar el error
que aparece cuando la entrada no se puede convertir en un número entero.

```bash
python3 semana-01/registro.py
```

**[repaso.py](semana-01/repaso.py) — Clasificar una sesión de estudio.**

Pide los minutos estudiados y clasifica la sesión como corta si dura menos de
30 minutos, o completa si dura 30 minutos o más. Acepta cero como sesión corta.

Si la entrada no es un número entero o es negativa, muestra un aviso y termina.
Este ejercicio realiza una sola petición de datos, sin volver a preguntar ante
un error.

Aquí repaso la conversión de datos, el tratamiento de errores y las condiciones
`if`, `elif` y `else`, que permiten elegir entre varios casos.

```bash
python3 semana-01/repaso.py
```

**[repaso_dia07.py](semana-01/repaso_dia07.py) — Varias sesiones y un resumen.**

Pide una cantidad de sesiones entre 1 y 6, ambos incluidos. Después solicita los
minutos de cada sesión, que deben ser enteros mayores que cero. Si una entrada
no cumple estas condiciones, muestra un aviso y vuelve a pedirla.

Al terminar, muestra el tiempo total, la duración media y cuántas sesiones han
alcanzado al menos 30 minutos. Por ejemplo, con dos sesiones de 20 y 35 minutos,
el total es 55, la media es 27,5 y hay una sesión completa.

Aquí practico bucles anidados: un bucle recorre las sesiones y otro, dentro del
primero, repite la petición de minutos hasta recibir un valor válido. También uso
contadores, que llevan la cuenta de las sesiones, y un acumulador, que va sumando
los minutos. Estos datos se mantienen en memoria mientras el programa está abierto;
este ejercicio todavía no los guarda en un archivo.

```bash
python3 semana-01/repaso_dia07.py
```

repaso_dia08.py -- Registro de estudio con historial guardado en JSON, un formato
de texto que permite conservar datos entre ejecuciones. Usa únicamente la biblioteca
estándar de Python, sin instalar dependencias.

Para ejecutarlo desde la carpeta `carrera-tech`:

```bash
python3 semana-01/repaso_dia08.py
```

El menú se repite hasta elegir salir:

1. **Registrar sesiones.** Pide cuántas sesiones registrar, la asignatura y los
   minutos de cada una. Las cantidades deben ser enteros positivos y la asignatura
   no puede estar vacía ni contener solo espacios. Guarda después de cada sesión
   válida y, al terminar el registro, muestra el resumen del historial completo.
2. **Consultar historial y resumen.** Muestra las asignaturas, los minutos y si cada
   sesión es corta (menos de 30 minutos) o completa (30 minutos o más). Incluye el
   total, las duraciones, la media, el número de sesiones cortas y completas, y las
   duraciones máxima y mínima. También agrupa los minutos por asignatura y muestra
   una sola entrada por asignatura con su total. No modifica el archivo. Si el
   historial está vacío, muestra `No hay sesiones` y total 0, sin calcular media,
   mínimo ni máximo.
3. **Salir.** Termina el programa. Una opción inválida vuelve a pedir la opción.

Para agrupar los minutos, los nombres se comparan exactamente, distinguiendo
mayúsculas y minúsculas: `Python` y `python` son asignaturas diferentes. Por
ejemplo, las sesiones de Python de 20 y 15 minutos y la de Redes de 30 minutos
producen los totales `Python: 35 minutos` y `Redes: 30 minutos`.

El historial se guarda en `semana-01/sesiones.json`, siempre junto al script,
independientemente de la carpeta desde la que se ejecute. Contiene una lista de
diccionarios: cada diccionario representa una sesión con `asignatura` y `minutos`.
Este archivo está excluido de Git mediante `.gitignore`.

Si el JSON no existe, el programa empieza con una lista vacía y lo crea al guardar
la primera sesión. Si está dañado o tiene una estructura incorrecta, muestra el
error y termina sin sobrescribirlo. También rechaza booleanos (`true` y `false`)
como minutos. Los errores de lectura, como la falta de permisos, se muestran como
errores y no se interpretan como un historial vacío. Para recuperar un archivo
dañado, conserva una copia y corrige el contenido antes de volver a ejecutar.

Cada guardado escribe primero un archivo temporal en la misma carpeta y lo cierra
antes de reemplazar el original. El reemplazo es atómico: el original pasa del
historial anterior al nuevo sin quedar escrito a medias. Si la escritura o el
reemplazo fallan, el programa informa del error y termina; el historial anterior
se conserva. El programa carga los datos al iniciar: conviene usar una sola
instancia a la vez para evitar que dos programas sobrescriban cambios entre sí.

Las pruebas están en `tests/test_repaso_dia08.py` y usan `unittest`, incluido en
Python. Trabajan en carpetas temporales y sustituyen la ruta del JSON durante
cada prueba, por lo que no leen ni modifican tu historial.

Para ejecutar todas las pruebas desde `carrera-tech`:

```bash
python3 -B -m unittest discover -s tests -v
```

La opción `-B` evita generar archivos de caché de Python durante las pruebas.
