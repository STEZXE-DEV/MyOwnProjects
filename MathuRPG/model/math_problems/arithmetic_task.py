import random as r
from .utils import *


'''<----> ZADANIE ARYTMETYCZNE <---->'''

# funkcja do generowania losowych wartości a i b do działań arytmetycznych 
def generate_arithmetic_values(level, min_a=None, max_a=None, min_b=None, max_b=None):

    # lista argumentów funckji
    list_of_arguments = [level, min_a, max_a, min_b, max_b]

    # walidowanie argumentów
    for i in range(len(list_of_arguments)):
        arg = list_of_arguments[i]
        # jeżeli jakiś argument nie jest None albo Int to zwraca ValueError (warto zaznaczyć, że isinstance(val, int) przepuszcza val == bool, dlatego dodatkowy "or")
        # dawniej (not isinstance(list_of_arguments[i], int) or isinstance(list_of_arguments[i], bool)) and list_of_arguments[i] is not None - okazało się to małoczytelne
        if arg is not None and (not isinstance(arg, int) or isinstance(arg, bool)):  
            raise ValueError(f"Argument na pozycji {i} powinien być INT albo None")


    min_a = min_a if min_a is not None else 4 ** (level - 1)
    max_a = max_a if max_a is not None else 10 * 5 ** (level - 1)

    # odporność na pomyłkę w zakresie liczby a
    if min_a > max_a:
        min_a, max_a = max_a, min_a

    a = r.randint(min_a, max_a)
    
    # jeśli nie podano jakiejś wartości dla b to b korzysta z wartości zakresu a
    min_b = min_b if min_b is not None else min_a
    max_b = max_b if max_b is not None else max_a

    # może zdarzyć się przypadek że min_a przekaże do min_b wartość większą niż max_b co spowoduje błąd przy losowaniu liczby
    if min_b > max_b:
        min_b, max_b = max_b, min_b

    b = r.randint(min_b, max_b)

    return a, b

# funkcja generująca zadanie arytmetyczne z losowym operatorem działania
def generate_arithmetic_task(level):
    
    level = level_clamp(level)

    mul_max = (100, 500, 1000) # maksymalne wyniki mnożenia
    div_max = (10, 25, 35) # maksymalna dzielna
    a, b = generate_arithmetic_values(level)

    while a == b: # dopóki obie liczby nie będą od siebie różne to losują się na nowo
        a, b = generate_arithmetic_values(level)

    # losowanie operatora do działania (pomiędzy liczbami a i b)
    indexes = [x for x in range(len(OPERATORS))]
    
    # szanse wylosowania się konkretnego rodzaju działania arytmetycznego zależne są od poziomu
    match level:
        case 1:
            chances = [60, 20, 10, 10] # typ 1: 60%, typ 2: 20%, typ 3: 10% typ 4: 10%
        case 2:
            chances = [30, 30, 20, 20]
        case 3:
            chances = [5, 5, 45, 45]

    random_idx = r.choices(indexes, weights=chances, k=1)[0]
    random_operator = OPERATORS[random_idx]

    # jeśli jest odejmowanie lub dzielenie i druga liczba jest większa od pierwszej to następuje zamiana liczb miejscami 
    if random_idx in [1, 3] and b > a:
        a, b = b, a

    elif random_idx == 2:
        while a * b > mul_max[level-1]:
            a, b = generate_arithmetic_values(level)

    # podczas gdy zostaje wybrane mnożenie, liczba przez którą jest dzielone nie może wynosić 0, modulo sprawdza czy dzielenie jest całkowite
    while random_idx == 3 and (b == 0 or a % b != 0):
        k, b = generate_arithmetic_values(level, 2, div_max[level-1], None, div_max[level-1]) # dawniej a = r.randint(1 * 4**(level-1) , div_max[level-1])
        a = b * k

    question = f"Jaki jest wynik działania {a} {random_operator} {b} ?"

    # dopasowanie działania do wylosowanego operatora
    match random_operator:
        case "+":
            answer = a + b
        case "-":
            answer = a - b
        case "*":
            answer = a * b
        case ":":
            answer = a // b

    return question, answer