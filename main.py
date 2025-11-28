from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict
from uuid import UUID

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

from services import TiendaService
from models import Usuario
from models import Producto, ProductoElectronico, ProductoRopa

# Creamos la instancia de FastAPI
app = FastAPI(title="Tienda Online API")
# Creamos la instancia del servicio de la tienda
tienda_service = TiendaService()

# ---------------------- SCHEMAS ---------------------- #

# ------ USUARIOS ------ #

class UsuarioCreate(BaseModel):
    # Esquema para crear un nuevo usuario
    nombre: str
    email: EmailStr
    tipo: str
    direccion_postal: Optional[str] = None


class UsuarioRead(BaseModel):
    # Esquema para leer/devolver información de un usuario
    id: UUID
    nombre: str
    email: str
    es_admin: bool


# ------ PRODUCTOS ------ #

class ProductoCreate(BaseModel):
    # Esquema para crear un nuevo producto
    tipo: str  # "electronico" o "ropa"
    nombre: str
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)
    # Atributos opcionales según tipo
    garantia_meses: Optional[int] = Field(default=24, ge=0)
    talla: Optional[str] = None
    color: Optional[str] = None


class ProductoRead(BaseModel):
    # Esquema para leer/devolver información de un producto
    id: UUID
    tipo: str
    nombre: str
    precio: float
    stock: int
    # Atributos opcionales
    garantia_meses: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None


# ------ PEDIDOS ------ #

class PedidoItemCreate(BaseModel):
    # Esquema para representar un item/línea al crear un pedido
    producto_id: UUID
    cantidad: int = Field(gt=0)


class PedidoCreate(BaseModel):
    # Esquema para crear un nuevo pedido
    cliente_id: UUID
    items: List[PedidoItemCreate]


class PedidoItemRead(BaseModel):
    # Esquema para leer/devolver información de un item de pedido
    producto_id: UUID
    nombre_producto: str
    cantidad: int
    precio_unitario: float
    subtotal: float


class PedidoRead(BaseModel):
    # Esquema para leer/devolver información completa de un pedido
    id: UUID
    cliente_id: UUID
    nombre_cliente: str
    fecha: datetime
    items: List[PedidoItemRead]
    total: float


# ---------------------- ENDPOINTS ---------------------- #

# ------ USUARIOS ------ #

@app.post("/usuarios", response_model=UsuarioRead, status_code=201)
def crear_usuario(datos: UsuarioCreate) -> UsuarioRead:
    # Endpoint para crear un nuevo usuario
    try:
        # Registramos el usuario usando el servicio
        usuario = tienda_service.registrar_usuario(
            tipo=datos.tipo,
            nombre=datos.nombre,
            email=datos.email,
            direccion=datos.direccion_postal
        )
        # Devolvemos el usuario creado en formato UsuarioRead
        return UsuarioRead(
            id=usuario.id,
            nombre=usuario.nombre,
            email=usuario.email,
            es_admin=usuario.is_admin()
        )
    except ValueError as e:
        # Si hay un error de validación, devolvemos un error 400
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: UUID) -> UsuarioRead:
    # Endpoint para obtener un usuario específico por ID
    try:
        # Obtenemos el usuario del servicio
        usuario = tienda_service.obtener_usuario(usuario_id)
        # Devolvemos el usuario en formato UsuarioRead
        return UsuarioRead(
            id=usuario.id,
            nombre=usuario.nombre,
            email=usuario.email,
            es_admin=usuario.is_admin()
        )
    except ValueError as e:
        # Si no existe, devolvemos un error 404
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/usuarios", response_model=List[UsuarioRead])
def listar_usuarios() -> List[UsuarioRead]:
    # Endpoint para listar todos los usuarios
    # Obtenemos todos los usuarios del servicio
    usuarios = tienda_service.listar_usuarios()
    # Convertimos cada usuario al formato UsuarioRead
    return [
        UsuarioRead(
            id=u.id,
            nombre=u.nombre,
            email=u.email,
            es_admin=u.is_admin()
        )
        for u in usuarios
    ]


# ------ PRODUCTOS ------ #

