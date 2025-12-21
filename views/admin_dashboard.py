from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QLineEdit
)
from PyQt6.QtCore import Qt

from views.employee_form_dialog import EmployeeFormDialog
from controllers.employee_controller import EmployeeController
from controllers.report_controller import ReportController
from views.admin_reports_view import AdminReportsView


class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Administrativo")
        self.resize(1100, 650)

        self.employee_controller = EmployeeController()
        self.report_controller = ReportController()

        self.employees = []

        self.init_ui()
        self.load_data()

    #UI
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(24, 24, 24, 24)

        #TÍTULO
        title = QLabel("Dashboard Administrativo")
        title.setObjectName("DashboardTitle")
        main_layout.addWidget(title)

        #CARDS
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        self.card_employees = self.create_card("Funcionários")
        self.card_total_hours = self.create_card("Horas Totais")
        self.card_average = self.create_card("Média / Funcionário")
        self.card_highlight = self.create_highlight_card("Destaque")

        cards_layout.addWidget(self.card_employees)
        cards_layout.addWidget(self.card_total_hours)
        cards_layout.addWidget(self.card_average)
        cards_layout.addWidget(self.card_highlight)

        main_layout.addLayout(cards_layout)

        #AÇÕES GERAIS
        actions_layout = QHBoxLayout()
        actions_layout.addStretch()

        btn_reports = QPushButton("Relatórios")
        btn_reports.clicked.connect(self.open_reports)

        btn_refresh = QPushButton("Atualizar")
        btn_refresh.clicked.connect(self.load_data)

        actions_layout.addWidget(btn_reports)
        actions_layout.addWidget(btn_refresh)

        main_layout.addLayout(actions_layout)

        #FILTROS
        filter_layout = QHBoxLayout()

        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Buscar por nome...")
        self.search_name.textChanged.connect(self.filter_employees)

        self.search_role = QLineEdit()
        self.search_role.setPlaceholderText("Buscar por cargo...")
        self.search_role.textChanged.connect(self.filter_employees)

        self.search_department = QLineEdit()
        self.search_department.setPlaceholderText("Buscar por departamento...")
        self.search_department.textChanged.connect(self.filter_employees)

        filter_layout.addWidget(self.search_name)
        filter_layout.addWidget(self.search_role)
        filter_layout.addWidget(self.search_department)
        filter_layout.addStretch()

        main_layout.addLayout(filter_layout)

        #AÇÕES DA TABELA
        table_actions = QHBoxLayout()

        btn_new = QPushButton("Novo")
        btn_new.clicked.connect(self.add_employee)

        btn_edit = QPushButton("Editar")
        btn_edit.clicked.connect(self.edit_employee)

        btn_delete = QPushButton("Excluir")
        btn_delete.clicked.connect(self.delete_employee)

        #ORDENAÇÃO
        btn_sort_az = QPushButton("Ordenar A–Z")
        btn_sort_az.clicked.connect(self.sort_az)

        btn_sort_za = QPushButton("Ordenar Z–A")
        btn_sort_za.clicked.connect(self.sort_za)

        table_actions.addWidget(btn_new)
        table_actions.addWidget(btn_edit)
        table_actions.addWidget(btn_delete)
        table_actions.addSpacing(16)
        table_actions.addWidget(btn_sort_az)
        table_actions.addWidget(btn_sort_za)
        table_actions.addStretch()

        main_layout.addLayout(table_actions)

        # TABELA
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(
            ["Nome", "Cargo", "Departamento"]
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        main_layout.addWidget(self.table)

    #COMPONENTES
    def create_card(self, title_text):
        card = QWidget()
        card.setObjectName("Card")

        layout = QVBoxLayout(card)
        layout.setSpacing(6)

        title = QLabel(title_text)
        title.setObjectName("CardTitle")

        value = QLabel("0")
        value.setObjectName("CardValue")

        layout.addWidget(title)
        layout.addWidget(value)

        card.value_label = value
        return card

    def create_highlight_card(self, title_text):
        card = QWidget()
        card.setObjectName("HighlightCard")

        layout = QVBoxLayout(card)
        layout.setSpacing(6)

        title = QLabel(title_text)
        title.setObjectName("CardTitle")

        value = QLabel("-")
        value.setObjectName("CardValue")

        layout.addWidget(title)
        layout.addWidget(value)

        card.value_label = value
        return card

    # DADOS
    def load_data(self):
        self.employees = self.employee_controller.all()
        summary = self.report_controller.admin_summary()

        total_employees = len(self.employees)
        total_hours = sum(item["hours"] for item in summary)
        avg_hours = total_hours / total_employees if total_employees else 0

        highlight = max(summary, key=lambda x: x["hours"], default=None)

        self.card_employees.value_label.setText(str(total_employees))
        self.card_total_hours.value_label.setText(f"{total_hours:.1f} h")
        self.card_average.value_label.setText(f"{avg_hours:.1f} h")

        if highlight:
            self.card_highlight.value_label.setText(
                f'{highlight["name"]} — {highlight["hours"]:.1f} h'
            )
        else:
            self.card_highlight.value_label.setText("-")

        self.populate_table(self.employees)

    def populate_table(self, employees):
        self.table.setRowCount(len(employees))
        for row, emp in enumerate(employees):
            self.table.setItem(row, 0, QTableWidgetItem(emp["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(emp["role"]))
            self.table.setItem(row, 2, QTableWidgetItem(emp["department"]))

    #FILTRO
    def filter_employees(self):
        name_filter = self.search_name.text().lower()
        role_filter = self.search_role.text().lower()
        department_filter = self.search_department.text().lower()

        filtered = [
            emp for emp in self.employees
            if name_filter in emp["name"].lower()
            and role_filter in emp["role"].lower()
            and department_filter in emp["department"].lower()
        ]

        self.populate_table(filtered)

    #ORDENAÇÃO
    def sort_az(self):
        self.employees.sort(key=lambda e: e["name"].lower())
        self.filter_employees()

    def sort_za(self):
        self.employees.sort(key=lambda e: e["name"].lower(), reverse=True)
        self.filter_employees()

    #AÇÕES
    def open_reports(self):
        self.reports_window = AdminReportsView()
        self.reports_window.show()

    def add_employee(self):
        dialog = EmployeeFormDialog(self)
        if dialog.exec():
            self.load_data()

    def edit_employee(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Atenção", "Selecione um funcionário.")
            return

        employee = self.employees[row]
        dialog = EmployeeFormDialog(self, employee)
        if dialog.exec():
            self.load_data()

    def delete_employee(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Atenção", "Selecione um funcionário.")
            return

        employee = self.employees[row]

        confirm = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Deseja realmente excluir {employee['name']}?"
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self.employee_controller.delete(employee["id"])
            self.load_data()
