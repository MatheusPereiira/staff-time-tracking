from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QHBoxLayout,
    QComboBox, QDateEdit, QFileDialog
)
from PyQt6.QtCore import QDate
from datetime import datetime
import csv

from controllers.punch_controller import PunchController

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


class ReportsView(QWidget):
    def __init__(self, employee):
        super().__init__()
        self.employee = employee
        self.controller = PunchController()

        self.setWindowTitle("Histórico de Pontos")
        self.setFixedSize(700, 450)

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Funcionário: {employee['name']}"))

        # FILTROS
        filters = QHBoxLayout()

        self.type_filter = QComboBox()
        self.type_filter.addItems(["todos", "entrada", "intervalo", "retorno", "saida"])

        self.start_date = QDateEdit(QDate.currentDate().addMonths(-1))
        self.start_date.setCalendarPopup(True)

        self.end_date = QDateEdit(QDate.currentDate())
        self.end_date.setCalendarPopup(True)

        btn_filter = QPushButton("Filtrar")
        btn_filter.clicked.connect(self.load_data)

        filters.addWidget(QLabel("Tipo:"))
        filters.addWidget(self.type_filter)
        filters.addWidget(QLabel("De:"))
        filters.addWidget(self.start_date)
        filters.addWidget(QLabel("Até:"))
        filters.addWidget(self.end_date)
        filters.addWidget(btn_filter)

        layout.addLayout(filters)

        # TABELA
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Data", "Hora", "Tipo"])
        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.table)

        # EXPORTAÇÃO
        export_layout = QHBoxLayout()

        btn_csv = QPushButton("Exportar CSV")
        btn_pdf = QPushButton("Exportar PDF")

        btn_csv.clicked.connect(self.export_csv)
        btn_pdf.clicked.connect(self.export_pdf)

        export_layout.addWidget(btn_csv)
        export_layout.addWidget(btn_pdf)

        layout.addLayout(export_layout)

        self.setLayout(layout)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)

        start = self.start_date.date().toPyDate()
        end = self.end_date.date().toPyDate()
        ptype = self.type_filter.currentText()

        self.data = self.controller.list_filtered(
            self.employee["id"], start, end, ptype
        )

        for p in self.data:
            row = self.table.rowCount()
            self.table.insertRow(row)

            dt = datetime.fromisoformat(p["timestamp"])

            self.table.setItem(row, 0, QTableWidgetItem(dt.strftime("%d/%m/%Y")))
            self.table.setItem(row, 1, QTableWidgetItem(dt.strftime("%H:%M:%S")))
            self.table.setItem(row, 2, QTableWidgetItem(p["type"].capitalize()))

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Salvar CSV", "", "CSV (*.csv)"
        )

        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Data", "Hora", "Tipo"])

            for p in self.data:
                dt = datetime.fromisoformat(p["timestamp"])
                writer.writerow([
                    dt.strftime("%d/%m/%Y"),
                    dt.strftime("%H:%M:%S"),
                    p["type"]
                ])

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Salvar PDF", "", "PDF (*.pdf)"
        )

        if not path:
            return

        pdf = canvas.Canvas(path, pagesize=A4)
        width, height = A4

        y = height - 50

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "Relatório de Pontos")
        y -= 30

        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, y, f"Funcionário: {self.employee['name']}")
        y -= 20

        for p in self.data:
            dt = datetime.fromisoformat(p["timestamp"])
            line = f"{dt.strftime('%d/%m/%Y')}  {dt.strftime('%H:%M:%S')}  {p['type']}"
            pdf.drawString(50, y, line)
            y -= 15

            if y < 50:
                pdf.showPage()
                y = height - 50

        pdf.save()
