"""
Base de datos de productos Greenmed
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Producto:
    """Clase para representar un producto de CBD"""
    nombre: str
    concentracion: float  # Porcentaje de CBD
    tipo: str  # "Full Spectrum" o "Isolado"
    presentacion: str  # "Gotero" o "Jeringa"
    gotas_por_ml: Optional[int] = None  # Solo para goteros
    volumenes_disponibles: List[int] = None  # Volúmenes en mL (ej: [10, 30])
    descripcion: str = ""

class CatalogoProductos:
    """Catálogo de productos Greenmed"""
    
    def __init__(self):
        self.productos: Dict[str, Producto] = {
            "Xpectra 10": Producto(
                nombre="Xpectra 10",
                concentracion=10.0,
                tipo="Full Spectrum",
                presentacion="Gotero",
                gotas_por_ml=32,
                volumenes_disponibles=[10, 30],
                descripcion="CBD al 10% en base a resina full spectrum - Administración con gotero"
            ),
            "Xatiplex 5": Producto(
                nombre="Xatiplex 5",
                concentracion=5.0,
                tipo="Isolado",
                presentacion="Jeringa",
                gotas_por_ml=None,
                volumenes_disponibles=[10, 30],
                descripcion="CBD al 5% en base a isolado - Administración con jeringa"
            ),
            "Xatiplex 10": Producto(
                nombre="Xatiplex 10",
                concentracion=10.0,
                tipo="Isolado",
                presentacion="Jeringa",
                gotas_por_ml=None,
                volumenes_disponibles=[10, 30],
                descripcion="CBD al 10% en base a isolado - Administración con jeringa"
            ),
            "Xatiplex 15": Producto(
                nombre="Xatiplex 15",
                concentracion=15.0,
                tipo="Isolado",
                presentacion="Jeringa",
                gotas_por_ml=None,
                volumenes_disponibles=[10, 30],
                descripcion="CBD al 15% en base a isolado - Administración con jeringa"
            ),
            "Xatiplex 20": Producto(
                nombre="Xatiplex 20",
                concentracion=20.0,
                tipo="Isolado",
                presentacion="Jeringa",
                gotas_por_ml=None,
                volumenes_disponibles=[10, 30],
                descripcion="CBD al 20% en base a isolado - Administración con jeringa"
            )
        }
    
    def get_producto(self, nombre: str) -> Optional[Producto]:
        """Obtener un producto por su nombre"""
        return self.productos.get(nombre)
    
    def listar_productos(self) -> List[str]:
        """Listar todos los nombres de productos"""
        return list(self.productos.keys())
    
    def get_productos_por_presentacion(self, presentacion: str) -> List[str]:
        """Obtener productos filtrados por presentación"""
        return [
            nombre for nombre, prod in self.productos.items()
            if prod.presentacion == presentacion
        ]
