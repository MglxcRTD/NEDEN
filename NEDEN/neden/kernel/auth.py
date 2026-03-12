# kernel/auth.py

class AuthModule:
    def __init__(self):
        # Definimos la jerarquía de poder. 
        # A mayor número, más privilegios tiene el rol.
        self.ROLE_HIERARCHY = {
            "guest": 0,
            "explorer": 1,
            "admin": 2
        }

        self.users = {
            "explorer01": {"password": "secure123", "role": "explorer"},
            "admin01": {"password": "rootaccess", "role": "admin"},
        }

    def validate(self, username, password):
        """Valida las credenciales del usuario."""
        user = self.users.get(username)
        if user and user["password"] == password:
            print(f"[SECURITY] Autenticación exitosa de '{username}'.")
            return True
        print(f"[SECURITY] Fallo de autenticación para '{username}'.")
        return False

    def get_role(self, username):
        """Devuelve el rol de un usuario o 'guest' si no existe/no está logueado."""
        if not username:
            return "guest"
        return self.users.get(username, {}).get("role", "guest")

    def has_permission(self, username, required_role):
        """
        Verifica si el nivel del usuario es igual o superior al requerido.
        Ejemplo: Si se requiere 'explorer' (1), un 'admin' (2) puede pasar.
        """
        user_role = self.get_role(username)
        
        user_level = self.ROLE_HIERARCHY.get(user_role, 0)
        required_level = self.ROLE_HIERARCHY.get(required_role, 0)

        return user_level >= required_level

    def add_user(self, admin_user, new_username, new_password, role):
        """Permite a un admin crear nuevos usuarios en tiempo de ejecución."""
        if self.get_role(admin_user) != "admin":
            print("[ERROR] Solo un administrador puede crear usuarios.")
            return False
        
        if role not in self.ROLE_HIERARCHY:
            print(f"[ERROR] El rol '{role}' no es válido.")
            return False

        self.users[new_username] = {"password": new_password, "role": role}
        print(f"[SECURITY] Usuario '{new_username}' creado con rol '{role}'.")
        return True