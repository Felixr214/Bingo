import numpy as np

max_tasks = 100

for i in range(max_tasks):
    operator = 3 - (4 * i // max_tasks)
    print(operator)