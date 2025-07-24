from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)
from PyQt5.QtCore import Qt

from optimizer import generate_combinations, calculate_resources, optimize_tasks


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

        self.calculate_button = QPushButton('计算')
        self.calculate_button.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_button)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels([
            '任务 1',
            '任务 2',
            '任务 3',
            '任务 4',
            '总量 (人力, 弹药, 口粮, 零件)',
        ])
        layout.addWidget(self.results_table)

        self.setLayout(layout)

    def calculate(self):
        try:
            weights = {
                'manpower': float(self.manpower_entry.text()),
                'ammo': float(self.ammo_entry.text()),
                'food': float(self.food_entry.text()),
                'parts': float(self.parts_entry.text()),
            }
        except ValueError:
            QMessageBox.warning(self, '输入错误', '请输入有效的数值。')
            return

        combinations = generate_combinations(self.tasks)
        best_combinations = optimize_tasks(combinations, weights)

        self.results_table.setRowCount(len(best_combinations))
        for i, (combination, value) in enumerate(best_combinations):
            for j, task in enumerate(combination):
                self.results_table.setItem(i, j, QTableWidgetItem(f"{task.level}-{task.task_no}"))
            total_manpower, total_ammo, total_food, total_parts = calculate_resources(combination)
            self.results_table.setItem(
                i,
                4,
                QTableWidgetItem(
                    f"{total_manpower:.1f}, {total_ammo:.1f}, {total_food:.1f}, {total_parts:.1f}"
                ),
            )
        return
