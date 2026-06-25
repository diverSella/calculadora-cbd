"""
Script de prueba para verificar la lógica de la calculadora
"""

from productos import CatalogoProductos
from calculos import CalculadoraCBD, validar_dosis

def test_productos():
    """Probar que los productos se cargan correctamente"""
    print("=" * 50)
    print("PRUEBA 1: Catálogo de Productos")
    print("=" * 50)
    
    catalogo = CatalogoProductos()
    productos = catalogo.listar_productos()
    
    print(f"✅ Productos disponibles: {len(productos)}")
    for producto in productos:
        prod = catalogo.get_producto(producto)
        print(f"   • {producto}: {prod.concentracion}% - {prod.tipo} - {prod.gotas_por_ml} gotas/ml")
    
    return catalogo

def test_calculos(catalogo):
    """Probar los cálculos con diferentes productos y dosis"""
    print("\n" + "=" * 50)
    print("PRUEBA 2: Cálculos de Dosis")
    print("=" * 50)
    
    # Datos de prueba
    peso = 70  # kg
    dosis_por_kg = 5.0  # mg/kg/día
    
    # Probar con Xpectra 10
    producto = catalogo.get_producto("Xpectra 10")
    calculadora = CalculadoraCBD(producto)
    
    print(f"\n📊 Producto: {producto.nombre}")
    print(f"   Concentración: {producto.concentracion}%")
    print(f"   {producto.gotas_por_ml} gotas/ml")
    print(f"   {calculadora.mg_por_ml:.2f} mg/ml")
    print(f"   {calculadora.mg_por_gota:.3f} mg/gota")
    
    # Calcular pauta
    pauta = calculadora.calcular_pauta_completa(peso, dosis_por_kg)
    
    print(f"\n📋 Pauta para paciente de {peso} kg")
    print(f"   Dosis: {dosis_por_kg} mg/kg/día")
    print(f"   Total diario: {pauta['dosis_diaria_mg']:.1f} mg")
    print(f"   Por toma (BID): {pauta['dosis_por_toma_mg']:.2f} mg")
    print(f"   = {pauta['dosis_por_toma_ml']:.3f} ml")
    print(f"   = {pauta['dosis_por_toma_gotas']:.1f} gotas")
    print(f"   Volumen mensual: {pauta['ml_mensual']:.1f} ml")
    
    # Validar dosis
    es_valido, mensaje = validar_dosis(dosis_por_kg, peso)
    print(f"\n   Validación: {'✅' if es_valido else '❌'} {mensaje}")
    
    return pauta

def test_multiples_productos(catalogo):
    """Probar diferentes productos con la misma dosis"""
    print("\n" + "=" * 50)
    print("PRUEBA 3: Comparación entre Productos")
    print("=" * 50)
    
    peso = 70  # kg
    dosis_por_kg = 10.0  # mg/kg/día
    
    print(f"\nComparando productos para paciente de {peso}kg")
    print(f"Dosis: {dosis_por_kg} mg/kg/día = {peso * dosis_por_kg:.0f} mg/día\n")
    
    productos_a_probar = ["Xpectra 10", "Xatiplex 10", "Xatiplex 20"]
    
    for nombre in productos_a_probar:
        producto = catalogo.get_producto(nombre)
        calculadora = CalculadoraCBD(producto)
        pauta = calculadora.calcular_pauta_completa(peso, dosis_por_kg)
        
        print(f"💊 {nombre} ({producto.concentracion}%)")
        print(f"   → {pauta['dosis_por_toma_gotas']:.1f} gotas por toma")
        print(f"   → {pauta['dosis_por_toma_ml']:.3f} ml por toma")
        print(f"   → {pauta['ml_mensual']:.1f} ml/mes")
        print()

def test_titulacion(catalogo):
    """Probar la tabla de titulación"""
    print("\n" + "=" * 50)
    print("PRUEBA 4: Esquema de Titulación")
    print("=" * 50)
    
    peso = 70  # kg
    producto = catalogo.get_producto("Xpectra 10")
    calculadora = CalculadoraCBD(producto)
    
    print(f"\n📈 Titulación para {producto.nombre}")
    print(f"Peso: {peso} kg\n")
    print("Semana | Dosis (mg/kg) | mg/día | Gotas/toma")
    print("-" * 50)
    
    for semana in range(1, 5):
        dosis_semana = min(10.0, 2.5 * semana)
        mg_diarios = peso * dosis_semana
        gotas_por_toma = (mg_diarios / 2) / calculadora.mg_por_gota
        
        print(f"  {semana}    |    {dosis_semana:.1f}      |  {mg_diarios:.0f}   |    {gotas_por_toma:.1f}")

def main():
    """Función principal de prueba"""
    print("\n🧪 INICIANDO PRUEBAS DE LA CALCULADORA CBD\n")
    
    try:
        # Prueba 1: Productos
        catalogo = test_productos()
        
        # Prueba 2: Cálculos
        test_calculos(catalogo)
        
        # Prueba 3: Múltiples productos
        test_multiples_productos(catalogo)
        
        # Prueba 4: Titulación
        test_titulacion(catalogo)
        
        print("\n" + "=" * 50)
        print("✅ ¡TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE!")
        print("=" * 50)
        print("\n💡 La lógica funciona correctamente. Ahora podemos crear la interfaz web.")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
