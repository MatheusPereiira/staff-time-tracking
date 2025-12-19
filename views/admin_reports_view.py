from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt6.QtCore import Qt

from controllers.report_controller import ReportController

import matplotlib.pyplot as plt


class AdminReportsView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Relatório Administrativo")
        self.setMinimumSize(750, 520)

        self.controller = ReportController()

        layout = QVBoxLayout(self)

        # Título
        title = QLabel("Relatório de Horas Trabalhadas")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold; margin-bottom: 10px;"
        )
        layout.addWidget(title)

        # Tabela
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([
            "Nome", "Usuário", "Horas Trabalhadas"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        layout.addWidget(self.table)

        # Botões
        buttons_layout = QHBoxLayout()

        btn_csv = QPushButton("Exportar CSV")
        btn_pdf = QPushButton("Exportar PDF")
        btn_chart = QPushButton("Gráfico de Horas")

        btn_csv.clicked.connect(self.export_csv)
        btn_pdf.clicked.connect(self.export_pdf)
        btn_chart.clicked.connect(self.show_chart)

        buttons_layout.addWidget(btn_csv)
        buttons_layout.addWidget(btn_pdf)
        buttons_layout.addWidget(btn_chart)

        layout.addLayout(buttons_layout)

        self.load_data()

    def load_data(self):
        reports = self.controller.admin_summary()
        self.table.setRowCount(len(reports))

        for row, report in enumerate(reports):
            self.table.setItem(row, 0, QTableWidgetItem(report["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(report["username"]))

            hours_item = QTableWidgetItem(f"{report['hours']:.2f}")
            hours_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 2, hours_item)

    def export_csv(self):
        from utils.json_manager import write_csv
        data = self.controller.admin_summary()
        write_csv("relatorio_admin.csv", data)

    def export_pdf(self):
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

        data = self.controller.admin_summary()
        pdf = canvas.Canvas("relatorio_admin.pdf", pagesize=A4)

        y = 800
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, y, "Relatório Administrativo de Horas")
        y -= 40

        pdf.setFont("Helvetica", 11)

        for item in data:
            line = f"{item['name']} ({item['username']}) - {item['hours']}h"
            pdf.drawString(50, y, line)
            y -= 20

            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 11)
                y = 800

        pdf.save()

    def show_chart(self):
        data = self.controller.admin_summary()

        names = [item["name"] for item in data]
        hours = [item["hours"] for item in data]

        plt.figure(figsize=(9, 5))

        bars = plt.bar(
            names,
            hours,
            color="#2E6BE6",
            edgecolor="#1f4fbf"
        )

        plt.title(
            "Horas Trabalhadas por Funcionário",
            fontsize=14,
            fontweight="bold",
            pad=15
        )

        plt.xlabel("Funcionário", fontsize=11)
        plt.ylabel("Horas Trabalhadas", fontsize=11)

        plt.grid(axis="y", linestyle="--", alpha=0.4)
        plt.xticks(rotation=30, ha="right")

        # Valores acima das barras
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{height:.2f} h",
                ha="center",
                va="bottom",
                fontsize=10
            )

        plt.tight_layout()
        plt.show()
