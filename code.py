'''
Taka prośba, nie edytujcie funkcji związanych z przeszukiwaniem rozwiązań.
Janek -> napisz funkcje testowe, np. takie, że wygeneruje 1,10,20,50,100,1000 przedmiotów i
będzie, je alokować wykorzystując algorytm, funkcja powinna w jakiś sposób mierzyć czas. W jakiś inny sposób
będziesz musiał obliczyć zajmowane zasoby.
'''

import random
import time
'''Parametry generatora przedmiotów'''
low_item_value = 1
max_item_value = 9
box_capacity = 10
'''
Returns k items which value is: low < value < max
'''


def generate_items(k):
    items = []
    i = 0
    while i < k:
        items.append(random.randint(low_item_value,max_item_value))
        i = i+1
    return items
'''Funkcja znajdująca optymalne rozwiązanie zgodnie z wizją algorytmu Branch&Bound'''
def branch_and_bound(items):
    best_box = []
    minimal_box = float('inf')
    temp_box = []
    items_copy = items.copy()
    items_copy.sort() #Sortujemy, aby przyśpieszyć proces znajdowania pierwszego rozwiązania
    #Pierwsze znalezione rozwiązanie pozwala skutecznie zastosować odcinanie gałęzi
    def backtrack(item_index, temp_box):
        nonlocal minimal_box, best_box #wykorzystuje zmienne z funkcji zewnętrznej
        #Odcinanie gałęzi (jeśli wcześniej znaleziono lepsze lub równe rozwiązanie->przerwij)
        if len(temp_box) >= minimal_box:
            return
        #Warunek stop, umieściliśmy wszystkie przedmioty w pudłach
        if item_index == len(items_copy):
            if len(temp_box) < minimal_box:
                minimal_box = len(temp_box)
                best_box = [i[:] for i in temp_box]
                return
        #zasadnicze działanie funkcji
        item = items_copy[item_index]
        #próbuje dodać przedmiot do istniejących pudeł
        for i in range(len(temp_box)):
            if sum(temp_box[i]) + item <= box_capacity:
                temp_box[i].append(item)
                backtrack(item_index +1, temp_box)
                temp_box[i].pop() #cofam zmianę, aby sprawdzić przypadek dodania nowego pudła na ten przedmiot.
        temp_box.append([item])
        backtrack(item_index+1, temp_box)
        temp_box.pop() #cofamy zmiany Backtracking

    #start rekurencji
    backtrack(0, [])
    #Format wyniku tak jak w FFD
    box_sums = [sum(box) for box in best_box]
    return box_sums, best_box

def first_fit_decreasing(items):
    #Tworzenie kopii, aby lista przedmiotów pozostała bez zmian do testów dla drugiego
    #przypadku
    # 1. Sortowanie malejąco
    items_copy = items.copy()
    items_copy.sort(reverse=True)

    # box_sums przechowuje aktualną sumę wag w każdym pudełku
    box_sums = []
    # box_contents przechowuje listy przedmiotów w każdym pudełku
    box_contents = []

    for item in items_copy:
        placed = False
        # 2. Próbujemy włożyć do istniejących pudełek
        for i in range(len(box_sums)):
            if box_sums[i] + item <= box_capacity:
                box_sums[i] += item
                box_contents[i].append(item)
                placed = True
                break  # Przedmiot włożony, wychodzimy z pętli wewnętrznej

        # 3. Jeśli nie pasuje nigdzie, twórz nowe pudełko
        if not placed:
            box_sums.append(item)
            box_contents.append([item])

    return box_sums, box_contents


def run_performance_tests():
    # Zestaw danych do testów
    test_sizes = [1, 10, 15,16,17,18,19, 20, 50, 100, 1000]

    print(f"{'N':<5} | {'Czas FFD (s)':<15} | {'Czas BF (s)':<18} | {'Pudełka FFD':<15} | {'Pudełka BF':<15}")
    print("-" * 80)

    for n in test_sizes:
        items = generate_items(n)

        # --- TEST FFD ---
        start_ffd = time.perf_counter()
        sums_ffd, bins_ffd = first_fit_decreasing(items)
        end_ffd = time.perf_counter()
        time_ffd = end_ffd - start_ffd

        # --- TEST BRUTE FORCE ---
        if n <= 18:  # BEZPIECZNIK - Brute force, żeby nie czekać godzin na koniec programu
            start_bf = time.perf_counter()
            sums_bf, bins_bf = branch_and_bound(items)
            end_bf = time.perf_counter()
            time_bf = f"{end_bf - start_bf:.6f}"
            res_bf = str(len(bins_bf))
        else:
            time_bf = "Pominięto (NP-trudny)"
            res_bf = "-"

        print(f"{n:<5} | {time_ffd:<15.6f} | {time_bf:<18} | {len(bins_ffd):<15} | {res_bf:<15}")

# WYKONANIE
if __name__ == "__main__":
    print("Rozpoczynam testy wydajnościowe...\n")
    run_performance_tests()

