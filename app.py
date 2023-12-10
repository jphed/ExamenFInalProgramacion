from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap
import sys
import requests

class Employee:
    def __init__(self, name, last_name, email, sex, image):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.sex = sex
        self.image = image

class QEmployee(QWidget):
    def __init__(self, employee):
        super().__init__()
        self.employee = employee
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label_name = QLabel(self.employee.name)
        label_last_name = QLabel(self.employee.last_name)
        label_email = QLabel(self.employee.email)
        label_sex = QLabel(self.employee.sex)
        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(self.employee.image).content)
        label_image = QLabel()
        label_image.setPixmap(pixmap)
        layout.addWidget(label_name)
        layout.addWidget(label_last_name)
        layout.addWidget(label_email)
        layout.addWidget(label_sex)
        layout.addWidget(label_image)
        self.setLayout(layout)

class QPanelEmployees(QWidget):
    def __init__(self, employees):
        super().__init__()
        self.employees = employees
        self.index = 0
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.employee_layout = QVBoxLayout()
        self.layout.addLayout(self.employee_layout)
        self.update_employee()

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        btn_layout = QHBoxLayout()
        btn_first = QPushButton('Primero')
        btn_first.clicked.connect(self.first)
        btn_previous = QPushButton('Anterior')
        btn_previous.clicked.connect(self.previous)
        btn_next = QPushButton('Siguiente')
        btn_next.clicked.connect(self.next_one)
        btn_last = QPushButton('Ultimo')
        btn_last.clicked.connect(self.last_one)
        btn_layout.addWidget(btn_first)
        btn_layout.addWidget(btn_previous)
        btn_layout.addWidget(btn_next)
        btn_layout.addWidget(btn_last)

        self.layout.addItem(spacer)
        self.layout.addLayout(btn_layout)
        self.setLayout(self.layout)

    def update_employee(self):
        for i in reversed(range(self.employee_layout.count())): 
            widget = self.employee_layout.itemAt(i).widget()
            if widget is not None:  # check if widget exists before removing it
                widget.setParent(None)
        self.employee_layout.addWidget(self.employees[self.index])

    def next_one(self):
        if self.index < len(self.employees) - 1:
            self.index += 1
            self.update_employee()

    def previous(self):
        if self.index > 0:
            self.index -= 1
            self.update_employee()

    def first(self):
        self.index = 0
        self.update_employee()

    def last_one(self):
        self.index = len(self.employees) - 1
        self.update_employee()

def get_data():
    response = requests.get('https://randomuser.me/api/?results=10')
    data = response.json()['results']
    return data

def create_employees(data):
    employees = []
    for item in data:
        name = item['name']['first']
        last_name = item['name']['last']
        email = item['email']
        sex = item['gender']
        image = item['picture']['large']
        employee = Employee(name, last_name, email, sex, image)
        employees.append(employee)
    return employees

def create_qemployees(employees):
    qemployees = []
    for employee in employees:
        qemployee = QEmployee(employee)
        qemployees.append(qemployee)
    return qemployees

def main():
    app = QApplication(sys.argv)
    data = get_data()
    employees = create_employees(data)
    qemployees = create_qemployees(employees)
    panel = QPanelEmployees(qemployees)
    panel.setWindowTitle("Empleados Examen Final Jorge Parra 13104")  # Set the window title here
    panel.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()