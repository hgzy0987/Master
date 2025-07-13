✅ Full Telegram Bot with Keep Alive, Captcha, Buttons, Package, Broadcast

from keep_alive import keep_alive from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton from telegram.ext import * from datetime import datetime import logging, random

✅ Bot Token & Admin ID

TOKEN = "7594686828:AAF5VdC0yvQRjpC0oYlyRksB-vy8am0tiS0" ADMIN_ID = 6243881362

✅ Logging

logging.basicConfig(level=logging.INFO)

✅ State Management

START, CAPTCHA, CALC1, CALC2 = range(4) captcha_answer = {}

✅ Start command

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): user = update.effective_user code = str(random.randint(1000, 9999)) captcha_answer[user.id] = code context.user_data['join'] = datetime.now().strftime("%d-%m-%Y")

await update.message.reply_text(
    f"👋 Welcome {user.first_name}!

Please enter this code to verify:

🔐 {code}", parse_mode="Markdown" ) return CAPTCHA

✅ Captcha Check

async def check_captcha(update: Update, context: ContextTypes.DEFAULT_TYPE): uid = update.effective_user.id if update.message.text.strip() == captcha_answer.get(uid): keyboard = [ [KeyboardButton("PROFILE"), KeyboardButton("SUPPORT")], [KeyboardButton("PACKAGE"), KeyboardButton("CALCULATE")] ] markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True) await update.message.reply_text("✅ Verified successfully!", reply_markup=markup)

await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🆕 New User Joined:\n👤 Name: {update.effective_user.full_name}\n🆔 ID: {uid}\n📅 Date: {context.user_data['join']}"
    )
    return ConversationHandler.END
else:
    await update.message.reply_text("❌ Wrong code. Please try again.")
    return CAPTCHA

✅ Profile

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE): user = update.effective_user join = context.user_data.get("join", "N/A") await update.message.reply_text( f"👤 Name: {user.full_name}\n🆔 ID: {user.id}\n📅 Join Date: {join}\n📦 Package: None" )

✅ Support

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text( "📩 Dear customer! For any need, please contact us:\n👉 https://t.me/Swygen_bd" )

✅ Package

async def package(update: Update, context: ContextTypes.DEFAULT_TYPE): buttons = [ [InlineKeyboardButton("1 DAY PACKAGE | 200 BDT", callback_data="pkg_1")], [InlineKeyboardButton("3 DAY PACKAGE | 550 BDT", callback_data="pkg_3")], [InlineKeyboardButton("5 DAY PACKAGE | 1050 BDT", callback_data="pkg_5")], [InlineKeyboardButton("7 DAY PACKAGE | 1550 BDT", callback_data="pkg_7")], ] await update.message.reply_text("📦 MASTER AI PACKAGE LIST", reply_markup=InlineKeyboardMarkup(buttons))

✅ Package Selection

async def package_select(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer() data = { "pkg_1": "200 BDT", "pkg_3": "550 BDT", "pkg_5": "1050 BDT", "pkg_7": "1550 BDT" } price = data[query.data] await query.edit_message_text( f"📤 Please send {price} to:\nBkash: 01775716460\nNagad: 01812774257\nThen submit your Transaction ID.", parse_mode="Markdown" )

✅ Calculate

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("📲 Enter LAST 4 DIGITS of GAME PERIOD:") return CALC1

async def calc1(update: Update, context: ContextTypes.DEFAULT_TYPE): context.user_data['last4'] = update.message.text await update.message.reply_text("🔢 Enter WIN NUMBER:") return CALC2

async def calc2(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text( "⚠️ Dear Customer! Please activate your account.\nTo activate, activate a package. Thank you." ) return ConversationHandler.END

✅ Broadcast (Admin only)

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE): if update.effective_user.id != ADMIN_ID: return msg = update.message.text.replace("/broadcast ", "") for uid in captcha_answer.keys(): try: await context.bot.send_message(chat_id=uid, text=msg) except: pass await update.message.reply_text("✅ Broadcast sent.")

✅ MAIN Function

def main(): keep_alive()  # Start keep-alive HTTP server app = Application.builder().token(TOKEN).build()

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CAPTCHA: [MessageHandler(filters.TEXT, check_captcha)],
        CALC1: [MessageHandler(filters.TEXT, calc1)],
        CALC2: [MessageHandler(filters.TEXT, calc2)],
    },
    fallbacks=[]
)

app.add_handler(conv)
app.add_handler(MessageHandler(filters.Regex("PROFILE"), profile))
app.add_handler(MessageHandler(filters.Regex("SUPPORT"), support))
app.add_handler(MessageHandler(filters.Regex("PACKAGE"), package))
app.add_handler(MessageHandler(filters.Regex("CALCULATE"), calculate))
app.add_handler(CallbackQueryHandler(package_select))
app.add_handler(CommandHandler("broadcast", broadcast))

app.run_polling()

if name == "main": main()

