import csv

class Task:
    def __init__(self, level: int, task_no: int, manpower: float, ammo: float, food: float, parts: float):
        self.level = level
        self.task_no = task_no
        self.manpower = manpower
        self.ammo = ammo
        self.food = food
        self.parts = parts

    def __repr__(self) -> str:
        return (
            f"Task({self.level}-{self.task_no}, manpower={self.manpower}, "
            f"ammo={self.ammo}, food={self.food}, parts={self.parts})"
        )

def load_tasks_from_csv(file_path: str):
    """Load task data from a CSV file."""
    tasks = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            level, task_no, manpower, ammo, food, parts = map(float, row)
            tasks.append(Task(int(level), int(task_no), manpower, ammo, food, parts))
    return tasks
