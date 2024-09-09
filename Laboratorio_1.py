import graphviz #INSTALAR ESTO BUSQUEN TUTORIAL
from typing import Any, Optional, Tuple
import openpyxl #INSTALAR ESTO EN LA TERMINAL "pip install openpyxl"

                    #nombre del nodo actual, nombre del que buscamos

def comparar_nombres(nombre_n, nombre_b):
    if len(nombre_n) < len(nombre_b):
        nombre_min=nombre_n
    elif len(nombre_n) > len(nombre_b):
        nombre_min=nombre_b             #agarra al nombre de menor tamaño en caso que sean iguales
    else:
        nombre_min=nombre_n
    for i in range(len(nombre_min)):
        if nombre_n[i]<nombre_b[i]:
            return nombre_n
        elif nombre_n[i] == nombre_b[i]:
            if i+1 == len(nombre_min):
                return nombre_min
            pass
        else:
           return nombre_b


class Nodo:
    def __init__(self, title, w_earn, d_earn, f_earn, d_p_earn, f_p_earn, year) -> None:
        self.title = title.replace(":", "") #titulo
        self.w_earn = w_earn #ganancias mundiales
        self.d_earn = d_earn #ganancias nacionales
        self.f_earn = f_earn #ganancias extranjeras
        self.d_p_earn = d_p_earn #porcentaje ganancias nacionales
        self.f_p_earn = f_p_earn #porcentaje ganancias extranjeras
        self.year = year #año 
        self.left: Optional["Nodo"] = None
        self.right: Optional["Nodo"] = None
        self.parent = None
        self.level = 0
        self.pos = [0, 0] #coordenadas para mostrar en el arbol x y
        self.height = 1 #altura es diferente de nivel
    def spos(self):
        #retorna la posicion del nodo actual con el formato que necesita para verse bien en el graphviz
        return str(self.pos[0]) + "," + str(self.pos[1]) + "!" #pos 0 es el x, pos 1 es el y

