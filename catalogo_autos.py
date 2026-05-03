import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="Catálogo de Vehículos RS", page_icon="🚗", layout="wide")

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

st.title("🚗 Catálogo de Vehículos RS")

# --- EL "CAMUFLAJE" ADMINISTRATIVO ---
for _ in range(15): st.sidebar.write("") # Espacio
if st.sidebar.checkbox(".", help="Admin"): 
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
                        with open(ruta, "wb") as f: f.write(foto.getbuffer())
                        
                        nuevo = pd.DataFrame([[m_sel, mod_sel, anio, precio, desc, ruta]], 
                                            columns=['marca', 'modelo', 'anio', 'precio', 'descripcion', 'foto'])
                        # Si el archivo no existe o está mal, lo sobreescribimos bien
                        if not os.path.exists('autos.csv'):
                            nuevo.to_csv('autos.csv', index=False)
                        else:
                            nuevo.to_csv('autos.csv', mode='a', header=False, index=False)
                        st.balloons()
                        st.rerun()
                    else: st.error("Sube una foto")

st.divider()

# --- MOSTRAR AUTOS (CON PROTECCIÓN DE ERRORES) ---
if os.path.exists('autos.csv'):
    try:
        df = pd.read_csv('autos.csv')
        # Limpiar espacios en los nombres de las columnas
        df.columns = [c.strip().lower() for c in df.columns]
        
        # Filtros
        st.sidebar.header("🔎 Buscar Auto")
        f_marca = st.sidebar.multiselect("Filtrar por Marca", options=MARCAS_DISPONIBLES)
        df_ver = df[df["marca"].isin(f_marca)] if f_marca else df

        items = st.columns(3)
        for i, row in df_ver.iterrows():
            with items[i % 3]:
                img_path = str(row['foto'])
                if os.path.exists(img_path): st.image(img_path, use_container_width=True)
                else: st.image("https://via.placeholder.com/400x300?text=Auto", use_container_width=True)
                
                st.subheader(f"{row['marca']} {row['modelo']}")
                st.markdown(f"### **${row['precio']:,} MXN**")
                with st.expander("🔍 Detalles"):
                    st.write(f"📅 **Año:** {row['anio']}")
                    st.write(f"📝 **Info:** {row['descripcion']}")
    except:
        st.warning("El archivo de datos se está inicializando. Por favor, carga tu primer auto en el panel secreto.")
else:
    st.info("Bienvenido. Usa el panel secreto abajo a la izquierda para inaugurar el catálogo.")