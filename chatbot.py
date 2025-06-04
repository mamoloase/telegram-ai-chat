importrandom
from telegram import *
from telegram.ext import *
from openai import OpenAI

config = {
    "TOKEN" : "TELEGRAM BOT TOKEN",
    "IMAGE_API_KEY" : "_",
    "API_KEY" : "(OPEN AI)CHAT GPT API KEY",
    "OWNER" : 6506165902,
}

user_messages = {}


def store_interaction(user_id, question, is_question = True):
    if user_id not in user_messages:
        user_messages[user_id] = []
    if is_question:
        user_messages[user_id].append({"role": "user", "content": question})
    else :
        user_messages[user_id].append({"role": "assistant", "content": question})

    if len(user_messages[user_id]) > 10:
        user_messages[user_id] = user_messages[user_id][-5:]


client = OpenAI(
  api_key = config["API_KEY"],
)

def answer_question(question):
    messages = question
    messages.append({"role": "system", "content": "شخصیت و اطلاعات اولیه ربات"})
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=messages
    )
    return completion.choices[0].message.content


BOT_NAME = "مهری"
BOT_NAMES = ["مهری" ,"غلام" ,"صگ"]
ANSWER_CALLNAME = ["بله" , "ها" , "جون" ,"مرگ" , "درد" ,"زهر مار","جان نفسوم"]

async def EventMessageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    me_id = context.bot.id

    if text in BOT_NAMES :
        answer = random.choice(ANSWER_CALLNAME)
        return await update.message.reply_text(
                text = f"<b>{answer}</b>",
                parse_mode = "HTML" ,reply_to_message_id = update.message.id)
    
    if update.message.chat.type in [constants.ChatType.GROUP ,constants.ChatType.SUPERGROUP]:
        if update.message.text and (update.message.text.startswith(BOT_NAME) or (update.message.reply_to_message and update.message.reply_to_message.from_user.id == me_id)):
            question = update.message.text.replace(BOT_NAME ,"")
            store_interaction(update.message.from_user.id ,question ,True)
            
            message = await update.message.reply_text(
                text = "<b>🤔</b>",
                parse_mode = "HTML" ,reply_to_message_id = update.message.id)
            answer = answer_question(user_messages[update.message.from_user.id])
            if answer:
                store_interaction(update.message.from_user.id ,answer ,False)
            await message.edit_text(text = answer,parse_mode = "Markdown")

        return  

    if text.lower().startswith("/start"):
        await update.message.reply_text(
            text = "<b>سلام زیبا چه کمکی از دست من بر میاد برات انجام بدم؟ 🤖</b>",
            parse_mode = "HTML")
    
    else :
        store_interaction(update.message.from_user.id ,text ,True)
        message = await update.message.reply_text(
            text = "<b>🤔</b>",
            parse_mode = "HTML" ,reply_to_message_id = update.message.id)
        answer = answer_question(user_messages[update.message.from_user.id])
        if answer:
            store_interaction(update.message.from_user.id ,answer ,False)
        await message.edit_text(text = answer ,parse_mode = "Markdown")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Exception : {context.error}")
    await context.bot.send_message(
        chat_id = config["OWNER"],
        text = f"Exception : <pre>{context.error}</pre>",
        parse_mode = "HTML"
    )

app = ApplicationBuilder().token(config["TOKEN"]).build()

app.add_error_handler(error_handler)
app.add_handler(MessageHandler(filters=filters.TEXT & filters.ChatType.PRIVATE | filters.ChatType.GROUP | filters.ChatType.SUPERGROUP, callback=EventMessageHandler))
app.run_polling()
