class Usuario:
    # Definimos la clase base que representa un usuario de la tienda
    # Usamos un contador incremental para asignar IDs únicos
    _contador_id = 1

    def __init__(self, nombre, email):
        # Asignamos un ID único y aumentamos el contador
        self.id = Usuario._contador_id
        Usuario._contador_id += 1

        # Guardamos el nombre y el email eliminando espacios sobrantes
        self.nombre = nombre.strip()
        self.email = email.strip()

        # Validamos que el nombre no esté vacío
        if not self.nombre:
            raise ValueError("El nombre no puede estar vacío.")
        # Validamos que el email contenga un '@'
        if "@" not in self.email:
            raise ValueError("El email debe ser válido.")

    def is_admin(self):
        # Por defecto, un usuario no es administrador
        return False

    def __str__(self):
        # Devolvemos una representación en texto del usuario
        return f"[Usuario#{self.id}] {self.nombre} ({self.email})"


class Cliente(Usuario):
    # Definimos un cliente que hereda de Usuario y añade dirección postal
    def __init__(self, nombre, email, direccion):
        # Llamamos al constructor de Usuario
        super().__init__(nombre, email)
        # Guardamos la dirección eliminando espacios
        self.direccion = direccion.strip()

        # Validamos que la dirección no esté vacía
        if not self.direccion:
            raise ValueError("La dirección no puede estar vacía.")

    def __str__(self):
        # Mostramos la información del cliente incluyendo su dirección
        return f"[Cliente#{self.id}] {self.nombre} ({self.email}) | Dirección: {self.direccion}"


class Administrador(Usuario):
    # Definimos un administrador que hereda de Usuario
    def __init__(self, nombre, email):
        # Llamamos al constructor de Usuario
        super().__init__(nombre, email)

    def is_admin(self):
        # Un administrador siempre es admin
        return True

    def __str__(self):
        # Mostramos la información del administrador
        return f"[Admin#{self.id}] {self.nombre} ({self.email})"
