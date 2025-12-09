import random

class AgenteQLearning:
    def __init__(self, alpha=0.015, gamma=1.0, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.99995):
        """
        Inicializa el agente con los hiperparámetros del paper de DeGranville.
        Referencias:
        Alpha=0.015 y Gamma=1.0 tomados de DeGranville, p.3.
        Epsilon decay: comenzamos explorando mucho (1.0) y bajamos gradualmente.
        """

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        
        # Q-table: Diccionario {(suma, carta_dealer, as_utilizable): [Q_stand, Q_hit]}
        self.q_table = {}
    
    def get_q_value(self, estado, accion):
        if estado not in self.q_table:
            self.q_table[estado] = [0.0, 0.0]
        return self.q_table[estado][accion] # Retorna el valor Q. Si el estado no existe, lo inicializa en 0.0
    
    def elegir_accion(self, estado):
        if random.random() < self.epsilon:
            return random.randint(0, 1) # Exploracion (Accion aleatoria), politica de Epsilon-Greedy
        else:
            return self.elegir_mejor_accion(estado) # Explotacion (Mejor accion conocida)
    
    def elegir_mejor_accion(self, estado):
        #Elige la accion con mayor valor Q (Greedy)
        q_plantarse = self.get_q_value(estado, 0)
        q_pedir = self.get_q_value(estado, 1) 
        
        # En caso de empate, o si pedir es mejor, pedimos. 
        if q_pedir > q_plantarse:
            return 1 # Pedir
        return 0 # Plantarse
    
    def actualizar_q_value(self, estado, accion, recompensa, siguiente_estado, terminado):
        """
        Actualiza la tabla Q usando la ecuacion de Bellman (Q-Learning):
        Q(s,a) <- Q(s,a) + alpha * [recompensa + gamma * max(Q(s', a')) - Q(s,a)]
        Ref: DeGranville, p.2, Ecuacion figura 1.
        """
        q_actual = self.get_q_value(estado, accion)
        
        if terminado:
            target = recompensa
        else:
            # miramos el valor maximo del siguiente estado (Off-policy)
            q_siguiente_max = max(self.get_q_value(siguiente_estado, 0), 
                                  self.get_q_value(siguiente_estado, 1))
            target = recompensa + self.gamma * q_siguiente_max
            
        # Actualizacion
        nuevo_valor = q_actual + self.alpha * (target - q_actual)
        
        # Guardar en la tabla
        if estado not in self.q_table:
            self.q_table[estado] = [0.0, 0.0]
            
        self.q_table[estado][accion] = nuevo_valor
    
    def disminuir_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay #Reduce la tasa de exploración después de cada episodio
