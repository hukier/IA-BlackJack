from src.utils import crear_baraja, calcular_puntaje

class Crupier:
    def __init__(self):
        # crupier comienza con una mano vacia
        self.mano = []
    
    def repartir_carta_inicial(self):
        # Le damos dos cartas al crupier al inicio
        carta1 = crear_baraja()
        carta2 = crear_baraja()
        
        # Agregamos las cartas a la mano
        self.mano.append(carta1)
        self.mano.append(carta2)
        
        # Retornamos la primera carta que es la que se ve
        carta_visible = self.mano[0]
        return carta_visible
    
    def jugar(self):
        # El crupier juega siguiendo las reglas del casino
        # Pide con 16 o menos, se planta con 17 o mas

        puntaje_actual = 0
        as_utilizable = False # Variable para saber si tiene As utilizable
        # Iniciamos un loop para que el crupier juegue
        seguir_jugando = True
        
        while seguir_jugando:
            # Calculamos el puntaje
            puntaje_actual, as_utilizable = calcular_puntaje(self.mano)
            
            # Revisamos si el puntaje es 17 o mas
            if puntaje_actual >= 17:
                # Si tiene 17 o mas, se planta
                seguir_jugando = False
            else:
                # Si tiene 16 o menos, pide otra carta
                nueva_carta = crear_baraja()
                self.mano.append(nueva_carta)
        
        # Retornamos el puntaje final
        return puntaje_actual, as_utilizable
    
    def obtener_puntaje(self):
        # calculmos y retornamos el puntaje actual del crupier
        puntaje = 0
        tiene_as = False
        puntaje, tiene_as = calcular_puntaje(self.mano)
        return puntaje, tiene_as
    
    def reiniciar(self):
        # Limpiamos la mano para empezar una nueva ronda
        self.mano = []
    
    def obtener_carta_visible(self):
        # retornamos la carta visible del crupier
        if len(self.mano) > 0:
            carta = self.mano[0]
            return carta
        else:
            return None
