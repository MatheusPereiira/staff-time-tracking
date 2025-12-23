import uuid
from utils.json_manager import JsonManager


class UserModel:
    def __init__(self):
        self.storage = JsonManager("data/users.json")

    def all(self):
        return self.storage.read()

    def find_by_username(self, username: str):
        users = self.storage.read()
        for user in users:
            if user["username"] == username:
                return user
        return None

    def create(self, data: dict):
        users = self.storage.read()

        new_user = {
            "id": str(uuid.uuid4()),
            "username": data["username"],
            "password": data["password"],  
            "role": data["role"]
        }

        users.append(new_user)
        self.storage.write(users)
        return new_user