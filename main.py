# Probamos el crupier y el environment sin el agente
from src.environment import BlackjackEnvironment
from src.crupier import Crupier
from src.utils import crear_baraja, calcular_puntaje

def probar_crupier():
    # probar crupier jugando varias manos
    print("PROBANDO EL CRUPIER")
    
    # Creamos un crupier
    crupier = Crupier()
    
    # Jugamos 5 manos de prueba
    for i in range(5):
        print(f"\nMano {i+1}:")
        # Damos cartas iniciales al crupier
        carta_visible = crupier.repartir_carta_inicial()
        print(f"  Carta visible del crupier: {carta_visible}")
        print(f"  Mano inicial del crupier: {crupier.mano}")
        
        # El crupier juega
        puntaje_final, tiene_as = crupier.jugar()
        print(f"  Mano final del crupier: {crupier.mano}")
        print(f"  Puntaje final: {puntaje_final}")
        
        if puntaje_final > 21:
            print(f"  El crupier se paso de 21!")
        # Reiniciamos para la siguiente mano
        crupier.reiniciar()


def probar_environment():
    print("PROBANDO EL ENVIRONMENT")
    
    # Creamos el environment
    env = BlackjackEnvironment()
    # Jugamos 3 manos de prueba
    for i in range(3):
        print(f"\n--- Mano {i+1} ---")
        
        # Reiniciamos el juego
        estado = env.reset()
        suma_jugador = estado[0]
        carta_crupier = estado[1]
        tiene_as = estado[2]
        
        print(f"Estado inicial:")
        print(f"  Mano jugador: {env.mano_jugador}")
        print(f"  Suma jugador: {suma_jugador}")
        print(f"  Carta visible crupier: {carta_crupier}")
        print(f"  As utilizable: {tiene_as}")
        
        # Jugamos la mano con una estrategia simple
        # Estrategia: pedir si tenemos menos de 17, plantarse si tenemos 17 o mas
        terminado = False
        
        while not terminado:
            # Decidimos accion segun estrategia simple
            if suma_jugador < 17:
                accion = 1  # Pedir
                print(f"\n  Accion: PEDIR (suma actual: {suma_jugador})")
            else:
                accion = 0  # Plantarse
                print(f"\n  Accion: PLANTARSE (suma actual: {suma_jugador})")
            
            # Ejecutamos la accion
            siguiente_estado, recompensa, terminado = env.step(accion)
            
            # Actualizamos el estado
            suma_jugador = siguiente_estado[0]
            carta_crupier = siguiente_estado[1]
            tiene_as = siguiente_estado[2]
            
            print(f"  Nueva mano: {env.mano_jugador}")
            print(f"  Nueva suma: {suma_jugador}")
            
            # Si el juego termino, mostramos el resultado
            if terminado:
                print(f"\n  JUEGO TERMINADO")
                print(f"  Mano crupier: {env.crupier.mano}")
                puntaje_crupier, _ = env.crupier.obtener_puntaje()
                print(f"  Puntaje crupier: {puntaje_crupier}")
                print(f"  Puntaje jugador: {suma_jugador}")
                
                if recompensa > 0:
                    print(f"  RESULTADO: VICTORIA! (recompensa: +1)")
                elif recompensa < 0:
                    print(f"  RESULTADO: DERROTA (recompensa: -1)")
                else:
                    print(f"  RESULTADO: EMPATE (recompensa: 0)")


def jugar_manualmente():
    # Esta funcion permite jugar una mano manualmente
    print("\n" + "=" * 50)
    print("JUGAR UNA MANO MANUALMENTE")
    print("=" * 50)
    
    # Creamos el environment
    env = BlackjackEnvironment()
    
    # Reiniciamos el juego
    estado = env.reset()
    suma_jugador = estado[0]
    carta_crupier = estado[1]
    tiene_as = estado[2]
    
    print(f"\nEstado inicial:")
    print(f"  Tu mano: {env.mano_jugador}")
    print(f"  Tu suma: {suma_jugador}")
    print(f"  Carta visible del crupier: {carta_crupier}")
    print(f"  Tienes As utilizable: {tiene_as}")
    
    # Jugamos la mano
    terminado = False
    
    while not terminado:
        # Preguntamos al usuario que hacer
        print(f"\nTu suma actual: {suma_jugador}")
        print("Que quieres hacer?")
        print("  0 = Plantarse")
        print("  1 = Pedir carta")
        
        # Leemos la accion del usuario
        accion_input = input("Ingresa tu accion (0 o 1): ")
        
        # Validamos la entrada
        if accion_input == "0":
            accion = 0
        elif accion_input == "1":
            accion = 1
        else:
            print("Accion invalida, intenta de nuevo")
            continue
        
        # Ejecutamos la accion
        siguiente_estado, recompensa, terminado = env.step(accion)
        
        # Actualizamos el estado
        suma_jugador = siguiente_estado[0]
        
        if accion == 1 and not terminado:
            print(f"Nueva carta! Tu mano: {env.mano_jugador}")
            print(f"Tu nueva suma: {suma_jugador}")
        
        # Si el juego termino, mostramos el resultado
        if terminado:
            print(f"\n{'='*50}")
            print("JUEGO TERMINADO")
            print(f"{'='*50}")
            print(f"Tu mano final: {env.mano_jugador}")
            print(f"Tu puntaje: {suma_jugador}")
            print(f"Mano del crupier: {env.crupier.mano}")
            puntaje_crupier, _ = env.crupier.obtener_puntaje()
            print(f"Puntaje del crupier: {puntaje_crupier}")
            
            if recompensa > 0:
                print(f"\nFELICIDADES! GANASTE!")
            elif recompensa < 0:
                print(f"\nPERDISTE :(")
            else:
                print(f"\nEMPATE!")


# Programa principal
if __name__ == "__main__":
    print("PRUEBAS DEL JUEGO DE BLACKJACK")
    # Probamos el crupier
    probar_crupier()
    
    # Probamos el environment
    probar_environment()
    
    # Preguntamos si quiere jugar manualmente
    jugar = input("Quieres jugar una mano manualmente? (s/n): ")
    
    if jugar.lower() == "s" or jugar.lower() == "si":
        jugar_manualmente()
    
    print("FIN DE LAS PRUEBAS")
