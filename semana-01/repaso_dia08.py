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
sesiones_cortas = 0
minutos_totales = 0
sesiones = pedir_numero("¿Cuantas sesiones de estudio vas a realizar?")
sesion_actual = 1


duraciones = []

while sesion_actual <= sesiones:
	print("Sesion:", sesion_actual)
	minutos = pedir_numero("¿Cuantos minutos estudiaste en la sesion?")
	duraciones.append(minutos)

	if minutos < 30:
		sesiones_cortas = sesiones_cortas + 1

	minutos_totales = minutos_totales + minutos
	sesion_actual = sesion_actual + 1

print("El total de minutos estudiados es de:", minutos_totales)
print("Usted ha estudiado:", sesiones_cortas, "de menos de 30 minutos")
print("Duraciones:", duraciones)
print("Duracion media:", sum(duraciones) / len(duraciones), "minutos")
print("Detalle de las sesiones:")

sesiones_completas = 0
for duracion in duraciones:
	print("Duracion:", duracion, "minutos")

	if duracion < 30:
		print("Sesion corta")
	else:
		print("Sesion completa")
		sesiones_completas = sesiones_completas + 1

print("Ha realizado:", sesiones_completas, "sesiones completas")

print("Sesion mas larga:", max(duraciones), "minutos")
print("Sesion mas corta:", min(duraciones), "minutos")
