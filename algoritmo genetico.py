import random
import math

# --- CLASE PRINCIPAL ---
class Disparo:
    def __init__(self, angulo, potencia, objetivo):
        self.angulo = angulo      # Grados
        self.potencia = potencia  # Metros por segundo
        self.objetivo = objetivo
        self.distancia_caida = self.calcular_distancia()
        self.error = abs(self.objetivo - self.distancia_caida)

    @classmethod
    def crear_aleatorio(cls, objetivo):
        angulo = random.uniform(10, 80)
        potencia = random.uniform(10, 200) # Rango ampliado para objetivos lejanos
        return cls(angulo, potencia, objetivo)

    def calcular_distancia(self):
        # Fórmula: d = (v² * sin(2*theta)) / g
        radianes = math.radians(self.angulo)
        gravedad = 9.8
        distancia = (self.potencia**2 * math.sin(2 * radianes)) / gravedad
        return distancia

    def cruzar(self, pareja):
        nuevo_angulo = (self.angulo + pareja.angulo) / 2
        nueva_potencia = (self.potencia + pareja.potencia) / 2
        return Disparo(nuevo_angulo, nueva_potencia, self.objetivo)

    def mutar(self, tasa):
        nuevo_angulo = self.angulo
        nueva_potencia = self.potencia
        
        if random.random() < tasa:
            nuevo_angulo += random.uniform(-5, 5)
            nueva_potencia += random.uniform(-10, 10)
            
        nuevo_angulo = max(1, min(89, nuevo_angulo))
        nueva_potencia = max(1, min(300, nueva_potencia))
        
        return Disparo(nuevo_angulo, nueva_potencia, self.objetivo)

def main():
    print("--- SIMULADOR DE TIRO PARABÓLICO (EVOLUTIVO) ---")
    
    # --- ENTRADA DE DATOS PROPIOS ---
    try:
        distancia_input = float(input("¿A qué distancia está el objetivo (metros)? [Ej: 750]: ") or 750)
        poblacion_input = int(input("¿Tamaño de la población? [Ej: 20]: ") or 20)
        mutacion_input = float(input("¿Tasa de mutación (0.0 a 1.0)? [Ej: 0.2]: ") or 0.2)
    except ValueError:
        print("Entrada no válida. Usando valores por defecto.")
        distancia_input, poblacion_input, mutacion_input = 750, 20, 0.2

    print(f"\n Iniciando búsqueda para {distancia_input}m...\n")
    
    # Crear población inicial
    poblacion = [Disparo.crear_aleatorio(distancia_input) for _ in range(poblacion_input)]
    generacion = 1
    exito = False

    while not exito:
        poblacion = sorted(poblacion, key=lambda x: x.error)
        mejor = poblacion[0]
        
        print(f"Gen {generacion} | Mejor: {mejor.distancia_caida:.2f}m | Error: {mejor.error:.2f}m | Ángulo: {mejor.angulo:.1f}°")

        if mejor.error < 1.0:
            exito = True
            break

        # Reproducción
        nueva_generacion = []
        nueva_generacion.extend(poblacion[:2]) # Elitismo
        
        padres_potenciales = poblacion[:int(len(poblacion)/2)]
        
        while len(nueva_generacion) < poblacion_input:
            p1, p2 = random.sample(padres_potenciales, 2)
            hijo = p1.cruzar(p2).mutar(mutacion_input)
            nueva_generacion.append(hijo)
            
        poblacion = nueva_generacion
        generacion += 1

        # Límite de seguridad por si no converge
        if generacion > 1000:
            print("\nSe alcanzó el límite de 1000 generaciones sin éxito total.")
            break

    print(f"\n ¡RESULTADO FINAL!")
    print(f"Configuración: {mejor.angulo:.2f}° de inclinación y {mejor.potencia:.2f} m/s de potencia.")

if __name__ == "__main__":
    main()