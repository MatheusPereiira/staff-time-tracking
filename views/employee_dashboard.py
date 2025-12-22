from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt

from controllers.punch_controller import PunchController
from views.reports_view import ReportsView


class EmployeeDashboard(QWidget):
    def __init__(self, employee):
        super().__init__()

        self.employee = employee
        self.controller = PunchController()

        self.setWindowTitle("Painel do Funcionário")
        self.setFixedSize(420, 520)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # ===== TÍTULO =====
        title = QLabel("Registro de Ponto")
        title.setObjectName("DashboardTitle")
        main_layout.addWidget(title)

        #CARD FUNCIONÁRIO
        card = QWidget()
        card.setObjectName("Card")

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(6)

        label_name = QLabel(f"Funcionário: {self.employee['name']}")
        label_user = QLabel(f"Usuário: {self.employee['user_username']}")

        label_name.setStyleSheet("font-weight: 600;")
        label_user.setStyleSheet("color: #475569;")

        card_layout.addWidget(label_name)
        card_layout.addWidget(label_user)

        main_layout.addWidget(card)

        #BOTÕES DE PONTO
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(12)

        btn_entry = QPushButton("Entrada")
        btn_break = QPushButton("Intervalo")
        btn_return = QPushButton("Retorno")
        btn_exit = QPushButton("Saída")

        btn_entry.clicked.connect(lambda: self.register("entrada"))
        btn_break.clicked.connect(lambda: self.register("intervalo"))
        btn_return.clicked.connect(lambda: self.register("retorno"))
        btn_exit.clicked.connect(lambda: self.register("saida"))

        buttons_layout.addWidget(btn_entry)
        buttons_layout.addWidget(btn_break)
        buttons_layout.addWidget(btn_return)
        buttons_layout.addWidget(btn_exit)

        main_layout.addLayout(buttons_layout)

        #RELATÓRIO 
        btn_report = QPushButton("Relatório de Horas")
        btn_report.clicked.connect(self.open_report)

        main_layout.addStretch()
        main_layout.addWidget(btn_report)

    #AÇÕES

    def register(self, punch_type):
        try:
            self.controller.register(
                employee_id=self.employee["id"],
                punch_type=punch_type
            )
            QMessageBox.information(
                self,
                "Sucesso",
                f"Ponto registrado: {punch_type.capitalize()}"
            )
        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))

    def open_report(self):
        self.report_window = ReportsView(self.employee)
        self.report_window.show()
