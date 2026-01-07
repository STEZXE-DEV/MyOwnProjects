import random as r

TASK_TYPES = ["arithmetic", "basic equation", "geometry", "square function", "trigonometry"] # lista możliwych typów zadań
DIFFICULTY_LEVELS = ["EASY", "NORMAL", "HARD"] # poziomy trudności rozgrywki
OPERATORS = ["+", "-", "*", ":"] # lista operatorów

__all__ = ["TASK_TYPES", "DIFFICULTY_LEVELS", "OPERATORS", "level_clamp", "operator_before_value", "val_next_to_x", "divided_by_val_with_sign", "draw_value_sign_randomly"]

# zakres poziomów [1, 3] - trzy poziomy trudności
def level_clamp(lvl):
    return max(1 , min(len(DIFFICULTY_LEVELS), lvl))
    
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