from models import Producto, ProductoElectronico, ProductoRopa
from models import Usuario, Cliente, Administrador, Pedido


class TiendaService:
    # Definimos el servicio central de gestión de la tienda online
    def __init__(self):
        # Creamos un diccionario para almacenar los usuarios por id
        self.usuarios = {}
        # Creamos un diccionario para almacenar los productos por id
        self.productos = {}
        # Creamos un diccionario para almacenar los pedidos por id
        self.pedidos = {}

    # USUARIOS 
    def registrar_usuario(self, tipo, nombre, email, direccion=None):
        # Registramos un nuevo usuario de tipo cliente o administrador
        if tipo.lower() == "cliente":
            # Validamos que el cliente tenga dirección
            if not direccion:
                raise ValueError("El cliente debe tener dirección postal.")
            usuario = Cliente(nombre, email, direccion)
        elif tipo.lower() in ("admin", "administrador"):
            usuario = Administrador(nombre, email)
        else:
            raise ValueError("Tipo de usuario no válido. Usa 'cliente' o 'admin'.")

        # Guardamos el usuario en el diccionario
        self.usuarios[usuario.id] = usuario
        return usuario

    def obtener_usuario(self, usuario_id):
        # Obtenemos un usuario por id o None si no existe
        return self.usuarios.get(usuario_id)

    # PRODUCTOS 
    def añadir_producto(self, producto):
        # Añadimos un producto al inventario
        self.productos[producto.id] = producto

    def eliminar_producto(self, producto_id):
        # Eliminamos un producto del inventario si existe
        if producto_id in self.productos:
            del self.productos[producto_id]
        else:
            raise ValueError("Producto no encontrado.")

    def listar_productos(self):
        # Devolvemos la lista de productos del inventario
        return list(self.productos.values())

    # PEDIDOS 
    def realizar_pedido(self, cliente_id, items):
        # Creamos un pedido de un cliente verificando stock
        cliente = self.usuarios.get(cliente_id)
        if not cliente or not isinstance(cliente, Cliente):
            raise ValueError("El usuario debe existir y ser un cliente.")

        # Preparamos un diccionario con los productos y cantidades del pedido
        productos_cantidades = {}
        for producto_id, cantidad in items.items():
            producto = self.productos.get(producto_id)
            if not producto:
                raise ValueError(f"Producto con id {producto_id} no encontrado.")
            if not producto.hay_stock(cantidad):
                raise ValueError(f"No hay stock suficiente para {producto.nombre}.")
            productos_cantidades[producto] = cantidad

        # Descontamos el stock de los productos vendidos
        for producto, cantidad in productos_cantidades.items():
            producto.actualizar_stock(-cantidad)

        # Creamos el pedido y lo guardamos
        pedido = Pedido(cliente, productos_cantidades)
        self.pedidos[pedido.id] = pedido
        return pedido

    def listar_pedidos_usuario(self, usuario_id):
        # Devolvemos todos los pedidos de un usuario por orden de fecha
        return [p for p in self.pedidos.values() if p.cliente.id == usuario_id]
