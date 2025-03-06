import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Configuración de credenciales
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)

# Cargar datos desde Google Sheets
@st.cache_data
def load_data():
    sheet = client.open("BCS_InventarioServicios_Otorgamiento [Kevin]").worksheet("Inventario_QA")
    data = sheet.get_all_records()
    return pd.DataFrame(data)

df = load_data()

# Crear la interfaz en Streamlit
st.title("📌 Inventario de Servicios OSB")
st.write("Filtra y busca servicios fácilmente")

# Agregar un filtro por Nombre de Servicio
filtro_servicio = st.text_input("Buscar servicio:")
if filtro_servicio:
    df = df[df["Nombre Servicio"].str.contains(filtro_servicio, case=False, na=False)]

# Mostrar la tabla
st.dataframe(df)
