from graphviz import Digraph


class NodoArbolB:
    def __init__(self, grado, hoja=False):
        self.grado = grado
        self.hoja = hoja
        self.claves = []
        self.hijos = []

    def __str__(self):
        return str(self.claves)


class ArbolB:
    def __init__(self, grado):
        self.raiz = NodoArbolB(grado, True)
        self.grado = grado

    # BÚSQUEDA
    def buscar(self, clave, nodo=None):

        if nodo is None:
            nodo = self.raiz

        indice = 0

        while indice < len(nodo.claves) and clave > nodo.claves[indice]:
            indice += 1

        if indice < len(nodo.claves) and clave == nodo.claves[indice]:
            return nodo

        if nodo.hoja:
            return None

        return self.buscar(clave, nodo.hijos[indice])

    # INSERCIÓN
    def insertar(self, clave):

        raiz = self.raiz

        if len(raiz.claves) == (2 * self.grado) - 1:

            nuevo_nodo = NodoArbolB(self.grado)

            self.raiz = nuevo_nodo

            nuevo_nodo.hijos.insert(0, raiz)

            self.dividir_hijo(nuevo_nodo, 0)

            self.insertar_no_lleno(nuevo_nodo, clave)

        else:
            self.insertar_no_lleno(raiz, clave)

    def insertar_no_lleno(self, nodo, clave):

        indice = len(nodo.claves) - 1

        if nodo.hoja:

            nodo.claves.append(None)

            while indice >= 0 and clave < nodo.claves[indice]:
                nodo.claves[indice + 1] = nodo.claves[indice]
                indice -= 1

            nodo.claves[indice + 1] = clave

        else:

            while indice >= 0 and clave < nodo.claves[indice]:
                indice -= 1

            indice += 1

            if len(nodo.hijos[indice].claves) == (2 * self.grado) - 1:

                self.dividir_hijo(nodo, indice)

                if clave > nodo.claves[indice]:
                    indice += 1

            self.insertar_no_lleno(nodo.hijos[indice], clave)

    def dividir_hijo(self, nodo_padre, indice):

        grado = self.grado

        nodo_actual = nodo_padre.hijos[indice]

        nuevo_nodo = NodoArbolB(grado, nodo_actual.hoja)

        nodo_padre.hijos.insert(indice + 1, nuevo_nodo)

        nodo_padre.claves.insert(indice, nodo_actual.claves[grado - 1])

        nuevo_nodo.claves = nodo_actual.claves[grado:(2 * grado) - 1]

        nodo_actual.claves = nodo_actual.claves[0:grado - 1]

        if not nodo_actual.hoja:

            nuevo_nodo.hijos = nodo_actual.hijos[grado:2 * grado]

            nodo_actual.hijos = nodo_actual.hijos[0:grado]

    # ELIMINACIÓN
    def eliminar(self, clave):

        self._eliminar(self.raiz, clave)

        if len(self.raiz.claves) == 0 and not self.raiz.hoja:
            self.raiz = self.raiz.hijos[0]

    def _eliminar(self, nodo, clave):

        grado = self.grado

        indice = 0

        while indice < len(nodo.claves) and clave > nodo.claves[indice]:
            indice += 1

        # clave encontrada en hoja
        if nodo.hoja:

            if indice < len(nodo.claves) and nodo.claves[indice] == clave:
                nodo.claves.pop(indice)

            return

        # clave encontrada en nodo interno
        if indice < len(nodo.claves) and nodo.claves[indice] == clave:

            return self.eliminar_nodo_interno(nodo, clave, indice)

        # clave no encontrada
        if len(nodo.hijos[indice].claves) < grado:

            self.llenar(nodo, indice)

        if indice > len(nodo.claves):
            self._eliminar(nodo.hijos[indice - 1], clave)
        else:
            self._eliminar(nodo.hijos[indice], clave)

    def eliminar_nodo_interno(self, nodo, clave, indice):

        grado = self.grado

        if len(nodo.hijos[indice].claves) >= grado:

            predecesor = self.obtener_predecesor(nodo, indice)

            nodo.claves[indice] = predecesor

            self._eliminar(nodo.hijos[indice], predecesor)

        elif len(nodo.hijos[indice + 1].claves) >= grado:

            sucesor = self.obtener_sucesor(nodo, indice)

            nodo.claves[indice] = sucesor

            self._eliminar(nodo.hijos[indice + 1], sucesor)

        else:

            self.unir(nodo, indice)

            self._eliminar(nodo.hijos[indice], clave)

    def obtener_predecesor(self, nodo, indice):

        actual = nodo.hijos[indice]

        while not actual.hoja:
            actual = actual.hijos[-1]

        return actual.claves[-1]

    def obtener_sucesor(self, nodo, indice):

        actual = nodo.hijos[indice + 1]

        while not actual.hoja:
            actual = actual.hijos[0]

        return actual.claves[0]

    def llenar(self, nodo, indice):

        grado = self.grado

        if indice != 0 and len(nodo.hijos[indice - 1].claves) >= grado:

            self.prestar_anterior(nodo, indice)

        elif indice != len(nodo.hijos) - 1 and len(nodo.hijos[indice + 1].claves) >= grado:

            self.prestar_siguiente(nodo, indice)

        else:

            if indice != len(nodo.hijos) - 1:
                self.unir(nodo, indice)
            else:
                self.unir(nodo, indice - 1)

    def prestar_anterior(self, nodo, indice):

        hijo = nodo.hijos[indice]

        hermano = nodo.hijos[indice - 1]

        hijo.claves.insert(0, nodo.claves[indice - 1])

        if not hijo.hoja:
            hijo.hijos.insert(0, hermano.hijos.pop())

        nodo.claves[indice - 1] = hermano.claves.pop()

    def prestar_siguiente(self, nodo, indice):

        hijo = nodo.hijos[indice]

        hermano = nodo.hijos[indice + 1]

        hijo.claves.append(nodo.claves[indice])

        if not hijo.hoja:
            hijo.hijos.append(hermano.hijos.pop(0))

        nodo.claves[indice] = hermano.claves.pop(0)

    def unir(self, nodo, indice):

        hijo = nodo.hijos[indice]

        hermano = nodo.hijos[indice + 1]

        hijo.claves.append(nodo.claves[indice])

        hijo.claves.extend(hermano.claves)

        if not hijo.hoja:
            hijo.hijos.extend(hermano.hijos)

        nodo.claves.pop(indice)

        nodo.hijos.pop(indice + 1)

    # RECORRIDO
    def recorrer(self, nodo=None):

        if nodo is None:
            nodo = self.raiz

        resultado = []

        for indice in range(len(nodo.claves)):

            if not nodo.hoja:
                resultado.extend(self.recorrer(nodo.hijos[indice]))

            resultado.append(nodo.claves[indice])

        if not nodo.hoja:
            resultado.extend(self.recorrer(nodo.hijos[len(nodo.claves)]))

        return resultado

    # GRAPHVIZ
    def graficar(self, nombre_archivo="arbol_b"):

        grafica = Digraph()

        self._graficar_nodo(grafica, self.raiz)

        grafica.render(nombre_archivo, format="png", cleanup=True)

        print(f"Árbol generado: {nombre_archivo}.png")

    def _graficar_nodo(self, grafica, nodo, padre=None):

        identificador_nodo = str(id(nodo))

        etiqueta = "|".join(str(clave) for clave in nodo.claves)

        grafica.node(identificador_nodo, etiqueta)

        if padre:
            grafica.edge(padre, identificador_nodo)

        for hijo in nodo.hijos:
            self._graficar_nodo(grafica, hijo, identificador_nodo)