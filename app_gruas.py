import streamlit as st
from PIL import Image
import os
import urllib.parse
from datetime import datetime

# 1. CONFIGURACIÓN DE LA APP
st.set_page_config(page_title="OKGRUAS RS Admin", page_icon="🚛", layout="wide")

# Estilo visual profesional
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; font-weight: bold; }
    .btn-ws { background-color: #25d366 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

if 'version' not in st.session_state:
    st.session_state.version = 0

# --- 2. ENCABEZADO CON LOGO ---
col_l, col_t, col_s = st.columns([1, 2, 2])

with col_l:
    # Busca tu logo rosa (logo.png o logo.pgn)
    for f in ["logo.png", "logo.pgn"]:
        if os.path.exists(f):
            st.image(f, width=100)
            break

with col_t:
    st.title("OKGRUAS RS")
    st.caption("Panel de Control de Servicios | Monterrey")

with col_s:
    st.info("🆔 Identificación del Servicio")
    socio = st.selectbox("Operador/Socio:", ["Juan G.", "Pedro L.", "Luis M.", "Yajaira Admin"], key=f"soc_{st.session_state.version}")
    eco = st.text_input("Unidad (Eco):", placeholder="Ej. G-01", key=f"eco_{st.session_state.version}")

# --- 3. CALCULADORA ---
st.divider()
c_in, c_out = st.columns(2)

with c_in:
    st.subheader("📍 Detalles del Viaje")
    km = st.number_input("Kilómetros totales:", min_value=0.0, value=30.0, key=f"km_{st.session_state.version}")
    
    col1, col2 = st.columns(2)
    with col1:
        sotano = st.checkbox("📍 ¿Es Sótano?", key=f"sot_{st.session_state.version}")
    with col2:
        falla = st.checkbox("🔧 ¿Falla Mecánica?", key=f"fal_{st.session_state.version}")
    
    pisos = st.number_input("Niveles de sótano:", min_value=0, step=1) if sotano else 0

# --- 4. LÓGICA DE COBRO ---
subtotal = 900.0 + (km * 25.0) + (pisos * 350.0) + (350.0 if falla else 0)
total_iva = subtotal * 1.16
utilidad_yaja = subtotal * 0.15
pago_socio = subtotal - utilidad_yaja

with c_out:
    st.subheader("💰 Resumen de Cuenta")
    st.metric("TOTAL A COBRAR (IVA)", f"${total_iva:,.2f}")
    st.metric("SUBTOTAL", f"${subtotal:,.2f}")
    
    st.warning(f"💎 Tu Utilidad: ${utilidad_yaja:,.2f}")
    st.info(f"🚛 Liquidación Operador: ${pago_socio:,.2f}")

# --- 5. ACCIONES Y CONTROL (ANTI-FUGAS) ---
st.divider()
b_new, b_ws, b_save = st.columns(3)

with b_new:
    if st.button("🔄 NUEVA COTIZACIÓN"):
        st.session_state.version += 1
        st.rerun()

with b_ws:
    # Botón de WhatsApp para que te manden el reporte antes de cobrar
    fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
    texto = f"*REPORTE OKGRUAS RS*\n📅 {fecha_hoy}\n👤 Socio: {socio}\n🚛 Unidad: {eco}\n📍 KM: {km}\n💵 Total: ${total_iva:,.2f}\n💎 Comisión Yajaira: ${utilidad_yaja:,.2f}"
    link = f"https://wa.me/5281XXXXXXXX?text={urllib.parse.quote(texto)}" # Pon tu número aquí
    st.markdown(f'<a href="{link}" target="_blank"><button style="width:100%; border-radius:10px; height:3.5em; background-color:#25d366; color:white; border:none; font-weight:bold; cursor:pointer;">📲 ENVIAR REPORTE POR WHATSAPP</button></a>', unsafe_allow_html=True)

with b_save:
    if st.button("💾 REGISTRAR EN EXCEL (DRIVE)"):
        st.success("¡Datos listos para sincronizar!")
        st.balloons()