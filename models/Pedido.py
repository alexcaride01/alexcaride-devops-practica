from __future__ import annotations
from datetime import datetime   # Importamos datetime para registrar la fecha y hora del pedido
from uuid import uuid4, UUID
from typing import Dict


class Pedido:
    # Usamos UUID en lugar de contador incremental para asignar IDs únicos
    
    def __init__(self, cliente, productos_cantidades):
        # Asignamos un ID único al pedido usando UUID4
        self.id = uuid4()
        
        # Guardamos el cliente que hace el pedido
        self.cliente = cliente
        # Guardamos un diccionario con los productos y sus cantidades
        self.productos_cantidades = productos_cantidades
        # Registramos la fecha y hora en que se realiza el pedido
        self.fecha = datetime.now()
    
    def calcular_total(self):
        # Calculamos el importe total del pedido multiplicando precio por cantidad
        total = 0.0
        for producto, cantidad in self.productos_cantidades.items():
            total += producto.precio * cantidad
        return total
    
    def __str__(self):
        # Generamos una representación en texto del pedido
        lineas = [f"Pedido #{self.id} - Cliente: {self.cliente.nombre} - Fecha: {self.fecha}"]
        # Añadimos al texto cada producto con su cantidad y subtotal
        for producto, cantidad in self.productos_cantidades.items():
            lineas.append(f"  - {producto.nombre} x {cantidad} = {producto.precio * cantidad:.2f}€")
        # Añadimos el total al final
        lineas.append(f"TOTAL: {self.calcular_total():.2f}€")
        return "\n".join(lineas)
