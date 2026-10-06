while True:
	try:
		minutos = int(input("¿Cuantos minutos has estudiado?"))
	except ValueError:
		print("Por favor, introduce un numero entero")
	else:
		if minutos < 0:
			print("Los minutos no pueden ser negativos")
		elif minutos < 30:
			print("Sesion corta")
			break
		else:
			print("Sesion completa")
			break
print("Registro terminado")
