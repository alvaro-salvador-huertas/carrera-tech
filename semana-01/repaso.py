try:
	minutos = int(input("¿Cuantos minutos has estudiado?"))
except ValueError:
	print("Debes introducir un numero entero, por ejemplo, 30.")
else:
	if minutos < 0:
		print("Los minutos no pueden ser negativos")
	elif minutos < 30:
		print("Sesion corta, intenta llegar a 30 minutos")
	else:
		print("Sesion completa")
