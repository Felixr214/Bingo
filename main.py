import Card
import random
import numpy as np
from copy import deepcopy
from reportlab.pdfgen import canvas

moves = 20
max_cards = 27
max_tasks = 100

multiplication_range = (0, 20)
division_range = (-60, 60)
other_range = (-100, 100)

tasks = []
results = []
i = 0
operators = {
    0: "+",
    1: "-",
    2: "*",
    3: "/"
}

def getAdditionTask():
    if np.random.randint(0, 2) == 0:
        num1 = random.randint(*other_range)
        num2 = random.randint(*other_range)
        result = num1 + num2
    else:
        num1 = random.randint(*division_range)
        num2 = random.randint(*division_range)
        divisor = np.random.randint(2, max(5, min(np.abs(num1), np.abs(num2))))

        while (num1 + num2) % divisor != 0:
            num1 = random.randint(*division_range)
            num2 = random.randint(*division_range)

        result = int((num1 + num2) / divisor)
        num1 = f"({num1}/{divisor})"
        num2 = f"({num2}/{divisor})"
    return num1, num2, result

def getSubtractionTask():
    num1 = random.randint(*other_range)
    num2 = random.randint(*other_range)
    result = num1 - num2
    return num1, num2, result

def getMultiplicationTask():
    num1 = random.randint(*multiplication_range)
    num2 = random.randint(*multiplication_range)
    while num1 ** 2 <= 1 or num2 ** 2 <= 1:
        num1 = random.randint(*multiplication_range)
        num2 = random.randint(*multiplication_range)
    result = num1 * num2
    return num1, num2, result

def getDivisionTask():
    num1 = random.randint(*division_range)
    num2 = random.randint(*division_range)
    while num1 ** 2 <= 1 or num2 ** 2 <= 1 or num2 >= num1 or num1 % num2 != 0:
        num1 = random.randint(*division_range)
        num2 = random.randint(*division_range)
    result = int(num1 / num2)
    return num1, num2, result

def getTask(operator):
    if operator == 0:
        num1, num2, result = getAdditionTask()

    elif operator == 1:
        num1, num2, result = getSubtractionTask()


    elif operator == 2:
        num1, num2, result = getMultiplicationTask()
    else:
        num1, num2, result = getDivisionTask()

    return num1, num2, result

while True:
    if i >= max_tasks:
        break

    operator = 3 - (4 * i // max_tasks)
    num1, num2, result = getTask(operator)

    while result in results:
        num1, num2, result = getTask(operator)

    results.append(result)
    tasks.append((str(num1) + operators[operator] + str(num2)))
    i+=1

indices = np.arange(max_tasks)
np.random.shuffle(indices)
indices = indices[:moves]

all_values = deepcopy(results)

results_ = np.array(deepcopy(all_values))
tasks_ = np.array(tasks)

results = list(results_[indices])
tasks = list(tasks_[indices])

c = canvas.Canvas("Karten/aufgaben.pdf")
c.setFont("Courier", 12)
y = 750
line_height = 14

for a in range(len(results)):
    task = f"{tasks[a]} = {results[a]}"
    print(task)
    task_string = f"{tasks[a]} = {results[a]}"
    c.drawString(100, y-a*line_height, task_string)

c.save()

cards = [Card.Card(all_values, results, True, moves, 0)]
cards += [Card.Card(all_values, results, False, moves, a) for a in range(1, max_cards)]

print()
cards[0].ascii_draw()
for card in cards:
    card.save("#")
