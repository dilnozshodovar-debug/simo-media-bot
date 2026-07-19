# -*- coding: utf-8 -*-
"""
SIMO.MEDIA — Telegram bot (нусхаи такмилёфта)
Прайс-лист, портфолио, тавсифҳо, FAQ, фармоиши пурра ва тамос.

Барои иҷро:
1) pip install -r requirements.txt
2) Токени ботро аз @BotFather гиред
3) Дар поён BOT_TOKEN-ро ё ENV variable BOT_TOKEN ворид кунед
4) python bot.py
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    ConversationHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ==================== ТАНЗИМОТ ====================

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8864413053:AAFSNnOT6SgRsp3zD16fEMR_BsqBhiloim4")

# ID-и админ(ҳо) барои гирифтани хабари фармоиш
ADMIN_IDS = []  # мисол: [123456789] — аз @userinfobot гиред

CONTACT_PHONE_DISPLAY = "+992 93 882 97 96"
CONTACT_PHONE_RAW = "992938829796"  # барои линки WhatsApp, бе + ва фосила
WHATSAPP_LINK = f"https://wa.me/{CONTACT_PHONE_RAW}"
TELEGRAM_USERNAME = "@editor2202"
TELEGRAM_LINK = "https://t.me/editor2202"
INSTAGRAM_LINK = "https://www.instagram.com/iam_shodovar?igsh=Z3g1NHhrOXM5NGdl"

# Намунаи корҳо (портфолио) — линкҳои воқеии видео/акси худро гузоред
PORTFOLIO_LINKS = [
    ("🎬 Намунаи клип — Reel", "https://www.instagram.com/reel/DYJFY9MoYnJ/?igsh=MWc4ZHNua2xyMzdkaw=="),
    ("📷 Барои намунаи бештари корҳои мо — Instagram", "https://www.instagram.com/iam_shodovar?igsh=Z3g1NHhrOXM5NGdl"),
]

# ==================== МАТНҲО ====================

WELCOME_TEXT = (
    "🎥 <b>SIMO.MEDIA</b>\n"
    "<i>Хотираҳоро ба филмҳои ҷовидона табдил медиҳем</i>\n\n"
    "✨ Хуш омадед!\n\n"
    "Рӯзи арӯсӣ танҳо як бор такрор мешавад. Мо ҳар табассум, ҳар ашки шодӣ ва "
    "ҳар лаҳзаи зебои ин рӯзи фаромӯшнашавандаро бо сифати баланд сабт мекунем, "
    "то барои шумо хотираи ҷовидона гардад.\n\n"
    "👇 Лутфан аз менюи поён интихоб кунед:"
)

ABOUT_TEXT = (
    "ℹ️ <b>Дар бораи SIMO.MEDIA</b>\n\n"
    "SIMO.MEDIA — студияи касбии наворбардории тӯй таҳти роҳбарии "
    "<b>Шодовар Нуриддинов</b> мебошад.\n\n"
    "📅 Студияи мо аз 20 феврали соли 2023 фаъолияти расмии худро оғоз намуд. "
    "Пеш аз таъсиси SIMO.MEDIA, мо дар шаҳри Хуҷанд тӯли ду сол тамоми нозукиҳои "
    "санъати наворбардорӣ, филмсозӣ ва коркарди видеоро аз худ намуда, таҷрибаи "
    "заруриро барои пешниҳоди хизматрасонии сатҳи баланд ба даст овардем.\n\n"
    "🎥 Имрӯз SIMO.MEDIA бо истифода аз камераҳои касбӣ, DJI Ronin, дронҳои муосир, "
    "таҷҳизоти рӯшноидиҳӣ ва сабти садои касбӣ лаҳзаҳои муҳим ва фаромӯшнашавандаи "
    "тӯйро бо сифати баланд сабт менамояд.\n\n"
    "💻 Коркарди видео дар асоси технологияҳои пешрафта бо истифода аз "
    "<b>Adobe Premiere Pro, Adobe After Effects</b> ва <b>DaVinci Resolve</b> "
    "анҷом дода мешавад. Инчунин барои беҳтар намудани сифати тасвир ва ислоҳи "
    "ранг аз имкониятҳои зеҳни сунъӣ (AI) низ истифода мебарем.\n\n"
    "Барои мо ҳар як тӯй қиссаи нотакрор аст 💍\n\n"
    "<b>SIMO.MEDIA — хотираҳоро ба филмҳои ҷовидона табдил медиҳем.</b>"
)

WHY_US_TEXT = (
    "✨ <b>ЧАРО МАҲЗ SIMO.MEDIA?</b>\n\n"
    "📸 Таҷҳизоти муосир ва сифати баланд\n"
    "🎬 Монтажи касбӣ бо услуби замонавӣ\n"
    "🚁 Наворбардорӣ бо дрон\n"
    "💍 Сабти тамоми лаҳзаҳои муҳими тӯй\n"
    "⚡ Омодасозии зуд ва саривақтии мавод\n"
    "🤖 Истифодаи AI барои сифати беҳтари ранг\n"
    "🤝 Муносибати масъулиятнок ба ҳар як фармоишгар"
)

FAQ_TEXT = (
    "❓ <b>САВОЛҲОИ МАЪМУЛ</b>\n\n"
    "🔹 <b>Оё пеш аз тӯй вохӯрӣ (консултатсия) мешавад?</b>\n"
    "Ҳа, мо тамоми ҷузъиётро пеш аз рӯзи тӯй муҳокима мекунем.\n\n"
    "🔹 <b>Пеш-пардохт лозим аст?</b>\n"
    "Ҳа, барои мустаҳкам кардани фармоиш кафолати андак гирифта мешавад.\n\n"
    "🔹 <b>Оё берун аз шаҳр меравед?</b>\n"
    "Ҳа, бо шартҳои иловагӣ метавонем ба навоҳии дигар низ равем.\n\n"
    "🔹 <b>То кай мавод омода мешавад?</b>\n"
    "Вобаста ба пакет — аз 7 то 30 рӯз (тафсилот дар прайс-лист).\n\n"
    "Саволи дигар доред? Ба бахши 📞 Тамос гузаред."
)

CONTACT_TEXT = (
    "📞 <b>Барои машварат ва фармоиш</b>\n\n"
    f"☎️ Телефон: {CONTACT_PHONE_DISPLAY}\n"
    f"💬 WhatsApp: {CONTACT_PHONE_DISPLAY}\n"
    f"✈️ Telegram: {TELEGRAM_USERNAME}\n"
    f"📷 Instagram: {INSTAGRAM_LINK}\n\n"
    "SIMO.MEDIA — Хотираҳоро ба вақт насупоред, онҳоро ба мо бовар кунед."
)

PACKAGES = {
    "standard": {
        "title": "🎥 STANDARD — 1500 сомонӣ",
        "short": "STANDARD (1500 сомонӣ)",
        "text": (
            "🎥 <b>STANDARD — 1500 сомонӣ</b>\n\n"
            "Интихоби беҳтарин барои сабти лаҳзаҳои муҳими тӯй.\n\n"
            "Ба пакет дохил мешавад:\n"
            "✔️ Наворбардории касбӣ\n"
            "✔️ Аксбардории касбӣ\n"
            "✔️ 1 адад камера\n"
            "✔️ 1 ҷуфт диски аслӣ (Original DVD)\n\n"
            "🎁 Тӯҳфа: 10 дона акси чопшуда\n\n"
            "⏳ Омодасозии мавод: 25–30 рӯз"
        ),
    },
    "vip": {
        "title": "👑 VIP — 2000 сомонӣ",
        "short": "VIP (2000 сомонӣ)",
        "text": (
            "👑 <b>VIP — 2000 сомонӣ</b>\n\n"
            "Сифати бештар, хотираҳои бештар.\n\n"
            "Ба пакет дохил мешавад:\n"
            "✔️ Наворбардории касбӣ\n"
            "✔️ Аксбардории касбӣ\n"
            "✔️ 1 адад камера\n"
            "✔️ 1 ҷуфт диски аслӣ (Original DVD)\n"
            "✔️ Флешкаи аслӣ (64 GB)\n"
            "✔️ 1 адад албоми зебои Wedding Day\n\n"
            "🎁 Тӯҳфа: 30 дона акси чопшуда\n\n"
            "⏳ Омодасозии мавод: 15–20 рӯз"
        ),
    },
    "vip_premium": {
        "title": "💎 VIP PREMIUM — 3000 сомонӣ",
        "short": "VIP PREMIUM (3000 сомонӣ)",
        "text": (
            "💎 <b>VIP PREMIUM — 3000 сомонӣ</b>\n\n"
            "Интихоби беҳтарин барои онҳое, ки беҳтаринро мехоҳанд.\n\n"
            "Ба пакет дохил мешавад:\n"
            "✔️ Наворбардории касбӣ\n"
            "✔️ Аксбардории касбӣ\n"
            "✔️ 1 адад камера\n"
            "✔️ 1 адад крани наворбардорӣ (Camera Crane)\n"
            "✔️ Клипи тӯёна\n"
            "✔️ Love Story\n"
            "✔️ 2 ҷуфт диски аслӣ (Original DVD)\n"
            "✔️ Флешкаи аслӣ (64 GB)\n"
            "✔️ Албоми Wedding Day\n"
            "✔️ Албом барои аксҳо\n\n"
            "🎁 Интихоби махсус: ба ҷойи карнай-сурнай — 1 камераи иловагӣ.\n\n"
            "🎁 Тӯҳфа: 50 дона акси чопшуда\n\n"
            "⏳ Омодасозии мавод: 7–10 рӯз"
        ),
    },
}

# States барои ConversationHandler (фармоиши пурра)
ASK_NAME, ASK_PHONE, ASK_DATE = range(3)

# ==================== КЛАВИАТУРАҲО ====================

def main_menu_kb():
    kb = [
        [InlineKeyboardButton("💰 Прайс-лист", callback_data="menu_prices"),
         InlineKeyboardButton("🎬 Портфолио", callback_data="menu_portfolio")],
        [InlineKeyboardButton("✨ Чаро маҳз мо?", callback_data="menu_why"),
         InlineKeyboardButton("❓ FAQ", callback_data="menu_faq")],
        [InlineKeyboardButton("ℹ️ Дар бораи мо", callback_data="menu_about")],
        [InlineKeyboardButton("📞 Тамос", callback_data="menu_contact")],
    ]
    return InlineKeyboardMarkup(kb)


def prices_menu_kb():
    kb = [
        [InlineKeyboardButton("🎥 STANDARD — 1500 сомонӣ", callback_data="pkg_standard")],
        [InlineKeyboardButton("👑 VIP — 2000 сомонӣ", callback_data="pkg_vip")],
        [InlineKeyboardButton("💎 VIP PREMIUM — 3000 сомонӣ", callback_data="pkg_vip_premium")],
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(kb)


def package_detail_kb(pkg_key: str):
    kb = [
        [InlineKeyboardButton("✅ Ин пакетро фармоиш медиҳам", callback_data=f"choose_{pkg_key}")],
        [InlineKeyboardButton("⬅️ Ба прайс-лист", callback_data="menu_prices")],
    ]
    return InlineKeyboardMarkup(kb)


def back_to_main_kb():
    kb = [[InlineKeyboardButton("⬅️ Ба меню асосӣ", callback_data="menu_main")]]
    return InlineKeyboardMarkup(kb)


def contact_kb():
    kb = [
        [InlineKeyboardButton("💬 WhatsApp", url=WHATSAPP_LINK)],
        [InlineKeyboardButton("✈️ Telegram", url=TELEGRAM_LINK)],
        [InlineKeyboardButton("📷 Instagram", url=INSTAGRAM_LINK)],
        [InlineKeyboardButton("⬅️ Ба меню асосӣ", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(kb)


def portfolio_kb():
    kb = [[InlineKeyboardButton(name, url=link)] for name, link in PORTFOLIO_LINKS]
    kb.append([InlineKeyboardButton("⬅️ Ба меню асосӣ", callback_data="menu_main")])
    return InlineKeyboardMarkup(kb)


def after_order_kb():
    kb = [
        [InlineKeyboardButton("💬 WhatsApp", url=WHATSAPP_LINK)],
        [InlineKeyboardButton("⬅️ Ба меню асосӣ", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(kb)


# ==================== ХЭНДЛЕРҲОИ АСОСӢ ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME_TEXT, reply_markup=main_menu_kb(), parse_mode="HTML"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_main":
        await query.edit_message_text(WELCOME_TEXT, reply_markup=main_menu_kb(), parse_mode="HTML")

    elif data == "menu_prices":
        await query.edit_message_text(
            "💰 <b>ПРАЙС-ЛИСТИ SIMO.MEDIA</b>\n\nЛутфан пакетро интихоб кунед 👇",
            reply_markup=prices_menu_kb(), parse_mode="HTML",
        )

    elif data == "menu_why":
        await query.edit_message_text(WHY_US_TEXT, reply_markup=back_to_main_kb(), parse_mode="HTML")

    elif data == "menu_faq":
        await query.edit_message_text(FAQ_TEXT, reply_markup=back_to_main_kb(), parse_mode="HTML")

    elif data == "menu_about":
        await query.edit_message_text(ABOUT_TEXT, reply_markup=back_to_main_kb(), parse_mode="HTML")

    elif data == "menu_portfolio":
        await query.edit_message_text(
            "🎬 <b>ПОРТФОЛИО</b>\n\n"
            "Намунаи баъзе корҳои мо дар поён 👇\n\n"
            "📷 Барои намунаи бештари корҳои мо, лутфан ба саҳифаи "
            "Instagram-и мо гузаред.",
            reply_markup=portfolio_kb(), parse_mode="HTML",
        )

    elif data == "menu_contact":
        await query.edit_message_text(CONTACT_TEXT, reply_markup=contact_kb(), parse_mode="HTML")

    elif data.startswith("pkg_"):
        pkg_key = data[len("pkg_"):]
        pkg = PACKAGES.get(pkg_key)
        if pkg:
            await query.edit_message_text(pkg["text"], reply_markup=package_detail_kb(pkg_key), parse_mode="HTML")


async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Лутфан аз тугмаҳои меню истифода баред 👇", reply_markup=main_menu_kb()
    )


# ==================== ФАРМОИШИ ПУРРА (Conversation) ====================

async def choose_package_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pkg_key = query.data[len("choose_"):]
    pkg = PACKAGES.get(pkg_key)
    if not pkg:
        return ConversationHandler.END

    context.user_data["order_pkg"] = pkg
    await query.edit_message_text(
        f"✅ Шумо пакети <b>{pkg['short']}</b>-ро интихоб кардед.\n\n"
        "Барои сабти фармоиш, лутфан <b>номи худро</b> нависед:",
        parse_mode="HTML",
    )
    return ASK_NAME


async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order_name"] = update.message.text
    await update.message.reply_text(
        "📱 Лутфан <b>рақами телефони</b> худро нависед (масалан 93 882 97 96):",
        parse_mode="HTML",
    )
    return ASK_PHONE


async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order_phone"] = update.message.text
    await update.message.reply_text(
        "📅 Лутфан <b>санаи тӯйро</b> нависед (масалан 15.08.2026):",
        parse_mode="HTML",
    )
    return ASK_DATE


async def ask_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order_date"] = update.message.text
    user = update.message.from_user
    pkg = context.user_data.get("order_pkg", {})
    name = context.user_data.get("order_name", "—")
    phone = context.user_data.get("order_phone", "—")
    date = context.user_data.get("order_date", "—")

    await update.message.reply_text(
        "🎉 <b>Фармоиши шумо қабул шуд!</b>\n\n"
        f"Пакет: {pkg.get('short', '—')}\n"
        f"Ном: {name}\n"
        f"Телефон: {phone}\n"
        f"Санаи тӯй: {date}\n\n"
        "Ходими мо ба наздикӣ бо шумо тамос мегирад. Ташаккур! 🙏",
        reply_markup=after_order_kb(),
        parse_mode="HTML",
    )

    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=(
                    "🆕 <b>ФАРМОИШИ НАВ!</b>\n\n"
                    f"📦 Пакет: {pkg.get('short', '—')}\n"
                    f"👤 Ном: {name}\n"
                    f"📱 Телефон: {phone}\n"
                    f"📅 Санаи тӯй: {date}\n\n"
                    f"Telegram: @{user.username if user.username else '—'}\n"
                    f"User ID: {user.id}"
                ),
                parse_mode="HTML",
            )
        except Exception as e:
            logger.error(f"Хабар ба админ нарафт: {e}")

    context.user_data.clear()
    return ConversationHandler.END


async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Фармоиш бекор карда шуд.", reply_markup=main_menu_kb()
    )
    return ConversationHandler.END


# ==================== MAIN ====================

def main():
    if not BOT_TOKEN or BOT_TOKEN == "PUT_YOUR_BOT_TOKEN_HERE":
        print("⚠️  Лутфан аввал BOT_TOKEN-ро дар bot.py ё дар ENV variable гузоред!")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    order_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(choose_package_start, pattern="^choose_")],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
            ASK_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_date)],
        },
        fallbacks=[CommandHandler("cancel", cancel_order)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(order_conv)
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.ALL, unknown_message))

    print("🤖 SIMO.MEDIA bot кор карда истодааст...")
    application.run_polling()


if __name__ == "__main__":
    main()
