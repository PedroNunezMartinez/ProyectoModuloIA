import streamlit as st

def obtener_mensaje_bienvenida():
    return "Hola este es mi primer proyecto con IA . esto los compilaremos para subirlo a git hub"

# Esto creará la interfaz visual en Streamlit
st.title("Mi Primer Proyecto de IA")
st.write(obtener_mensaje_bienvenida())
