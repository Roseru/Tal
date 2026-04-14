'''
Taka prośba, nie edytujcie funkcji związanych z przeszukiwaniem rozwiązań. 
Janek -> napisz funkcje testowe, np takie, że wygeneruje 1,10,20,50,100,1000 przedmiotów i 
będzię je alokować wykorzystując algorytm, funkcja powinna w jakiś spobób mierzyć czas. W jakiś inny sposób
będziesz musiał obliczyć zajmowane zasoby.
'''

import random
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
def brute_force(items):
    minimal_box = []
    temp_box = []
    j = 0


def first_fit_decreasing(items):
    # 1. Sortowanie malejąco
    items.sort(reverse=True)

    # box_sums przechowuje aktualną sumę wag w każdym pudełku
    box_sums = []
    # box_contents przechowuje listy przedmiotów w każdym pudełku
    box_contents = []

    for item in items:
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


# Test
items = generate_items(10)
print(f"Przedmioty: {items}")
sums, contents = first_fit_decreasing(items)
print(f"Sumy w pudełkach: {sums}")
print(f"Zawartość pudełek: {contents}")
items = generate_items(10)
box_abs = first_fit_decreasing(items)
print(box_abs[0])


