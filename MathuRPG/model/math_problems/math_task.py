import time as t
import random as r
from tasks_generators import TASK_TYPES

#klasa zadania matematycznego
class MathTask:
    def __init__(self, question, time_limit, correct_ans, difficulty=r.randint(1,10) ):
        self.time_start = int(t.time()) #czas rozpoczęcia
        self.time_limit = time_limit #limit czasu w sekundach
        self.question = str(question) #dyspozycja/zadanie/pytanie
        self.answer = None #odpowiedź gracza
        self.correct_ans = correct_ans  #poprawna odpowiedź
        difficulty = max(1, min(10, int(difficulty))) #ograniczenie wartości trudności do przedziału [1,10]
        self.difficulty = int(difficulty) #trudność pytania
        self.task_type = TASK_TYPES[self.difficulty-1] #typ zadania wedle trudności
    
    #funkcja licząca pozostały czas
    def time_left(self):
        return max(0, (self.time_start + self.time_limit) - int(t.time())) #uniknięcie wartości ujemnych poprzez max(0, -/+ x)
    
    def submit_answer(self, ans):
        self.answer = ans

    #funckja sprawdzająca poprawność odpowiedzi
    def is_ans_correct(self):
        return self.answer == self.correct_ans
    
    #funkcja sprawdzająca czay zadanie zostało poprawnie ukończone w czasie
    def is_task_done_correctly_in_time(self):
        return self.time_left() > 0 and self.is_ans_correct()
    