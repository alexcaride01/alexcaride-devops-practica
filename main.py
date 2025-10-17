from services import TiendaService
from models import ProductoElectronico, ProductoRopa


def main():
    tienda = TiendaService()

    # Registramos usuarios
    cliente1 = tienda.registrar_usuario("cliente", "Alex", "alex@gmail.com", "Calle Manuel Murguía 31")
    cliente2 = tienda.registrar_usuario("cliente", "Luis", "luis@gmail.com", "Calle Ángel Rebollo 60")
    cliente3 = tienda.registrar_usuario("cliente", "Nerea", "nerea@gmail.com", "Calle Ervedelo 40")
    admin1 = tienda.registrar_usuario("admin", "Carlos", "carlos@gmail.com")

    # Añadimos productos
    p1 = ProductoElectronico("Portátil", 800, 5, 24)
    p2 = ProductoElectronico("Auriculares", 50, 10, 12)
    p3 = ProductoRopa("Camiseta", 15, 20, "M", "Rojo")
    p4 = ProductoRopa("Pantalón", 35, 15, "L", "Negro")
    p5 = ProductoRopa("Sudadera", 40, 8, "XL", "Azul")

    for p in [p1, p2, p3, p4, p5]:
        tienda.añadir_producto(p)

    # Listamos el inventario 
    print("\n Inventario inicial:")
    for prod in tienda.listar_productos():
        print(" ", prod)

    # Simulamos pedidos
    print("\n Pedidos realizados:")

    pedido1 = tienda.realizar_pedido(cliente1.id, {p1.id: 1, p3.id: 2})
    print(pedido1, "\n")

    pedido2 = tienda.realizar_pedido(cliente2.id, {p2.id: 2, p4.id: 1})
    print(pedido2, "\n")

    pedido3 = tienda.realizar_pedido(cliente3.id, {p5.id: 1})
    print(pedido3, "\n")

    # Todos los pedidos de un cliente 
    print("\n Todos los pedidos de Alex:")
    pedidos_alex = tienda.listar_pedidos_usuario(cliente1.id)
    for ped in pedidos_alex:
        print(ped, "\n")

        # Inventario tras ventas 
    print("\n Inventario actualizado:")
    for prod in tienda.listar_productos():
        print(" ", prod)


if __name__ == "__main__":
    main()
