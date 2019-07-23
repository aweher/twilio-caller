#!/usr/bin/python3
import random
import logging
import time
import sys
from pprint import pprint
from twilio.rest import Client
from config import TWILIOCFG, NUMEROS

def TwilioLogin(apilogindata):
    account_sid = apilogindata['sid']
    auth_token = apilogindata['token']
    try:
        cli = Client(account_sid, auth_token)
    except Exception as e:
        print(f"Error al iniciar sesión en Twilio: {e}")
        return False
    logging.info(f'Logueado correctamente en Twilio')
    return cli

def GetTwilioNumbers(cli):
    numeros = []
    incoming_phone_numbers = cli.incoming_phone_numbers.list(limit=20)
    for record in incoming_phone_numbers:
        pn = record.sid
        incoming_phone_number = cli.incoming_phone_numbers(pn).fetch()
        numeros.append(incoming_phone_number.friendly_name)
    return numeros

def Llamar(cli, numfrom, numto, numurl):
    call = cli.calls.create(url=numurl, to=numto, from_=numfrom, timeout=20, record=True)
    return [call.sid]

if __name__ == "__main__":
    client = None

    if TWILIOCFG is not None:
        client = TwilioLogin(TWILIOCFG)
    else:
        print("No encuentro las opciones para loguearme en Twilio")
        sys.exit(-1)

    for numto, url in NUMEROS.items():
        print(f'Llamando a {numto}')
        print(Llamar(client, random.choice(GetTwilioNumbers(client)), numto, url))

    print("Have a nice day")