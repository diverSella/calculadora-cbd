"""
Calculadora de Dosis de CBD - Greenmed
Aplicación para profesionales de la salud
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from productos import CatalogoProductos
from calculos import CalculadoraCBD, validar_dosis
from receta import generar_receta_html
from exportar_pdf import generar_pdf_bytes

# Configuración de la página
st.set_page_config(
    page_title="Calculadora CBD - Greenmed",
    page_icon="💊",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 10px 0;
        border-bottom: 2px solid #2E7D32;
        margin-bottom: 20px;
    }
    .main-header img {
        max-height: 60px;
    }
    .main-header h1 {
        color: #2E7D32;
        margin: 0;
        font-size: 2rem;
    }
    .main-header .subtitle {
        color: #666;
        font-size: 1rem;
        margin: 0;
    }
    .highlight-product {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        margin-bottom: 20px;
        text-align: center;
    }
    .highlight-product .producto-nombre {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2E7D32;
        margin: 0;
    }
    .highlight-product .producto-dosis {
        font-size: 1.4rem;
        color: #333;
        margin: 10px 0 0 0;
    }
    .highlight-product .producto-detalle {
        font-size: 1rem;
        color: #666;
        margin: 5px 0 0 0;
    }
    .footer {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        padding-top: 20px;
        border-top: 1px solid #ddd;
        margin-top: 30px;
    }
    .equivalencia-resaltada {
        background-color: #fff3e0;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #FF9800;
        margin-top: 10px;
    }
    .product-image-container {
        text-align: center;
        padding: 10px;
        background: #f5f5f5;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .product-image-container img {
        max-width: 100%;
        max-height: 150px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Función para mostrar imágenes con manejo de errores
def mostrar_imagen_producto(nombre_archivo, caption):
    """Intenta mostrar una imagen, si falla muestra un placeholder"""
    try:
        if nombre_archivo in ["Logo empresa.JPG", "logo-greenmed.png"]:
            st.image(f"assets/images/{nombre_archivo}", width=80)
        else:
            st.image(f"assets/images/{nombre_archivo}", caption=caption, use_container_width=True)
    except:
        # Fallback: mostrar emoji
        if "Xpectra" in caption:
            st.markdown("""
            <div style="text-align: center; padding: 10px; background: #f5f5f5; border-radius: 10px; margin-bottom: 15px;">
                <p style="font-size: 3rem; margin: 0;">💊</p>
                <p style="margin: 5px 0 0 0; font-weight: bold;">Xpectra 10</p>
            </div>
            """, unsafe_allow_html=True)
        elif "Xatiplex" in caption:
            st.markdown("""
            <div style="text-align: center; padding: 10px; background: #f5f5f5; border-radius: 10px; margin-bottom: 15px;">
                <p style="font-size: 3rem; margin: 0;">💉</p>
                <p style="margin: 5px 0 0 0; font-weight: bold;">Xatiplex</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 10px; background: #f5f5f5; border-radius: 10px; margin-bottom: 15px;">
                <p style="font-size: 2rem; margin: 0;">🌿</p>
                <p style="margin: 5px 0 0 0; font-weight: bold;">Greenmed</p>
            </div>
            """, unsafe_allow_html=True)

# Logo y título en cabecera
col_logo, col_title = st.columns([1, 5])
with col_logo:
    try:
        st.image("assets/images/Logo empresa.JPG", width=80)
    except:
        st.markdown("🌿")
with col_title:
    st.markdown("""
    <div class="main-header">
        <div>
            <h1>Calculadora de Dosis de CBD</h1>
            <p class="subtitle">Laboratorios Greenmed - Basado en prospecto de Xpectra/Xatiplex</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Inicializar catálogo
catalogo = CatalogoProductos()

# Inicializar variables en session_state
if 'dosis_personalizada' not in st.session_state:
    st.session_state.dosis_personalizada = 5.0
if 'observaciones' not in st.session_state:
    st.session_state.observaciones = ""
if 'receta_generada' not in st.session_state:
    st.session_state.receta_generada = False
if 'receta_html' not in st.session_state:
    st.session_state.receta_html = ""

# Sidebar - Datos del paciente
with st.sidebar:
    st.header("Datos del Paciente")
    
    paciente_nombre = st.text_input("Nombre del paciente", placeholder="Ej: Juan Pérez")
    peso = st.number_input(
        "Peso (kg)",
        min_value=0.5,
        max_value=300.0,
        value=70.0,
        step=0.5,
        help="Ingrese el peso del paciente en kilogramos"
    )
    
    st.divider()
    
    st.subheader("Producto Greenmed")
    producto_nombre = st.selectbox(
        "Seleccione el producto",
        catalogo.listar_productos()
    )
    
    producto = catalogo.get_producto(producto_nombre)
    
    if producto:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Concentración", f"{producto.concentracion}%")
        with col2:
            st.metric("Presentación", producto.presentacion)
        
        st.info(f"**Descripción:** {producto.descripcion}")
    
    st.divider()
    
    st.subheader("Configuración")
    tomas_por_dia = st.selectbox(
        "Tomas por día",
        [1, 2, 3, 4],
        index=1,
        help="Número de administraciones diarias"
    )

