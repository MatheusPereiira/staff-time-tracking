from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt

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

        self.init_ui()
        self.load_data()

    #  UI 

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # TÍTULO
        title = QLabel("Dashboard Administrativo")
        title.setObjectName("DashboardTitle")
        main_layout.addWidget(title)

        # CARDS
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

        # AÇÕES GERAIS
        actions_layout = QHBoxLayout()
        actions_layout.addStretch()

        btn_reports = QPushButton("Relatórios")
        btn_reports.clicked.connect(self.open_reports)

        btn_refresh = QPushButton("Atualizar")
        btn_refresh.clicked.connect(self.load_data)

        actions_layout.addWidget(btn_reports)
        actions_layout.addWidget(btn_refresh)
        main_layout.addLayout(actions_layout)

        # AÇÕES DA TABELA
        table_actions = QHBoxLayout()

        btn_new = QPushButton("Novo")
        btn_new.clicked.connect(self.add_employee)

        btn_edit = QPushButton("Editar")
        btn_edit.clicked.connect(self.edit_employee)

        btn_delete = QPushButton("Excluir")
        btn_delete.clicked.connect(self.delete_employee)

        table_actions.addWidget(btn_new)
        table_actions.addWidget(btn_edit)
        table_actions.addWidget(btn_delete)
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

    # COMPONENTES 

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
        employees = self.employee_controller.all()
        summary = self.report_controller.admin_summary()

        total_employees = len(employees)
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

        self.table.setRowCount(len(employees))
        for row, emp in enumerate(employees):
            self.table.setItem(row, 0, QTableWidgetItem(emp["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(emp["role"]))
            self.table.setItem(row, 2, QTableWidgetItem(emp["department"]))

    #AÇÕES

    def open_reports(self):
        self.reports_window = AdminReportsView()
        self.reports_window.show()

    def add_employee(self):
        QMessageBox.information(
            self, "Novo Funcionário",
            "Aqui você pode abrir um formulário para cadastrar funcionário."
        )

    def edit_employee(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Atenção", "Selecione um funcionário.")
            return
        QMessageBox.information(
            self, "Editar Funcionário",
            "Aqui você pode editar o funcionário selecionado."
        )

    def delete_employee(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Atenção", "Selecione um funcionário.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            "Deseja realmente excluir este funcionário?"
        )

        if confirm == QMessageBox.StandardButton.Yes:
            QMessageBox.information(
                self, "Excluído", "Funcionário removido com sucesso."
            )
