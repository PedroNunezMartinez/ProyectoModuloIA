import os
import json
import datetime
import pandas as pd
from flask import Flask, request, jsonify, make_response
from google import genai
from google.genai import types
from twilio.rest import Client
from pydantic import BaseModel

app = Flask(__name__)

# Extracción de variables de entorno de ciberseguridad
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = "whatsapp:+14155238886"

CSV_PATH = "mensajes_clasificados_ia.csv"

# Inicialización segura de Clientes de API
if GEMINI_API_KEY:
    ai_client = genai.Client(api_key=GEMINI_API_KEY)
else:
    raise ValueError("ERROR: Variable GEMINI_API_KEY no detectada.")

if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
else:
    raise ValueError("ERROR: Variables de Twilio no detectadas.")

# Esquema de salida requerido para la clasificación semántica en <3s
class ClasificacionLead(BaseModel):
    interes_ia: str  
    motivo_semantico: str
    respuesta_automatica: str

@app.route("/", methods=["POST"])
def webhook():
    try:
        # Extraer parámetros del payload URL-encoded enviado por Twilio
        from_number = request.values.get("From", "")  
        message_body = request.values.get("Body", "").strip()

        if not from_number or not message_body:
            return jsonify({"status": "error", "message": "Payload incompleto"}), 400

        clean_phone = from_number.replace("whatsapp:", "")

        # System Prompt con reglas estrictas de negocio para la Maestría en IA
        system_instruction = """
        Actúas como el Agente de IA experto de la concesionaria de motocicletas "R&V Motor".
        Analiza el contexto del mensaje enviado por el cliente en menos de 3 segundos y clasifícalo en una de estas categorías:
        1. 'Lead Caliente': Intención clara e inmediata de compra (precios específicos, cuotas, financiamiento, métodos de pago, quiere ir hoy mismo con el dinero).
        2. 'Cliente Potencial': Interés real pero con planes a futuro (agendar citas próxima semana, disponibilidad próximo mes, catálogos generales).
        3. 'Cliente que Solo Pregunta': Soporte o información general operativa sin venta directa (horarios, dirección física, repuestos, vacantes).
        4. 'Lead Frío': Negativa, descartes ("No gracias"), emoticones por error o textos sin sentido ajenos a motos.

        REGLA DE RESPUESTA AUTOMÁTICA: Genera una respuesta persuasiva, humana y empática en español, orientada a cerrar la venta o resolver el soporte.
        """

        # Invocación al modelo Gemini 3.8 Flash con SDK google-genai==1.3.0
        response = ai_client.models.generate_content(
            model='gemini-3.8-flash',
            contents=message_body,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=ClasificacionLead,
                temperature=0.1
            ),
        )

        # Parsear la salida JSON estructurada del cerebro de IA
        ai_data = json.loads(response.text)
        
        # Búsqueda tolerante a fallos de mayúsculas/minúsculas en el JSON de la IA
        interes_ia = ai_data.get("interes_ia") or ai_data.get("interesIa") or "Cliente que Solo Pregunta"
        motivo_semantico = ai_data.get("motivo_semantico") or ai_data.get("motivoSemantico") or "Consulta general"
        respuesta_automatica = ai_data.get("respuesta_automatica") or ai_data.get("respuestaAutomatica") or "Hola, gracias por escribir a R&V Motor. En breve un asesor te atenderá."

        # Fusión de datos en caliente para inyectar realismo métrico al Dashboard
        ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ventas_estimadas = 1 if interes_ia in ["Lead Caliente", "Cliente Potencial"] else 0
        ingreso_estimado = 2500.0 if interes_ia == "Lead Caliente" else (1200.0 if interes_ia == "Cliente Potencial" else 0.0)
        costo_marketing = 150.0  
        roi_calculado = ((ingreso_estimado - costo_marketing) / costo_marketing) if costo_marketing > 0 else 0.0

        nuevo_row = {
            "fecha_registro": ahora, "telefono_cliente": clean_phone, "mensaje_original": message_body,
            "interes_ia": interes_ia, "motivo_semantico": motivo_semantico, "ventas_estimadas": ventas_estimadas,
            "ingreso_estimado": ingreso_estimado, "costo_marketing": costo_marketing, "roi_calculado": roi_calculado
        }

        if os.path.exists(CSV_PATH):
            df_historico = pd.read_csv(CSV_PATH)
            df_final = pd.concat([df_historico, pd.DataFrame([nuevo_row])], ignore_index=True)
        else:
            df_final = pd.DataFrame([nuevo_row])
        
        df_final.to_csv(CSV_PATH, index=False)

        # Usar la API de Twilio para enviar la respuesta de la IA de regreso al cliente
        twilio_client.messages.create(body=str(respuesta_automatica), from_=TWILIO_NUMBER, to=from_number)

        # Crear respuesta con el encabezado de bypass para omitir la advertencia visual de Ngrok Free
        resp = make_response(jsonify({"status": "success", "clasificacion": interes_ia}), 200)
        resp.headers["ngrok-skip-browser-warning"] = "true"
        return resp

    except Exception as e:
        print(f"Error crítico en Webhook: {str(e)}")
        error_resp = make_response(jsonify({"status": "error", "message": str(e)}), 500)
        error_resp.headers["ngrok-skip-browser-warning"] = "true"
        return error_resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)