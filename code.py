import random
import time
import tracemalloc
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


def measure_algorithm(algorithm, items):
    tracemalloc.start()
    start_time = time.perf_counter()
    box_sums, box_contents = algorithm(items)
    end_time = time.perf_counter()
    _current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "time": end_time - start_time,
        "peak_memory": peak_memory / 1024,
        "box_count": len(box_contents),
        "box_sums": box_sums,
        "box_contents": box_contents,
    }


def run_performance_tests():
    # Zestaw danych do testów
    test_sizes = [1, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 50, 100, 1000]
    branch_and_bound_limit = 17

    header = (
        f"{'N':<6} | {'Czas FFD (s)':<15} | {'Czas B&B (s)':<15} | "
        f"{'Pamięć FFD (KiB)':<18} | {'Pamięć B&B (KiB)':<18} | {'Pudełka FFD':<12} | {'Pudełka B&B':<12}"
    )
    print(header)
    print("-" * len(header))

    for n in test_sizes:
        items = generate_items(n)

        ffd_result = measure_algorithm(first_fit_decreasing, items)

        # Branch&Bound ma złożoność wykładniczą, więc większe testy są celowo pomijane.
        if n <= branch_and_bound_limit:
            bnb_result = measure_algorithm(branch_and_bound, items)
            bnb_time = f"{bnb_result['time']:.6f}"
            bnb_memory = f"{bnb_result['peak_memory']:.2f}"
            bnb_boxes = str(bnb_result["box_count"])
        else:
            bnb_time = "Pominięto"
            bnb_memory = "-"
            bnb_boxes = "-"

        print(
            f"{n:<6} | {ffd_result['time']:<15.6f} | {bnb_time:<15} | "
            f"{ffd_result['peak_memory']:<18.2f} | {bnb_memory:<18} | {ffd_result['box_count']:<12} | {bnb_boxes:<12}"
        )

# WYKONANIE
if __name__ == "__main__":
    print("Rozpoczynam testy wydajnościowe...\n")
    run_performance_tests()

