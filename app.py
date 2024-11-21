import streamlit as st
import pandas as pd
import mysql.connector

# Función para conectarse a MySQL
def create_connection():
    return mysql.connector.connect(
        host="localhost",          # Cambia por tu host de MySQL
        user="root",          # Cambia por tu usuario de MySQL
        password="admin123.",  # Cambia por tu contraseña
        database="adminerp_garden"   # Cambia por tu base de datos
    )

# Función para ejecutar consultas
def fetch_data(query, params=None):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)  # Retorna resultados como diccionarios
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return pd.DataFrame(result)

# Función para obtener datos con filtros dinámicos
def get_data(id_min):
    query = """
    SELECT
      o.id AS id_operativa,
      o.nombre_operacion AS operativa,
      SUM(c.ventas) AS total_ventas,
      SUM(c.efectivo) AS total_efectivo,
      SUM(c.con_tarjeta) AS total_tarjeta
    FROM ope_conciliacion c
      INNER JOIN ope_operacion o ON c.id_operacion = o.id
    WHERE c.id_operacion >= %s
    GROUP BY o.id, o.nombre_operacion
    ORDER BY o.id ASC
    """
    data = fetch_data(query, (id_min,))
    if data.empty:
        st.warning("La consulta no devolvió resultados.")
    else:
        st.write(data)  # Para depuración: Muestra los datos obtenidos
    return data


# Interfaz de Streamlit
st.title("Consulta de Operativas Dinámicas")
st.sidebar.header("Filtros")

# Filtros interactivos
id_min = st.sidebar.number_input("ID mínimo de operativa", min_value=5, value=5, step=1)

# Obtener y mostrar datos
st.header("Resultados")
data = get_data(id_min)

if not data.empty:
    st.dataframe(data)  # Mostrar tabla interactiva
    st.bar_chart(data.set_index("operativa")[["total_ventas", "total_efectivo", "total_tarjeta"]])  # Gráfico de barras
else:
    st.warning("No se encontraron datos para los filtros seleccionados.")
