import random as r

TASK_TYPES = ["arithmetic", "algebraic", "geometry", "square function", "trigonometry", None, None, None, None, None] #lista możliwych typów zadań
OPERATORS = ["+", "-", "*", "/"]


def generate_arithmetic_task(level):
    level = max(1 , min(3, level))
    mul_max = (100, 500, 1000) #maksymalne wyniki mnożenia
    div_max = (10, 25, 35) #maksymalna dzielna
    a = None
    b = None

    while a == b: #dopoki obie liczby nie będą od siebie różne to losują się na nowo
        a = r.randint(1 * 5**(level-1) , 10 * 5**(level-1))
        b = r.randint(1 * 5**(level-1) , 10 * 5**(level-1))

    idx = r.randint(0, len(OPERATORS)-1)
    random_operator = OPERATORS[idx]

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

    match random_operator:
        case "+":
            answer = a + b
        case "-":
            answer = a - b
        case "*":
            answer = a * b
        case "/":
            answer = a // b

    return question, answer

print(f"Zadanie arytmetyczne 1 poziomu: {generate_arithmetic_task(1)}")
print(f"Zadanie arytmetyczne 2 poziomu: {generate_arithmetic_task(2)}")
print(f"Zadanie arytmetyczne 3 poziomu: {generate_arithmetic_task(3)}")
    
def generate_algebraic_task(level):
    level = max(1 , min(3, level))
