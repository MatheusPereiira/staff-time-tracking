from datetime import datetime
from models.punch_model import PunchModel


class PunchController:
    def __init__(self):
        self.model = PunchModel()

    def register(self, employee_id: str, punch_type: str):
        now = datetime.now().isoformat()

        punch = {
            "employee_id": employee_id,
            "type": punch_type,
            "timestamp": now
        }

        self.model.add(punch)

    def list_by_employee(self, employee_id: str):
        return self.model.by_employee(employee_id)

    def get_current_status(self, employee_id: str):
        punches = self.model.by_employee(employee_id)

        if not punches:
            return "fora"

        last = punches[-1]["type"]

        if last == "entrada" or last == "retorno":
            return "trabalhando"

        if last == "intervalo":
            return "intervalo"

        return "fora"

    # 🔥 MÉTODO USADO NO RELATÓRIO
    def list_filtered(self, employee_id, start_date, end_date, punch_type):
        punches = self.model.by_employee(
            employee_id,
            start_date.isoformat(),
            end_date.isoformat()
        )

        if punch_type != "todos":
            punches = [
                p for p in punches
                if p["type"] == punch_type
            ]

        return punches
