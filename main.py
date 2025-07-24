import sys
from PyQt5.QtWidgets import QApplication

from tasks import load_tasks_from_csv
from ui import LogisticsApp


if __name__ == '__main__':
    tasks = load_tasks_from_csv('tasks.csv')
    app = QApplication(sys.argv)
    ex = LogisticsApp(tasks)
    ex.show()
    sys.exit(app.exec_())