class Arbol:
    def __init__(self, root: Optional["Nodo"] = None) -> None:
        self.root = root

    def search(self, title: Any) -> Tuple[Optional["Nodo"], Optional["Nodo"]]:
        p, pad = self.root, None
        while p is not None:
            if title == p.title:
                print(f"Película encontrada: {p.title}")
                return p, pad #retorna el nodo y su padre
            else:
                pad = p
                direccion = comparar_nombres(p.title, title) # si retorna el que estamos buscando significa que esta va a la izquierda, si retorna el otro entonces va a la derecha
                if direccion == title:
                    p = p.left
                else:
                    p = p.right
        return None, pad #en caso de que no los encuentre
    

    def insert(self, title) -> bool:
        found = False #para ver si se encontro la pelicula en el excel
        libro = openpyxl.load_workbook(filename="laboratorio_excel.xlsx")
        hoja = libro.active #primera hoja del excel
        for fila in hoja.iter_rows(min_row=2, values_only=True):  # min_row=2 fila minima desde la que comienza
            title1 = str(fila[0]) #title1 para diferenciar del title del insert
            w_earn = int(fila[1])
            d_earn = int(fila[2])
            d_p_earn = float(fila[3])
            f_earn = int(fila[4])
            f_p_earn = float(fila[5])
            year = int(fila[6])
            title = title.replace(":", "")
            title1 = title1.replace(":", "")
            if title == title1:
                insertar = Nodo(title, w_earn, d_earn, f_earn, d_p_earn, f_p_earn, year)
                found = True
                break
        if not found:
            print("El nombre no se encontró")
            return
        
        if self.root is None:
            self.root = insertar
            self.root.level = 0
            return True
        else:
            p, pad = self.search(title)
            if p is not None:
                return False
            else: #si retorna el que estamos buscando significa que va a la izquierda, si retorna el otro entonces a la derecha
                if comparar_nombres(pad.title, title) == title:
                    pad.left = insertar
                    pad.left.parent = pad #padres de los nodos
                    self.rev_insert(pad.left) #para revisar si necesitamos hacer algun rebalance
                    self._rev_level(self.root)
                else:
                    pad.right = insertar
                    pad.right.parent = pad #padres de los nodos
                    self.rev_insert(pad.right) #para revisar si necesitamos hacer algun rebalance
                    self._rev_level(self.root)
                return True      

    def height(self, node: Optional["Nodo"]): #altura del nodo actual
        if node == None:
            return 0
        else:
            return node.height
        
    def delete(self, title: Any, mode: bool = True) -> bool: #CODIGO DEL PROFESOR
        p, pad = self.search(title)
        if p is not None:
            if p == self.root:
                if p.left is None and p.right is None:
                    self.root = None
                    del p
                elif p.left is not None and p.right is None:
                    self.root = p.left
                    p.left = None
                    del p
                elif p.left is None and p.right is not None:
                    self.root = p.right
                    p.right = None
                    del p
                else:
                    if mode:
                        pred, pad_pred, son_pred = self.__pred(p)
                        p.title = pred.title
                        if p == pad_pred:
                            pad_pred.left = son_pred
                            if pad_pred.left != None:
                                pad_pred.left.parent = pad_pred
                        else:
                            pad_pred.right = son_pred
                            if pad_pred.right != None:
                                pad_pred.right.parent = pad_pred
                        del pred
                    else:
                        sus, pad_sus, son_sus = self.__sus(p)
                        p.title = sus.title
                        if p == pad_sus:
                            pad_sus.right = son_sus
                            pad_sus.right.parent = pad_sus
                        else:
                            pad_sus.left = son_sus
                            pad_sus.left.parent = pad_sus
                        del sus
            elif p.left is None and p.right is None:
                if p == pad.left:
                    pad.left = None
                else:
                    pad.right = None
                del p
            elif p.left is None and p.right is not None:
                if p == pad.left:
                    pad.left = p.right
                    pad.left.parent = pad
                else:
                    pad.right = p.right
                    pad.right.parent = pad
                    pad.right.height += 1
                del p
            elif p.left is not None and p.right is None:
                if p == pad.left:
                    pad.left = p.left
                    pad.left.parent = pad
                else:
                    pad.right = p.left
                    pad.right.parent = pad
                    pad.right.height += 1
                del p
            else:
                if mode:
                    pred, pad_pred, son_pred = self.__pred(p)
                    p.title = pred.title
                    if p == pad_pred:
                        pad_pred.left = son_pred
                        if pad_pred.left != None:
                            pad_pred.left.parent = pad_pred
                    else:
                        pad_pred.right = son_pred
                        if pad_pred.right != None:
                            pad_pred.right.parent = pad_pred
                    del pred
                else:
                    sus, pad_sus, son_sus = self.__sus(p)
                    p.title = sus.title
                    if p == pad_sus:
                        pad_sus.right = son_sus
                        pad_sus.right.parent = pad_sus
                    else:
                        pad_sus.left = son_sus
                        pad_sus.left.parent = pad_sus
                    del sus
            self.rev_delete(pad)
            self._rev_level(self.root) #revisa los niveles
            return True
        return False

    def __pred(self, node: "Nodo") -> Tuple["Nodo", "Nodo", Optional["Nodo"]]: #CODIGO DEL PROFESOR
        p, pad = node.left, node
        while p.right is not None:
            p, pad = p.right, p
        return p, pad, p.left

    def __sus(self, node: "Nodo") -> Tuple["Nodo", "Nodo", Optional["Nodo"]]: #CODIGO DEL PROFESOR
        p, pad = node.right, node
        while p.left is not None:
            p, pad = p.left, p
        return p, pad, p.right
    
    def rev_insert(self, node: "Nodo", path=[]): #revision al insertar, path es una tupla con los nodos que se van a rotar 
        if node.parent == None: return
        path=[node]+path

        left_height = self.height(node.parent.left)
        right_height = self.height(node.parent.right)
        
        if abs(right_height-left_height)>1:
            path=[node.parent]+path
            self.balance(path[0], path[1], path[2])
            return
        
        new_height = 1+node.height
        if new_height > node.parent.height:
            node.parent.height = new_height

        self.rev_insert(node.parent, path) #va de abajo hacia arriba desde el nodo que ingresamos

    def rev_delete(self, node: "Nodo"): #revision al borrar
        if node == None: return

        left_height = self.height(node.left)
        right_height = self.height(node.right)

        if abs(right_height-left_height)>1:
            y = self.taller_child(node)
            x = self.taller_child(y)
            self.balance(node, y, x)

        self.rev_delete(node.parent)

    def _rev_level(self, node: Optional["Nodo"]): #se llama cada vez que se borra o inserta un nuevo elemento y le agrega el nivel al nodo
        if node == None:
            return
        else:
            if node == self.root:
                node.level = 0
                self._rev_level(node.left)
                self._rev_level(node.right)
            else:
                node.level = node.parent.level+1
                self._rev_level(node.left)
                self._rev_level(node.right)

    def balance(self, nodo1, nodo2, nodo3): #balanceos con las rotaciones
        if nodo2==nodo1.left and nodo3 == nodo2.left:
            self.srr(nodo1)
        elif nodo2==nodo1.left and nodo3 == nodo2.right:
            self.slr(nodo2)
            self.srr(nodo1)
        elif nodo2==nodo1.right and nodo3 == nodo2.right:
            self.slr(nodo1)
        elif nodo2==nodo1.right and nodo3 == nodo2.left:
            self.srr(nodo2)
            self.slr(nodo1)
        else:
            raise Exception("Error") #en caso de que no cumple niguno de los casos (no debería pasar)
        self._rev_level(self.root) #revisa los niveles

    def srr(self, nodo): #rotacion derecha
        parent = nodo.parent
        aux = nodo.left
        hijo_aux = aux.right
        aux.right = nodo
        nodo.parent = aux
        nodo.left = hijo_aux
        if hijo_aux!=None: 
            hijo_aux.parent = nodo
        aux.parent = parent
        if aux.parent == None:
            self.root = aux
        else:
            if aux.parent.left==nodo:
                aux.parent.left=aux
            else:
                aux.parent.right=aux
        nodo.height=1+max(self.height(nodo.left), self.height(nodo.right))
        aux.height=1+max(self.height(aux.left), self.height(aux.right))

    def slr(self, nodo): #rotacion izquierda
        parent = nodo.parent
        aux = nodo.right
        hijo_aux = aux.left
        aux.left = nodo
        nodo.parent = aux
        nodo.right = hijo_aux
        if hijo_aux!=None: 
            hijo_aux.parent = nodo
        aux.parent = parent
        if aux.parent == None:
            self.root = aux
        else:
            if aux.parent.left==nodo:
                aux.parent.left=aux
            else:
                aux.parent.right=aux
        nodo.height=1+max(self.height(nodo.left), self.height(nodo.right))
        aux.height=1+max(self.height(aux.left), self.height(aux.right))

    def taller_child(self, nodo): #hijo mayor
        left=self.height(nodo.left)
        right=self.height(nodo.right)
        return nodo.left if left >= right else nodo.right
    
    def r_levels(self) -> None: #llama a _r_levels y crea la listas
        listM = [] #lista de listas
        elem = [] #elementos por niveles
        for i in range(arbol_peliculas.root.height): #crea tantas listas en listM como niveles existan
            list = []
            listM.append(list)
        self._r_levels(self.root, listM)
        for y in listM:
            elem += y #une las listas
        print(elem)


    def _r_levels(self, node: Optional["Nodo"], listM): 
        if node is not None:
            listM[int(node.level)].append(node.title) #agrega elemento a la lista de su nivel
            self._r_levels(node.left, listM)
            self._r_levels(node.right, listM)

        return listM #retorna la lista

    def search_criteria(self, year, f_earnings):
        listE=[]
        self._search_criteria(self.root, year, f_earnings, listE)
        return listE #retorna la lista con elementos que cumplen

    def _search_criteria(self, node: Optional["Nodo"], year1, f_earnings, listE):
        if node == None: 
            return
        else:
            if node.year == year1 and node.d_p_earn < node.f_p_earn and node.f_earn > f_earnings:
                listE.append(node)
            self._search_criteria(node.left, year1, f_earnings, listE)
            self._search_criteria(node.right, year1, f_earnings, listE)

        return listE

    #esta clase crea el arbol en graphviz
