import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns

#ver metricas de desempeño, evolucion de recompensas
class AnalizadorDesempeño:
    def __init__(self):
        self.recompensas = [] #recompensas por partida
        self.epsilons = []#epsilon por partida
    #registrar partida
    def registrar_partida(self, partida, recompensa, epsilon):
        self.recompensas.append(recompensa)
        self.epsilons.append(epsilon)
    #promedio movil, es decir ventana de 1000 datos para calcular el promedio
    def calcular_promedio_movil(self, datos, ventana=1000):
        promedios = []
        for i in range(len(datos)):
            inicio = max(0, i - ventana + 1)
            promedios.append(np.mean(datos[inicio:i+1]))
        return promedios
    #graficar las recompensas
    def grafico_recompensas(self):
        plt.figure(figsize=(10, 6))
        promedios = self.calcular_promedio_movil(self.recompensas, 1000)
        plt.plot(promedios, linewidth=2, color='hotpink') 
        plt.axhline(y=0, color='Pink', linestyle='--', alpha=0.5)
        plt.title('Evolución de Recompensas')
        plt.xlabel('Partidas')
        plt.ylabel('Recompensa Promedio')
        plt.grid(True)
        return plt.gcf()
    
    #graficar las victorias
    def grafico_victorias(self):
        plt.figure(figsize=(10, 6))
        # Convertir recompensas a victorias (1 si gana, 0 si no)
        victorias = [1 if r == 1 else 0 for r in self.recompensas]
        #calcular el win rate usando prom movil
        win_rate = self.calcular_promedio_movil(victorias, 1000)
        plt.plot(win_rate, linewidth=2, color='violet')
        plt.title('Tasa de Victorias')
        plt.xlabel('Partidas')
        plt.ylabel('Win Rate')
        plt.ylim([0, 1])
        plt.grid(True)
        return plt.gcf()
    #grafico epsilon, para ver como va disminuyendo en el tiempo
    def grafico_epsilon(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.epsilons, linewidth=2, color='purple')
        plt.title('Evolución de Epsilon')
        plt.xlabel('Partidas')
        plt.ylabel('Epsilon')
        plt.grid(True)
        return plt.gcf()
    
    #grafico de distribucion de victorias, empates y derrotas
    def grafico_distribucion(self):
        #victorias 1, empates 0, derrotas -1
        victorias = self.recompensas.count(1)
        empates = self.recompensas.count(0)
        derrotas = self.recompensas.count(-1)
        total = len(self.recompensas)
        
        plt.figure(figsize=(8, 6))
        categorias = ['Victorias', 'Empates', 'Derrotas']
        valores = [victorias, empates, derrotas]
        colores = ['Pink', 'gray', 'violet']
        #graficar barras
        bars = plt.bar(categorias, valores, color=colores, alpha=0.7)
        
        for bar, val in zip(bars, valores):
            #porcentajes sobre las barras
            height = bar.get_height()
            pct = val/total*100
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{pct:.1f}%', ha='center', va='bottom')
        
        plt.title('Distribución de Resultados')
        plt.ylabel('Cantidad')
        plt.grid(True, alpha=0.3, axis='y')
        return plt.gcf()
    
    #grafico para las politicas aprendidas por el agente
    def grafico_politica(self, agente):
        #figura con as y sin as
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        # recorrer estados posibles
        for as_util, ax, titulo in [(True, ax1, 'Con As'), (False, ax2, 'Sin As')]:
            matriz = np.zeros((10, 10))
            #llenar la matriz con acciones
            for suma in range(12, 22): #suma del jugador
                for carta in range(1, 11): #carta del crupier
                    estado = (suma, carta, as_util) #estado
                    if estado in agente.q_table: #si el estado esta en la q_table
                        accion = agente.elegir_mejor_accion(estado) #mejor accion
                        matriz[suma-12, carta-1] = accion #0=plantarse,1=pedir
                    else:
                        matriz[suma-12, carta-1] = -0.5 #estado no visitado
            #heatmap de la matriz
            sns.heatmap(matriz, ax=ax, cmap='PuRd', center=0.5,
                       xticklabels=['A', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                       yticklabels=range(12, 22),
                       linewidths=0.5, vmin=-0.5, vmax=1)
            
            ax.set_title(titulo)
            ax.set_xlabel('Carta Crupier')
            ax.set_ylabel('Suma Jugador')
        
        plt.suptitle('Política Aprendida (Rosa=Pedir, Morado=Plantarse)')
        plt.tight_layout()
        return plt.gcf()
    
    #imprimir resumen de estadisticas
    def imprimir_estadisticas_resumen(self):
        total = len(self.recompensas)
        if total == 0:
            print("No hay datos")
            return
        
        victorias = self.recompensas.count(1)
        empates = self.recompensas.count(0)
        derrotas = self.recompensas.count(-1)

        print("RESUMEN")
        print(f"Total partidas:  {total:,}")
        print(f"Victorias:       {victorias:,} ({victorias/total*100:.1f}%)")
        print(f"Empates:         {empates:,} ({empates/total*100:.1f}%)")
        print(f"Derrotas:        {derrotas:,} ({derrotas/total*100:.1f}%)")
        print(f"Recompensa avg:  {np.mean(self.recompensas):.3f}")
        
        #ultimas 1000 partidas para ver que tanto ha aprendido el agente
        if total >= 1000:
            ultimas = self.recompensas[-1000:]
            vic_ultimas = ultimas.count(1)
            print(f"\nÚltimas 1000 partidas:")
            print(f"Win Rate: {vic_ultimas/10:.1f}%")
    
    def guardar_todos_los_graficos(self, agente, carpeta_salida="results", ventana=1000):
        if not os.path.exists(carpeta_salida):
            os.makedirs(carpeta_salida)
        
        print("Generando graficos de desempeño")
        
        fig1 = self.grafico_recompensas()
        fig1.savefig(os.path.join(carpeta_salida, "1_recompensas.png"), dpi=150)
        plt.close(fig1)
        
        fig2 = self.grafico_victorias()
        fig2.savefig(os.path.join(carpeta_salida, "2_victorias.png"), dpi=150)
        plt.close(fig2)
        
        fig3 = self.grafico_epsilon()
        fig3.savefig(os.path.join(carpeta_salida, "3_epsilon.png"), dpi=150)
        plt.close(fig3)
        
        fig4 = self.grafico_distribucion()
        fig4.savefig(os.path.join(carpeta_salida, "4_distribucion.png"), dpi=150)
        plt.close(fig4)
        
        fig5 = self.grafico_politica(agente)
        fig5.savefig(os.path.join(carpeta_salida, "5_politica.png"), dpi=150)
        plt.close(fig5)

        print(f"Graficos guardados en la carpeta '{carpeta_salida}'")

        
