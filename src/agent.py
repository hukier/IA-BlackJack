import random

class AgenteQLearning:
    #agente aprendendo con Q-Learning
    
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0):
        # alpha es la tasa de aprendizaje
        # gamma es el factor de descuento
        # epsilon es para la exploracion (epsilon-greedy)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        
        # epsilon_min es el valor minimo de epsilon, este no se si esta bien, revisar
        self.epsilon_min = 0.01
        # epsilon_decay es cuanto disminuye epsilon cada episodio, revisar
        self.epsilon_decay = 0.9995
        
        # Q-table es un diccionario donde guardamos los valores Q
        # La clave es el estado (suma_jugador, carta_crupier, as_utilizable)
        # El valor es una lista con los valores Q para cada accion [Q(plantarse), Q(pedir)]
        self.q_table = {}
    
    def get_q_value(self, estado, accion):
        # Esta funcion obtiene el valor Q para un estado y accion
        
        # Si el estado no esta en la tabla, lo inicializamos en 0
        if estado not in self.q_table:
            self.q_table[estado] = [0.0, 0.0]  # [Q(plantarse), Q(pedir)]
        
        # Retornamos el valor Q
        valor_q = self.q_table[estado][accion]
        return valor_q
    
    def elegir_accion(self, estado):
        # Esta funcion elige una accion usando la politica epsilon-greedy
        
        # Generamos un numero aleatorio entre 0 y 1
        numero_aleatorio = random.random()
        
        # Si el numero es menor que epsilon, exploramos (accion aleatoria)
        if numero_aleatorio < self.epsilon:
            # Elegimos una accion aleatoria
            accion = random.randint(0, 1)  # 0 = plantarse, 1 = pedir
        
        # Si no, explotamos (elegimos la mejor accion)
        else:
            # Obtenemos los valores Q para ambas acciones
            q_plantarse = self.get_q_value(estado, 0)
            q_pedir = self.get_q_value(estado, 1)
            
            # Elegimos la accion con mayor valor Q
            if q_plantarse > q_pedir:
                accion = 0  # Plantarse
            elif q_pedir > q_plantarse:
                accion = 1  # Pedir
            else:
                # Si son iguales, elegimos aleatoriamente
                accion = random.randint(0, 1)
        
        return accion
    
    def elegir_mejor_accion(self, estado):
        # Esta funcion elige la mejor accion sin explorar (para evaluar)
        
        # Obtenemos los valores Q para ambas acciones
        q_plantarse = self.get_q_value(estado, 0)
        q_pedir = self.get_q_value(estado, 1)
        
        # Elegimos la accion con mayor valor Q
        if q_plantarse > q_pedir:
            accion = 0  # Plantarse
        elif q_pedir > q_plantarse:
            accion = 1  # Pedir
        else:
            # Si son iguales, elegimos plantarse (mas conservador)
            accion = 0
        
        return accion
    
    def actualizar_q_value(self, estado, accion, recompensa, siguiente_estado, terminado):
        # Esta funcion actualiza el valor Q usando la formula de Q-Learning
        
        # Obtenemos el valor Q actual
        q_actual = self.get_q_value(estado, accion)
        
        # Si el episodio termino, no hay siguiente estado
        if terminado:
            # Q(s,a) = Q(s,a) + alpha * (recompensa - Q(s,a))
            nuevo_valor_q = q_actual + self.alpha * (recompensa - q_actual)
        
        # Si el episodio no termino, consideramos el siguiente estado
        else:
            # Obtenemos el maximo valor Q del siguiente estado
            q_siguiente_plantarse = self.get_q_value(siguiente_estado, 0)
            q_siguiente_pedir = self.get_q_value(siguiente_estado, 1)
            
            # Tomamos el maximo
            if q_siguiente_plantarse > q_siguiente_pedir:
                max_q_siguiente = q_siguiente_plantarse
            else:
                max_q_siguiente = q_siguiente_pedir
            
            # Aplicamos la formula de Q-Learning
            # Q(s,a) = Q(s,a) + alpha * (recompensa + gamma * max_Q(s',a') - Q(s,a))
            nuevo_valor_q = q_actual + self.alpha * (recompensa + self.gamma * max_q_siguiente - q_actual)
        
        # Actualizamos la Q-table
        if estado not in self.q_table:
            self.q_table[estado] = [0.0, 0.0]
        
        self.q_table[estado][accion] = nuevo_valor_q
    
    def disminuir_epsilon(self):
        # Esta funcion disminuye epsilon para explorar menos con el tiempo
        
        # Multiplicamos epsilon por el decay
        self.epsilon = self.epsilon * self.epsilon_decay
        
        # No dejamos que epsilon sea menor que epsilon_min
        if self.epsilon < self.epsilon_min:
            self.epsilon = self.epsilon_min
    
    def obtener_politica(self):
        # Esta funcion retorna la politica aprendida
        # Es un diccionario que mapea estados a la mejor accion
        
        politica = {}
        
        # Para cada estado en la Q-table
        for estado in self.q_table:
            # Obtenemos la mejor accion
            mejor_accion = self.elegir_mejor_accion(estado)
            politica[estado] = mejor_accion
        
        return politica
