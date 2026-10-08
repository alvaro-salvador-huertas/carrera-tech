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

while sesion_actual <= sesiones:
	print("Sesion:", sesion_actual)
	minutos = pedir_numero("¿Cuantos minutos estudiaste en la sesion?")

	if minutos < 30:
		sesiones_cortas = sesiones_cortas + 1

	minutos_totales = minutos_totales + minutos
	sesion_actual = sesion_actual + 1

print("El total de minutos estudiados es de:", minutos_totales)
print("Usted ha estudiado:", sesiones_cortas, "de menos de 30 minutos")
