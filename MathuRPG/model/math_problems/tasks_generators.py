import random as r

TASK_TYPES = ["arithmetic", "basic equation", "geometry", "square function", "trigonometry"] # lista możliwych typów zadań
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
    else: 
        op = OPERATORS[0] # plus

    return op, val

#funkcja do redukcji w zapisie jeśli 1 lub -1 występuje przed "x"
def val_next_to_x(val):
    return "" if val == 1 else "-" if val == -1 else str(val)

#funkcja do zapisu dzielenia przez liczbę z możliwym znakiem +/-
def divided_by_val_with_sign(val):
    if val < 0:
        return f"({val})"       #jeśli dzielnik jest ujemny to zapis wyglada np. (-27)
    else: 
        return str(val)       #jeśli dodatni to bez zmian

# losowo przyznaje znak liczbie 
def draw_value_sign_randomly(val):
    return -val if r.randint(0, 1) == 0 else val # nowy, lepszy skrócony zapis + jest bardziej czytelny

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

    while idx == 3 and (b == 0 or a % b != 0):
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
            return first_range if not str(level).isnumeric() else first_range if level < 1 else third_range

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

    for _ in range(25):
        if a != c:
            break
        c = r.randint(*ranges["d"]) if r.randint(0,1) else r.randint(*ranges["x"])
    else:
        c += 1

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

    # tu mam zamiar napisać instrukcję, która sprawi, że pod wpływem poziomu zmieniają się szanse na poszczególny typ zadania algebraicznego prostego
    match level:
        case 1:
            chances = [70, 20, 10] # typ 1: 70%, typ 2: 20%, typ 3: 10%
        case 2:
            chances = [30, 50, 20]
        case 3:
            chances = [10, 20, 70]

    generators = [gen_type_one, gen_type_two, gen_type_three]
    result = r.choices(generators, weights = chances, k = 1)[0] #gen_type_three(level) #gen_type_one(level), gen_type_two(level)

    # random choices działa trochę inaczej od choice - zwraca krotkę zamiast dwóch wartości
    question, answer = result(level)
    
    return question, answer

# funkcja do testowania generowania zadań
def gen_test():

    def functions_test_handling(function, type, quantity):
        for x in range(quantity):
            print(f"\nTEST NR. {x+1}")
            for i in range(1, 4):
                    qstn, ans = function(i)
                    print(f"Zadanie typu {type.upper()} ({i} poziomu): {qstn}\t\tPoprawna odpowiedź: {ans}")
        print()

    def tests_quantity():
        number_of_tests = input("Zadeklaruj ilość testów (max 20): \n> ")
        if not number_of_tests.isnumeric():
            number_of_tests = 1
        elif number_of_tests.isnumeric():
            number_of_tests = int(number_of_tests)
            if number_of_tests < 1 or number_of_tests > 20:
                number_of_tests = 1
        return number_of_tests
            

    print("TESTY FUNKCJI")
    list_of_choices = enumerate(TASK_TYPES) #ponumerowana lista wyborów
    for number, task in list_of_choices:
        print(f"{number+1} - {task}")
    print("x - EXIT")
    choice = input("Podaj numer funkcji do przetestowania: \n> ")
    if choice.isnumeric():
        choice = int(choice)
        if choice in range(1, len(TASK_TYPES)+1):
            chosen_type = TASK_TYPES[choice - 1]
        else:
            print("Funkcja niedostępna lub nie istnieje!")

    # w zależności od wyboru pokazuje odpowiadające testy
    match choice:

        case 1:
              # TESTY FUNKCJI generate_arithmetic_task()
            print()
            print("TEST FUNKCJI generate_arithmetic_task() -> Działania arytmetyczne")
            print()
            functions_test_handling(generate_arithmetic_task, chosen_type, tests_quantity())
            
        case 2:
            # TESTY FUNKCJI generate_basic_equation_task()
            print()
            print("TEST FUNKCJI generate_basic_equation_task() -> Działania algebraiczne proste")
            print()
            functions_test_handling(generate_basic_equation_task, chosen_type, tests_quantity())
        
        # zakończenie testów
        case "x":
            print()
            print("ZAKOŃCZONO TESTY")
            print()
            exit()
            
        case _: #stan domyślny
            print()
            print("Funkcja niedostępna lub nie istnieje!")
            print()

# zapobiegnięcie wywoływania testów kiedy moduł jest importowany
if __name__ == "__main__":
    while True:
        gen_test()
        input("Wciśnij ENTER by kontynuować... \n")
