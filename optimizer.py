import itertools
from typing import Iterable, Tuple

from tasks import Task


def generate_combinations(tasks: Iterable[Task], max_tasks: int = 4):
    """Generate all possible task combinations."""
    return itertools.combinations(tasks, max_tasks)


def calculate_resources(combination: Iterable[Task]) -> Tuple[float, float, float, float]:
    """Sum the resources for a combination of tasks."""
    total_manpower = sum(task.manpower for task in combination)
    total_ammo = sum(task.ammo for task in combination)
    total_food = sum(task.food for task in combination)
    total_parts = sum(task.parts for task in combination)
    return total_manpower, total_ammo, total_food, total_parts


def optimize_tasks(combinations: Iterable[Iterable[Task]], weights: dict):
    """Return the top five task combinations based on weighted value."""
    best_combinations = []

    for combination in combinations:
        total_manpower, total_ammo, total_food, total_parts = calculate_resources(combination)

        value = (
            total_manpower * weights['manpower'] +
            total_ammo * weights['ammo'] +
            total_food * weights['food'] +
            total_parts * weights['parts']
        )

        best_combinations.append((combination, value))

    best_combinations.sort(key=lambda x: x[1], reverse=True)
    return best_combinations[:5]
