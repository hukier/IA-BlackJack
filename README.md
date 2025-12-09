# Proyecto: Agente de RL para Blackjack

Este proyecto implementa un agente de **Aprendizaje por Refuerzo (Reinforcement Learning)** utilizando el algoritmo **Q-Learning** para aprender a jugar Blackjack de manera óptima.

Desarrollado como parte del proyecto semestral para la asignatura **Inteligencia Artificial (501.351)** de la Universidad de Concepción.

## Descripción del Problema

El objetivo es maximizar la ganancia esperada en el juego de Blackjack interactuando con un entorno simulado.

- **Entorno:** Simulación discreta basada en reglas de casino estándar.
- **Agente:** Q-Learning con política Epsilon-Greedy y decaimiento de exploración.
- **Estado:** Tupla `(Suma Jugador, Carta Dealer, As Utilizable)`.
- **Acciones:** `Pedir (1)` o `Plantarse (0)`.

## Instalación y Requisitos

El proyecto está construido en Python. Necesitas las siguientes librerías para ejecutarlo y generar los gráficos:

```bash
pip install numpy matplotlib
```

## Instrucciones de Ejecución

Para entrenar al agente desde cero y ver una demostracion final, ejecuta el archivo principal.

```bash
python main.py
```

## Resultados esperados

El entrenamiento genera un gráfico en `results/entrenamiento_blackjack.png.` Se espera que el agente alcance una tasa de victorias (Win Rate) cercana al 42-43%, lo cual es el estándar para un jugador óptimo en Blackjack (dada la ventaja matemática de la casa).
