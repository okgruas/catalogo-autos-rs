import streamlit as st
import os
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from datetime import datetime

# 1. Configuración de carpetas y página
for folder in ["documentos", "biometria"]:
    if not os.path.exists(folder):
        os.makedirs(folder)

st.set_page_config(page_title="CrediCheck Pro", layout="wide")

# --- FUNCIÓN DE SEGURIDAD (LOGIN) ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        col_a, col_b, col_c = st.columns([1, 1, 1])
        with col_b:
            st.write("## 🔐 Acceso")
            st.text_input("Contraseña de CrediCheck Pro", type="password", on_change=password_entered, key="password")
            if "password_correct" in st.session_state and not st.session_state["password_correct"]:
                st.error("😕 Contraseña incorrecta")
        return False
    else:
        return st.session_state["password_correct"]

# --- LÓGICA PRINCIPAL DEL SOFTWARE ---
if check_password():
    # Header con botón de cerrar sesión
    col_t1, col_t2 = st.columns([0.8, 0.2])
    with col_t1:
        st.title("🛡️ CrediCheck Pro")
    with col_t2:
        if st.button("Cerrar Sesión"):
            st.session_state.clear()
            st.rerun()

    # --- BARRA LATERAL (ESTADO DEL REGISTRO) ---
    st.sidebar.header("Estado del Registro")
    
    # --- SECCIÓN DE DATOS DEL CLIENTE ---
    st.subheader("👤 Datos del Cliente")
    nombre = st.text_input("Nombre Completo del Cliente")
    
    col_tel, col_monto, col_espacio = st.columns([0.25, 0.25, 0.5]) 
    with col_tel:
        telefono = st.text_input("Teléfono de Contacto")
    with col_monto:
        monto = st.number_input("Monto Solicitado ($)", min_value=0, step=500)

    # --- NUEVA SECCIÓN: DATOS DE AVALES ---
    st.write("---")
    st.subheader("👥 Datos de Avales")
    col_av1, col_av2 = st.columns(2)
    
    with col_av1:
        st.markdown("**Aval 1**")
        nombre_aval1 = st.text_input("Nombre Aval 1")
        tel_aval1 = st.text_input("Teléfono Aval 1")
        
    with col_av2:
        st.markdown("**Aval 2**")
        nombre_aval2 = st.text_input("Nombre Aval 2")
        tel_aval2 = st.text_input("Teléfono Aval 2")

    # Actualización Estado en Sidebar
    if nombre and telefono and monto > 0:
        st.sidebar.write(f"👤 **Datos Cliente:** Listos ✅")
    else:
        st.sidebar.write("👤 **Datos Cliente:** Pendiente ❌")
        
    if nombre_aval1 and nombre_aval2:
        st.sidebar.write(f"👥 **Avales:** Listos ✅")
    else:
        st.sidebar.write("👥 **Avales:** Pendiente ❌")

    # --- PASO 1: FOTO ---
    st.write("---")
    st.subheader("📸 Paso 1: Validación Facial")
    foto = st.camera_input("Capturar Rostro", key="cam_final")
    
    if foto:
        st.image(foto, caption="✅ Foto capturada", width=250)
        st.sidebar.write("📸 **Foto:** Lista ✅")
    else:
        st.sidebar.write("📸 **Foto:** Pendiente ❌")

    # --- PASO 2: DOCUMENTACIÓN ---
    st.write("---")
    st.subheader("📄 Paso 2: Documentación")
    col_doc1, col_doc2, col_doc3 = st.columns(3)
    with col_doc1:
        ine_frente = st.file_uploader("Subir INE (Frente)", type=['png', 'jpg', 'pdf'])
    with col_doc2:
        ine_reverso = st.file_uploader("Subir INE (Reverso)", type=['png', 'jpg', 'pdf'])
    with col_doc3:
        domicilio = st.file_uploader("Comprobante Domicilio", type=['png', 'jpg', 'pdf'])

    st.sidebar.write("🪪 **INE Frente:** " + ("✅" if ine_frente else "❌"))
    st.sidebar.write("🪪 **INE Reverso:** " + ("✅" if ine_reverso else "❌"))
    st.sidebar.write("🏠 **DOM:** " + ("✅" if domicilio else "❌"))

    # --- PASO 3: FIRMA ---
    st.write("---")
    st.subheader("✍️ Paso 3: Firma Digital")
    canvas_result = st_canvas(
        stroke_width=3, stroke_color="#000000", background_color="#EEEEEE",
        height=200, drawing_mode="freedraw", key="canvas_final"
    )

    firma_valida = False
    if canvas_result.json_data is not None:
        if len(canvas_result.json_data["objects"]) > 0:
            firma_valida = True

    if firma_valida:
        st.sidebar.write("✍️ **Firma:** Lista ✅")
    else:
        st.sidebar.write("✍️ **Firma:** Pendiente ❌")

    st.write("---")

    # --- BOTÓN DE GUARDADO ---
    if st.button("🚀 GUARDAR EXPEDIENTE COMPLETO"):
        if nombre and telefono and foto and firma_valida:
            id_nombre = nombre.replace(" ", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path_face = f"biometria/{id_nombre}_face_{timestamp}.png"
            path_firma = f"documentos/{id_nombre}_firma_{timestamp}.png"
            
            # Guardar archivos físicos
            Image.open(foto).save(path_face)
            Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').save(path_firma)
                
            archivo_excel = 'base_datos_prestamos.xlsx'
            
            datos_fila = {
                "Fecha": [datetime.now().strftime("%d/%m/%Y %H:%M")],
                "Nombre Cliente": [nombre],
                "Teléfono": [telefono],
                "Monto": [f"${monto:,.2f}"],
                "Nombre Aval 1": [nombre_aval1],
                "Tel Aval 1": [tel_aval1],
                "Nombre Aval 2": [nombre_aval2],
                "Tel Aval 2": [tel_aval2],
                "INE Frente": ["✅" if ine_frente is not None else "❌"],
                "INE Reverso": ["✅" if ine_reverso is not None else "❌"],
                "Foto": ["✅"],
                "Comprobante": ["✅" if domicilio is not None else "❌"],
                "Firma": ["✅"],
                "Ruta Foto": [path_face],
                "Ruta Firma": [path_firma]
            }
            
            df_nuevo = pd.DataFrame(datos_fila)
            
            if not os.path.exists(archivo_excel):
                df_nuevo.to_excel(archivo_excel, index=False)
            else:
                df_existente = pd.read_excel(archivo_excel)
                df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
                df_final.to_excel(archivo_excel, index=False)

            st.balloons()
            st.success(f"¡Expediente de {nombre} guardado correctamente!")
        else:
            st.error("⚠️ Falta completar Nombre, Teléfono, Foto o Firma.")