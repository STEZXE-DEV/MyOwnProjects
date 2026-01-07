import random as r
from .utils import *

'''<----> ZADANIE ALGEBRAICZNE PROSTE <---->'''

# zakresy wartości współczynników w prostych rówaniach z niewiadomą "x"
def simple_equation_gen_ranges(level):

    # zakres dla pierwszego poziomu
    first_range = {
        "a": (1, 3), 
        "b": (1, 10), 
        "x": (1, 5),
        "d": (2, 20), #dawniej r.choice([(2, 20), (-20, -2)])
        "y": (1, 20)}
    
    # zakres dla drugiego poziomu
    second_range = {
        "a": (1, 6),
        "b": (2, 20),
        "x": (2, 10),
        "d": (5, 50),
        "y": (1, 20)}

    # zakres dla trzeciego poziomu
    third_range = {
        "a": (3, 12), 
        "b": (5, 50), 
        "x": (5, 20), 
        "d": (10, 100), 
        "y": (1, 20)}

    # zwrócenie zakresu w zależności od poziomu
    match level:
        case 1:
            return first_range
        case 2:
            return second_range
        case 3:
            return third_range
        case _:
            return first_range 

# generowanie zadania typu pierwszego
def gen_type_one(level): # ax + b = y
        
        ranges = simple_equation_gen_ranges(level)
        a, b, x = r.randint(*ranges["a"]), r.randint(*ranges["b"]), r.randint(*ranges["x"])
        
        # jeśli poziom jest większy niż 1 to pojawiają się liczby ujemne
        if level > 1:
            a, b, x = draw_value_sign_randomly(a), draw_value_sign_randomly(b), draw_value_sign_randomly(x)

        y = a * x + b
        a_val = val_next_to_x(a)
        op, b_val = operator_before_value(b)
        y_val = str(y)

        question = f"Dane jest równanie {a_val}x {op} {b_val} = {y_val}. Jaką wartość ma \"x\"?"
        
        return question, x

# generowanie zadania typu drugiego
def gen_type_two(level): # ax + b = cx + y

    ranges = simple_equation_gen_ranges(level)
    a, b, c, x = r.randint(*ranges["a"]), r.randint(*ranges["b"]), r.randint(*ranges["d"]) if r.randint(0,1) else r.randint(*ranges["x"]), r.randint(*ranges["x"])
    
    if level > 1:
            a, b, c, x = draw_value_sign_randomly(a), draw_value_sign_randomly(b), draw_value_sign_randomly(c), draw_value_sign_randomly(x)

    while a == c:
        c = r.randint(*ranges["d"]) if r.randint(0,1) == 0 else r.randint(*ranges["x"])

    # ten wzór gwarantuje, że równanie ma rozwiązanie i że jest ono całkowite
    y = (a - c) * x + b
 
    a_val = val_next_to_x(a)
    op1, b_val = operator_before_value(b)
    c_val = val_next_to_x(c)
    op2, y_val = operator_before_value(y)

 
    question = f"Dane jest równanie {a_val}x {op1} {b_val} = {c_val}x {op2} {y_val}. Jaką wartość ma \"x\"?"

    return question, x

# generowanie zadania typu trzeciego
def gen_type_three(level): # (ax+b​) / d = y

    # zebranie zakresów względem obecnego poziomu
    ranges = simple_equation_gen_ranges(level)
    
    # przypisanie zakresów do zmiennych równania
    a, x, d, y = r.randint(*ranges["a"]), r.randint(*ranges["x"]), r.randint(*ranges["d"]), r.randint(*ranges["y"])

    if level > 1:
            a, x, d, y = draw_value_sign_randomly(a), draw_value_sign_randomly(x), draw_value_sign_randomly(d), draw_value_sign_randomly(y)

    # zapewnienie, że wynik równania będzie liczbą całkowitą 
    b = y * d - (a * x)

    y_val = str(y)
    a_val = str(val_next_to_x(a))
    op, b_val = operator_before_value(b)
    d_val =  divided_by_val_with_sign(d)

    question = f"Dane jest równanie ({a_val}x {op} {b_val}):{d_val} = {y_val}. Jaka jest wartość \"x\"?"

    return question, x

# główna funkcja do generowania prostego zadania z algebry
def generate_basic_equation_task(level):

    level = level_clamp(level) 

    # instrukcja, która sprawia, że pod wpływem poziomu zmieniają się szanse na poszczególny typ zadania algebraicznego prostego
    match level:
        case 1:
            chances = [70, 20, 10] # typ 1: 70%, typ 2: 20%, typ 3: 10%
        case 2:
            chances = [30, 50, 20]
        case 3:
            chances = [10, 20, 70]

    # random choices działa trochę inaczej od choice - zwraca krotki zamiast samych wartości, dlatego w tym przypadku potrzebne jest [0]
    gen_result = r.choices([gen_type_one, gen_type_two, gen_type_three], weights = chances, k = 1)[0] # gen_type_one(level), gen_type_two(level), gen_type_three(level) 

    question, answer = gen_result(level)
    
    return question, answer