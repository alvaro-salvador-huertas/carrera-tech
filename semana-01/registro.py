asignatura = input("¿Que asignatura has estudiado?")
minutos = int(input("¿Cuantos minutos has estudiado?"))
objetivo = 60
restantes = objetivo - minutos

print("Asignatura:", asignatura)
print("Minutos estudiados:", minutos)
if minutos < objetivo:
	print("Minutos restantes:", restantes)
elif minutos == objetivo:
        print("Objetivo alcanzado justo")
else:
	print("Minutos por encima del objetivo", minutos - objetivo)

