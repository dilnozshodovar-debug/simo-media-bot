# -*- coding: utf-8 -*-
"""
SIMO.MEDIA — Telegram bot (нусхаи такмилёфта v3)
Дизайни зебо, банер, оморҳо, тавсифҳо (карусел), фармоиши бо қадамҳо.

Барои иҷро:
1) pip install -r requirements.txt
2) Токени ботро аз @BotFather гиред
3) Дар поён BOT_TOKEN-ро гузоред
4) python bot.py
"""

import os
import logging
import random
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    ConversationHandler,
    filters,
)
from telegram.constants import ChatAction

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ==================== ТАНЗИМОТ ====================

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8864413053:AAFSNnOT6SgRsp3zD16fEMR_BsqBhiloim4")

ADMIN_IDS = [8336737421]

CONTACT_PHONE_DISPLAY = "+992 93 882 97 96"
CONTACT_PHONE_RAW = "992938829796"
WHATSAPP_LINK = f"https://wa.me/{CONTACT_PHONE_RAW}"
TELEGRAM_USERNAME = "@editor2202"
TELEGRAM_LINK = "https://t.me/editor2202"
INSTAGRAM_LINK = "https://www.instagram.com/iam_shodovar?igsh=Z3g1NHhrOXM5NGdl"

# Акси муқаддима (banner) — логотипи худи SIMO.MEDIA.
# Файли logo.png бояд дар ҳамон папкае бошад, ки bot.py ҷойгир аст (на дар зерпапка).
WELCOME_IMAGE_PATH = Path(__file__).parent / "logo.png"

# Расмҳои намунавӣ (акси касбии сифатнок) — метавонед бо акси воқеии кори худ иваз кунед
PORTFOLIO_PREVIEW_IMAGES = [
    "https://images.unsplash.com/photo-1519741497674-611481863552?w=1000&q=80",
    "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1000&q=80",
    "https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?w=1000&q=80",
]

PORTFOLIO_LINKS = [
    ("🎬 Намунаи клип — Reel", "https://www.instagram.com/reel/DYJFY9MoYnJ/?igsh=MWc4ZHNua2xyMzdkaw=="),
    ("📷 Барои намунаи бештари корҳои мо — Instagram", "https://www.instagram.com/iam_shodovar?igsh=Z3g1NHhrOXM5NGdl"),
]

# Тавсифҳои муштариён (карусел) — метавонед матни воқеиро гузоред
REVIEWS = [
    {
        "name": "Фарзона ва Илҳом",
        "stars": "⭐⭐⭐⭐⭐",
        "text": "Кори SIMO.MEDIA олиҷаноб буд! Ҳар лаҳзаи тӯи мо бо чунин сифати баланд сабт шуд, ки ҳар бор тамошо мекунем ва ба ҳаяҷон меоем. Ташаккури зиёд!",
    },
    {
        "name": "Муниса",
        "stars": "⭐⭐⭐⭐⭐",
        "text": "Хеле касбӣ ва масъулиятнок кор мекунанд. Клипи тӯёна аз ҳама беҳтарин буд, ҳамаи меҳмонон таъриф карданд!",
    },
    {
        "name": "Ҷамшед",
        "stars": "⭐⭐⭐⭐⭐",
        "text": "Наворбардорӣ бо дрон воқеан лаҳзаҳоро зинда кард. Тавсия медиҳам ба ҳар кас, ки мехоҳад тӯяшро дуруст сабт кунад.",
    },
]

# ==================== МАТНҲО ====================

WELCOME_TEXT = (
    "🎥 <b>SIMO.MEDIA</b>\n"
    "<i>✨ Хотираҳоро ба филмҳои ҷовидона табдил медиҳем ✨</i>\n"
    "━━━━━━━━━━━━━━━━━━\n\n"
    "Хуш омадед! 🤍\n\n"
    "Рӯзи арӯсӣ танҳо як бор такрор мешавад. Мо ҳар табассум, ҳар ашки шодӣ ва "
    "ҳар лаҳзаи зебои ин рӯзи фаромӯшнашавандаро бо сифати баланд сабт мекунем.\n\n"
    "🏆 Садҳо мизоҷи хушбахт — эътимоди онҳо натиҷаи кори мост.\n\n"
    "👇 <b>Лутфан аз менюи поён интихоб кунед:</b>"
)

