from PIL import Image
import numpy
import os

# Iterar sobre todos los archivos PNG en el directorio actual del script
for archivo in os.listdir():
    if archivo.endswith(".png"):
        # Obtener ruta del archivo PNG
        ruta_imagen = os.path.join(os.getcwd(), archivo)

        # Indicar archivo cargado
        print(f"{archivo} processing")

        # Cargar la imagen
        imagen_val = Image.open(ruta_imagen)

        # Verificar que el archivo PNG tenga 4 canales (RGBA)
        if imagen_val.mode == 'RGBA':
            # Convertir la imagen a un array de numpy (asumiendo que siempre es RGBA)
            matriz_inicio = numpy.array(imagen_val)

            # Crear una nueva matriz para la imagen procesada con las mismas dimensiones que la matriz_inicio
            imagen_procesada = numpy.zeros((matriz_inicio.shape[0], matriz_inicio.shape[1], 3), dtype=numpy.uint8)

            # Rellenar el fondo con blanco absoluto (RGB = 255, 255, 255)
            imagen_procesada[:, :] = [255, 255, 255]

            # Procesar cada píxel
            for y in range(matriz_inicio.shape[0]):
                for x in range(matriz_inicio.shape[1]):
                    if matriz_inicio[y, x, 3] != 0:  # Si el píxel no es transparente (canal alfa != 0)
                        # Convertir a negro en los tres canales (Rojo, Verde y Azul)
                        imagen_procesada[y, x] = [0, 0, 0]

            # Eliminar dos canales (quedarse con un solo canal)
            imagen_un_canal = imagen_procesada[:, :, 0]

            # Crear una nueva matriz con 2 filas y 2 columnas adicionales (borde de 2 píxeles)
            matriz_imagen = numpy.zeros(
                (imagen_un_canal.shape[0] + 2, imagen_un_canal.shape[1] + 2), # +2 píxeles en alto y ancho
                dtype=numpy.uint8
            )

            # Rellenar el borde con blanco absoluto (valor = 255)
            matriz_imagen[:, :] = 255

            # Copiar la imagen procesada en el centro de la nueva matriz
            matriz_imagen[1:-1, 1:-1] = imagen_un_canal

            # Obtener alto y ancho de la matriz
            alto_imagen = matriz_imagen.shape[0]
            ancho_imagen = matriz_imagen.shape[1]

            # Obtener el nombre de la imagen
            imagen_nombre = archivo.split('.')[0]

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
                cuadrado_iterador[4] = matriz_imagen[coord_y, coord_x]  # Píxel central (no requiere normalización)
                cuadrado_iterador[5] = matriz_imagen[funcion_normalizacion(coord_y, coord_x + 1)]
                cuadrado_iterador[6] = matriz_imagen[funcion_normalizacion(coord_y + 1, coord_x - 1)]
                cuadrado_iterador[7] = matriz_imagen[funcion_normalizacion(coord_y + 1, coord_x)]
                cuadrado_iterador[8] = matriz_imagen[funcion_normalizacion(coord_y + 1, coord_x + 1)]
                
                return cuadrado_iterador

            # Determinar las coordenadas para el siguiente píxel
            def funcion_coordenadas_pixel_elegido(pixel_elegido, coord_y, coord_x):
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
                
                return coord_y, coord_x

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
                    # Agregar la coordenada actual si no se encuentra en la lista del objeto
                    if (coord_x, coord_y) not in objeto_actual:
                        objeto_actual.append((coord_x, coord_y))
                    else:
                        break
                    
                    # Actualizar el cuadrado iterador
                    cuadrado_iterador_2 = actualizar_cuadrado_iterador(coord_y, coord_x, matriz_imagen, cuadrado_iterador_2)
                    
                    # Variable para el pixel elegido (se inicia en blanco)
                    pixel_elegido = 255
                    
                    # Buscar en sentido horario el grupo de píxel no nulo seguido de uno nulo o viceversa, más cercano
                    for iter in range(len(orden_giro) - 1):
                        pixel_actual = orden_giro[iter]
                        pixel_siguiente = orden_giro[iter + 1]
                        
                        # Verificar si el píxel actual es negro y el siguiente es blanco o viceversa y además la coordenada del píxel negro se encuentra previamente registrada
                        if (cuadrado_iterador_2[pixel_actual] == 0 and cuadrado_iterador_2[pixel_siguiente] == 255) or (cuadrado_iterador_2[pixel_actual] == 255 and cuadrado_iterador_2[pixel_siguiente] == 0):
                            # De los dos píxeles se escogerá el negro
                            if cuadrado_iterador_2[pixel_actual] == 255 and cuadrado_iterador_2[pixel_siguiente] == 0:
                                pixel_elegido = pixel_siguiente
                            elif cuadrado_iterador_2[pixel_actual] == 0 and cuadrado_iterador_2[pixel_siguiente] == 255:
                                pixel_elegido = pixel_actual
                            
                            # Determinar coordenadas del píxel negro
                            temp_y, temp_x = funcion_coordenadas_pixel_elegido(pixel_elegido, coord_y, coord_x)
                            
                            # Revisar si el píxel negro está previamente registrado
                            if (temp_x, temp_y) not in objeto_actual:
                                # Terminar el giro en sentido horario (ciclo for)
                                break
                    
                    # Si no se asigno un píxel, terminar el seguimiento
                    if pixel_elegido == 255:
                        break
                    
                    # Determinar las coordenadas para el siguiente píxel
                    coord_y, coord_x = funcion_coordenadas_pixel_elegido(pixel_elegido, coord_y, coord_x)
                    
                    # Si las nuevas coordenadas se encuentran en alguna de las listas de coordenadas, terminar el seguimiento
                    if any((coord_x, coord_y) in objeto_iter for objeto_iter in listas_coordenadas):
                        break
                    
                    # Si volvemos al punto inicial, registrar y terminar el seguimiento
                    if (coord_x, coord_y) == objeto_actual[0]:
                        # Agregar el objeto a la lista de coordenadas
                        listas_coordenadas.append(objeto_actual)
                        
                        break

            # Función para decidir si registrar o no una coordenada de la imagen
            def funcion_registrar_coord(coord_y, coord_x, matriz_imagen, listas_coordenadas, cuadrado_iterador):
                # Verificar si la coordenada no está ya registrada
                if not any((coord_x, coord_y) in objeto_iter for objeto_iter in listas_coordenadas):
                    # Iniciar seguimiento de la forma del objeto
                    funcion_seguimiento_forma(coord_y, coord_x, matriz_imagen, listas_coordenadas)

            # Iterar sobre la imagen
            for coord_y in range(alto_imagen):
                for coord_x in range(ancho_imagen):
                    # Actualizar cuadrado iterador
                    cuadrado_iterador = actualizar_cuadrado_iterador(coord_y, coord_x, matriz_imagen, cuadrado_iterador)
                    
                    # Si el píxel central es negro y alguno del perímetro es blanco
                    if cuadrado_iterador[4] == 0 and any(pixel_b == 255 for pixel_b in cuadrado_iterador[:3] + cuadrado_iterador[5:8]):
                        # Registrar o no coordenada de píxel central del cuadrado iterador
                        funcion_registrar_coord(coord_y, coord_x, matriz_imagen, listas_coordenadas, cuadrado_iterador)

            # Retopología
            # Variable para la línea de interación
            iter_linea = [0.0] * 3

            # Número de vértices de longuitud del iterador de líneas (número impar)
            vertices_iterador = 7

            # Posición del punto medio de la línea en el arreglo
            pm_val = (vertices_iterador - 1) // 2

            # Longuitud en píxeles del cuadrado de margen de tolerancia
            long_cuad_tolerancia = vertices_iterador - 2

            # Número de píxeles de margen de tolerancia
            tolerancia_x = (long_cuad_tolerancia - 1) / 2
            tolerancia_y = (long_cuad_tolerancia - 1) / 2

            def funcion_estimar_eliminar(objeto_iter, ind_cor):
                global iter_linea, pm_val, tolerancia_x, tolerancia_y
                
                # Calcular coordenada estimada
                coordenada_estimada = (
                    (iter_linea[0][0] + iter_linea[2][0]) / 2, # Valor medio de eje X
                    (iter_linea[0][1] + iter_linea[2][1]) / 2 # Valor medio de eje Y
                )
                
                # Eliminar la coordenada si está dentro del margen de error (punto medio)
                if (abs(coordenada_estimada[0] - iter_linea[1][0]) <= tolerancia_x or
                    abs(coordenada_estimada[1] - iter_linea[1][1]) <= tolerancia_y):
                    # Eliminar el vértice
                    objeto_iter.pop(iter + pm_val - ind_cor)
                    
                    # Corregir índice
                    ind_cor += 1
                
                return objeto_iter, ind_cor

            # Iterar sobre los objetos de la listas de coordenadas
            for objeto_iter in listas_coordenadas:
                # Verificar que hayan suficientes coordenadas en el objeto
                if len(objeto_iter) >= vertices_iterador:
                    # Espacios eliminados (corrección de índice en objeto)
                    ind_cor = 0
                    
                    # Itera en grupos de longuitud definida por el iterador de líneas
                    for iter in range(pm_val, len(objeto_iter) - (vertices_iterador - 1)):
                        # Asignar extremos y punto medio a la variable de iteración
                        iter_linea[0] = objeto_iter[iter - ind_cor]
                        iter_linea[1] = objeto_iter[iter + pm_val - ind_cor]
                        iter_linea[2] = objeto_iter[iter + (vertices_iterador - 1) - ind_cor]
                        
                        # Estimar y eliminar coordenadas del objeto
                        objeto_iter, ind_cor = funcion_estimar_eliminar(objeto_iter, ind_cor)
                    
                    # Retornar espacios eliminados a cero
                    ind_cor = 0
                    
                    # Eliminar vértices restantes usando una línea de longuitud de 3 píxeles
                    for iter in range(0, 2 * pm_val):
                        if iter < pm_val:
                            iter_linea[0] = objeto_iter[iter - ind_cor]
                            iter_linea[1] = objeto_iter[iter + 1 - ind_cor]
                            iter_linea[2] = objeto_iter[iter + 2 - ind_cor]
                            
                            # Estimar y eliminar coordenadas del objeto
                            objeto_iter, ind_cor = funcion_estimar_eliminar(objeto_iter, ind_cor)
                        else:
                            iter_linea[0] = objeto_iter[(len(objeto_iter) - 1) - (iter - pm_val) - 2 - ind_cor]
                            iter_linea[1] = objeto_iter[(len(objeto_iter) - 1) - (iter - pm_val) - 1 - ind_cor]
                            iter_linea[2] = objeto_iter[(len(objeto_iter) - 1) - (iter - pm_val) - ind_cor]
                            
                            # Estimar y eliminar coordenadas del objeto
                            objeto_iter, ind_cor = funcion_estimar_eliminar(objeto_iter, ind_cor)

            # Procesamiento de archivo OBJ
            # Contadores para vértices (distinguen el inicio y final de vértices para cada objeto)
            contador_vertices_inicio = 1
            contador_vertices_fin = 1

            # Crear archivo OBJ conservando el nombre de la imagen en el mismo directorio del script
            archivo_obj = open(f"{imagen_nombre}.obj", "w")

            # Asignar datos de cada objeto de la lista de coordenadas al archivo OBJ (escribir en modo texto)
            for objeto_iter in listas_coordenadas:
                # Asignar vértices del objeto
                for pos_iter in objeto_iter:
                    # Invertir la coordenada Y para corregir la orientación
                    y_invertido = alto_imagen - pos_iter[1]
                    
                    archivo_obj.write(f"v {pos_iter[0]} {y_invertido} 0.0\n")
                    
                    contador_vertices_fin += 1
                
                # Asignar cara a objeto (polígono de una única cara)
                archivo_obj.write("f ")
                
                for iter in range(contador_vertices_inicio, contador_vertices_fin):
                    archivo_obj.write(f"{iter} ")
                
                archivo_obj.write("\n")
                
                # Actualizar el inicio para el siguiente objeto
                contador_vertices_inicio = contador_vertices_fin

            # Cerrar archivo OBJ
            archivo_obj.close()

            # Indicar archivo de salida
            print(f"{imagen_nombre}.obj generated\n")

input()