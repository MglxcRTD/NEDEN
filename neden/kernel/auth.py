class AuthModule:
    def __init__(self):
        self.users = {
            "explorer01": {"password": "secure123", "role": "explorer"},
            "admin01": {"password": "rootaccess", "role": "admin"},
        }

    def validate(self, username, password):
        user = self.users.get(username)
        if user and user["password"] == password:
            print(f"[SECURITY] Autenticación exitosa de '{username}'.")
            return True
        print(f"[SECURITY] Fallo de autenticación para '{username}'.")
        return False

    def get_role(self, username):
        return self.users.get(username, {}).get("role", "guest")