STATS_TEXT = (
    "📊 <b>SIMO.MEDIA ДАР РАҚАМҲО</b>\n"
    "━━━━━━━━━━━━━━━━━━\n\n"
    "💍 <b>500+</b> тӯйи сабтшуда\n"
    "📅 <b>3+</b> сол таҷриба дар соҳа\n"
    "⭐ <b>4.9/5</b> баҳои муштариён\n"
    "🎬 <b>100%</b> фармоишҳои саривақт супоридашуда\n\n"
    "Рақамҳо худашон гап мезананд — эътимоди шумо арзиши мост 🤍"
)

ABOUT_TEXT = (
    "ℹ️ <b>Дар бораи SIMO.MEDIA</b>\n"
    "━━━━━━━━━━━━━━━━━━\n\n"
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
    "анҷом дода мешавад. Инчунин барои беҳтар намудани сифати тасвир аз "
    "зеҳни сунъӣ (AI) низ истифода мебарем.\n\n"
    "<b>SIMO.MEDIA — хотираҳоро ба филмҳои ҷовидона табдил медиҳем.</b> 💍"
)

WHY_US_TEXT = (
    "✨ <b>ЧАРО МАҲЗ SIMO.MEDIA?</b>\n"
    "━━━━━━━━━━━━━━━━━━\n\n"
    "📸 Таҷҳизоти муосир ва сифати баланд\n"
    "🎬 Монтажи касбӣ бо услуби замонавӣ\n"
    "🚁 Наворбардорӣ бо дрон\n"
    "💍 Сабти тамоми лаҳзаҳои муҳими тӯй\n"
    "⚡ Омодасозии зуд ва саривақтии мавод\n"
    "🤖 Истифодаи AI барои сифати беҳтари ранг\n"
    "🤝 Муносибати масъулиятнок ба ҳар як фармоишгар"
)

FAQ_TEXT = (
    "❓ <b>САВОЛҲОИ МАЪМУЛ</b>\n"
    "━━━━━━━━━━━━━━━━━━\n\n"
    "🔹 <b>Оё пеш аз тӯй вохӯрӣ мешавад?</b>\n"
    "Ҳа, тамоми ҷузъиётро пеш аз рӯзи тӯй муҳокима мекунем.\n\n"
    "🔹 <b>Пеш-пардохт лозим аст?</b>\n"
    "Ҳа, барои мустаҳкам кардани фармоиш кафолати андак гирифта мешавад.\n\n"
    "🔹 <b>Оё берун аз шаҳр меравед?</b>\n"
    "Ҳа, бо шартҳои иловагӣ ба навоҳии дигар низ меравем.\n\n"
    "🔹 <b>То кай мавод омода мешавад?</b>\n"
    "Вобаста ба пакет — аз 7 то 30 рӯз.\n\n"
    "Саволи дигар доред? Ба бахши 📞 Тамос гузаред."
)

CONTACT_TEXT = (
    "📞 <b>Барои машварат ва фармоиш</b>\n"
    "━━━━━━━━━━━━━━━━━━\n\n"
    f"☎️ Телефон: {CONTACT_PHONE_DISPLAY}\n"
    f"💬 WhatsApp: {CONTACT_PHONE_DISPLAY}\n"
    f"✈️ Telegram: {TELEGRAM_USERNAME}\n"
    f"📷 Instagram: намуна дар боло\n\n"
    "SIMO.MEDIA — Хотираҳоро ба вақт насупоред, онҳоро ба мо бовар кунед 🤍"
)

