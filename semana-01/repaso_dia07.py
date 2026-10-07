while True:
	try:
		sesiones = int(input("¿Cuantas sesiones quieres hacer hoy?"))
	except ValueError:
		print("Las sesiones deben ser un numero entero")
	else:
		if sesiones < 1:
			print("Debes indicar al menos 1 sesion, intenta de nuevo")
		elif sesiones > 6:
			print("Las sesiones deben estar entre 1-6, prueba con un numero entre este rango")
		else:
			break
print("Sesiones previstas: ", sesiones)

sesion_actual = 1
total_minutos = 0

while sesion_actual <= sesiones:
	print("Sesion", sesion_actual)
	while True:
		try:
			minutos = int(input("¿Cuantos minutos has estudiado en esta sesion?"))
		except ValueError:
			print("Los minutos deben ser numeros enteros")
		else:
			if minutos <= 0:
				print("Los minutos deben ser numeros positivos, prueba de nuevo")
			else:
				total_minutos = total_minutos + minutos
				sesion_actual = sesion_actual + 1
				break
print("Minutos totales:", total_minutos)
print("Plan terminado")
