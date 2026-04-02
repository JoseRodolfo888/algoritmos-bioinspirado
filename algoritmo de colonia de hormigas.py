import random

# --- CONFIGURACIÓN DEL PROBLEMA ---
# Matriz de distancias entre 4 ciudades (0, 1, 2, 3)
# 0 significa que es la misma ciudad. 
distancias = [
    [0,  10, 15, 20],
    [10,  0, 35, 25],
    [15, 35,  0, 30],
    [20, 25, 30,  0]
]

NUM_CIUDADES = len(distancias)
NUM_HORMIGAS = 5
ITERACIONES = 15
EVAPORACION = 0.5  # Qué tan rápido desaparece el rastro (50%)
Q = 100            # Cantidad constante para calcular cuánta feromona depositar

# Inicializamos la matriz de feromonas con un nivel base (1.0) en todos los caminos
feromonas = [[1.0 for _ in range(NUM_CIUDADES)] for _ in range(NUM_CIUDADES)]

def calcular_distancia_ruta(ruta):
    distancia_total = 0
    # Sumar la distancia de salto en salto
    for i in range(len(ruta) - 1):
        actual = ruta[i]
        siguiente = ruta[i+1]
        distancia_total += distancias[actual][siguiente]
    return distancia_total

def elegir_siguiente_ciudad(actual, visitadas):
    probabilidades = []
    ciudades_disponibles = []

    # Calculamos qué tan atractiva es cada ciudad no visitada
    for destino in range(NUM_CIUDADES):
        if destino not in visitadas:
            visibilidad = 1.0 / distancias[actual][destino] # Preferimos ciudades más cercanas
            nivel_feromona = feromonas[actual][destino]
            
            # Atracción = Feromona * Visibilidad
            atraccion = nivel_feromona * visibilidad
            probabilidades.append(atraccion)
            ciudades_disponibles.append(destino)

    # Convertir las atracciones en porcentajes (probabilidades)
    total_atraccion = sum(probabilidades)
    probabilidades = [p / total_atraccion for p in probabilidades]
    
    # Elegir aleatoriamente, pero con sesgo hacia los caminos más probables (ruleta)
    eleccion = random.choices(ciudades_disponibles, weights=probabilidades)[0]
    return eleccion

def main():
    print("--- ALGORITMO DE COLONIA DE HORMIGAS (ACO) ---\n")
    mejor_ruta_global = None
    mejor_distancia_global = float('inf')

    for iteracion in range(ITERACIONES):
        rutas_hormigas = []
        distancias_rutas = []

        # 1. Las hormigas exploran y construyen sus caminos
        for _ in range(NUM_HORMIGAS):
            ciudad_inicial = random.randint(0, NUM_CIUDADES - 1)
            ruta = [ciudad_inicial]
            
            # Visitar todas las ciudades
            while len(ruta) < NUM_CIUDADES:
                siguiente = elegir_siguiente_ciudad(ruta[-1], ruta)
                ruta.append(siguiente)
                
            # Regresar a la ciudad de origen para cerrar el ciclo
            ruta.append(ruta[0])
            
            distancia = calcular_distancia_ruta(ruta)
            rutas_hormigas.append(ruta)
            distancias_rutas.append(distancia)

            # Actualizar el mejor registro global
            if distancia < mejor_distancia_global:
                mejor_distancia_global = distancia
                mejor_ruta_global = ruta

        # 2. Evaporación: El rastro viejo pierde fuerza
        for i in range(NUM_CIUDADES):
            for j in range(NUM_CIUDADES):
                feromonas[i][j] *= (1.0 - EVAPORACION)

        # 3. Refuerzo: Las hormigas depositan nuevas feromonas
        for i in range(NUM_HORMIGAS):
            ruta = rutas_hormigas[i]
            distancia = distancias_rutas[i]
            
            # Las rutas más cortas dejan más cantidad de feromonas
            aporte = Q / distancia 
            
            for j in range(len(ruta) - 1):
                origen = ruta[j]
                destino = ruta[j+1]
                # Sumamos la feromona en ambas direcciones del camino
                feromonas[origen][destino] += aporte
                feromonas[destino][origen] += aporte

        print(f"Iteración {iteracion + 1} | Mejor distancia de la ronda: {min(distancias_rutas)}")

    print("\n ¡BÚSQUEDA TERMINADA!")
    print(f"La mejor ruta encontrada fue: {mejor_ruta_global}")
    print(f"Con una distancia total de: {mejor_distancia_global}")

if __name__ == "__main__":
    main()