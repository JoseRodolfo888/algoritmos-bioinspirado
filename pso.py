import random

# --- Configuración del algoritmo ---
n_particulas = 30
iteraciones = 50
w = 0.5   # Inercia: qué tanto la partícula quiere seguir en su dirección original
c1 = 1.5  # Cognitivo: qué tanto la partícula quiere regresar a su propio mejor récord
c2 = 2.0  # Social: qué tanto la partícula quiere seguir al líder del grupo

# --- Función objetivo ---
# Queremos encontrar los valores de x e y que hagan que este resultado sea lo más cercano a 0
def funcion_objetivo(x, y):
    return (x * x) + (y * y)

# --- 1. Inicialización (Crear nuestro enjambre) ---
enjambre = []

for i in range(n_particulas):
    # Creamos cada partícula como un "diccionario" con sus datos
    particula = {
        "x": random.uniform(-5, 5),
        "y": random.uniform(-5, 5),
        "vx": random.uniform(-1, 1), # Velocidad en x
        "vy": random.uniform(-1, 1), # Velocidad en y
        "mejor_x_propio": 0,
        "mejor_y_propio": 0,
        "mejor_valor_propio": float('inf') # 'inf' es infinito. Empezamos muy alto para que cualquier valor sea mejor.
    }
    
    # Evaluamos en dónde cayó la partícula por primera vez
    valor_inicial = funcion_objetivo(particula["x"], particula["y"])
    particula["mejor_x_propio"] = particula["x"]
    particula["mejor_y_propio"] = particula["y"]
    particula["mejor_valor_propio"] = valor_inicial
    
    # Agregamos la partícula a nuestra lista del enjambre
    enjambre.append(particula)

# Variables para guardar al líder del grupo (la partícula con el mejor récord de todas)
mejor_x_grupo = 0
mejor_y_grupo = 0
mejor_valor_grupo = float('inf')

# Buscamos quién es el mejor líder para empezar
for particula in enjambre:
    if particula["mejor_valor_propio"] < mejor_valor_grupo:
        mejor_valor_grupo = particula["mejor_valor_propio"]
        mejor_x_grupo = particula["x"]
        mejor_y_grupo = particula["y"]

# --- 2. Ciclo de optimización (¡A moverse!) ---
for t in range(iteraciones):
    for particula in enjambre:
        
        # Números aleatorios para darle un toque impredecible al movimiento
        r1 = random.random()
        r2 = random.random()
        
        # -- PASO A: Actualizar velocidad (hacia dónde se va a mover) --
        # Calculamos el impulso en el eje X
        impulso_propio_x = c1 * r1 * (particula["mejor_x_propio"] - particula["x"])
        impulso_grupo_x  = c2 * r2 * (mejor_x_grupo - particula["x"])
        particula["vx"]  = (w * particula["vx"]) + impulso_propio_x + impulso_grupo_x
        
        # Calculamos el impulso en el eje Y
        impulso_propio_y = c1 * r1 * (particula["mejor_y_propio"] - particula["y"])
        impulso_grupo_y  = c2 * r2 * (mejor_y_grupo - particula["y"])
        particula["vy"]  = (w * particula["vy"]) + impulso_propio_y + impulso_grupo_y
        
        # -- PASO B: Actualizar posición (dar el paso) --
        particula["x"] = particula["x"] + particula["vx"]
        particula["y"] = particula["y"] + particula["vy"]
        
        # -- PASO C: Evaluar la nueva posición --
        valor_actual = funcion_objetivo(particula["x"], particula["y"])
        
        # -- PASO D: ¿Rompió su récord personal? --
        if valor_actual < particula["mejor_valor_propio"]:
            particula["mejor_valor_propio"] = valor_actual
            particula["mejor_x_propio"] = particula["x"]
            particula["mejor_y_propio"] = particula["y"]
            
            # -- PASO E: ¿Rompió el récord de todo el grupo? --
            if valor_actual < mejor_valor_grupo:
                mejor_valor_grupo = valor_actual
                mejor_x_grupo = particula["x"]
                mejor_y_grupo = particula["y"]
                
    # Imprimir cómo le va al grupo cada 10 pasos
    if t % 10 == 0:
        print(f"Iteración {t}: Mejor valor del grupo = {mejor_valor_grupo:.5f}")

# --- 3. Resultados finales ---
print(f"\n¡Resultado final!")
print(f"Mejor posición encontrada: X = {mejor_x_grupo:.5f}, Y = {mejor_y_grupo:.5f}")
print(f"Valor mínimo: {mejor_valor_grupo:.10f}")