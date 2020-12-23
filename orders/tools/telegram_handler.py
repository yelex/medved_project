import requests

TELEGRAM_TOKEN = '1463355381:AAEjkUkZTFd5_-cI5Z06veiLwbElOx1cHHo'
# TELEGRAM_CHAT_ID = '159404105'
TELEGRAM_CHAT_ID = '731195934'


def send_message(message):

    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
    }
    return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TELEGRAM_TOKEN),
							 data=payload).content