import os
from telethon import TelegramClient, events
from googletrans import Translator

# Récupérer les variables d'environnement
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
source_channels = os.getenv('SOURCE_CHANNELS').split(',')  # Liste des canaux sources
target_channel = os.getenv('TARGET_CHANNEL')

# Créer le client Telegram
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Initialiser le traducteur
translator = Translator()

# Fonction pour traduire un message
def translate_message(message):
    try:
        translated = translator.translate(message, src='auto', dest='fr')  # Langue cible ici 'fr' (français)
        return translated.text
    except Exception as e:
        print(f"Erreur lors de la traduction: {e}")
        return message

# Fonction pour envoyer le message traduit au canal cible
async def forward_message(event):
    # Traduire le message
    translated_message = translate_message(event.message.text)
    
    # Envoyer le message traduit au canal cible
    await client.send_message(target_channel, translated_message)

# Ajouter des écouteurs d'événements pour chaque canal source
for channel in source_channels:
    @client.on(events.NewMessage(chats=channel))
    async def handler(event):
        await forward_message(event)

# Lancer le client
client.start()
client.run_until_disconnected()
