# 🏍️ R&V Motor - Sistema CRM & Chatbot Automático con IA

Este proyecto corresponde al entregable final del **Módulo de Programación con Inteligencia Artificial** de la Maestría en IA. Consiste en un prototipo funcional (MVP) de un CRM inteligente capaz de procesar mensajes entrantes de clientes, simular interacciones de campañas de marketing de motocicletas, clasificar el nivel de interés de los leads y visualizar las métricas en un Dashboard analítico en tiempo real.

---

## 📅 Hito Semana 1: Infraestructura Base y Entorno de Despliegue

En esta primera semana se ha configurado con éxito la arquitectura de software y el entorno de despliegue continuo para garantizar la estabilidad del proyecto sin interferir con las prácticas del aula regular.

### 📁 Estructura del Proyecto
El código de este módulo final se encuentra completamente aislado dentro de la carpeta `rv_motor_crm/`:
* `app_dashboard.py`: Archivo principal de la interfaz visual construido sobre **Streamlit**.
* `requirements.txt`: Archivo de configuración que contiene las dependencias analíticas y de IA requeridas.
* `README.md`: Documentación técnica del estado del arte del proyecto (este archivo).

### ⚙️ Tecnologías y Librerías Utilizadas
Las dependencias han sido congeladas en versiones estables dentro de la carpeta del proyecto para asegurar la replicabilidad:
* **Streamlit (v1.35.0):** Framework para el desarrollo de la interfaz de usuario web.
* **Pandas (v2.2.2):** Biblioteca de manipulación y análisis de estructuras de datos.
* **Google Generative AI (v0.5.4):** SDK oficial para conectar con los modelos fundacionales de Gemini 1.5.
* **Plotly (v5.22.0):** Biblioteca gráfica interactiva para el cálculo visual de analíticas de negocio.

---

## 🔒 Buenas Prácticas de Ciberseguridad Aplicadas

Siguiendo las directrices avanzadas de desarrollo seguro, **este proyecto prohíbe estrictamente la exposición de API Keys (credenciales duras) en el código fuente**.
* **En desarrollo (Google Colab):** Las llaves de acceso se consumen mediante el gestor nativo de secrets (`from google.colab import userdata`).
* **En producción (Streamlit Cloud):** Las credenciales se inyectan dinámicamente utilizando el entorno cifrado de Streamlit Secrets (`st.secrets`).

---

## 🛠️ Instrucciones de Evaluación para el Docente

Para compilar y visualizar el estado actual del prototipo de la Semana 1 en Streamlit Cloud de forma independiente:
1. En el panel de control de Streamlit Cloud, cree una nueva aplicación conectada a este repositorio.
2. En el campo **"Main file path"**, asegúrese de apuntar a la ruta interna: `rv_motor_crm/app_dashboard.py`.
3. La aplicación se ejecutará de forma aislada, instalando su propio contenedor de dependencias sin alterar la práctica `app.py` ubicada en la raíz del repositorio.