class binary_tree_viz:
    def __init__(self, arbol_b):
        self.arbol_b = arbol_b

    def visualize(self):
        if self.arbol_b.root != None:
            nodo = self.arbol_b.root
            dot = graphviz.Digraph()
            dot.engine = 'neato'
            h = self.arbol_b.height(nodo) #altura de la raiz (se usa porque la posicion de los nodos se calcula a partir de este)
            nodo.pos = [0, h] ######
            dot.node(str(nodo.title), shape="circle", fixedsize="True", width="1", pos=nodo.spos()) #nodo raiz
            
            def add_nodes_edges(nodo, dot):
                h = self.arbol_b.height(nodo)
                if nodo.left: #hijo a la izquierda
                    nodo.left.pos[0] = nodo.pos[0] - h/1.5 + nodo.level/4# x
                    nodo.left.pos[1] = nodo.pos[1] - 1 # y
                    dot.node(str(nodo.left.title), shape="circle", fixedsize="True", width="1", pos=nodo.left.spos()) #agrega el nodo izquierda
                    dot.edge(str(nodo.title), str(nodo.left.title)) #agrega la arista a la izquierda
                    dot = add_nodes_edges(nodo.left, dot=dot)
                if nodo.right: #hijo a la derecha
                    nodo.right.pos[0] = nodo.pos[0] + h/1.5 - nodo.level/4 # x
                    nodo.right.pos[1] = nodo.pos[1] - 1 # y
                    dot.node(str(nodo.right.title), shape="circle", fixedsize="True", width="1", pos=nodo.right.spos()) #agrega el nodo derecha
                    dot.edge(str(nodo.title), str(nodo.right.title)) #agrega la arista a la derecha
                    dot = add_nodes_edges(nodo.right, dot=dot)
                return dot
            
            add_nodes_edges(nodo, dot)
            dot.render('binary_tree', view=True, format='png') #renderiza el arbol

        

