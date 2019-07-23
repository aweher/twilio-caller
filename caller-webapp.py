from flask import Flask
import random
from config import TWILIOCFG, FRASES, CUMPLE
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

def SeleccionarFrase(listadefrases):
    return random.choice(listadefrases)

def TwiMLResponse(texto):
    #voices = ['man', 'woman', 'alice']
    voices = ['alice']
    selectedvoice = random.choice(voices)
    if selectedvoice == 'alice':
        lang = 'es-MX'
    else:
        lang = 'es' 
    tr = VoiceResponse()
    tr.pause(length=1)
    tr.say(message=texto, voice=selectedvoice, loop=0, language=lang)
    tr.hangup()
    return tr.to_xml()

@app.route("/", methods=['GET', 'POST'])
def home():
    return ""

@app.route("/obtenerfrase", methods=['GET', 'POST'])
def answer_call():
    return str(TwiMLResponse(SeleccionarFrase(FRASES)))

@app.route("/diasparaelcumple", methods=['GET', 'POST'])
def calcular_dias():
    import datetime
    cumple=datetime.date(CUMPLE['anio'], CUMPLE['mes'], CUMPLE['dia'])
    hoy = datetime.date.today()
    dias = (cumple-hoy).days
    if dias > 0:
        return str(TwiMLResponse('Buenos días. Le informamos que faltan {} días para el cumple de {}. Saludos!'.format(dias, CUMPLE['nombre'])))
    else:
        return str(TwiMLResponse('Buenos días. Le informamos que hoy es el cumple de {}. Saludos!'.format(CUMPLE['nombre'])))

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=10000, debug=True)
    app.run(host='127.0.0.1')