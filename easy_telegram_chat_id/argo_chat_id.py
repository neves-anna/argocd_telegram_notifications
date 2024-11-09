from telegram import Update
from telegram.ext import Application, MessageHandler, filters

async def message_handler(update: Update, context):
    if update.message: 
        chat_id = update.message.chat.id
    elif update.channel_post:
        chat_id = update.channel_post.chat.id
    else:
        return
    
    print(f"ID da mensagem: {chat_id}")
    print(f"Conteúdo: {update.message.text if update.message else update.channel_post.text}")

application = Application.builder().token("<telegram-bot-token").build()

application.add_handler(MessageHandler(filters.ALL, message_handler))

application.run_polling()