# Área principal - Pestañas
tab1, tab2, tab3 = st.tabs(["Calculadora de Dosis", "Tabla de Equivalencias", "Receta Médica"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Selección de Dosis")
        
        dosis_tipo = st.radio(
            "Tipo de dosis",
            ["Dosis estándar (Epidiolex)", "Dosis personalizada"],
            horizontal=True
        )
        
        if dosis_tipo == "Dosis estándar (Epidiolex)":
            dosis_por_kg = st.select_slider(
                "Dosis (mg/kg/día)",
                options=[2.5, 5.0, 10.0, 15.0, 20.0],
                value=5.0
            )
            
            st.info("""
            **Rango terapéutico Epidiolex:**
            - Dosis inicial: 2.5 mg/kg/día
            - Dosis de mantenimiento: 5-10 mg/kg/día
            - Dosis máxima: 20 mg/kg/día
            """)
        else:
            st.markdown("**Dosis rápidas:**")
            col_rapidas = st.columns(5)
            
            dosis_rapidas = [2.5, 5.0, 10.0, 15.0, 20.0]
            for i, dosis in enumerate(dosis_rapidas):
                with col_rapidas[i]:
                    if st.button(f"{dosis} mg/kg", key=f"dosis_{dosis}"):
                        st.session_state.dosis_personalizada = float(dosis)
                        st.rerun()
            
            dosis_por_kg = st.number_input(
                "Dosis personalizada (mg/kg/día)",
                min_value=0.5,
                max_value=30.0,
                value=st.session_state.dosis_personalizada,
                step=0.5,
                help="Ingrese la dosis en mg/kg/día según su criterio clínico",
                key="dosis_input"
            )
            st.session_state.dosis_personalizada = float(dosis_por_kg)
    
    with col2:
        st.header("Producto seleccionado")
        
        if producto:
            # Mostrar foto del producto según selección
            if "Xpectra" in producto_nombre:
                mostrar_imagen_producto("Xpectra_10.webp", "Xpectra 10")
            else:
                mostrar_imagen_producto("xatiplex_5.webp", "Xatiplex")
            
            calculadora = CalculadoraCBD(producto)
            st.metric("CBD por ml", f"{calculadora.mg_por_ml:.2f} mg")
            
            if calculadora.mg_por_gota:
                st.metric("CBD por gota", f"{calculadora.mg_por_gota:.3f} mg")
                st.metric("Gotas por ml", f"{producto.gotas_por_ml} gotas")
            else:
                st.info("Administración con jeringa - No aplican gotas")
    
    # Calcular y mostrar resultados
    if peso > 0 and producto:
        st.divider()
        
        es_valido, mensaje_validacion = validar_dosis(dosis_por_kg, peso)
        
        if not es_valido:
            st.error(f"⚠️ {mensaje_validacion}")
        else:
            st.success(f"✅ {mensaje_validacion}")
        
        calculadora = CalculadoraCBD(producto)
        pauta = calculadora.calcular_pauta_completa(peso, dosis_por_kg)
        
        st.header("Pauta de Administración")
        
        # ============================================
        # RECUADRO VERDE - Mensaje principal
        # ============================================
        tiene_gotas = "dosis_por_toma_gotas" in pauta
        
        # Construir el mensaje principal
        if tiene_gotas:
            mensaje_dosis = f"{pauta['dosis_por_toma_gotas']:.1f} gotas"
        else:
            mensaje_dosis = f"{pauta['dosis_por_toma_ml']:.3f} ml"
        
        # Texto de frecuencia
        if tomas_por_dia == 1:
            frecuencia = "una vez al día"
        elif tomas_por_dia == 2:
            frecuencia = "dos veces al día (cada 12 horas)"
        elif tomas_por_dia == 3:
            frecuencia = "tres veces al día (cada 8 horas)"
        else:
            frecuencia = f"{tomas_por_dia} veces al día"
        
        st.markdown(f"""
        <div class="highlight-product">
            <p class="producto-nombre">✅ {pauta['producto']} ({pauta['concentracion']}%)</p>
            <p class="producto-dosis">{mensaje_dosis} {frecuencia}</p>
            <p class="producto-detalle">Presentación: {pauta['presentacion']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ============================================
        # INFORMACIÓN DETALLADA (debajo del recuadro)
        # ============================================
        st.subheader("Detalles de la Dosis")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Dosis por kg",
                f"{pauta['dosis_por_kg']:.1f} mg/kg/día",
                help="Dosis basada en el peso del paciente"
            )
        with col2:
            st.metric(
                "Dosis diaria total",
                f"{pauta['dosis_diaria_mg']:.1f} mg",
                help="Cantidad total de CBD por día"
            )
        with col3:
            st.metric(
                "Dosis por toma",
                f"{pauta['dosis_por_toma_mg']:.2f} mg",
                help=f"{tomas_por_dia} veces al día"
            )
        
        # Mostrar Administración
        st.subheader("Detalles de Administración")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Volumen por toma",
                f"{pauta['dosis_por_toma_ml']:.3f} ml",
                help="Volumen en ml por administración"
            )
        with col2:
            if tiene_gotas:
                st.metric(
                    "Gotas por toma",
                    f"{pauta['dosis_por_toma_gotas']:.1f} gotas",
                    help="Si usa Xpectra 10 (gotero)"
                )
            else:
                st.metric(
                    "Volumen por toma",
                    f"{pauta['dosis_por_toma_ml']:.3f} ml",
                    help="Si usa Xatiplex (jeringa)"
                )
        with col3:
            st.metric(
                "Tomas por día",
                f"{tomas_por_dia} veces",
                help=f"Cada {24/tomas_por_dia:.0f} horas"
            )
        
        # ============================================
        # TABLA DE EQUIVALENCIAS - CALCULADA DINÁMICAMENTE
        # ============================================
        st.divider()
        st.subheader("Equivalencias para esta dosis")
        st.markdown("Si el paciente no puede comprar el producto seleccionado, estas son las dosis equivalentes con otros productos:")
        
        # Obtener la dosis por toma en mg
        mg_por_toma = pauta['dosis_por_toma_mg']
        
        # Crear diccionario con todos los productos y sus equivalencias
        productos_equivalencias = {}
        
        # Xpectra 10
        xpectra = catalogo.get_producto("Xpectra 10")
        calc_xpectra = CalculadoraCBD(xpectra)
        gotas_xpectra = calc_xpectra.convertir_a_gotas(mg_por_toma)
        if gotas_xpectra:
            productos_equivalencias["Xpectra 10"] = f"{gotas_xpectra:.1f} gotas"
        else:
            productos_equivalencias["Xpectra 10"] = f"{calc_xpectra.convertir_a_ml(mg_por_toma):.3f} ml"
        
        # Xatiplex 5
        xatiplex_5 = catalogo.get_producto("Xatiplex 5")
        calc_5 = CalculadoraCBD(xatiplex_5)
        productos_equivalencias["Xatiplex 5"] = f"{calc_5.convertir_a_ml(mg_por_toma):.3f} ml"
        
        # Xatiplex 10
        xatiplex_10 = catalogo.get_producto("Xatiplex 10")
        calc_10 = CalculadoraCBD(xatiplex_10)
        productos_equivalencias["Xatiplex 10"] = f"{calc_10.convertir_a_ml(mg_por_toma):.3f} ml"
        
        # Xatiplex 15
        xatiplex_15 = catalogo.get_producto("Xatiplex 15")
        calc_15 = CalculadoraCBD(xatiplex_15)
        productos_equivalencias["Xatiplex 15"] = f"{calc_15.convertir_a_ml(mg_por_toma):.3f} ml"
        
        # Xatiplex 20
        xatiplex_20 = catalogo.get_producto("Xatiplex 20")
        calc_20 = CalculadoraCBD(xatiplex_20)
        productos_equivalencias["Xatiplex 20"] = f"{calc_20.convertir_a_ml(mg_por_toma):.3f} ml"
        
        # Crear DataFrame
        df_equivalencias = pd.DataFrame({
            "Producto": list(productos_equivalencias.keys()),
            "Cantidad por toma": list(productos_equivalencias.values())
        })
        
        # Mostrar tabla
        st.dataframe(
            df_equivalencias,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Producto": st.column_config.TextColumn("Producto", width="medium"),
                "Cantidad por toma": st.column_config.TextColumn("Cantidad por toma", width="medium")
            }
        )
        
        # Resaltar el producto seleccionado
        producto_seleccionado = pauta['producto']
        cantidad_seleccionada = productos_equivalencias[producto_seleccionado]
        st.markdown(f"""
        <div class="equivalencia-resaltada">
            <strong>✅ Producto seleccionado:</strong> {producto_seleccionado} 
            <span style="color: #FF9800;">➡️</span> 
            <strong>{cantidad_seleccionada}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Recomendaciones
        st.divider()
        st.subheader("Recomendaciones Importantes")
        
        col_adv1, col_adv2 = st.columns(2)
        
        with col_adv1:
            st.markdown("""
            **Titulación:**
            - Iniciar con dosis baja (2.5 mg/kg/día)
            - Aumentar gradualmente según tolerancia
            - Evaluar respuesta clínica semanalmente
            """)
        
        with col_adv2:
            st.markdown("""
            **Monitorización:**
            - Función hepática (transaminasas)
            - Interacciones medicamentosas
            - Efectos adversos (somnolencia, diarrea)
            - Ajustar según tolerancia individual
            """)

with tab2:
    st.header("Tabla de Equivalencias")
    st.markdown("""
    Esta tabla muestra la correspondencia entre **gotas de Xpectra 10** y **ml de Xatiplex**.
    Útil para convertir rápidamente entre productos.
    """)
    
    # Mostrar tabla de equivalencias completa
    from comparativa import tabla_equivalencias
    df_equivalencias_completa, gotas = tabla_equivalencias()
    
    st.dataframe(
        df_equivalencias_completa,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Xpectra 10": st.column_config.TextColumn(
                "Xpectra 10 (10%)",
                help="Gotas de Xpectra 10 (32 gotas/ml)"
            ),
            "Xatiplex 5": st.column_config.TextColumn(
                "Xatiplex 5",
                help="ml de Xatiplex 5%"
            ),
            "Xatiplex 10": st.column_config.TextColumn(
                "Xatiplex 10",
                help="ml de Xatiplex 10%"
            ),
            "Xatiplex 15": st.column_config.TextColumn(
                "Xatiplex 15",
                help="ml de Xatiplex 15%"
            ),
            "Xatiplex 20": st.column_config.TextColumn(
                "Xatiplex 20",
                help="ml de Xatiplex 20%"
            )
        }
    )
    
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Xpectra 10 (Gotero)**
        - 32 gotas = 1 ml
        - Full Spectrum
        - Administración con gotero
        """)
    
    with col2:
        st.markdown("""
        **Xatiplex (Jeringa)**
        - Administración con jeringa
        - Isolado de CBD
        - Mayor precisión en la dosis
        """)

with tab3:
    st.header("Receta Médica")
    st.markdown("""
    Complete los datos del paciente y la dosis en la pestaña **Calculadora de Dosis**,
    luego agregue sus observaciones y genere la receta.
    """)
    
    if peso > 0 and producto:
        calculadora = CalculadoraCBD(producto)
        pauta = calculadora.calcular_pauta_completa(peso, dosis_por_kg)
        pauta['paciente_nombre'] = paciente_nombre if paciente_nombre else "No especificado"
        
        st.subheader("Observaciones")
        observaciones = st.text_area(
            "Escriba aquí sus observaciones, indicaciones adicionales o advertencias:",
            value=st.session_state.observaciones,
            height=100,
            placeholder="Ej: Iniciar con dosis baja. Evaluar respuesta en 2 semanas.",
            key="observaciones_input"
        )
        st.session_state.observaciones = observaciones
        
        if st.button("Generar Receta", type="primary"):
            with st.spinner("Generando receta..."):
                receta_html = generar_receta_html(pauta, observaciones)
                st.session_state.receta_html = receta_html
                st.session_state.receta_generada = True
        
        if st.session_state.get('receta_generada', False):
            st.divider()
            st.subheader("Receta Generada")
            
            st.components.v1.html(
                st.session_state.receta_html,
                height=600,
                scrolling=True
            )
            
            st.divider()
            st.subheader("Exportar")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nombre_limpio = paciente_nombre.replace(' ', '_') if paciente_nombre else "paciente"
                fecha_actual = datetime.now().strftime('%Y%m%d')
                nombre_archivo_html = f"receta_{nombre_limpio}_{fecha_actual}.html"
                
                st.download_button(
                    label="Descargar HTML",
                    data=st.session_state.receta_html,
                    file_name=nombre_archivo_html,
                    mime="text/html",
                    use_container_width=True
                )
            
            with col2:
                try:
                    pdf_bytes = generar_pdf_bytes(st.session_state.receta_html)
                    nombre_archivo_pdf = f"receta_{nombre_limpio}_{fecha_actual}.pdf"
                    
                    st.download_button(
                        label="Descargar PDF",
                        data=pdf_bytes,
                        file_name=nombre_archivo_pdf,
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary"
                    )
                except Exception as e:
                    st.error(f"Error al generar PDF: {e}")
                    st.info("Asegúrate de tener instalado weasyprint")
    else:
        st.warning("Primero complete los datos del paciente y seleccione un producto.")

# Footer
st.markdown("""
<div class="footer">
    <p>⚠️ Esta herramienta es de apoyo para profesionales de la salud.</p>
    <p>La decisión final de prescripción es responsabilidad del médico tratante.</p>
    <p>Greenmed | Basado en prospecto de Xpectra/Xatiplex</p>
</div>
""", unsafe_allow_html=True)
