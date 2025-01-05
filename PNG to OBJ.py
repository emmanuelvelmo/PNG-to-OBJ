from PIL import Image
import numpy

# Cargar imagen a matriz de arreglo (unir todas la capas de colores en una misma con valores nulos (transparencia) y no nulos)
ruta_imagen = r'C:\Users\-\Desktop\MP\UI\Aim.png'
imagen_val = Image.open(ruta_imagen)
matriz_imagen = numpy.array(imagen_val)

# Obtener el nombre de la imagen
imagen_nombre = ruta_imagen.split('\\')[-1].split('.')[0]

# Obtener alto y ancho de imagen
alto_imagen, ancho_imagen = imagen_val.size

# Primer cuadrado iterador
cuadrado_iterador = [None] * 9

# Arreglo para coordenadas registradas (lista de listas de tuplas (X,Y)) para cada objeto encontrado
listas_coordenadas = []

# Función de normalización de coordenadas en bordes de la imagen
def funcion_normalizacion(coord_y, coord_x):
    global alto_imagen, ancho_imagen
    
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
    
    return cuadrado_iterador

# Función de seguimiento de la forma del objeto
def funcion_seguimiento_forma(coord_y, coord_x, matriz_imagen, listas_coordenadas):
    # Inicializar lista de coordenadas del objeto actual
    objeto_actual = []
    
    # Segundo cuadrado iterador
    cuadrado_iterador_2 = [None] * 9
    
    # Orden de giro en sentido horario: [1, 2, 5, 8, 7, 6, 3, 0, 1]
    orden_giro = [1, 2, 5, 8, 7, 6, 3, 0, 1]
    
    # Bucle para seguir el contorno del objeto
    while True:
        # Agregar la coordenada actual a la lista
        objeto_actual.append((coord_x, coord_y))
        
        # Actualizar el cuadrado iterador
        cuadrado_iterador_2 = actualizar_cuadrado_iterador(coord_y, coord_x, matriz_imagen, cuadrado_iterador_2)
        
        # Variable para el pixel elegido
        pixel_elegido = None
        
        # Buscar en sentido horario el grupo de píxel no nulo seguido de uno nulo o viceversa, más cercano
        for iter in range(len(orden_giro) - 1):
            pixel_actual = orden_giro[iter]
            pixel_siguiente = orden_giro[iter + 1]
            
            # Verificar si el píxel actual es no nulo y el siguiente es nulo o viceversa
            if (cuadrado_iterador_2[pixel_actual] is None and cuadrado_iterador_2[pixel_siguiente] is not None) or (cuadrado_iterador_2[pixel_actual] is not None and cuadrado_iterador_2[pixel_siguiente] is None):
                # De los dos píxeles se escogerá el no nulo
                if cuadrado_iterador_2[pixel_actual] is None and cuadrado_iterador_2[pixel_siguiente] is not None:
                    pixel_elegido = pixel_siguiente
                elif cuadrado_iterador_2[pixel_actual] is not None and cuadrado_iterador_2[pixel_siguiente] is None:
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
def funcion_registrar_coord(coord_y, coord_x, matriz_imagen, listas_coordenadas, cuadrado_iterador):
    # Verificar si el píxel central es no nulo
    if cuadrado_iterador[4].any():
        # Verificar si la coordenada no está ya registrada
        if not any((coord_x, coord_y) in objeto_iter for objeto_iter in listas_coordenadas):
            # Iniciar seguimiento de la forma del objeto
            funcion_seguimiento_forma(coord_y, coord_x, matriz_imagen, listas_coordenadas)

# Iterar sobre la imagen
for coord_y in range(alto_imagen):
    for coord_x in range(ancho_imagen):
        # Actualizar cuadrado iterador
        cuadrado_iterador = actualizar_cuadrado_iterador(coord_y, coord_x, matriz_imagen, cuadrado_iterador)
        
        # Si el píxel central no está vacío y alguno del perímetro está vacío 
        if cuadrado_iterador[4] is not None and any(pixel is None for pixel in cuadrado_iterador[:3] + cuadrado_iterador[5:8]):
            # Registrar o no coordenada de píxel central del cuadrado iterador
            funcion_registrar_coord(coord_y, coord_x, matriz_imagen, listas_coordenadas, cuadrado_iterador)

# Retopología
# Variable para iterar sobre coordenadas en grupos de 3 (evaluar líneas rectas)
iter_linea = [0.0] * 3

# Función para evaluar líneas rectas
def funcion_evaluar_linear():
    global iter_linea
    
    # Márgenes de error (en píxeles)
    margen_x = 2
    margen_y = 2
    
    # Iterar sobre los objetos de la listas de coordenadas
    for objeto_iter in listas_coordenadas:
        # Iterar sobre las coordenadas del objeto de la listas de coordenadas
        for iter in range(len(objeto_iter) - 2):
            # Asignar 3 coordenadas a la variable de iteración
            iter_linea[0] = objeto_iter[iter]
            iter_linea[1] = objeto_iter[iter + 1]
            iter_linea[2] = objeto_iter[iter + 2]
            
            # Calcular coordenada estimada
            coordenada_estimada = (
                (objeto_iter[iter][0] + objeto_iter[iter + 2][0]) / 2, # valor medio de eje X
                (objeto_iter[iter][1] + objeto_iter[iter + 2][1]) / 2 # valor medio de eje Y
            )
            
            # Si la coordenada estimada está dentro del márgen de error entonces se elimina la coordenada de listas de coordenadas
            if abs(coordenada_estimada[0] - objeto_iter[iter + 1][0]) <= margen_x and abs(coordenada_estimada[1] - objeto_iter[iter + 1][1]) <= margen_y:
                objeto_iter.pop(iter + 1)

# Procesamiento de archivo OBJ
# Crear archivo OBJ conservando el nombre de la imagen el mismo directorio del script
archivo_obj = open(f"{imagen_nombre}.obj", "w")

# Asignar datos de cada objeto de la listas de coordenadas al archivo OBJ (escribir en modo texto)
for objeto_iter in listas_coordenadas:
    # Asignar vértices del objeto
    for coord in objeto_iter:
        archivo_obj.write(f"v {coord[0]} {coord[1]} 0.0\n")
    
    # Asignar cara (polígono de una única cara)
    archivo_obj.write("f ")
    for i in range(1, len(objeto_iter) + 1):
        archivo_obj.write(f"{i} ")
    archivo_obj.write("\n")

# Cerrar archivo OBJ
archivo_obj.close()