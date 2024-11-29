import sys
import itertools
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt

class Task:
    def __init__(self, level, task_no, manpower, ammo, food, parts):
        self.level = level
        self.task_no = task_no
        self.manpower = manpower
        self.ammo = ammo
        self.food = food
        self.parts = parts

    def __repr__(self):
        return f"Task({self.level}-{self.task_no}, manpower={self.manpower}, ammo={self.ammo}, food={self.food}, parts={self.parts})"

def load_tasks_from_csv(file_path):
    """从CSV文件加载任务数据"""
    tasks = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            level, task_no, manpower, ammo, food, parts = map(float, row)
            tasks.append(Task(int(level), int(task_no), manpower, ammo, food, parts))
    return tasks

def generate_combinations(tasks, max_tasks=4):
    """生成所有可能的任务组合"""
    return itertools.combinations(tasks, max_tasks)

def calculate_resources(combination):
    """计算任务组合的资源总量"""
    total_manpower = sum(task.manpower for task in combination)
    total_ammo = sum(task.ammo for task in combination)
    total_food = sum(task.food for task in combination)
    total_parts = sum(task.parts for task in combination)
    return total_manpower, total_ammo, total_food, total_parts

def optimize_tasks(combinations, weights):
    """根据权重找到最优的任务组合"""
    best_combinations = []

    for combination in combinations:
        total_manpower, total_ammo, total_food, total_parts = calculate_resources(combination)

        # 计算加权偏差
        value = (
            total_manpower * weights['manpower'] +
            total_ammo * weights['ammo'] +
            total_food * weights['food'] +
            total_parts * weights['parts']
        )

        best_combinations.append((combination, value))

    # 按加权偏差排序并取前五个组合
    best_combinations.sort(key=lambda x: x[1], reverse=True)
    return best_combinations[:5]

class LogisticsApp(QWidget):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Logistics Support Optimizer')

        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        self.resize(screen_size.width() * 2 // 3, screen_size.height() * 2 // 3)

        layout = QVBoxLayout()

        # 输入权重的标签和输入框
        self.manpower_label = QLabel('人力权重:')
        self.manpower_entry = QLineEdit()
        layout.addWidget(self.manpower_label)
        layout.addWidget(self.manpower_entry)

        self.ammo_label = QLabel('弹药权重:')
        self.ammo_entry = QLineEdit()
        layout.addWidget(self.ammo_label)
        layout.addWidget(self.ammo_entry)

        self.food_label = QLabel('口粮权重:')
        self.food_entry = QLineEdit()
        layout.addWidget(self.food_label)
        layout.addWidget(self.food_entry)

        self.parts_label = QLabel('零件权重:')
        self.parts_entry = QLineEdit()
        layout.addWidget(self.parts_label)
        layout.addWidget(self.parts_entry)

        # 计算按钮
        self.calculate_button = QPushButton('计算')
        self.calculate_button.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_button)

        # 结果表格
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(['任务 1', '任务 2', '任务 3', '任务 4', '总量 (人力, 弹药, 口粮, 零件)'])
        layout.addWidget(self.results_table)

        self.setLayout(layout)

    def calculate(self):
        try:
            # 读取用户输入的权重
            weights = {
                'manpower': float(self.manpower_entry.text()),
                'ammo': float(self.ammo_entry.text()),
                'food': float(self.food_entry.text()),
                'parts': float(self.parts_entry.text())
            }
        except ValueError:
            QMessageBox.warning(self, '输入错误', '请输入有效的数值。')
            return

        # 生成所有任务组合并优化选择
        combinations = generate_combinations(self.tasks)
        best_combinations = optimize_tasks(combinations, weights)

        # 显示结果
        self.results_table.setRowCount(len(best_combinations))
        for i, (combination, value) in enumerate(best_combinations):
            for j, task in enumerate(combination):
                self.results_table.setItem(i, j, QTableWidgetItem(f"{task.level}-{task.task_no}"))
            total_manpower, total_ammo, total_food, total_parts = calculate_resources(combination)
            self.results_table.setItem(i, 4, QTableWidgetItem(
                f"{total_manpower:.1f}, {total_ammo:.1f}, {total_food:.1f}, {total_parts:.1f}"
            ))

if __name__ == '__main__':
    # 从CSV文件中加载任务数据
    tasks = load_tasks_from_csv('tasks.csv')
    app = QApplication(sys.argv)
    ex = LogisticsApp(tasks)
    ex.show()
    sys.exit(app.exec_())
