import requests


TOKEN = '5942481613:AAE27ofhXgvfc0XpsTcsUU5o40djmTClcrY'
ID = -801278776

# enviar mensagens utilizando o bot para um chat específico
def send_message(message):
    try:
        data = {"chat_id": -801278776, "text": message}
        url = "https://api.telegram.org/bot5942481613:AAE27ofhXgvfc0XpsTcsUU5o40djmTClcrY/sendMessage"
        requests.post(url, data)
    except Exception as e:
        print("Erro no sendMessage:", e)
