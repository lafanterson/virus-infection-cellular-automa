import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

# Константы для типов клеток
EMPTY, UNINFECTED, INFECTED = 0, 1, 2
INFECTED_LIFESPAN = 8  # Время жизни зараженной клетки
FIELD_SIZE = 50  # Размер поля
NUM_STEPS = 200  # Количество шагов в анимации
NUM_INFECTED = 10  # Начальное количество зараженных клеток
NUM_UNINFECTED = 200  # Начальное количество незараженных клеток

# Определяем цветовую карту для визуализации
cmap = ListedColormap(['black', 'green', 'red'])

# Создаем начальное поле
field = np.full((FIELD_SIZE, FIELD_SIZE), EMPTY)

# Располагаем зараженные и незараженные клетки
initial_positions = np.random.choice(FIELD_SIZE * FIELD_SIZE, NUM_INFECTED + NUM_UNINFECTED, replace=False)
infected_positions = initial_positions[:NUM_INFECTED]
uninfected_positions = initial_positions[NUM_INFECTED:]

for pos in infected_positions:
    field[pos // FIELD_SIZE][pos % FIELD_SIZE] = INFECTED

for pos in uninfected_positions:
    field[pos // FIELD_SIZE][pos % FIELD_SIZE] = UNINFECTED

# Матрица для отслеживания времени жизни зараженных клеток
infected_timer = np.zeros_like(field)


def update_field(field, infected_timer): # функция обновления состояния поля
    new_field = np.copy(field)
    for i in range(FIELD_SIZE):
        for j in range(FIELD_SIZE):
            if field[i, j] == INFECTED:
                # Увеличиваем время жизни зараженной клетки
                infected_timer[i, j] += 1
                # Распространение вируса
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if (di, dj) != (0, 0) and 0 <= i + di < FIELD_SIZE and 0 <= j + dj < FIELD_SIZE:
                            if field[i + di, j + dj] == UNINFECTED:
                                new_field[i + di, j + dj] = INFECTED
                                infected_timer[i + di, j + dj] = 0
                # Смерть зараженной клетки после INFECTED_LIFESPAN ходов
                if infected_timer[i, j] == INFECTED_LIFESPAN:
                    new_field[i, j] = EMPTY
            elif field[i, j] == UNINFECTED:
                # Попытка убежать или размножаться
                empty_neighbors = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1]
                                   if 0 <= i + di < FIELD_SIZE and 0 <= j + dj < FIELD_SIZE and field[i + di, j + dj] == EMPTY]
                if empty_neighbors:
                    di, dj = empty_neighbors[np.random.choice(len(empty_neighbors))]
                    if np.random.rand() <= 0.1:  # Вероятность размножения
                        new_field[i + di, j + dj] = UNINFECTED
                    else:  # Вероятность перемещения
                        new_field[i, j] = EMPTY
                        new_field[i + di, j + dj] = UNINFECTED
    return new_field


# Функция анимации для Matplotlib
def animate(steps, interval):
    fig, ax = plt.subplots()
    mat = ax.matshow(field, cmap=cmap)

    def update(i):
        global field, infected_timer
        field = update_field(field, infected_timer)
        mat.set_data(field)
        return mat,

    ani = animation.FuncAnimation(fig, update, frames=steps, interval=interval)
    plt.show()

# Запускаем анимацию на NUM_STEPS шагов с интервалом в 100 мс между кадрами
animate(NUM_STEPS, 100)