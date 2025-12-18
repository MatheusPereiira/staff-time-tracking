from models.punch_model import PunchModel
from datetime import datetime


class PunchController:
    def __init__(self):
        self.model = PunchModel()

    def register(self, employee_id, punch_type):
        punches = self.model.all()

        last = None
        if punches:
            last = punches[-1]

        if last and last["employee_id"] == employee_id:
            if last["type"] == punch_type:
                raise ValueError("Esse ponto já foi registrado.")

        punch = {
            "employee_id": employee_id,
            "type": punch_type,
            "timestamp": datetime.now().isoformat()
        }

        self.model.add(punch)

    def list_by_employee(self, employee_id):
        return [
            p for p in self.model.all()
            if p["employee_id"] == employee_id
        ]

    def list_filtered(self, employee_id, start_date, end_date, punch_type=None):
        result = []

        for p in self.model.all():
            if p["employee_id"] != employee_id:
                continue

            date = datetime.fromisoformat(p["timestamp"]).date()

            if not (start_date <= date <= end_date):
                continue

            if punch_type and punch_type != "todos":
                if p["type"] != punch_type:
                    continue

            result.append(p)

        return result
