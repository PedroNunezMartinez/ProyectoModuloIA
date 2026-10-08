import streamlit as st

def obtener_mensaje_bienvenida():
    return "Hola este es mi primer proyecto con IA . esto los compilaremos para subirlo a git hub"

# Esto creará la interfaz visual en Streamlit
st.title("Mi Primer Proyecto de IA")
st.write(obtener_mensaje_bienvenida())
# --- AQUÍ EMPIEZA LO NUEVO ---
st.markdown("---") # Esto dibuja una línea divisoria visual

# Añadimos una caja interactiva para que pruebes la página
nombre_alumno = st.text_input("Ingresa tu nombre para saludarte:")

# Si escribes algo en la caja, la página te responderá de inmediato
if nombre_alumno:
    st.success(f"¡Excelente trabajo, {nombre_alumno}! Tu código en GitHub está conectado correctamente con Streamlit.")
