def calcular_media(total, cantidad):
	return total / cantidad

media = calcular_media(60, 2)
print("Media:", media)

otra_media = calcular_media(85, 3)
print("Otra media:", otra_media)

def calcular_restantes(objetivo, estudiados):
	if objetivo >= estudiados:
		return objetivo - estudiados
	else:
		return 0

print(calcular_restantes(60, 40))
print(calcular_restantes(60, 60))
print(calcular_restantes(60, 75))


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

sesiones = pedir_numero("¿Cuantas sesiones quieres hacer?")
minutos  = pedir_numero("¿Cuantos minutos has estudiado?")
print("Has elegido:", sesiones)
print("Minutos introducidos", minutos)


