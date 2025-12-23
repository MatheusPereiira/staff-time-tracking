from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMessageBox, QFrame
)
from PyQt6.QtCore import QTimer, QTime, Qt

from controllers.punch_controller import PunchController
from views.reports_view import ReportsView


class EmployeeDashboard(QWidget):
    def __init__(self, employee):
        super().__init__()

        self.employee = employee
        self.controller = PunchController()

        self.setWindowTitle("Registro de Ponto")
        self.setFixedSize(440, 560)

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)

        self.work_timer = QTimer(self)
        self.work_timer.timeout.connect(self.update_work_time)

        self.seconds_worked = 0
        self.is_working = False

        self.init_ui()
        self.clock_timer.start(1000)
        self.update_status()

    #  UI 

    def init_ui(self):
        main = QVBoxLayout(self)
        main.setSpacing(20)
        main.setContentsMargins(24, 24, 24, 24)

        # TOP BALLOONS 
        top_layout = QHBoxLayout()
        top_layout.setSpacing(16)

        # LEFT BALLOON
        user_card = QFrame()
        user_card.setStyleSheet("""
            QFrame {
                background:#2563eb;
                border-radius:16px;
                padding:14px;
            }
        """)

        user_layout = QVBoxLayout(user_card)
        user_layout.setSpacing(6)

        self.label_name = QLabel(self.employee["name"])
        self.label_name.setStyleSheet("""
            font-size:16px;
            font-weight:600;
            color:white;
        """)

        self.label_user = QLabel(f"@{self.employee['user_username']}")
        self.label_user.setStyleSheet("""
            font-size:13px;
            color:#dbeafe;
        """)

        self.work_label = QLabel("Timer: 00:00:00")
        self.work_label.setStyleSheet("""
            font-size:12px;
            color:#bfdbfe;
            margin-top:4px;
        """)

        user_layout.addWidget(self.label_name)
        user_layout.addWidget(self.label_user)
        user_layout.addWidget(self.work_label)
        user_layout.addStretch()

        
        status_card = QFrame()
        status_card.setStyleSheet("""
            QFrame {
                background:#2563eb;
                border-radius:16px;
                padding:14px;
            }
        """)

        status_layout = QVBoxLayout(status_card)
        status_layout.setSpacing(8)
        status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.clock_label = QLabel("--:--")
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clock_label.setStyleSheet("""
            font-size:28px;
            font-weight:700;
            color:white;
        """)

        self.status_label = QLabel("Fora")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFixedWidth(120)
        self.status_label.setStyleSheet("""
            background:#fee2e2;
            color:#991b1b;
            font-size:13px;
            font-weight:600;
            padding:6px;
            border-radius:10px;
        """)

        status_layout.addWidget(self.clock_label)
        status_layout.addWidget(self.status_label)

        top_layout.addWidget(user_card, 1)
        top_layout.addWidget(status_card, 1)

        main.addLayout(top_layout)

        # ACTION BUTTONS 
        def styled_button(text):
            b = QPushButton(text)
            b.setFixedHeight(44)
            return b

        btn_entry = styled_button("Entrada")
        btn_break = styled_button("Intervalo")
        btn_return = styled_button("Retorno")
        btn_exit = styled_button("Saída")
        btn_report = styled_button("Relatório de Horas")

        btn_entry.clicked.connect(lambda: self.register("entrada"))
        btn_break.clicked.connect(lambda: self.register("intervalo"))
        btn_return.clicked.connect(lambda: self.register("retorno"))
        btn_exit.clicked.connect(lambda: self.register("saida"))
        btn_report.clicked.connect(self.open_report)

        main.addWidget(btn_entry)
        main.addWidget(btn_break)
        main.addWidget(btn_return)
        main.addWidget(btn_exit)
        main.addWidget(btn_report)

    #  CLOCK 

    def update_clock(self):
        self.clock_label.setText(QTime.currentTime().toString("HH:mm"))

    def update_work_time(self):
        self.seconds_worked += 1
        h = self.seconds_worked // 3600
        m = (self.seconds_worked % 3600) // 60
        s = self.seconds_worked % 60
        self.work_label.setText(
            f"Tempo trabalhado: {h:02d}:{m:02d}:{s:02d}"
        )

    #  STATUS 

    def update_status(self):
        status = self.controller.get_current_status(self.employee["id"])

        if status == "trabalhando":
            self.status_label.setText("Trabalhando")
            self.status_label.setStyleSheet("""
                background:#dcfce7;
                color:#166534;
                font-size:13px;
                font-weight:600;
                padding:6px;
                border-radius:10px;
            """)
            self.start_work_timer()

        elif status == "intervalo":
            self.status_label.setText("Intervalo")
            self.status_label.setStyleSheet("""
                background:#fef9c3;
                color:#854d0e;
                font-size:13px;
                font-weight:600;
                padding:6px;
                border-radius:10px;
            """)
            self.stop_work_timer()

        else:
            self.status_label.setText("Fora")
            self.status_label.setStyleSheet("""
                background:#fee2e2;
                color:#991b1b;
                font-size:13px;
                font-weight:600;
                padding:6px;
                border-radius:10px;
            """)
            self.stop_work_timer()

    # ACTIONS
    def register(self, punch_type):
        try:
            self.controller.register(
                employee_id=self.employee["id"],
                punch_type=punch_type
            )
            self.update_status()
            QMessageBox.information(self, "Sucesso", "Ponto registrado!")
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

    def open_report(self):
        self.report_window = ReportsView(self.employee)
        self.report_window.show()