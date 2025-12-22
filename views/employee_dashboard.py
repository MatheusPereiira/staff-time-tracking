from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QLabel, QMessageBox
)
from PyQt6.QtCore import QTimer, QTime, Qt 
from datetime import datetime

from controllers.punch_controller import PunchController
from views.reports_view import ReportsView


class EmployeeDashboard(QWidget):
    def __init__(self, employee):
        super().__init__()

        self.employee = employee
        self.controller = PunchController()

        self.setWindowTitle("Registro de Ponto")
        self.setFixedSize(400, 460)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)

        self.work_timer = QTimer(self)
        self.work_timer.timeout.connect(self.update_work_time)

        self.seconds_worked = 0
        self.is_working = False

        self.init_ui()
        self.timer.start(1000)

    #UI

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # INFO FUNCIONÁRIO
        self.label_employee = QLabel(f"Funcionário: {self.employee['name']}")
        self.label_user = QLabel(f"Usuário: {self.employee['user_username']}")

        self.label_employee.setStyleSheet("font-weight:600;")
        self.label_user.setStyleSheet("color:#475569;")

        layout.addWidget(self.label_employee)
        layout.addWidget(self.label_user)

        # RELÓGIO ATUAL
        self.clock_label = QLabel("--:--:--")
        self.clock_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            text-align: center;
        """)
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.clock_label)

        # CONTADOR DE HORAS
        self.work_label = QLabel("Tempo trabalhado: 00:00:00")
        self.work_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.work_label.setStyleSheet("font-size:16px;")

        layout.addWidget(self.work_label)

        # BOTÕES
        btn_entry = QPushButton("Entrada")
        btn_break = QPushButton("Intervalo")
        btn_return = QPushButton("Retorno")
        btn_exit = QPushButton("Saída")
        btn_report = QPushButton("Relatório de Horas")

        btn_entry.clicked.connect(lambda: self.register("entrada"))
        btn_break.clicked.connect(lambda: self.register("intervalo"))
        btn_return.clicked.connect(lambda: self.register("retorno"))
        btn_exit.clicked.connect(lambda: self.register("saida"))
        btn_report.clicked.connect(self.open_report)

        layout.addWidget(btn_entry)
        layout.addWidget(btn_break)
        layout.addWidget(btn_return)
        layout.addWidget(btn_exit)
        layout.addWidget(btn_report)

        self.setLayout(layout)

    #RELÓGIO

    def update_clock(self):
        now = QTime.currentTime()
        self.clock_label.setText(now.toString("HH:mm:ss"))

    def update_work_time(self):
        self.seconds_worked += 1
        h = self.seconds_worked // 3600
        m = (self.seconds_worked % 3600) // 60
        s = self.seconds_worked % 60
        self.work_label.setText(
            f"Tempo trabalhado: {h:02d}:{m:02d}:{s:02d}"
        )

    # PONTO

    def register(self, punch_type):
        try:
            self.controller.register(
                employee_id=self.employee["id"],
                punch_type=punch_type
            )

            # CONTROLE DO TIMER
            if punch_type == "entrada":
                self.start_work_timer()

            elif punch_type == "intervalo":
                self.stop_work_timer()

            elif punch_type == "retorno":
                self.start_work_timer()

            elif punch_type == "saida":
                self.stop_work_timer()

            QMessageBox.information(
                self,
                "Sucesso",
                f"Ponto registrado: {punch_type.capitalize()}"
            )

        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))

    def start_work_timer(self):
        if not self.is_working:
            self.is_working = True
            self.work_timer.start(1000)

    def stop_work_timer(self):
        if self.is_working:
            self.is_working = False
            self.work_timer.stop()

    #RELATÓRIO

    def open_report(self):
        self.report_window = ReportsView(self.employee)
        self.report_window.show()
