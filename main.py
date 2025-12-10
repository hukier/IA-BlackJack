import matplotlib.pyplot as plt
import numpy as np
import os
from src.environment import BlackjackEnvironment
from src.agent import AgenteQLearning
from src.desempeño import AnalizadorDesempeño

def entrenar_agente(episodios=100000):
    # Crear entorno y agente
    env = BlackjackEnvironment()
    # Usamos los hiperparametros del paper (alpha=0.015, gamma=1.0)
    agent = AgenteQLearning(alpha=0.015, gamma=1.0, epsilon=1.0, epsilon_decay=0.99995)
    
    historia_victorias = []  # 1 (Ganar), 0 (Empate/Perder)
    win_rates = []           # Promedio movil para el grafico
    analizador = AnalizadorDesempeño()  # Añadido para analisis
    
    print(f"Iniciando Entrenamiento ({episodios} episodios)")
    print(f"Alpha={agent.alpha}, Gamma={agent.gamma}")
    
    for e in range(episodios):
        # Reiniciar episodio
        estado = env.reset()
        terminado = False
        
        while not terminado:
            # 1 El agente elige accion
            accion = agent.elegir_accion(estado)
            
            # 2 El entorno responde
            siguiente_estado, recompensa, terminado = env.step(accion)
            
            # 3 El agente aprende (actualiza Q-Table)
            agent.actualizar_q_value(estado, accion, recompensa, siguiente_estado, terminado)
            
            # Avanzar estado
            estado = siguiente_estado
            
            if terminado:
                # Guardamos 1 si gano, 0 si no
                # Nota: En Blackjack ganar es +1.
                historia_victorias.append(1 if recompensa == 1 else 0)
                
                # Registrar en el analizador
                analizador.registrar_partida(e, recompensa, agent.epsilon)
                
                # Reducimos la exploracion
                agent.disminuir_epsilon()
        
        # Registro de progreso cada 1000 episodios
        if (e + 1) % 1000 == 0:
            # Calculamos el promedio de victorias de los ultimos 1000 juegos
            promedio_actual = np.mean(historia_victorias[-1000:])
            win_rates.append(promedio_actual)
            
            print(f"Episodio {e+1}: Win Rate={promedio_actual:.1%} | Epsilon={agent.epsilon:.4f}")

    # Generacion del Grafico
    if not os.path.exists("results"):
        os.makedirs("results")
        
    plt.figure(figsize=(10, 6))
    plt.plot(win_rates, label=f'Alpha={agent.alpha}, Gamma={agent.gamma}', color='purple')
    plt.title("Evolucion del Aprendizaje (Win Rate por cada 1000 juegos)")
    plt.xlabel("Bloques de 1000 Episodios")
    plt.ylabel("Tasa de Victorias")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/entrenamiento_blackjack.png")
    print(f"\nEntrenamiento finalizado. Grafico guardado en 'results/entrenamiento_blackjack.png'")
    
    # Generar analisis de desempeño
    print("\nGenerando analisis de desempeño")
    analizador.imprimir_estadisticas_resumen()
    analizador.guardar_todos_los_graficos(agent, carpeta_salida="results")
    
    return agent

def demostracion(agente):
    """Juega una partida con el agente ya entrenado y muestra los pasos."""
    print("\nDEMOSTRACION FINAL: AGENTE VS CRUPIER")
    env = BlackjackEnvironment()
    estado = env.reset()
    terminado = False
    
    print(f"Mano Inicial: {env.mano_jugador} (Suma: {estado[0]})")
    print(f"Carta Visible Crupier: {estado[1]}")
    
    while not terminado:
        # Usamos elegir_mejor_accion (sin exploracion) para probar lo aprendido
        accion = agente.elegir_mejor_accion(estado)
        accion_str = "PEDIR" if accion == 1 else "PLANTARSE"
        print(f"--> Agente decide: {accion_str}")
        
        estado, recompensa, terminado = env.step(accion)
        
        if accion == 1:
            print(f"    Recibe carta. Nueva Suma: {estado[0]}")
    
    print(f"Resultado final: {recompensa} (1=Gano, -1=Perdio, 0=Empate)")
    print(f"Mano Crupier: {env.crupier.mano}")

if __name__ == "__main__":

    agente_entrenado = entrenar_agente(episodios=100000)
    demostracion(agente_entrenado)