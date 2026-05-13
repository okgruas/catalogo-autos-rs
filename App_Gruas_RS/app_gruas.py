import streamlit as st
import urllib.parse
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="OKGRUAS RS - Solicitud", page_icon="🚛", layout="centered")

# 2. ESTILO VISUAL "BLINDADO" (Negro, Verde Neón y Limpieza de Interfaz)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    /* FORZAR FONDO NEGRO ABSOLUTO */
    .stApp {
        background-color: #000000 !important;
    }

    /* ELIMINAR MENÚS, CORONA, MARCA DE AGUA Y BARRAS DE STREAMLIT */
    header, footer, .stAppDeployButton, #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* BLOQUEO ESPECÍFICO DE ICONOS EN CELULARES (Toolbar, Decoration, Status) */
    [data-testid="stHeader"], 
    [data-testid="stDecoration"], 
    [data-testid="stToolbar"], 
    [data-testid="stStatusWidget"],
    [data-testid="manage-app-button"],
    button[title="View source"], 
    button[title="Manage app"],
    .st-emotion-cache-15z92p5, 
    .st-emotion-cache-6q9sum {
        display: none !important;
        visibility: hidden !important;
    }

    /* ELIMINAR ESPACIO BLANCO SUPERIOR */
    .block-container {
        padding-top: 0rem !important;
    }

    /* TIPOGRAFÍA Y COLOR DE TEXTO */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Montserrat', sans-serif;
        color: #FFFFFF !important;
    }

    /* ESTILO DE CAJAS DE TEXTO (INPUTS) */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea { 
        background-color: #1A1A1A !important; 
        color: #00FF00 !important; 
        border: 1px solid #00FF00 !important; 
    }

    /* ETIQUETAS EN VERDE NEÓN */
    label { 
        color: #00FF00 !important; 
        font-weight: bold !important; 
        font-size: 1.1rem !important;
    }

    /* TÍTULOS */
    h1, h2, h3 { 
        color: #00FF00 !important; 
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
    }

    /* BOTÓN DEL FORMULARIO */
    .stButton>button { 
        background-color: #00FF00 !important; 
        color: #000000 !important; 
        border-radius: 10px; 
        font-weight: bold;
        border: none;
        height: 3em;
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 20px #00FF00;
        color: #000000 !important;
    }

    /* LÍNEA DIVISORIA VERDE */
    hr {
        border-top: 1px solid #00FF00 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CABECERA
col_head1, col_head2 = st.columns([1, 4])

with col_head1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=100)
    else:
        st.markdown("<h1 style='margin:0;'>🚛</h1>", unsafe_allow_html=True)

with col_head2:
    st.markdown("<h1 style='margin-bottom: 0px; padding-top: 10px;'>OKGRUAS RS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; margin-top: 0px;'>Solicitud de Servicio de Grúa</p>", unsafe_allow_html=True)

st.divider()

# 4. FORMULARIO DE SOLICITUD
st.markdown("### 📱 Completa los datos para tu cotización")

with st.form("solicitud_servicio"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Tu Nombre")
        modelo = st.text_input("Modelo del Auto")
    with col2:
        origen = st.text_input("📍 Punto de Recolección")
        destino = st.text_input("🏁 Punto de Entrega")
    
    tipo_falla = st.selectbox("¿Qué problema presenta el vehículo?", [
        "Falla Mecánica", 
        "Choque / Siniestro", 
        "Llanta Ponchada", 
        "Sin Batería", 
        "Auto Bloqueado",
        "Otro (Especificar en notas)"
    ])
    
    notas = st.text_area("Notas adicionales (ej. sótano, sin llaves, etc.)")
    
    st.markdown("<p style='color: #00FF00; font-size: 0.9rem;'>💡 Al enviar, un asesor te contactará por WhatsApp.</p>", unsafe_allow_html=True)
    
    btn_enviar = st.form_submit_button("📩 SOLICITAR COTIZACIÓN POR WHATSAPP")

# 5. LÓGICA DE ENVÍO
if btn_enviar:
    if nombre and modelo and origen and destino:
        texto = (
            f"*NUEVA SOLICITUD DE SERVICIO - OKGRUAS RS*\n\n"
            f"👤 *Cliente:* {nombre}\n"
            f"🚗 *Vehículo:* {modelo}\n"
            f"🛠️ *Problema:* {tipo_falla}\n"
            f"📍 *Origen:* {origen}\n"
            f"🏁 *Destino:* {destino}\n"
            f"📝 *Notas:* {notas}\n\n"
            f"🧐 *Solicito cotización y tiempo de llegada.*"
        )
        mensaje_url = urllib.parse.quote(texto)
        mi_numero = "528143029578"
        whatsapp_link = f"https://wa.me/{mi_numero}?text={mensaje_url}"
        
        st.markdown(f'''
            <a href="{whatsapp_link}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; width: 100%; text-align: center; font-weight: bold; font-size: 16px; cursor: pointer;">
                    ✅ CLICK AQUÍ PARA CONFIRMAR EN WHATSAPP
                </div>
            </a>
        ''', unsafe_allow_html=True)
    else:
        st.error("⚠️ Por favor, llena los campos obligatorios.")

st.markdown("<br><p style='text-align: center; color: #444; font-size: 10px;'>OKGRUAS RS © 2026 | Programación Profesional</p>", unsafe_allow_html=True)
