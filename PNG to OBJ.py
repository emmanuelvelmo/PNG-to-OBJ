from PIL import Image
import numpy

# Cargar imagen a matriz de arreglo
ruta_imagen = r'C:\Users\-\Desktop\MP\UI\Aim.png'
imagen_val = Image.open(ruta_imagen)
matriz_imagen = numpy.array(imagen_val)

# Obtener alto y ancho de imagen
alto_imagen, ancho_imagen = imagen_val.size

# Arreglo para coordenadas registradas (lista de listas de tuplas (X,Y)) para cada objeto encontrado
listas_coordenadas = []

# Función de normalización de coordenadas en bordes de la imagen
def funcion_normalizacion(coord_y, coord_x):
    # Si un píxel se encuentra fuera de la matriz, se corrige
    if coord_y < 0:
        coord_y = 0
    elif coord_y >= alto_imagen:
        coord_y = alto_imagen - 1
    
    if coord_x < 0:
        coord_x = 0
    elif coord_x >= ancho_imagen:
        coord_x = ancho_imagen - 1
    
    return coord_y, coord_x

# Función para actualizar el cuadrado iterador
def actualizar_cuadrado_iterador(coord_y, coord_x, matriz_imagen, cuadrado_iterador):
    # Actualizar las 9 posiciones del cuadrado iterador
    cuadrado_iterador[0] = matriz_imagen[funcion_normalizacion(coord_y - 1, coord_x - 1)]
    cuadrado_iterador[1] = matriz_imagen[funcion_normalizacion(coord_y - 1, coord_x)]
    cuadrado_iterador[2] = matriz_imagen[funcion_normalizacion(coord_y - 1, coord_x + 1)]
    cuadrado_iterador[3] = matriz_imagen[funcion_normalizacion(coord_y, coord_x - 1)]
    cuadrado_iterador[4] = matriz_imagen[coord_y, coord_x] # Píxel central (no requiere normalización)
    cuadrado_iterador[5] = matriz_imagen[funcion_normalizacion(coord_y, coord_x + 1)]
    cuadrado_iterador[6] = matriz_imagen[funcion_normalizacion(coord_y + 1, coord_x - 1)]
    cuadrado_iterador[7] = matriz_imagen[funcion_normalizacion(coord_y + 1, coord_x)]
    cuadrado_iterador[8] = matriz_imagen[funcion_normalizacion(coord_y + 1, coord_x + 1)]

# Función de seguimiento de la forma del objeto
def funcion_seguimiento_forma(coord_y, coord_x, matriz_imagen, listas_coordenadas):
    # Inicializar lista de coordenadas del objeto actual
    objeto_actual = []
    
    # Variable con 9 posiciones (cuadrado iterador)
    cuadrado_iterador = [None] * 9
    
    # Orden de giro en sentido horario: [1, 2, 5, 8, 7, 6, 3, 0, 1]
    orden_giro = [1, 2, 5, 8, 7, 6, 3, 0, 1]
    
    # Bucle para seguir el contorno del objeto
    while True:
        # Agregar la coordenada actual a la lista
        objeto_actual.append((coord_x, coord_y))
        
        # Actualizar el cuadrado iterador
        actualizar_cuadrado_iterador(coord_y, coord_x, matriz_imagen, cuadrado_iterador)
        
        # Variable para el pixel elegido
        pixel_elegido = None
        
        # Buscar en sentido horario el grupo de píxel no nulo seguido de uno nulo o viceversa, más cercano
        for iter in range(len(orden_giro) - 1):
            pixel_actual = orden_giro[iter]
            pixel_siguiente = orden_giro[iter + 1]
            
            # Verificar si el píxel actual es no nulo y el siguiente es nulo o viceversa
            if (cuadrado_iterador[pixel_actual] is None and cuadrado_iterador[pixel_siguiente] is not None) or (cuadrado_iterador[pixel_actual] is not None and cuadrado_iterador[pixel_siguiente] is None):
                # De los dos píxeles se escogerá el no nulo
                if cuadrado_iterador[pixel_actual] is None and cuadrado_iterador[pixel_siguiente] is not None:
                    pixel_elegido = pixel_siguiente
                elif cuadrado_iterador[pixel_actual] is not None and cuadrado_iterador[pixel_siguiente] is None:
                    pixel_elegido = pixel_actual
                else:
                    # No se encontró seguimiento del borde, terminar el seguimiento
                    break
        
        # Determinar las coordenadas para el siguiente píxel
        if pixel_elegido == 1:
            coord_y, coord_x = coord_y - 1, coord_x
        elif pixel_elegido == 2:
            coord_y, coord_x = coord_y - 1, coord_x + 1
        elif pixel_elegido == 5:
            coord_y, coord_x = coord_y, coord_x + 1
        elif pixel_elegido == 8:
            coord_y, coord_x = coord_y + 1, coord_x + 1
        elif pixel_elegido == 7:
            coord_y, coord_x = coord_y + 1, coord_x
        elif pixel_elegido == 6:
            coord_y, coord_x = coord_y + 1, coord_x - 1
        elif pixel_elegido == 3:
            coord_y, coord_x = coord_y, coord_x - 1
        elif pixel_elegido == 0:
            coord_y, coord_x = coord_y - 1, coord_x - 1
        
        # Si las nuevas coordenadas se encuentran en alguna de las listas de coordenadas, terminar el seguimiento
        if any((coord_x, coord_y) in objeto_iter for objeto_iter in listas_coordenadas):
            break
        
        # Si volvemos al punto inicial, terminar el seguimiento
        if (coord_x, coord_y) == objeto_actual[0]:
            break
    
    # Agregar el objeto a la lista de coordenadas
    listas_coordenadas.append(objeto_actual)

# Función para decidir si registrar o no una coordenada de la imagen
def funcion_registrar_coord(coord_y, coord_x, matriz_imagen, listas_coordenadas):
    # Verificar si el píxel central es no nulo
    if matriz_imagen[coord_y, coord_x].any():
        # Verificar si la coordenada no está ya registrada
        if not any((coord_x, coord_y) in objeto_iter for objeto_iter in listas_coordenadas):
            # Iniciar seguimiento de la forma del objeto
            funcion_seguimiento_forma(coord_y, coord_x, matriz_imagen, listas_coordenadas)

# Iterar sobre la imagen
for coord_y in range(alto_imagen):
    for coord_x in range(ancho_imagen):
        # Registrar o no coordenada de píxel central del cuadrado iterador
        funcion_registrar_coord(coord_y, coord_x, matriz_imagen, listas_coordenadas)

# Procesamiento de archivo OBJ
# Crear archivo OBJ conservando el nombre de la imagen


# Asignar coordenadas de la lista a archivo OBJ (leer en modo texto, asignar cero para el eje Z en todas las coordenadas)


# Asignar cara única a figuras

