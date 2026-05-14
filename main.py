import csv
from arbol_b import ArbolB


def cargar_csv(arbol, archivo):

    with open(archivo, newline='', encoding='utf-8') as archivo_csv:

        lector = csv.reader(archivo_csv)

        for fila in lector:

            try:
                arbol.insertar(int(fila[0]))
            except:
                pass

    print(f"Datos cargados desde {archivo}")


def menu():

    grado = int(input("Ingrese el grado del Árbol B: "))

    arbol = ArbolB(grado)

    while True:

        print("\n===== MENÚ =====")
        print("1. Insertar clave")
        print("2. Buscar clave")
        print("3. Eliminar clave")
        print("4. Mostrar recorrido")
        print("5. Cargar CSV")
        print("6. Generar gráfica")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        # INSERTAR
        if opcion == "1":

            clave = int(input("Ingrese la clave: "))

            arbol.insertar(clave)

            print("Clave insertada.")

        # BUSCAR
        elif opcion == "2":

            clave = int(input("Ingrese la clave a buscar: "))

            resultado = arbol.buscar(clave)

            if resultado:
                print("Clave encontrada.")
            else:
                print("Clave NO encontrada.")

        # ELIMINAR
        elif opcion == "3":

            clave = int(input("Ingrese la clave a eliminar: "))

            arbol.eliminar(clave)

            print("Clave eliminada.")

        # RECORRIDO
        elif opcion == "4":

            print("Recorrido del Árbol B:")

            print(arbol.recorrer())

        # CARGAR CSV
        elif opcion == "5":

            nombre_archivo = input("Ingrese el nombre del archivo CSV: ")

            cargar_csv(arbol, nombre_archivo)

        # GRAPHVIZ
        elif opcion == "6":

            arbol.graficar()

        # SALIR
        elif opcion == "7":

            print("Programa finalizado.")

            break

        else:
            print("Opción inválida.")


menu()