import requests
import os

PAGE_ACCESS_TOKEN = 'EAASg2dfAMj0BPGMvyZAH3ZBN2XzgO4d85hsaJWGWfIZBQeCv5gWNTibAMTVuXSnAs0dQCPoqPDQSwiScGLm7N9uz1V222VPRjeK3CNdjJAptQcLJP5fwVZC9hsLPNYx2nVrag5tIHQ6oNVAoYVEtASaMLlc2kn3yze9Ahl1RPsZAO6ExYiZALjx8vjphoFaFB6dBJMhZAOiAVroiM5GG3FUZBjR0yAZDZD'

def send_message(recipient_id, buttons):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    print(buttons)
    if buttons:
            payload = {
                "recipient": {"id": recipient_id},
          "message": {
            "attachment": {
              "type": "template",
              "payload": {
                "template_type": "button",
                "text": "Wybierz mecz, którego wynik chcesz zaktualizować:",
                "buttons": buttons
              }
            }
          }
        }
    else: 
          payload = {
              "recipient": {"id": recipient_id},
              "message": {
                  "text": 'Nie ma meczów'
              }
          }
    res = requests.post(url, json=payload)
    print(res.status_code, res.text)