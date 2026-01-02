import random as r

TASK_TYPES = ["arithmetic", "equation", "geometry", "square function", "trigonometry", None, None, None, None, None] # lista możliwych typów zadań
OPERATORS = ["+", "-", "*", ":"] #lista operatorów

# zakres poziomów [1, 3] - trzy poziomy trudności
def level_clamp(lvl):
    lvl = max(1 , min(3, lvl))
    return lvl

# funkcja do ustalenia operatora przed liczbą w zależności od jej znaku (ujemna czy dodatnia)
def operator_before_value(val):

    if val < 0:
        op = OPERATORS[1] # minus
        val = str(abs(val)) # uniknięcie podwójnego minusa w zapisie, który nie spełnia równiania
    else: op = OPERATORS[0] # plus

    return op, val

#funkcja do redukcji w zapisie jeśli 1 lub -1 występuje przed "x"
def val_next_to_x(val):
    if val == 1:
        str_val = ""
    elif val == -1:
        str_val = "-"
    else: str_val = str(val)

    return str_val

#funkcja do zapisu dzielenia przez liczbę z możliwym znakiem +/-
def divided_by_val_with_sign(val):
    if val < 0:
        return f"({val})"       #jeśli dzielnik jest ujemny to zapis wyglada np. (-27)
    else: return str(val)       #jeśli dodatni to bez zmian

# losowo przyznaje znak liczbie 
def draw_value_sign_randomly(val):
    draw = r.randint(0, 1)
    if draw < 1:
        val = -val
    return val

'''<----> ZADANIE ARYTMETYCZNE <---->'''

# funkcja generująca zadanie arytmetyczne z losowym operatorem działania
def generate_arithmetic_task(level):

    level = level_clamp(level)
    mul_max = (100, 500, 1000) # maksymalne wyniki mnożenia
    div_max = (10, 25, 35) # maksymalna dzielna
    a = None
    b = None

    while a == b: # dopóki obie liczby nie będą od siebie różne to losują się na nowo
        a = r.randint(1 * 5**(level-1) , 10 * 5**(level-1))
        b = r.randint(1 * 5**(level-1) , 10 * 5**(level-1))

    idx = r.randint(0, len(OPERATORS)-1)
    random_operator = OPERATORS[idx]

    #jeśli odejmowanie lub dzielenie i druga liczba jest większa od pierwszej to następuje zamiana
    if idx in [1, 3] and b > a:
        a, b = b, a

    elif idx == 2:
        while a * b > mul_max[level-1]:
            a = r.randint(1 * 5**(level-1) , 10 * 5**(level-1))
            b = r.randint(1 * 5**(level-1) , 10 * 5**(level-1))

    while idx == 3 and a%b!=0:
        a = r.randint(1 * 5**(level-1) , div_max[level-1])
        b = r.randint(1 * 5**(level-1) , div_max[level-1])
        if b > a:
            a, b = b, a
        a *= b

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

# TESTY FUNKCJI generate_arithmetic_task()

print(f"Zadanie arytmetyczne 1 poziomu: {generate_arithmetic_task(1)}")
print(f"Zadanie arytmetyczne 2 poziomu: {generate_arithmetic_task(2)}")
print(f"Zadanie arytmetyczne 3 poziomu: {generate_arithmetic_task(3)}")


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
        "a": (2, 6),
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

    # zwrócenie zakresu w  zależności od poziomu
    match level:
        case 1:
            return first_range
        case 2:
            return second_range
        case 3:
            return third_range

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
    a, b, c, x = r.randint(*ranges["a"]), r.randint(*ranges["b"]), r.choice([r.randint(*ranges["d"]), r.randint(*ranges["x"])]), r.randint(*ranges["x"])

    while a == c:
        c = r.choice([r.randint(*ranges["d"]), r.randint(*ranges["x"])])
    
    if level > 1:
            a, b, c, x = draw_value_sign_randomly(a), draw_value_sign_randomly(b), draw_value_sign_randomly(c), draw_value_sign_randomly(x)

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
    
    #przypisanie zakresów do zmiennych równania
    a, x, d, y = r.randint(*ranges["a"]), r.randint(*ranges["x"]), r.randint(*ranges["d"]), r.randint(*ranges["y"])

    if level > 1:
            a, x, d, y = draw_value_sign_randomly(a), draw_value_sign_randomly(x), draw_value_sign_randomly(d), draw_value_sign_randomly(y)

    #zapewnienie, że wynik równania będzie liczbą całkowitą 
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

    #match level: # tu mam zamiar napisać instrukcję, która sprawi, że pod wpływem poziomu zmieniają się szanse na poszczególny typ zadania algebraicznego prostego

    question, answer = r.choice([gen_type_one(level), gen_type_two(level), gen_type_three(level)]) #gen_type_three(level) #gen_type_one(level), gen_type_two(level),

    return question, answer

# TESTY FUNKCJI generate_basic_equation_task()

print(f"Zadanie algebraiczne proste 1 poziomu: {generate_basic_equation_task(1)}")
print(f"Zadanie algebraiczne proste 2 poziomu: {generate_basic_equation_task(2)}")
print(f"Zadanie algebraiczne proste 3 poziomu: {generate_basic_equation_task(3)}")  