"""
Probar el generador de recetas
"""

from productos import CatalogoProductos
from calculos import CalculadoraCBD
from receta import generar_receta_texto, generar_receta_html

# Crear una pauta de ejemplo
catalogo = CatalogoProductos()
producto = catalogo.get_producto("Xpectra 10")
calculadora = CalculadoraCBD(producto)

peso = 70
dosis_por_kg = 5.0
pauta = calculadora.calcular_pauta_completa(peso, dosis_por_kg)
pauta['paciente_nombre'] = "Juan Pérez"

# Generar receta en texto
print("=" * 80)
print("RECETA EN TEXTO")
print("=" * 80)
receta_texto = generar_receta_texto(
    pauta,
    observaciones="Iniciar con dosis baja. Evaluar respuesta en 2 semanas.",
    producto_recetado="Xpectra 10"
)
print(receta_texto)

# Generar receta en HTML
print("\n" + "=" * 80)
print("RECETA EN HTML (vista previa)")
print("=" * 80)
receta_html = generar_receta_html(
    pauta,
    observaciones="Iniciar con dosis baja. Evaluar respuesta en 2 semanas."
)
print("HTML generado correctamente. Revisar en navegador.")
print(receta_html[:500] + "...")

# Guardar HTML para ver en navegador
with open("receta_ejemplo.html", "w", encoding="utf-8") as f:
    f.write(receta_html)
print("\n✅ Receta HTML guardada en 'receta_ejemplo.html'")
print("   Abre este archivo en tu navegador para ver el resultado.")
