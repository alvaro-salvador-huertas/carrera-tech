objetivo = 60
asignatura = input("¿Que asignatura has estudiado?")
while True:
	try:
		minutos = int(input("¿Cuantos minutos has estudiado?"))
	except ValueError:
		print("Los minutos deben ser un número entero")
	else:
		if minutos < 0:
			print("Los minutos no pueden ser negativos")
		else:
			break
if minutos >= objetivo:
        print("Sesion completada con exito")
else:
        print("Sesion corta, debes estudiar", objetivo - minutos, "minutos mas")
