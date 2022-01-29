import requests

ACCESS_CODE = # Insert access code for Notify Me here
NOTIFYME_URL = 'https://api.notifymyecho.com/v1/NotifyMe'

def send_notification(message: str):
    data = {'notification': message, 'accessCode': ACCESS_CODE, 'title': 'It is hot'}

    notification = requests.post(NOTIFYME_URL, json=data)
    print('Notification sent: %s' % notification.status_code)
