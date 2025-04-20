import telebot
import requests

# Tokens fixos (usando os que você me passou)
TOKEN_TELEGRAM = '6800142516:AAGFwV5lPIMl-xpiQVQ7JHUJQjT3mbsupW0'
GROQ_API_KEY = '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'
GROQ_ENDPOINT = 'https://api.groq.com/openai/v1/chat/completions'

bot = telebot.TeleBot(TOKEN_TELEGRAM)

def enviar_para_groq(pergunta):
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        "model": "qwen-qwq-32b",
        "temperature": 0.5,
        "top_p": 0.9,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Você é uma IA estratégica que ajuda o Celso com automações, bots no Telegram, Groq API, negócios, geração de catálogos, leads e raciocínio lógico. "
                    "Responda com clareza, estrutura (passo a passo ou tópicos), e com foco em ação prática. "
                    "Evite frases genéricas. "
                    "Se a pergunta estiver vaga, peça mais contexto antes de responder. "
                    "Não diga que é um modelo de linguagem. Seja prático, inteligente e objetivo."
                )
            },
            {"role": "user", "content": pergunta}
        ]
    }

    resposta = requests.post(GROQ_ENDPOINT, headers=headers, json=payload)

    if resposta.status_code == 200:
        return resposta.json()['choices'][0]['message']['content']
    else:
        return f"Erro da Groq [{resposta.status_code}]: {resposta.text}"

@bot.message_handler(func=lambda message: True)
def responder_mensagem(message):
    texto_usuario = message.text
    resposta = enviar_para_groq(texto_usuario)
    bot.reply_to(message, resposta)

print("Bot rodando com Qwen-32B...")
bot.polling()
