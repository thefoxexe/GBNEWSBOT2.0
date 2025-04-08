from telethon import TelegramClient, events
from googletrans import Translator
import os

# Récupération des variables d'environnement
api_id = os.getenv('API_ID')  # Remplacer par votre API_ID
api_hash = os.getenv('API_HASH')  # Remplacer par votre API_HASH
bot_token = os.getenv('BOT_TOKEN')  # Remplacer par votre BOT_TOKEN
source_channel = os.getenv('SOURCE_CHANNEL')  # Canaux source à suivre
target_channel = os.getenv('TARGET_CHANNEL')  # Canaux cible où envoyer les messages

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
translator = Translator()

# Fonction pour traduire un message
def translate_message(message_text, src_lang='auto', dest_lang='fr'):
    translated = translator.translate(message_text, src=src_lang, dest=dest_lang)
    return translated.text

# Écoute des messages du canal source
@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    original_message = event.message.text
    translated_message = translate_message(original_message, src_lang='auto', dest_lang='fr')
    
    # Envoie le message traduit vers le canal cible
    await client.send_message(target_channel, translated_message)

# Démarre le bot
client.start()
client.run_until_disconnected()
