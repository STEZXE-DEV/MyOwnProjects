from .task_generator import *
from .utils import *


# funkcja do testowania generowania zadań
def gen_test():

    # funckja do wypisania testów w konsoli
    def functions_test_handling(function, task_type, quantity):
        for x in range(quantity):
            print(f"\nTEST NR. {x+1}")
            for i in range(len(DIFFICULTY_LEVELS)):
                    qstn, ans = function(i)
                    print(f"Zadanie typu {task_type.upper()} (poziom {DIFFICULTY_LEVELS[i]}): {qstn}\t\tPoprawna odpowiedź: {ans}")
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
            functions_test_handling(TASK_GEN_FUNCTIONS[0], chosen_type, tests_quantity())
            
        # TESTY FUNKCJI generate_basic_equation_task()
        case 2:
            print()
            print("TEST FUNKCJI generate_basic_equation_task() -> Działania algebraiczne proste")
            print()
            functions_test_handling(TASK_GEN_FUNCTIONS[1], chosen_type, tests_quantity())
        
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