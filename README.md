# Sistema de Gestión de Tienda Online

Proyecto correspondiente a la Práctica 1.3, que implementa una primera versión en consola de una tienda online usando Python y POO. El sistema permite gestionar productos, usuarios y pedidos mediante una estructura modular preparada para ampliarse en futuras prácticas.

## Descripción general

El programa permite registrar usuarios, añadir productos al inventario, verificar stock, realizar pedidos y consultar el historial de compras de un cliente. Toda la lógica se organiza mediante clases independientes y un servicio central que coordina las operaciones.

## Estructura del proyecto

- models/: Clases del dominio (Producto, ProductoElectronico, ProductoRopa, Usuario, Cliente, Administrador, Pedido).
- services/: Contiene TiendaService, encargado de gestionar usuarios, productos y pedidos.
- main.py: Simula el flujo completo del sistema (creación de usuarios, productos, pedidos e inventario actualizado).

## Clases principales

- Producto y subclases: definen los artículos de la tienda (garantía, talla y color).

- Usuario y subclases: clientes con dirección postal y administradores.

- Pedido: agrupa productos y cantidades, calcula el total y almacena la fecha.

- TiendaService: registra usuarios, gestiona inventario y crea pedidos comprobando stock.