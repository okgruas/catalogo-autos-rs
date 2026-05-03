import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="Catálogo de Vehículos RS", layout="wide")

# --- BASE DE DATOS DE MODELOS ---
DATA_MODELOS = {
    "Nissan": ["Versa", "Sentra", "March", "Altima", "Kicks", "Frontier"],
    "Toyota": ["Corolla", "Hilux", "Tacoma", "Yaris", "RAV4", "Camry"],
    "Chevrolet": ["Aveo", "Onix", "Captiva", "Silverado", "Tracker", "S10"],
    "Volkswagen": ["Jetta", "Vento", "Taos", "Tiguan", "Polo", "Saveiro"],
    "Ford": ["Lobo", "Ranger", "Mustang", "Territory", "Bronco"],
    "Kia": ["Rio", "Forte", "Sportage", "Seltos", "Sorrento"],
    "Mazda": ["Mazda 3", "Mazda 2", "CX-5", "CX-30", "CX-9"],
    "Honda": ["Civic", "City", "CR-V", "HR-V", "Accord"]
}
MARCAS_DISPONIBLES = sorted(list(DATA_MODELOS.keys()))

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 Catálogo de Vehículos RS")

# --- VISTA DEL CLIENTE (FILTROS NORMALES) ---
st.sidebar.header("🔎 Buscar Auto")
f_marca = st.sidebar.multiselect("Filtrar por Marca", options=MARCAS_DISPONIBLES)

# --- EL "CAMUFLAJE" ADMINISTRATIVO ---
# Añadimos mucho espacio para que el acceso se vaya hasta abajo
for _ in range(20):
    st.sidebar.write("")

# Esto parece una simple nota de versión o un espacio vacío
if st.sidebar.checkbox(".", help="Solo personal autorizado"): 
    clave = st.sidebar.text_input("Token", type="password")
    
    if clave == "RL1994":
        st.sidebar.success("Acceso Maestro")
        with st.expander("➕ PANEL DE CARGA", expanded=True):
            with st.form("form_carga", clear_on_submit=True):
                c1, c2 = st.columns(2)
                with c1:
                    m_sel = st.selectbox("Marca", options=MARCAS_DISPONIBLES)
                    mod_sel = st.selectbox("Modelo", options=DATA_MODELOS[m_sel])
                    precio = st.number_input("Precio (MXN)", min_value=0)
                with c2:
                    anio = st.number_input("Año", min_value=1990, max_value=2027, value=2024)
                    foto = st.file_uploader("Imagen", type=['jpg', 'png', 'jpeg'])
                
                desc = st.text_area("Descripción")
                if st.form_submit_button("Guardar"):
                    if foto:
                        if not os.path.exists("fotos"): os.makedirs("fotos")
                        ruta = os.path.join("fotos", foto.name)
                        with open(ruta, "wb") as f:
                            f.write(foto.getbuffer())
                        
                        nuevo = pd.DataFrame([[m_sel, mod_sel, anio, precio, desc, ruta]], 
                                            columns=['marca', 'modelo', 'anio', 'precio', 'descripcion', 'foto'])
                        nuevo.to_csv('autos.csv', mode='a', header=not os.path.exists('autos.csv'), index=False)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Sube una foto")

st.divider()

# --- MOSTRAR AUTOS ---
if os.path.exists('autos.csv'):
    df = pd.read_csv('autos.csv')
    df.columns = [c.lower() for c in df.columns]
    
    df_ver = df
    if f_marca:
        df_ver = df[df["marca"].isin(f_marca)]

    items = st.columns(3)
    for i, row in df_ver.iterrows():
        with items[i % 3]:
            img_path = str(row['foto'])
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/400x300?text=Auto", use_container_width=True)
            
            st.subheader(f"{row['marca']} {row['modelo']}")
            st.markdown(f"### **${row['precio']:,} MXN**")
            
            with st.expander("🔍 Detalles"):
                st.write(f"📅 **Año:** {row['anio']}")
                st.write(f"📝 **Info:** {row['descripcion']}")
                st.button("Preguntar", key=f"int_{i}")
else:
    st.info("Inventario disponible próximamente.")