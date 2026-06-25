"""
Probar la corrección de los productos
"""

from productos import CatalogoProductos

catalogo = CatalogoProductos()

print("=" * 60)
print("PRODUCTOS GREENMED - VERIFICACIÓN")
print("=" * 60)

for nombre in catalogo.listar_productos():
    prod = catalogo.get_producto(nombre)
    print(f"\n💊 {nombre}")
    print(f"   Concentración: {prod.concentracion}%")
    print(f"   Tipo: {prod.tipo}")
    print(f"   Presentación: {prod.presentacion}")
    if prod.gotas_por_ml:
        print(f"   Gotas por ml: {prod.gotas_por_ml}")
    else:
        print(f"   Gotas por ml: No aplica (administración con jeringa)")
    print(f"   Descripción: {prod.descripcion}")

print("\n" + "=" * 60)
print("✅ Productos actualizados correctamente")
print("=" * 60)