arbol_peliculas = Arbol()

while True:
    print("Bienvenido al arbol AVL de películas, que deseas hacer?")
    menu=input("Escribe 1 para insertar película, 2 para eliminar, 3 buscar un nodo, 4 buscar un nodo por criterios, 5 mostrar el recorrido por niveles del arbol, 6 para visualizar arbol: ")
    while not menu.isdigit():
         menu=input("Escribe 1 para insertar película, 2 para eliminar, 3 buscar un nodo, 4 buscar un nodo por criterios, 5 mostrar el recorrido por niveles del arbol, 6 para visualizar arbol: ")
    menu=int(menu)

    if menu == 1:
        title = str(input("Ingrese el nombre de la película en el CSV, tenga en cuenta que el algoritmo es case sensitive: "))
        arbol_peliculas.insert(title)
        binary_tree_viz(arbol_peliculas).visualize()
    if menu == 2:
        if arbol_peliculas.root == None:
            print("No hay elementos en el arbol que eliminar")
        else:
            title = str(input("Ingrese el nombre de la película en el arbol que desea eliminar, tenga en cuenta que el algoritmo es case sensitive: "))
            arbol_peliculas.delete(title.replace(":", ""))
            binary_tree_viz(arbol_peliculas).visualize()
    if menu == 3:
        if arbol_peliculas.root == None:
            print("No hay elementos en el arbol que buscar")
        else:
            title = str(input("Ingrese el nombre de la película en el arbol que desea buscar, tenga en cuenta que el algoritmo es case sensitive: "))
            nodo = arbol_peliculas.search(title.replace(":", ""))
            while nodo[0] == None: #por si no encuentra ningun nodo con ese nombre
                title = str(input("Ingrese el nombre de la película en el arbol que desea buscar, tenga en cuenta que el algoritmo es case sensitive: "))
                nodo = arbol_peliculas.search(title.replace(":", ""))
            menu3=True
            while menu3:
                menu3_x = "P" #para que entre al while y evalue si es un número valido
                while not menu3_x.isdigit():
                    menu3_x=input("Escriba 1 para obtener el nivel del nodo, 2 para su factor balanceo, 3 para su padre, 4 para su abuelo, 5 para su tío, 6 para dejar este nodo:")
                menu3_x = int(menu3_x)
                if menu3_x == 1:
                    print(nodo[0].level) #nivel
                if menu3_x == 2:
                    print(arbol_peliculas.height(nodo[0].right) - arbol_peliculas.height(nodo[0].left)) #factor balanceo
                if menu3_x == 3:
                    if nodo[0].parent == None:
                        print("El nodo no tiene padre")
                    else:
                        print(nodo[0].parent.title) #padre
                if menu3_x == 4:
                    if nodo[0].parent == None:
                        print("El nodo no tiene abuelo")
                    elif nodo[0].parent.parent == None:
                        print("El nodo no tiene abuelo")
                    else:
                        print(nodo[0].parent.parent.title) #abuelo
                if menu3_x == 5:
                    if nodo[0].parent == None:
                        print("El nodo no tiene tio")
                    elif nodo[0].parent.parent == None:
                        print("El nodo no tiene tio")
                    else:
                        if nodo[0].parent.parent.left == nodo[0].parent:
                            print(f"El tio del nodo es {nodo[0].parent.parent.right.title}")
                        elif nodo[0].parent.parent.right == nodo[0].parent:
                            print(f"El tio del nodo es {nodo[0].parent.parent.left.title}")
                        else:
                            print("El nodo no tiene tío")
                if menu3_x == 6:
                    menu3=False
    if menu == 4:
        if arbol_peliculas.root == None:
            print("No hay elementos en el arbol que buscar")
        else:
            title = "P" #para que entre en el while y evalue si es un año valido
            while not title.isdigit():
                title = input("Ingrese el año en el que se estreno la película que desea buscar: ")
            title=int(title)

            f_earnings = "P" #para que entre en el while y evalue si es un valor valido
            while not f_earnings.isdigit():
                f_earnings = input("Ingrese las ganancias en el extranjero la película que desea buscar: ")
            f_earnings=int(f_earnings)

            Lnodo = arbol_peliculas.search_criteria(title, f_earnings)
            for i in Lnodo: #le pasa la lista con nodos
                print(i.title) #imprime el titulo de los nodos de la lista

            if len(Lnodo) != 0:
                selecc = "P" #para que entre al while y evalue si es un número valido
                while not selecc.isdigit() or int(selecc)>len(Lnodo) or int(selecc) < 1:
                    selecc=input("Escriba el número del nodo de la lista al que quiere evaluar, empieza desde el 1: ")
                selecc = int(selecc) #numero del elemento

                nodo = Lnodo[selecc-1] #agarra el nodo de la lista
                print(f"Nodo seleccionado: {nodo.title}")
                menu4=True
                while menu4:
                    menu4_x = "P" #para que entre al while y evalue si es un número valido
                    while not menu4_x.isdigit():
                        menu4_x=input("Escriba 1 para obtener el nivel del nodo, 2 para su factor balanceo, 3 para su padre, 4 para su abuelo, 5 para su tío, 6 para dejar este nodo:")
                    menu4_x = int(menu4_x)
                    if menu4_x == 1:
                        print(nodo.level)
                    if menu4_x == 2:
                        print(arbol_peliculas.height(nodo.right) - arbol_peliculas.height(nodo.left))
                    if menu4_x == 3:
                        if nodo.parent == None:
                            print("El nodo no tiene padre")
                        else:
                            print(nodo.parent.title) #padre
                    if menu4_x == 4:
                        if nodo.parent == None:
                            print("El nodo no tiene abuelo")
                        elif nodo.parent.parent == None: 
                            print("El nodo no tiene abuelo")
                        else:
                            print(nodo.parent.parent.title) #abuelo
                    if menu4_x == 5:
                        if nodo.parent == None:
                            print("El nodo no tiene abuelo")
                        elif nodo.parent.parent == None:
                            print("El nodo no tiene tio") #tio
                        else:
                            if nodo.parent.parent.left == nodo.parent:
                                print(f"El tio del nodo es {nodo.parent.parent.right.title}")
                            elif nodo.parent.parent.right == nodo.parent:
                                print(f"El tio del nodo es {nodo.parent.parent.left.title}")
                            else:
                                print("El nodo no tiene tío")
                    if menu4_x == 6:
                        menu4=False
            else:
                print("No se encontraron elementos con las características")
    if menu == 5:
        if arbol_peliculas.root == None:
            print("No hay arbol")
        else:
            arbol_peliculas.r_levels()
    if menu == 6:
        binary_tree_viz(arbol_peliculas).visualize()





