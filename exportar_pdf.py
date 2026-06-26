"""
Módulo para exportar recetas a PDF
"""

from weasyprint import HTML
from datetime import datetime
import io

def generar_pdf_bytes(html_content: str) -> bytes:
    """
    Genera PDF en memoria (bytes) para descarga directa
    
    Args:
        html_content: Contenido HTML de la receta
    
    Returns:
        Bytes del archivo PDF
    """
    try:
        # Generar PDF con configuración optimizada
        pdf_bytes = HTML(string=html_content).write_pdf(
            presentational_hints=True,
            optimize_size=('fonts', 'images')
        )
        return pdf_bytes
    except Exception as e:
        # Si falla, devolver un mensaje de error
        raise Exception(f"Error generando PDF: {str(e)}")