@app.post("/productos", response_model=ProductoRead, status_code=201)
def crear_producto(datos: ProductoCreate) -> ProductoRead:
    # Endpoint para crear un nuevo producto
    try:
        tipo_lower = datos.tipo.lower()
        
        # Creamos el producto según su tipo
        if tipo_lower == "electronico":
            producto = ProductoElectronico(
                nombre=datos.nombre,
                precio=datos.precio,
                stock=datos.stock,
                garantia_meses=datos.garantia_meses or 24
            )
        elif tipo_lower == "ropa":
            # Validamos que tenga talla y color
            if not datos.talla or not datos.color:
                raise ValueError("Los productos de ropa requieren talla y color.")
            producto = ProductoRopa(
                nombre=datos.nombre,
                precio=datos.precio,
                stock=datos.stock,
                talla=datos.talla,
                color=datos.color
            )
        else:
            raise ValueError("Tipo de producto no válido. Usa 'electronico' o 'ropa'.")
        
        # Añadimos el producto al inventario
        tienda_service.añadir_producto(producto)
        
        # Devolvemos el producto creado en formato ProductoRead
        return ProductoRead(
            id=producto.id,
            tipo=tipo_lower,
            nombre=producto.nombre,
            precio=producto.precio,
            stock=producto.stock,
            garantia_meses=getattr(producto, 'garantia_meses', None),
            talla=getattr(producto, 'talla', None),
            color=getattr(producto, 'color', None)
        )
    except ValueError as e:
        # Si hay un error de validación, devolvemos un error 400
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/productos", response_model=List[ProductoRead])
def listar_productos() -> List[ProductoRead]:
    # Endpoint para listar todos los productos
    # Obtenemos todos los productos del servicio
    productos = tienda_service.listar_productos()
    resultado = []
    
    # Convertimos cada producto al formato ProductoRead
    for p in productos:
        # Determinamos el tipo de producto
        if isinstance(p, ProductoElectronico):
            tipo = "electronico"
        elif isinstance(p, ProductoRopa):
            tipo = "ropa"
        else:
            tipo = "generico"
        
        resultado.append(ProductoRead(
            id=p.id,
            tipo=tipo,
            nombre=p.nombre,
            precio=p.precio,
            stock=p.stock,
            garantia_meses=getattr(p, 'garantia_meses', None),
            talla=getattr(p, 'talla', None),
            color=getattr(p, 'color', None)
        ))
    
    return resultado


@app.get("/productos/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: UUID) -> ProductoRead:
    # Endpoint para obtener un producto específico por ID
    try:
        # Obtenemos el producto del servicio
        p = tienda_service.obtener_producto(producto_id)
        
        # Determinamos el tipo de producto
        if isinstance(p, ProductoElectronico):
            tipo = "electronico"
        elif isinstance(p, ProductoRopa):
            tipo = "ropa"
        else:
            tipo = "generico"
        
        # Devolvemos el producto en formato ProductoRead
        return ProductoRead(
            id=p.id,
            tipo=tipo,
            nombre=p.nombre,
            precio=p.precio,
            stock=p.stock,
            garantia_meses=getattr(p, 'garantia_meses', None),
            talla=getattr(p, 'talla', None),
            color=getattr(p, 'color', None)
        )
    except ValueError as e:
        # Si no existe, devolvemos un error 404
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/productos/{producto_id}", status_code=204)
def eliminar_producto(producto_id: UUID) -> None:
    # Endpoint para eliminar un producto del inventario
    try:
        # Eliminamos el producto usando el servicio
        tienda_service.eliminar_producto(producto_id)
    except ValueError as e:
        # Si no existe, devolvemos un error 404
        raise HTTPException(status_code=404, detail=str(e))


# ------ PEDIDOS ------ #

@app.post("/pedidos", response_model=PedidoRead, status_code=201)
def crear_pedido(datos: PedidoCreate) -> PedidoRead:
    # Endpoint para crear un nuevo pedido
    try:
        # Convertimos la lista de items a un diccionario
        items_dict: Dict[UUID, int] = {item.producto_id: item.cantidad for item in datos.items}
        # Creamos el pedido usando el servicio
        pedido = tienda_service.realizar_pedido(datos.cliente_id, items_dict)
        
        # Construimos la lista de items para la respuesta
        items_read = []
        for producto, cantidad in pedido.productos_cantidades.items():
            items_read.append(PedidoItemRead(
                producto_id=producto.id,
                nombre_producto=producto.nombre,
                cantidad=cantidad,
                precio_unitario=producto.precio,
                subtotal=producto.precio * cantidad
            ))
        
        # Devolvemos el pedido creado en formato PedidoRead
        return PedidoRead(
            id=pedido.id,
            cliente_id=pedido.cliente.id,
            nombre_cliente=pedido.cliente.nombre,
            fecha=pedido.fecha,
            items=items_read,
            total=pedido.calcular_total()
        )
    except ValueError as e:
        # Si hay un error de validación, devolvemos un error 400
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/usuarios/{cliente_id}/pedidos", response_model=List[PedidoRead])
def listar_pedidos_cliente(cliente_id: UUID) -> List[PedidoRead]:
    # Endpoint para listar todos los pedidos de un cliente
    try:
        # Verificamos que el usuario existe
        tienda_service.obtener_usuario(cliente_id)
        # Obtenemos todos los pedidos del cliente
        pedidos = tienda_service.listar_pedidos_usuario(cliente_id)
        
        resultado = []
        # Convertimos cada pedido al formato PedidoRead
        for pedido in pedidos:
            items_read = []
            for producto, cantidad in pedido.productos_cantidades.items():
                items_read.append(PedidoItemRead(
                    producto_id=producto.id,
                    nombre_producto=producto.nombre,
                    cantidad=cantidad,
                    precio_unitario=producto.precio,
                    subtotal=producto.precio * cantidad
                ))
            
            resultado.append(PedidoRead(
                id=pedido.id,
                cliente_id=pedido.cliente.id,
                nombre_cliente=pedido.cliente.nombre,
                fecha=pedido.fecha,
                items=items_read,
                total=pedido.calcular_total()
            ))
        
        return resultado
    except ValueError as e:
        # Si no existe el usuario, devolvemos un error 404
        raise HTTPException(status_code=404, detail=str(e))