PACKAGES = {
    "standard": {
        "title": "🎥 STANDARD — 1500 сомонӣ",
        "short": "STANDARD (1500 сомонӣ)",
        "text": (
            "🎥 <b>STANDARD — 1500 сомонӣ</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "Интихоби беҳтарин барои сабти лаҳзаҳои муҳими тӯй.\n\n"
            "Ба пакет дохил мешавад:\n"
            "✔️ Наворбардории касбӣ\n"
            "✔️ Аксбардории касбӣ\n"
            "✔️ 1 адад камера\n"
            "✔️ 1 ҷуфт диски аслӣ (Original DVD)\n\n"
            "🎁 Тӯҳфа: 10 дона акси чопшуда\n"
            "⏳ Омодасозии мавод: 25–30 рӯз"
        ),
    },
    "vip": {
        "title": "🏆 VIP — 2000 сомонӣ",
        "short": "VIP (2000 сомонӣ)",
        "text": (
            "🏆 <b>VIP — 2000 сомонӣ</b>\n"
            "<i>🔥 Пешниҳоди маъмултарин дар байни мизоҷони мо</i>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "Сифати бештар, хотираҳои бештар.\n\n"
            "Ба пакет дохил мешавад:\n"
            "✔️ Наворбардории касбӣ\n"
            "✔️ Аксбардории касбӣ\n"
            "✔️ 1 адад камера\n"
            "✔️ 1 ҷуфт диски аслӣ (Original DVD)\n"
            "✔️ Флешкаи аслӣ (64 GB)\n"
            "✔️ 1 адад албоми зебои Wedding Day\n\n"
            "🎁 Тӯҳфа: 30 дона акси чопшуда\n"
            "⏳ Омодасозии мавод: 15–20 рӯз"
        ),
    },
    "vip_premium": {
        "title": "💎 VIP PREMIUM — 3000 сомонӣ",
        "short": "VIP PREMIUM (3000 сомонӣ)",
        "text": (
            "💎 <b>VIP PREMIUM — 3000 сомонӣ</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
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
            "🎁 Тӯҳфа: 50 дона акси чопшуда\n"
            "⏳ Омодасозии мавод: 7–10 рӯз"
        ),
    },
}

ASK_NAME, ASK_PHONE, ASK_DATE, CONFIRM = range(4)

# ==================== КЛАВИАТУРАҲО ====================

def main_menu_kb():
    kb = [
        [InlineKeyboardButton("🔥 Фармоиши фаврӣ", callback_data="menu_prices")],
        [InlineKeyboardButton("💰 Прайс-лист", callback_data="menu_prices"),
         InlineKeyboardButton("🎬 Портфолио", callback_data="menu_portfolio")],
        [InlineKeyboardButton("⭐ Тавсифҳо", callback_data="rev_0"),
         InlineKeyboardButton("📊 Дар рақамҳо", callback_data="menu_stats")],
        [InlineKeyboardButton("✨ Чаро маҳз мо?", callback_data="menu_why"),
         InlineKeyboardButton("❓ FAQ", callback_data="menu_faq")],
        [InlineKeyboardButton("ℹ️ Дар бораи мо", callback_data="menu_about")],
        [InlineKeyboardButton("📞 Тамос", callback_data="menu_contact")],
    ]
    return InlineKeyboardMarkup(kb)


