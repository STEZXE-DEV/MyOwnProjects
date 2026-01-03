import random as r

TASK_TYPES = ["arithmetic", "basic equation", "geometry", "square function", "trigonometry"] # lista możliwych typów zadań
OPERATORS = ["+", "-", "*", ":"] # lista operatorów

# zakres poziomów [1, 3] - trzy poziomy trudności
def level_clamp(lvl):
    return max(1 , min(3, lvl))
    
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
    # jeśli 0 to zwraca 0 bez zmieniania znaku
    if val == 0:
        return 0
    else: 
        return -val if r.randint(0, 1) == 0 else val # nowy, lepszy skrócony zapis + jest bardziej czytelny

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

# funkcja do testowania generowania zadań
def gen_test():

    # funckja do wypisania testów w konsoli, każdy jeden test to 
    def functions_test_handling(function, task_type, quantity):
        for x in range(quantity):
            print(f"\nTEST NR. {x+1}")
            for i in range(1, 4):
                    qstn, ans = function(i)
                    print(f"Zadanie typu {task_type.upper()} ({i} poziomu): {qstn}\t\tPoprawna odpowiedź: {ans}")
        print()

    # funkcja zwracająca ilość testów wedle podanej wartości przez użytkownika
    def tests_quantity(): # jeżeli input jest inny niż przedział [1, max_number_of_tests] to wykona się tylko jeden test
        max_number_of_tests = 50
        number_of_tests = input(f"Zadeklaruj ilość testów (max {max_number_of_tests}): \n> ")
        if not number_of_tests.isnumeric():
            number_of_tests = 1
        elif number_of_tests.isnumeric():
            number_of_tests = int(number_of_tests)
            if number_of_tests < 1 or number_of_tests > max_number_of_tests:
                number_of_tests = 1
        return number_of_tests
            
    print("TESTY FUNKCJI")

    list_of_choices = enumerate(TASK_TYPES, 1) # ponumerowana lista wyborów (zaczyna numerować od 1)

    for number, task in list_of_choices:
        print(f"{number} - {task}")
    print("x - EXIT")

    choice = input("Podaj numer funkcji do przetestowania: \n> ")
    if choice.isnumeric():
        choice = int(choice)
        if choice in range(1, len(TASK_TYPES) + 1):
            chosen_type = TASK_TYPES[choice - 1]
        # else:
        #     print("Funkcja niedostępna lub nie istnieje!")

    # w zależności od wyboru pokazuje odpowiadające testy
    match choice:

        # TESTY FUNKCJI generate_arithmetic_task()
        case 1:
            print()
            print("TEST FUNKCJI generate_arithmetic_task() -> Działania arytmetyczne")
            print()
            functions_test_handling(generate_arithmetic_task, chosen_type, tests_quantity())
            
        # TESTY FUNKCJI generate_basic_equation_task()
        case 2:
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

        #stan domyślny 
        case _: 
            print()
            print("Funkcja niedostępna lub nie istnieje!")
            print()

# zapobiegnięcie wywoływania testów kiedy moduł jest importowany
if __name__ == "__main__":
    while True:
        gen_test()
        input("Wciśnij ENTER by kontynuować... \n")
