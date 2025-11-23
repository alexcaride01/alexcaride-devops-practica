from __future__ import annotations
from uuid import uuid4, UUID


class Producto:
    def __init__(self, nombre, precio, stock):
        # Generamos un identificador único para cada producto
        self.id = uuid4()
        # Guardamos el nombre del producto eliminando espacios sobrantes
        self.nombre = nombre.strip()
        # Guardamos el precio
        self.precio = precio
        # Guardamos el stock inicial
        self.stock = stock
        
        # Validamos que el precio no sea negativo
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        # Validamos que el stock no sea negativo
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        # Validamos que el nombre no esté vacío
        if not self.nombre:
            raise ValueError("El nombre no puede estar vacío.")
    
    def hay_stock(self, cantidad):
        # Comprobamos si tenemos suficientes unidades disponibles
        return cantidad > 0 and self.stock >= cantidad
    
    def actualizar_stock(self, delta):
        # Calculamos el nuevo stock tras aplicar el cambio
        nuevo_stock = self.stock + delta
        # Validamos que no se quede en negativo
        if nuevo_stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        # Actualizamos el stock
        self.stock = nuevo_stock
    
    def __str__(self):
        # Devolvemos una representación en texto del producto
        return f"[Producto#{self.id}] {self.nombre} - {self.precio:.2f}€ (stock: {self.stock})"


class ProductoElectronico(Producto):
    def __init__(self, nombre, precio, stock, garantia_meses=24):
        # Llamamos al constructor de la clase padre Producto
        super().__init__(nombre, precio, stock)
        # Validamos que la garantía no sea negativa
        if garantia_meses < 0:
            raise ValueError("La garantía no puede ser negativa.")
        # Guardamos la garantía en meses
        self.garantia_meses = garantia_meses
    
    def __str__(self):
        # Mostramos también la garantía en la representación del producto
        return super().__str__() + f" | garantía: {self.garantia_meses} meses"


class ProductoRopa(Producto):
    def __init__(self, nombre, precio, stock, talla, color):
        # Llamamos al constructor de la clase padre Producto
        super().__init__(nombre, precio, stock)
        # Validamos que la talla no esté vacía
        if not talla.strip():
            raise ValueError("La talla no puede estar vacía.")
        # Validamos que el color no esté vacío
        if not color.strip():
            raise ValueError("El color no puede estar vacío.")
        # Guardamos la talla
        self.talla = talla.strip()
        # Guardamos el color
        self.color = color.strip()
    
    def __str__(self):
        # Mostramos también la talla y el color en la representación del producto
        return super().__str__() + f" | talla: {self.talla}, color: {self.color}"
