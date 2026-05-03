import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="Vehículos RS", page_icon="🚗", layout="wide")

# --- OCULTAR ICONOS DE GITHUB/EDITAR (Solo se ven si eres admin) ---
# Esto oculta el menú de arriba a la derecha que me mostraste en la foto
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""

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

st.title("🚗 Vehículos RS")

# --- LÓGICA DE ADMINISTRACIÓN ---
# Primero ponemos los filtros arriba en la barra lateral
st.sidebar.header("🔎 Buscar en Inventario")
f_marca = st.sidebar.multiselect("Filtrar por Marca", options=MARCAS_DISPONIBLES)

for _ in range(10): st.sidebar.write("") # Espacio para mandar el admin abajo

# El "Cuadrito" Secreto (Admin)
es_admin = False
if st.sidebar.checkbox(".", help="Configuración Maestro"):
    # Si activas el cuadro, mostramos los iconos de arriba para que puedas editar
    st.sidebar.markdown("---")
    token = st.sidebar.text_input("Token de Acceso", type="password")
    if token == "RL1994":
        es_admin = True
        st.sidebar.success("Modo Maestro Activo")
    else:
        st.markdown(hide_style, unsafe_allow_html=True) # Siguen ocultos si la clave está mal
else:
    st.markdown(hide_style, unsafe_allow_html=True) # Ocultos por defecto

# --- PANEL DE CARGA Y BORRADO (Solo para Admin) ---
if es_admin:
    with st.expander("🛠️ GESTIÓN DE INVENTARIO", expanded=True):
        tab1, tab2 = st.tabs(["➕ Agregar Auto", "🗑️ Borrar Vendido"])
        
        with tab1:
            with st.form("form_carga", clear_on_submit=True):
                c1, c2 = st.columns(2)
                with c1:
                    m_sel = st.selectbox("Marca", options=MARCAS_DISPONIBLES)
                    mod_sel = st.selectbox("Modelo", options=DATA_MODELOS[m_sel])
                    precio = st.number_input("Precio (MXN)", min_value=0)
                with c2:
                    anio = st.number_input("Año", min_value=1990, max_value=2027, value=2024)
                    foto = st.file_uploader("Subir Foto", type=['jpg', 'png', 'jpeg'])
                
                desc = st.text_area("Descripción corta")
                if st.form_submit_button("Publicar Vehículo"):
                    if foto and precio > 0:
                        if not os.path.exists("fotos"): os.makedirs("fotos")
                        ruta = os.path.join("fotos", foto.name)
                        with open(ruta, "wb") as f: f.write(foto.getbuffer())
                        
                        nuevo = pd.DataFrame([[m_sel, mod_sel, anio, precio, desc, ruta]], 
                                            columns=['marca', 'modelo', 'anio', 'precio', 'descripcion', 'foto'])
                        if not os.path.exists('autos.csv'):
                            nuevo.to_csv('autos.csv', index=False)
                        else:
                            nuevo.to_csv('autos.csv', mode='a', header=False, index=False)
                        st.success("¡Auto guardado con éxito!")
                        st.rerun()
                    else: st.warning("Faltan datos o foto.")

        with tab2:
            if os.path.exists('autos.csv'):
                df_temp = pd.read_csv('autos.csv')
                if not df_temp.empty:
                    st.write("Selecciona el auto que ya se vendió:")
                    # Creamos una lista de nombres para identificar qué borrar
                    df_temp['id_borrar'] = df_temp['marca'] + " " + df_temp['modelo'] + " ($" + df_temp['precio'].astype(str) + ")"
                    auto_a_borrar = st.selectbox("Vehículo a eliminar", options=df_temp['id_borrar'].tolist())
                    
                    if st.button("Confirmar Borrado", type="primary"):
                        df_final = df_temp[df_temp['id_borrar'] != auto_a_borrar]
                        # Quitamos la columna temporal antes de guardar
                        df_final = df_final.drop(columns=['id_borrar'])
                        df_final.to_csv('autos.csv', index=False)
                        st.error("Vehículo eliminado del catálogo.")
                        st.rerun()
                else: st.info("No hay autos para borrar.")

st.divider()

# --- MOSTRAR EL CATÁLOGO ---
if os.path.exists('autos.csv'):
    try:
        df = pd.read_csv('autos.csv')
        df_ver = df[df["marca"].isin(f_marca)] if f_marca else df

        if df_ver.empty:
            st.info("No se encontraron vehículos con esos filtros.")
        else:
            # Grid de 3 columnas
            cols = st.columns(3)
            for i, row in df_ver.iterrows():
                with cols[i % 3]:
                    if os.path.exists(str(row['foto'])):
                        st.image(row['foto'], use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/400x300?text=Sin+Foto", use_container_width=True)
                    
                    st.subheader(f"{row['marca']} {row['modelo']}")
                    st.write(f"📅 **Año:** {row['anio']}")
                    st.markdown(f"### **${row['precio']:,} MXN**")
                    with st.expander("Más información"):
                        st.write(row['descripcion'])
    except Exception as e:
        st.error("Hubo un problema al leer los datos. Carga un auto nuevo para reiniciar.")
else:
    st.info("Iniciando catálogo... Por favor, usa el acceso maestro para cargar el primer vehículo.")