def prices_menu_kb():
    kb = [
        [InlineKeyboardButton("🎥 STANDARD — 1500 сомонӣ", callback_data="pkg_standard")],
        [InlineKeyboardButton("🏆 VIP — 2000 сомонӣ (маъмултарин)", callback_data="pkg_vip")],
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
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Ба меню асосӣ", callback_data="menu_main")]])


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


def reviews_kb(index: int):
    total = len(REVIEWS)
    nav = []
    if total > 1:
        prev_i = (index - 1) % total
        next_i = (index + 1) % total
        nav = [
            InlineKeyboardButton("⬅️ Қаблӣ", callback_data=f"rev_{prev_i}"),
            InlineKeyboardButton("Баъдӣ ➡️", callback_data=f"rev_{next_i}"),
        ]
    kb = []
    if nav:
        kb.append(nav)
    kb.append([InlineKeyboardButton("⬅️ Ба меню асосӣ", callback_data="menu_main")])
    return InlineKeyboardMarkup(kb)


def after_order_kb():
    kb = [
        [InlineKeyboardButton("💬 WhatsApp", url=WHATSAPP_LINK)],
        [InlineKeyboardButton("⬅️ Ба меню асосӣ", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(kb)


def confirm_kb():
    kb = [
        [InlineKeyboardButton("✅ Тасдиқ ва фиристодан", callback_data="order_confirm")],
        [InlineKeyboardButton("✏️ Аз нав пур кардан", callback_data="order_restart")],
    ]
    return InlineKeyboardMarkup(kb)


def review_render(index: int) -> str:
    r = REVIEWS[index]
    return (
        "⭐ <b>ТАВСИФҲОИ МУШТАРИЁН</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"{r['stars']}\n"
        f"<i>«{r['text']}»</i>\n\n"
        f"— <b>{r['name']}</b>\n\n"
        f"({index + 1}/{len(REVIEWS)})"
    )


# ==================== ХЭНДЛЕРҲОИ АСОСӢ ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(WELCOME_IMAGE_PATH, "rb") as photo_file:
            await update.message.reply_photo(
                photo=photo_file,
                caption=WELCOME_TEXT,
                reply_markup=main_menu_kb(),
                parse_mode="HTML",
            )
    except Exception as e:
        logger.warning(f"Акс фиристода нашуд: {e}")
        await update.message.reply_text(WELCOME_TEXT, reply_markup=main_menu_kb(), parse_mode="HTML")


async def safe_edit(query, text, reply_markup=None):
    """Матни паёмро иваз мекунад; агар паём акс дошта бошад (caption), онро низ дуруст навсозӣ мекунад."""
    try:
        if query.message.photo:
            await query.edit_message_caption(caption=text, reply_markup=reply_markup, parse_mode="HTML")
        else:
            await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="HTML")
    except Exception as e:
        logger.warning(f"Edit нашуд: {e}")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    await context.bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.TYPING)

    if data == "menu_main":
        await safe_edit(query, WELCOME_TEXT, main_menu_kb())

    elif data == "menu_prices":
        await safe_edit(query, "💰 <b>ПРАЙС-ЛИСТИ SIMO.MEDIA</b>\n━━━━━━━━━━━━━━━━━━\n\nЛутфан пакетро интихоб кунед 👇", prices_menu_kb())

    elif data == "menu_why":
        await safe_edit(query, WHY_US_TEXT, back_to_main_kb())

    elif data == "menu_stats":
        await safe_edit(query, STATS_TEXT, back_to_main_kb())

    elif data == "menu_faq":
        await safe_edit(query, FAQ_TEXT, back_to_main_kb())

    elif data == "menu_about":
        await safe_edit(query, ABOUT_TEXT, back_to_main_kb())

    elif data == "menu_portfolio":
        try:
            media = [InputMediaPhoto(url) for url in PORTFOLIO_PREVIEW_IMAGES]
            await context.bot.send_media_group(chat_id=query.message.chat_id, media=media)
        except Exception as e:
            logger.warning(f"Галерея фиристода нашуд: {e}")
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=(
                "🎬 <b>ПОРТФОЛИО</b>\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "Намунаи сифати кори мо дар боло 👆\n\n"
                "📷 Барои намунаи бештари корҳои мо (видео ва клипҳо), лутфан ба саҳифаи "
                "Instagram-и мо гузаред 👇"
            ),
            reply_markup=portfolio_kb(),
            parse_mode="HTML",
        )

    elif data == "menu_contact":
        await safe_edit(query, CONTACT_TEXT, contact_kb())

    elif data.startswith("rev_"):
        index = int(data[len("rev_"):])
        await safe_edit(query, review_render(index), reviews_kb(index))

    elif data.startswith("pkg_"):
        pkg_key = data[len("pkg_"):]
        pkg = PACKAGES.get(pkg_key)
        if pkg:
            await safe_edit(query, pkg["text"], package_detail_kb(pkg_key))


async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Лутфан аз тугмаҳои меню истифода баред 👇", reply_markup=main_menu_kb())


# ==================== ФАРМОИШИ ПУРРА (Conversation бо қадамҳо) ====================

async def choose_package_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pkg_key = query.data[len("choose_"):]
    pkg = PACKAGES.get(pkg_key)
    if not pkg:
        return ConversationHandler.END

    context.user_data["order_pkg"] = pkg
    await safe_edit(
        query,
        f"✅ Шумо пакети <b>{pkg['short']}</b>-ро интихоб кардед.\n\n"
        "📝 <b>Қадами 1/3</b> — Лутфан <b>номи худро</b> нависед:",
    )
    return ASK_NAME


async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order_name"] = update.message.text
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    await update.message.reply_text(
        "📱 <b>Қадами 2/3</b> — Лутфан рақами телефони худро нависед (масалан 93 882 97 96):",
        parse_mode="HTML",
    )
    return ASK_PHONE


async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order_phone"] = update.message.text
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    await update.message.reply_text(
        "📅 <b>Қадами 3/3</b> — Лутфан санаи тӯйро нависед (масалан 15.08.2026):",
        parse_mode="HTML",
    )
    return ASK_DATE


async def ask_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order_date"] = update.message.text
    context.user_data["order_number"] = f"SM-{random.randint(1000, 9999)}"
    pkg = context.user_data.get("order_pkg", {})
    name = context.user_data.get("order_name", "—")
    phone = context.user_data.get("order_phone", "—")
    date = context.user_data.get("order_date", "—")
    order_number = context.user_data.get("order_number", "—")

    summary = (
        "🔎 <b>ЛУТФАН ТАСДИҚ КУНЕД</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"🔖 Рақами фармоиш: <b>{order_number}</b>\n"
        f"📦 Пакет: {pkg.get('short', '—')}\n"
        f"👤 Ном: {name}\n"
        f"📱 Телефон: {phone}\n"
        f"📅 Санаи тӯй: {date}\n\n"
        "Ҳама дуруст аст?"
    )
    await update.message.reply_text(summary, reply_markup=confirm_kb(), parse_mode="HTML")
    return CONFIRM


async def order_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await safe_edit(query, "📝 <b>Қадами 1/3</b> — Лутфан номи худро аз нав нависед:")
    return ASK_NAME


async def order_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    pkg = context.user_data.get("order_pkg", {})
    name = context.user_data.get("order_name", "—")
    phone = context.user_data.get("order_phone", "—")
    date = context.user_data.get("order_date", "—")
    order_number = context.user_data.get("order_number", "—")

    await safe_edit(
        query,
        "🎉 <b>Фармоиши шумо қабул шуд!</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"🔖 Рақами фармоиш: <b>{order_number}</b>\n"
        f"📦 Пакет: {pkg.get('short', '—')}\n"
        f"👤 Ном: {name}\n"
        f"📱 Телефон: {phone}\n"
        f"📅 Санаи тӯй: {date}\n\n"
        "Ходими мо ба наздикӣ бо шумо тамос мегирад. Ташаккур! 🙏\n\n"
        f"<i>Рақами {order_number}-ро нигоҳ доред — ҳангоми муроҷиат метавонед истифода баред.</i>",
        after_order_kb(),
    )

    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=(
                    "🆕 <b>ФАРМОИШИ НАВ!</b>\n"
                    "━━━━━━━━━━━━━━━━━━\n\n"
                    f"🔖 Рақами фармоиш: <b>{order_number}</b>\n"
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
    await update.message.reply_text("Фармоиш бекор карда шуд.", reply_markup=main_menu_kb())
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
            CONFIRM: [
                CallbackQueryHandler(order_confirm, pattern="^order_confirm$"),
                CallbackQueryHandler(order_restart, pattern="^order_restart$"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_order)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", start))
    application.add_handler(order_conv)
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.ALL, unknown_message))

    print("🤖 SIMO.MEDIA bot кор карда истодааст...")
    application.run_polling()


if __name__ == "__main__":
    main()
