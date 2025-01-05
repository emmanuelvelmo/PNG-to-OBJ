from PIL import Image
import numpy

# Cargar imagen a matriz de arreglo
ruta_imagen = r'C:\Users\-\Desktop\MP\UI\Aim.png'
imagen = Image.open(ruta_imagen)
matriz_imagen = numpy.array(imagen)

# Obtener alto y ancho de imagen
alto_imagen, ancho_imagen = imagen.size

# Arreglo para coordenadas registradas (lista de tuplas (X,Y)) para cada objeto encontrado (instancias dinámicas)
lista_coordenadas = [][]

# Variable con 9 posiciones (cuadrado iterador)
cuadrado_iterador = [None] * 9

# Función de normalización de coordenadas en bordes de la imagen
def funcion_normalizacion(matriz_imagen, coord_y, coord_x):
    # Si un píxel se encuentra fuera de la matriz, se corrige
    if coord_y < 0:
        coord_y = 0
    elif coord_y >= alto_imagen:
        coord_y = alto_imagen - 1
    
    if coord_x < 0:
        coord_x = 0
    elif coord_x >= ancho_imagen:
        coord_x = ancho_imagen - 1
    
    # Retornar valor del píxel corregido si aplica
    return matriz_imagen[coord_y, coord_x]

def funcion_seguimiento_forma(coord_x, coord_y):
    global lista_coordenadas[][], cuadrado_iterador
    
    #lista_coordenadas[x][].len()
    
    siguiente_pixel[2] = {0.0, 0.0}
    
    # Buscar en sentido horario el grupo de píxel no nulo seguido de uno nulo, más cercano
    pixel_1 = cuadrado_iterador[1]
    pixel_2 = cuadrado_iterador[2]
    
    # Recursividad hasta toparse con una coordenada registrada en la lista (la coordenada de inicio en la recursividad)
    
    
    # Determinar las coordenadas para el siguiente píxel
    if cuadrado_iterador[1] != null and cuadrado_iterador[2] = null:
        siguiente_pixel = cuadrado_iterador[1]
    elif cuadrado_iterador[2] != null and cuadrado_iterador[5] = null:
        siguiente_pixel = cuadrado_iterador[2]
    elif cuadrado_iterador[5] != null and cuadrado_iterador[8] = null:
        siguiente_pixel = cuadrado_iterador[5]
    elif cuadrado_iterador[8] != null and cuadrado_iterador[7] = null:
        siguiente_pixel = cuadrado_iterador[8]
    elif cuadrado_iterador[7] != null and cuadrado_iterador[6] = null:
        siguiente_pixel = cuadrado_iterador[7]
    elif cuadrado_iterador[6] != null and cuadrado_iterador[3] = null:
        siguiente_pixel = cuadrado_iterador[6]
    elif cuadrado_iterador[3] != null and cuadrado_iterador[0] = null:
        siguiente_pixel = cuadrado_iterador[3]
    elif cuadrado_iterador[0] != null and cuadrado_iterador[1] = null:
        siguiente_pixel = cuadrado_iterador[0]
    
    # Trasladar píxel central de cuadro iterador hacia el siguiente pixel determinado (actualizar posiciones del cuadro iterador considerando la normalización de coordenadas)
    
    
    # Registrar píxel central actualizado en la lista de coordenadas
    





# Función para decidir si registrar o no una coordenada de la imagen
def funcion_registrar_coord(coord_y, coord_x):
    global lista_coordenadas[][], cuadrado_iterador
    
    # Si alguno de los píxeles del perímetro es espacio vacío y el píxel central no es nulo
    if (None in cuadrado_iterador[:4] + cuadrado_iterador[5:]) and cuadrado_iterador[4] is not None:
        # El píxel central no debe encontrarse previamente en las listas de coordenadas
        if cuadrado_iterador[4] != in lista_coordenadas[][x]:
            # De cumplirse lo anterior se ha encontrado un nuevo objeto en la imagen
            # Crear nuevo objeto en lista
            lista_coordenadas[x + 1][]
            
            # Agregar coordenada de píxel central en lista de coordenadas (como tupla (x, y))
            lista_coordenadas[][x].append(coord_x, coord_y)
            
            # Función para realizar seguimiento de la forma del objeto (agregar más coordenadas a la lista)
            funcion_seguimiento_forma(coord_x, coord_y)

# Iterar sobre la imagen
for coord_y in range(alto_imagen):
    for coord_x in range(ancho_imagen):
        # Comenzar por quinta posición del cuadro iterador sobre la esquina superior izquierda de la imagen
        cuadrado_iterador[0] = funcion_normalizacion(matriz_imagen, coord_y - 1, coord_x - 1)
        cuadrado_iterador[1] = funcion_normalizacion(matriz_imagen, coord_y - 1, coord_x)
        cuadrado_iterador[2] = funcion_normalizacion(matriz_imagen, coord_y - 1, coord_x + 1)
        cuadrado_iterador[3] = funcion_normalizacion(matriz_imagen, coord_y, coord_x - 1)
        # Píxel central del cuadrado iterador (no requiere normalización)
        cuadrado_iterador[4] = matriz_imagen[coord_y, coord_x]
        cuadrado_iterador[5] = funcion_normalizacion(matriz_imagen, coord_y, coord_x + 1)
        cuadrado_iterador[6] = funcion_normalizacion(matriz_imagen, coord_y + 1, coord_x - 1)
        cuadrado_iterador[7] = funcion_normalizacion(matriz_imagen, coord_y + 1, coord_x)
        cuadrado_iterador[8] = funcion_normalizacion(matriz_imagen, coord_y + 1, coord_x + 1)
        
        # Registrar o no coordenada de píxel central del cuadrado iterador
        funcion_registrar_coord(coord_y, coord_x)

# Retopología sobre lista de coordenadas
# Variable para iteración sobre coordenadas
linea_iter = [None] * 3

# Función para evaluar líneas rectas
def funcion_linea_recta(linea_iter, iter, lista_coordenadas):
    # Estimación de vértice central (punto medio para coordenadas X y Y)
    estimacion_vertice = (
        (linea_iter[0][0] + linea_iter[2][0]) / 2, # Punto medio en X
        (linea_iter[0][1] + linea_iter[2][1]) / 2 # Punto medio en Y
    )
    
    # Margen de error en coordenadas (grado de inclinación que no debe excederse)
    margen_error_x = 4
    margen_error_y = 4
    
    # Si el vértice central se encuentra dentro del margen de error, es una línea recta
    if abs(linea_iter[1][0] - estimacion_vertice[0]) <= margen_error_x and abs(linea_iter[1][1] - estimacion_vertice[1]) <= margen_error_y:
        # Eliminar vértice de la lista de vértices
        lista_coordenadas.pop(iter)

# Iterar sobre todas las coordenadas
iter = 1

while iter < len(lista_coordenadas) - 1:
    linea_iter[0] = lista_coordenadas[iter - 1] # Coordenada anterior
    linea_iter[1] = lista_coordenadas[iter] # Coordenada actual
    linea_iter[2] = lista_coordenadas[iter + 1] # Coordenada siguiente
    
    funcion_linea_recta(linea_iter, iter, lista_coordenadas)
    
    iter += 1

# Procesamiento de archivo OBJ
# Crear archivo OBJ conservando el nombre de la imagen


# Asignar coordenadas de la lista a archivo OBJ (leer en modo texto, asignar cero para el eje Z en todas las coordenadas)


# Asignar cara única a figuras


