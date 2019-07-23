from flask import Flask
import random
from config import TWILIOCFG, FRASES
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

def SeleccionarFrase(listadefrases):
    return random.choice(listadefrases)

def TwiMLResponse(texto):
    voices = ['man', 'woman', 'alice']
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

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=10000, debug=True)