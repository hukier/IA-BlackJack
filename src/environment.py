from src.utils import crear_baraja, calcular_puntaje
from src.crupier import Crupier

#entorno del juego de blackjack
class BlackjackEnvironment:
    def __init__(self):
        # Inicializamos el crupier
        self.crupier = Crupier()
        
        # Inicializamos la mano del jugador, empieza vacia
        self.mano_jugador = []
        self.suma_jugador = 0
        self.carta_crupier = 0
        self.as_utilizable = False
        self.juego_terminado = False
    
    def reset(self):
        #reinicia el juego y devuelve el estado inicial
        self.mano_jugador = []
        self.crupier.reiniciar()
        
        # jugador recibe dos cartas
        carta1 = crear_baraja()
        carta2 = crear_baraja()
        self.mano_jugador.append(carta1)
        self.mano_jugador.append(carta2)
        
        # Le damos dos cartas al crupier y obtenemos la carta visible
        self.carta_crupier = self.crupier.repartir_carta_inicial()
        
        # Calculamos el puntaje del jugador
        self.suma_jugador, self.as_utilizable = calcular_puntaje(self.mano_jugador)
        
        # Si el jugador tiene menos de 12, le damos mas cartas automaticamente
        # porque nunca se va a pasar de 21 con menos de 12
        while self.suma_jugador < 12:
            nueva_carta = crear_baraja()
            self.mano_jugador.append(nueva_carta)
            self.suma_jugador, self.as_utilizable = calcular_puntaje(self.mano_jugador)
        
        # El juego no ha terminado todavia
        self.juego_terminado = False
        
        # Retornamos el estado inicial
        estado = (self.suma_jugador, self.carta_crupier, self.as_utilizable)
        return estado
    
    #hacer una funcion para actuar en entorno 
    def step(self, accion):
        # Esta funcion realiza una accion (0=plantarse, 1=pedir) y retorna
        # el nuevo estado, la recompensa, y si el juego ha terminado
    
        if self.juego_terminado:
            print("El juego ya ha terminado")
            return (self.suma_jugador, self.carta_crupier, self.as_utilizable), 0, self.juego_terminado
        
        if accion == 1:  # Pedir carta
            nueva_carta = crear_baraja()
            self.mano_jugador.append(nueva_carta)
            self.suma_jugador, self.as_utilizable = calcular_puntaje(self.mano_jugador)
            
            # Revisamos si el jugador se paso de 21
            if self.suma_jugador > 21:
                self.juego_terminado = True
                recompensa = -1  # El jugador pierde
            else:
                recompensa = 0  # El juego continua
            
            estado = (self.suma_jugador, self.carta_crupier, self.as_utilizable)
            return estado, recompensa, self.juego_terminado
        
        elif accion == 0:  # Plantarse
            # El jugador se planta, ahora juega el crupier
            puntaje_crupier, as_utilizable_crupier = self.crupier.jugar()
            
            # Determinamos el resultado del juego
            self.juego_terminado = True
            if puntaje_crupier > 21 or self.suma_jugador > puntaje_crupier:
                recompensa = 1  # El jugador gana
            elif self.suma_jugador < puntaje_crupier:
                recompensa = -1  # El jugador pierde
            else:
                recompensa = 0  # Empate
            
            estado = (self.suma_jugador, self.carta_crupier, self.as_utilizable)
            return estado, recompensa, self.juego_terminado
        
        else:
            print("Accion invalida")
            return (self.suma_jugador, self.carta_crupier, self.as_utilizable), 0, self.juego_terminado
    