import random

def crear_baraja():
    """baraja simulada de cartas, donde devuelve una aleatoria con los valores 1(As), 2-9, 10 (J, Q, K)"""

    cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10]
    return random.choice(cards)

def calcular_puntaje(hand):
    """Aca se calcula el puntaje de la mano y revisa si es que tiene un As (1 o 11) utilizable"""
    score = sum(hand)
    has_ace = 1 in hand
    usable_ace = False

    #Logica del As: Si se tiene un As y al sumarlo a la mano no se pasa de 21, se utiliza.
    if has_ace and score + 10 <= 21:
        score += 10
        usable_ace = True # Se establece como true si es que se utiliza As como 11

    return score, usable_ace