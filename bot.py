# -*- coding: utf-8 -*-
"""
SIMO.MEDIA — Telegram bot (нусхаи касбии v15 Master)
- Иловаи Имзои Электронии Рақамӣ (Digital Signature Stamp) дар PDF
- Календари озода ва саҳеҳ
- Бехатарии 100% аз гум шудани омор ва маълумоти мизоҷон (/exportdb & /importdb)
- PDF Шартнома бе квадратҳои сиёҳ
- Командаҳои пурраи Админ ва Хизматрасониҳо
"""

import os
import re
import io
import random
import pickle
import logging
import calendar
from datetime import datetime, timezone, timedelta

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    ConversationHandler,
    PicklePersistence,
    filters,
)

# Модулҳо барои сохтани PDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ==================== ТАНЗИМИ ПАЙГИРИИ ХОТИРА ВА ШРИФТ ====================

def get_persistence_path():
    if os.path.exists("/data") and os.access("/data", os.W_OK):
        return "/data/bot_data.pkl"
    return "bot_data.pkl"

FONT_NAME = "Helvetica"

def get_pdf_font():
    global FONT_NAME
    possible_files = ["DejaVuSans.ttf", "TajikFont.ttf", "arial.ttf"]
    for font_file in possible_files:
        if os.path.exists(font_file) and os.path.getsize(font_file) > 10000:
            try:
                pdfmetrics.registerFont(TTFont("CustomTajikFont", font_file))
                FONT_NAME = "CustomTajikFont"
                return "CustomTajikFont", True
            except Exception as e:
                logger.error(f"Хато дар сабти {font_file}: {e}")
    
    FONT_NAME = "Helvetica"
    return "Helvetica", False

# ==================== ТАНЗИМОТИ АСОСӢ ====================

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8864413053:AAFSNnOT6SgRsp3zD16fEMR_BsqBhiloim4")
ADMIN_IDS = [8336737421]
BOT_USERNAME = "simoo129_bot"

CONTACT_PHONE_DISPLAY = "+992 93 882 97 96"
CONTACT_PHONE_RAW = "992938829796"
WHATSAPP_LINK = f"https://wa.me/{CONTACT_PHONE_RAW}"
TELEGRAM_USERNAME = "@editor2202"
TELEGRAM_LINK = "https://t.me/editor2202"
INSTAGRAM_LINK = "https://www.instagram.com/iam_shodovar?igsh=Z3g1NHhrOXM5NGdl"

WELCOME_IMAGE_URL = "https://raw.githubusercontent.com/dilnozshodovar-debug/simo-media-bot/main/logo.png"
ABOUT_IMAGE_URL = "https://raw.githubusercontent.com/dilnozshodovar-debug/simo-media-bot/main/about.jpg"

DEFAULT_REVIEWS = [
    {"name": "Фарзона ва Илҳом", "stars": "⭐⭐⭐⭐⭐",
     "tj": "Кори SIMO.MEDIA олиҷаноб буд! Ҳар лаҳзаи тӯи мо бо чунин сифати баланд сабт шуд, ки ҳар бор тамошо мекунем ва ба ҳаяҷон меоем.",
     "ru": "Работа SIMO.MEDIA была превосходной! Каждый момент нашей свадьбы был снят в высоком качестве."},
    {"name": "Муниса", "stars": "⭐⭐⭐⭐⭐",
     "tj": "Хеле касбӣ ва масъулиятнок кор мекунанд. Клипи тӯёна аз ҳама беҳтарин буд!",
     "ru": "Работают очень профессионально и ответственно. Свадебный клип получился лучшим!"},
    {"name": "Ҷамшед", "stars": "⭐⭐⭐⭐⭐",
     "tj": "Наворбардорӣ бо дрон воқеан лаҳзаҳоро зинда кард. Тавсия медиҳам!",
     "ru": "Съёмка с дрона по-настоящему оживила моменты. Рекомендую!"},
]

DEPOSIT_AMOUNT = "100 сомонӣ"
PAYMENT_LINK = "http://pay.expresspay.tj/?A=5058270376098736&s=100&c=&f1=133&FIELD2=&FIELD3="

# ==================== ХИЗМАТРАСОНИҲОИ ИЛОВАГӢ ====================

EXTRA_SERVICES_TEXTS = {
    "love_story": "❤️ <b>Love Story (Фотосессияи ошиқона)</b>\n━━━━━━━━━━━━━━━━━━\n\nМуҳаббати шумо сазовори беҳтарин хотираҳост!\nМо барои шумо фотосессияи ошиқона бо идеяҳои эҷодӣ, ҷойҳои зебо ва коркарди касбии аксҳоро омода мекунем.\n\n✨ <b>Аксҳои табиӣ • Коркарди касбӣ • Сифати олӣ</b>",
    "photo_print": "🖼 <b>Чопи аксҳо</b>\n━━━━━━━━━━━━━━━━━━\n\nХотираҳоро танҳо дар телефон нигоҳ надоред!\nАксҳои худро бо сифати баланд чоп намуда, ҳамчун туҳфа ё ороиши хона истифода баред.\n\n📏 <b>Андозаҳои гуногун • Рангҳои зинда • Коғази босифат</b>",
    "portraits": "🎨 <b>Портретҳо</b>\n━━━━━━━━━━━━━━━━━━\n\nНаздикони худро бо як туҳфаи махсус шод гардонед.\nМо аз акси шумо портретҳои зебо дар андозаҳои 20×30 то 60×90 омода менамоем.\n\n🎁 <b>Беҳтарин туҳфа барои зодрӯз ва ҷашнҳо.</b>",
    "ai_videos": "🤖 <b>Видеоҳои табрикотӣ бо AI</b>\n━━━━━━━━━━━━━━━━━━\n\nТабрикоте, ки ҳама аз он ҳайрон мешаванд!\nБо истифода аз технологияҳои зеҳни сунъӣ (AI) барои шумо видеоҳои табрикотии ҷолиб таҳия мекунем.\n\n🎉 <b>Барои зодрӯз • Тӯй • Ҷашнҳо • Ширкатҳо</b>",
    "promo_clips": "📢 <b>Роликҳои рекламавӣ</b>\n━━━━━━━━━━━━━━━━━━\n\nБизнеси худро бо рекламаи касбӣ муаррифӣ кунед.\nМо барои бренд, мағоза, тарабхона ва дигар соҳибкорон роликҳои ҷолиб омода мекунем.\n\n📈 <b>Рекламаи хуб = Мизоҷони бештар</b>",
    "ad_filming": "🎥 <b>Наворбардории реклама</b>\n━━━━━━━━━━━━━━━━━━\n\nБо камераҳои касбӣ ва таҷҳизоти муосир аз маҳсулот ё хизматрасонии шумо наворбардорӣ мекунем.\n\n✨ <b>Навори босифат барои Instagram, TikTok ва YouTube.</b>",
    "clips_concerts": "🎤 <b>Клип ва консерт</b>\n━━━━━━━━━━━━━━━━━━\n\nНаворбардорӣ ва монтажи касбии клипҳои мусиқӣ ва консертҳо бо сифати баланд ва услуби муосир.",
    "video_editing": "🎬 <b>Монтажи видео</b>\n━━━━━━━━━━━━━━━━━━\n\nВидеоҳои худро ба сатҳи нав бардоред!\nМо ҳама гуна видеоҳоро (Reels, TikTok, YouTube, Тӯйҳо) бо услуби касбӣ монтаж мекунем.",
}

# ==================== МАТНҲО ВА ПАКЕТҲО ====================

BTN = {
    "tj": {
        "urgent": "🔥 Фармоиши фаврӣ", "prices": "💰 Прайс-лист", "portfolio": "🎬 Портфолио",
        "extra_services": "🎬 Хизматрасониҳои иловагӣ", "reviews": "⭐ Тавсифҳо", "stats": "📊 Дар рақамҳо",
        "why": "✨ Чаро маҳз мо?", "faq": "❓ FAQ", "about": "ℹ️ Дар бораи мо", "contact": "📞 Тамос",
        "availability": "📅 Санҷиши сана", "track": "📋 Пайгирии фармоиш",
        "referral": "🎁 Даъвати дӯстон", "lang": "🇷🇺 На русском",
        "back": "⬅️ Ба менюи асосӣ", "back_prices": "⬅️ Ба прайс-лист",
        "order": "✅ Ин пакетро фармоиш медиҳам",
        "whatsapp": "💬 WhatsApp", "telegram": "✈️ Telegram", "instagram": "📷 Instagram",
    },
    "ru": {
        "urgent": "🔥 Быстрый заказ", "prices": "💰 Прайс-лист", "portfolio": "🎬 Портфолио",
        "extra_services": "🎬 Доп. услуги SIMO.MEDIA", "reviews": "⭐ Отзывы", "stats": "📊 В цифрах",
        "why": "✨ Почему мы?", "faq": "❓ FAQ", "about": "ℹ️ О нас", "contact": "📞 Контакты",
        "availability": "📅 Проверить дату", "track": "📋 Отследить заказ",
        "referral": "🎁 Пригласить друзей", "lang": "🇹🇯 Тоҷикӣ",
        "back": "⬅️ Главное меню", "back_prices": "⬅️ К прайс-листу",
        "order": "✅ Заказать этот пакет",
        "whatsapp": "💬 WhatsApp", "telegram": "✈️ Telegram", "instagram": "📷 Instagram",
    },
}

TEXT = {
    "welcome": {
        "tj": ("🎥 <b>SIMO.MEDIA</b>\n<i>✨ Хотираҳоро ба филмҳои ҷовидона табдил медиҳем ✨</i>\n"
               "━━━━━━━━━━━━━━━━━━\n\n🤍 Хуш омадед!\n\n"
               "Рӯзи арӯсӣ яке аз муҳимтарин ва фаромӯшнашавандатарин рӯзҳои зиндагист. Мо ҳар табассум, "
               "ҳар ашки шодӣ ва ҳар лаҳзаи пур аз эҳсосоти ин рӯзи махсусро бо сифати баланд ва услуби "
               "касбӣ сабт намуда, онҳоро ба филме табдил медиҳем.\n\n"
               "👇 Лутфан аз менюи поён яке аз бахшҳоро интихоб намоед:"),
        "ru": ("🎥 <b>SIMO.MEDIA</b>\n<i>✨ Превращаем воспоминания в вечные фильмы ✨</i>\n"
               "━━━━━━━━━━━━━━━━━━\n\n🤍 Добро пожаловать!\n\n"
               "👇 Пожалуйста, выберите один из разделов в меню ниже:"),
    },
    "stats": {
        "tj": ("📊 <b>SIMO.MEDIA ДАР РАҚАМҲО</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               "💍 <b>500+</b> тӯйи сабтшуда\n📅 <b>3+</b> сол таҷриба\n"
               "⭐ <b>4.9/5</b> баҳои муштариён\n🎬 <b>100%</b> фармоишҳои саривақт супоридашуда"),
        "ru": ("📊 <b>SIMO.MEDIA В ЦИФРАХ</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               "💍 <b>500+</b> отснятых свадеб\n📅 <b>3+</b> года опыта\n"
               "⭐ <b>4.9/5</b> оценка клиентов\n🎬 <b>100%</b> заказов сдано вовремя"),
    },
    "about": {
        "tj": ("ℹ️ <b>Дар бораи SIMO.MEDIA</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               "SIMO.MEDIA — студияи касбии наворбардории тӯй таҳти роҳбарии "
               "<b>Шодовар Нуриддинов</b> мебошад.\n\n"
               "📅 Студияи мо аз 20 феврали соли 2023 фаъолияти расмии худро оғоз намуд.\n\n"
               "<b>SIMO.MEDIA — хотираҳоро ба филмҳои ҷовидона табдил медиҳем.</b> 💍"),
        "ru": ("ℹ️ <b>О SIMO.MEDIA</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               "SIMO.MEDIA — профессиональная студия свадебной видеосъёмки под руководством "
               "<b>Шодовара Нуриддинова</b>.\n\n"
               "<b>SIMO.MEDIA — превращаем воспоминания в вечные фильмы.</b> 💍"),
    },
    "why": {
        "tj": "✨ <b>ЧАРО МАҲЗ SIMO.MEDIA?</b>\n━━━━━━━━━━━━━━━━━━\n\n📸 Таҷҳизоти муосир ва сифати баланд\n🎬 Монтажи касбӣ бо услуби замонавӣ\n🚁 Наворбардорӣ бо дрон\n💍 Сабти тамоми лаҳзаҳои муҳими тӯй",
        "ru": "✨ <b>ПОЧЕМУ ИМЕННО SIMO.MEDIA?</b>\n━━━━━━━━━━━━━━━━━━\n\n📸 Современное оборудование и высокое качество\n🎬 Профессиональный монтаж\n🚁 Съёмка с дрона",
    },
    "faq": {
        "tj": "❓ <b>САВОЛҲОИ МАЪМУЛ</b>\n━━━━━━━━━━━━━━━━━━\n\n🔹 <b>Оё пеш аз тӯй вохӯрӣ мешавад?</b>\nҲа, тамоми ҷузъиётро пеш муҳокима мекунем.\n\n🔹 <b>То кай мавод омода мешавад?</b>\nАз 7 то 30 рӯз.",
        "ru": "❓ <b>ЧАСТЫЕ ВОПРОСЫ</b>\n━━━━━━━━━━━━━━━━━━\n\n🔹 <b>Есть ли встреча перед свадьбой?</b>\nДа, мы обсуждаем все детали заранее.",
    },
    "contact": {
        "tj": f"📞 <b>Барои машварат ва фармоиш</b>\n━━━━━━━━━━━━━━━━━━\n\n☎️ Телефон: {CONTACT_PHONE_DISPLAY}\n💬 WhatsApp: {CONTACT_PHONE_DISPLAY}\n✈️ Telegram: {TELEGRAM_USERNAME}",
        "ru": f"📞 <b>Для консультации и заказа</b>\n━━━━━━━━━━━━━━━━━━\n\n☎️ Телефон: {CONTACT_PHONE_DISPLAY}\n💬 WhatsApp: {CONTACT_PHONE_DISPLAY}\n✈️ Telegram: {TELEGRAM_USERNAME}",
    },
    "prices_title": {"tj": "💰 <b>ПРАЙС-ЛИСТИ SIMO.MEDIA</b>\n━━━━━━━━━━━━━━━━━━\n\nЛутфан пакетро интихоб кунед 👇", "ru": "💰 <b>ПРАЙС-ЛИСТ SIMO.MEDIA</b>\n━━━━━━━━━━━━━━━━━━\n\nВыберите пакет 👇"},
    "ask_name": {"tj": "📝 <b>Қадами 1/4</b> — Лутфан <b>номи худро</b> нависед:", "ru": "📝 <b>Шаг 1/4</b> — Напишите <b>ваше имя</b>:"},
    "ask_phone": {"tj": "📱 <b>Қадами 2/4</b> — Лутфан рақами телефони худро нависед (масалан 93 882 97 96):", "ru": "📱 <b>Шаг 2/4</b> — Напишите ваш номер телефона:"},
    "phone_invalid": {"tj": "⚠️ Рақами телефон нодуруст аст. Лутфан танҳо рақамҳо нависед:", "ru": "⚠️ Неверный номер телефона:"},
    "ask_date_cal": {"tj": "📅 <b>Қадами 3/4</b> — Лутфан <b>санаи тӯйро аз календари зерин интихоб кунед</b>:\n\nРақамҳо (1, 2, 3...) — Санаи озод\n🔴 — Санаи банд", "ru": "📅 <b>Шаг 3/4</b> — Выберите <b>дату свадьбы из календаря</b>:"},
    "ask_payment": {"tj": f"💳 <b>Қадами 4/4</b> — Оё ҳоло мехоҳед пешпардохт кунед?\n\nПешпардохт: {DEPOSIT_AMOUNT}", "ru": f"💳 <b>Шаг 4/4</b> — Хотите внести предоплату сейчас?\n\nПредоплата: {DEPOSIT_AMOUNT}"},
    "payment_link_text": {"tj": f"💳 <b>Пешпардохти {DEPOSIT_AMOUNT}</b>\n━━━━━━━━━━━━━━━━━━\n\n🔗 {PAYMENT_LINK}\n\nБаъди пардохт чекро (скриншот) фиристед 👇", "ru": f"💳 <b>Предоплата {DEPOSIT_AMOUNT}</b>\n━━━━━━━━━━━━━━━━━━\n\n🔗 {PAYMENT_LINK}\n\nОтправьте чек после оплаты 👇"},
    "ask_receipt": {"tj": "📸 <b>Чеки пардохт</b>\n━━━━━━━━━━━━━━━━━━\n\nЛутфан расми чекро фиристед.", "ru": "📸 <b>Чек оплаты</b>\n━━━━━━━━━━━━━━━━━━\n\nОтправьте фото чека."},
    "receipt_received": {"tj": "✅ Чек гирифта шуд!", "ru": "✅ Чек получен!"},
    "order_accepted": {"tj": "🎉 <b>Дархости шумо бомуваффақият сабт гардид!</b>", "ru": "🎉 <b>Ваша заявка успешно сохранена!</b>"},
    "order_thanks": {"tj": "Ташаккур, ки SIMO.MEDIA-ро интихоб намудед. 🤍\n\nШартнома ва чеки шумо бо <b>Имзои Электронии Рақамӣ (Digital Signature)</b> дар файли PDF-и зерин омода шуд 👇", "ru": "Спасибо, что выбрали SIMO.MEDIA. 🤍\n\nВаш договор готов с <b>цифровой подписью</b> в PDF 👇"},
    "ask_track_number": {"tj": "📋 <b>Пайгирии фармоиш</b>\n━━━━━━━━━━━━━━━━━━\n\nЛутфан рақами фармоишро нависед (масалан SM-4821):", "ru": "📋 <b>Отслеживание заказа</b>\n━━━━━━━━━━━━━━━━━━\n\nНапишите номер вашего заказа:"},
    "track_not_found": {"tj": "❌ Фармоише бо ин рақам ёфт нашуд.", "ru": "❌ Заказ с таким номером не найден."},
}

PACKAGES = {
    "standard": {
        "short": "STANDARD (1500 сомонӣ)",
        "price": 1500,
        "text": {
            "tj": "🎥 <b>STANDARD — 1500 сомонӣ</b>\n━━━━━━━━━━━━━━━━━━\n\n✔️ Наворбардории касбӣ\n✔️ Аксбардории касбӣ\n✔️ 1 адад камера\n✔️ 1 ҷуфт диски аслӣ\n\n🎁 Тӯҳфа: 10 дона акси чопшуда\n⏳ Омодасозии мавод: 25–30 рӯз",
            "ru": "🎥 <b>STANDARD — 1500 сомони</b>\n━━━━━━━━━━━━━━━━━━\n\n✔️ Профессиональная видеосъёмка\n✔️ Профессиональная фотосъёмка\n✔️ 1 камера\n✔️ 1 оригинальный DVD-диск\n\n🎁 Подарок: 10 печатных фото",
        },
    },
    "vip": {
        "short": "VIP (2000 сомонӣ)",
        "price": 2000,
        "text": {
            "tj": "👑 <b>VIP — 2000 сомонӣ</b>\n━━━━━━━━━━━━━━━━━━\n\n✔️ Наворбардории касбӣ\n✔️ Аксбардории касбӣ\n✔️ 1 адад камера\n✔️ 1 ҷуфт диски аслӣ\n✔️ Флешкаи аслӣ (64 GB)\n✔️ 1 адад албоми Wedding Day\n\n🎁 Тӯҳфа: 30 дона акси чопшуда\n⏳ Омодасозии мавод: 15–20 рӯз",
            "ru": "👑 <b>VIP — 2000 сомони</b>\n━━━━━━━━━━━━━━━━━━\n\n✔️ Профессиональная видеосъёмка\n✔️ Профессиональная фотосъёмка\n✔️ 1 камера\n✔️ Флешка (64 GB)\n✔️ Альбом Wedding Day",
        },
    },
    "vip_premium": {
        "short": "VIP PREMIUM (3000 сомонӣ)",
        "price": 3000,
        "text": {
            "tj": "💎 <b>VIP PREMIUM — 3000 сомонӣ</b>\n━━━━━━━━━━━━━━━━━━\n\n✔️ Наворбардории касбӣ\n✔️ Аксбардории касбӣ\n✔️ 1 адад камера\n✔️ Операторский кран\n✔️ Клипи тӯёна\n✔️ Love Story\n✔️ Флешкаи аслӣ (64 GB)\n✔️ Албоми Wedding Day\n\n🎁 Тӯҳфа: 50 дона акси чопшуда\n⏳ Омодасозии мавод: 7–10 рӯз",
            "ru": "💎 <b>VIP PREMIUM — 3000 сомони</b>\n━━━━━━━━━━━━━━━━━━\n\n✔️ Профессиональная видеосъёмка\n✔️ Свадебный клип\n✔️ Love Story\n✔️ Альбом Wedding Day",
        },
    },
}

ASK_NAME, ASK_PHONE, ASK_DATE, PAYMENT_CHOICE, ASK_RECEIPT, CONFIRM, ASK_PROMO = range(7)

# ==================== ФУНКСИЯҲОИ КӮМАКӢ ====================

def get_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("lang", "tj")

def t(key: str, lang: str) -> str:
    return TEXT[key][lang]

def validate_phone(text: str) -> bool:
    digits = re.sub(r"[^\d]", "", text)
    return 7 <= len(digits) <= 15

# ==================== ГЕНЕРАТОРИ КИБОРД ДАР КАЛЕНДАР ====================

def generate_calendar_keyboard(year: int, month: int, booked_dates: dict):
    kb = []
    month_names = ["Январ", "Феврал", "Март", "Апрел", "Май", "Июн", "Июл", "Август", "Сентябр", "Октябр", "Ноябр", "Декабр"]
    
    kb.append([InlineKeyboardButton(f"📅 {month_names[month-1]} {year}", callback_data="cal_ignore")])
    
    week_days = ["Дш", "Сш", "Чш", "Пш", "Ҷм", "Шб", "Як"]
    kb.append([InlineKeyboardButton(day, callback_data="cal_ignore") for day in week_days])
    
    cal = calendar.monthcalendar(year, month)
    for week in cal:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data="cal_ignore"))
            else:
                date_str = f"{day:02d}.{month:02d}.{year}"
                is_booked = date_str in booked_dates
                btn_text = f"{day} 🔴" if is_booked else f"{day}"
                row.append(InlineKeyboardButton(btn_text, callback_data=f"cal_date_{date_str}"))
        kb.append(row)
        
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    kb.append([
        InlineKeyboardButton("◀️ Қаблӣ", callback_data=f"cal_nav_{prev_year}_{prev_month}"),
        InlineKeyboardButton("Баъдӣ ▶️", callback_data=f"cal_nav_{next_year}_{next_month}")
    ])
    return InlineKeyboardMarkup(kb)

# ==================== ГЕНЕРАТОРИ ФАЙЛИ PDF БО ИМЗОИ ЭЛЕКТРОНӢ ====================

def create_contract_pdf(order_num, name, phone, date, pkg_name, price, prepay_status, user_id=None):
    font_name, has_custom_font = get_pdf_font()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    now_str = datetime.now().strftime('%d.%m.%Y %H:%M')
    uid_str = str(user_id) if user_id else "8336737421"
    
    if has_custom_font:
        title = "ШАРТНОМАИ РАСМИИ SIMO.MEDIA"
        subtitle = "Студияи наворбардорӣ ва таҳияи контент"
        lbl_order = f"Рақами фармоиш: {order_num}"
        lbl_created = f"Таърихи сабт: {now_str}"
        lbl_name = f"Ному насаби мизоҷ: {name}"
        lbl_phone = f"Рақами телефон: {phone}"
        lbl_date = f"Санаи тӯй: {date}"
        lbl_pkg = f"Пакет: {pkg_name}"
        lbl_price = f"Маблағи умумӣ: {price} сомонӣ"
        lbl_prepay = f"Ҳолати пешпардохт: {prepay_status}"
        lbl_terms = "Шартҳои шартнома:"
        t1 = "1. Студия сифати баланди наворбардорӣ ва аксбардориро кафолат медиҳад."
        t2 = "2. Мӯҳлати супоридани мавод аз пакети интихобшуда вобаста аст (7-30 рӯз)."
        t3 = "3. SIMO.MEDIA барои нигоҳдории бехатарии маводҳои сабтшуда масъул аст."
        lbl_exec = "Роҳбари студия: Шодовар Нуриддинов"
        lbl_sign = "Имзои мизоҷ: ____________"
    else:
        title = "SIMO.MEDIA - SHARTNOMAI RASMI"
        subtitle = "Studioi navorbardori va tahiyai content"
        lbl_order = f"Raqami farmoish: {order_num}"
        lbl_created = f"Ta'rikhi sabt: {now_str}"
        lbl_name = f"Nomu nasabi mizoj: {name}"
        lbl_phone = f"Raqami telefon: {phone}"
        lbl_date = f"Sanai tuy: {date}"
        lbl_pkg = f"Paket: {pkg_name}"
        lbl_price = f"Mablaghi umumii: {price} TJS"
        lbl_prepay = f"Holati peshpardokht: {prepay_status}"
        lbl_terms = "Sharthoi shartnoma:"
        t1 = "1. Studio sifati balandi navorbardori va aksbardoriro kafolat medihad."
        t2 = "2. Muxlati suporidani mavod az paketi intikhooshuda vobasta ast."
        t3 = "3. SIMO.MEDIA baroi nigohdorii bekhatarii mavodho mas'ul ast."
        lbl_exec = "Rohbari studio: Shodovar Nuriddinov"
        lbl_sign = "Imzoi mizoj: ____________"

    p.setFont(font_name, 16)
    p.drawString(120, 750, title)
    p.setFont(font_name, 10)
    p.drawString(180, 735, subtitle)
    p.line(50, 720, 550, 720)
    
    p.setFont(font_name, 11)
    p.drawString(50, 680, lbl_order)
    p.drawString(50, 660, lbl_created)
    
    p.setFont(font_name, 10)
    p.drawString(50, 620, lbl_name)
    p.drawString(50, 600, lbl_phone)
    p.drawString(50, 580, lbl_date)
    p.drawString(50, 560, lbl_pkg)
    p.drawString(50, 540, lbl_price)
    p.drawString(50, 520, lbl_prepay)
    
    p.line(50, 500, 550, 500)
    p.setFont(font_name, 11)
    p.drawString(50, 470, lbl_terms)
    p.setFont(font_name, 9)
    p.drawString(50, 450, t1)
    p.drawString(50, 432, t2)
    p.drawString(50, 414, t3)

    # --- ИЛОВАИ ИМЗОИ ЭЛЕКТРОНИИ РАҚАМӢ (DIGITAL SIGNATURE STAMP) ---
    p.setLineWidth(1)
    p.setStrokeColorRGB(0.1, 0.5, 0.2) # Чорчӯбаи сабзи касбӣ
    p.rect(50, 290, 500, 75)
    
    if has_custom_font:
        p.setFont(font_name, 10)
        p.drawString(60, 350, "✔ ТАСДИҚИ РАҚАМИИ SIMO.MEDIA (DIGITAL SIGNATURE)")
        p.setFont(font_name, 8)
        p.drawString(60, 333, f"Имзокунанда (Telegram ID): {uid_str}")
        p.drawString(60, 318, f"Таърихи тасдиқи рақамӣ: {now_str}")
        p.drawString(60, 303, f"Коди бехатарӣ: VERIFIED-{order_num}-{uid_str[-4:]}")
        p.drawString(340, 333, "Ҳолат: РАСМАН ТАСДИҚ ШУД")
        p.drawString(340, 318, "Студия: SIMO.MEDIA Studio")
        p.drawString(340, 303, "Пайванд: t.me/simoo129_bot")
    else:
        p.setFont(font_name, 10)
        p.drawString(60, 350, "✔ SIMO.MEDIA DIGITAL SIGNATURE (VERIFIED)")
        p.setFont(font_name, 8)
        p.drawString(60, 333, f"Telegram ID: {uid_str}")
        p.drawString(60, 318, f"Verified Date: {now_str}")
        p.drawString(60, 303, f"Security Hash: VERIFIED-{order_num}-{uid_str[-4:]}")
        p.drawString(340, 333, "Status: OFFICIAL CONTRACT")
        p.drawString(340, 318, "Studio: SIMO.MEDIA Studio")
        p.drawString(340, 303, "Link: t.me/simoo129_bot")

    p.setFont(font_name, 10)
    p.drawString(50, 240, lbl_exec)
    p.drawString(350, 240, lbl_sign)
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# ==================== КЛАВИАТУРАҲО ====================

def main_menu_kb(lang: str):
    b = BTN[lang]
    kb = [
        [InlineKeyboardButton(b["urgent"], callback_data="menu_prices")],
        [InlineKeyboardButton(b["prices"], callback_data="menu_prices"), InlineKeyboardButton(b["portfolio"], callback_data="menu_portfolio")],
        [InlineKeyboardButton(b["extra_services"], callback_data="menu_extra_services")],
        [InlineKeyboardButton(b["availability"], callback_data="menu_availability"), InlineKeyboardButton(b["track"], callback_data="menu_track")],
        [InlineKeyboardButton(b["reviews"], callback_data="rev_0"), InlineKeyboardButton(b["stats"], callback_data="menu_stats")],
        [InlineKeyboardButton(b["why"], callback_data="menu_why"), InlineKeyboardButton(b["faq"], callback_data="menu_faq")],
        [InlineKeyboardButton(b["about"], callback_data="menu_about"), InlineKeyboardButton(b["referral"], callback_data="menu_referral")],
        [InlineKeyboardButton(b["contact"], callback_data="menu_contact")],
        [InlineKeyboardButton(b["lang"], callback_data="toggle_lang")],
    ]
    return InlineKeyboardMarkup(kb)

def extra_services_kb(lang: str):
    b = BTN[lang]
    kb = [
        [InlineKeyboardButton("❤️ Love Story", callback_data="extra_svc_love_story")],
        [InlineKeyboardButton("🖼 Чопи аксҳо", callback_data="extra_svc_photo_print")],
        [InlineKeyboardButton("🎨 Портретҳо", callback_data="extra_svc_portraits")],
        [InlineKeyboardButton("🤖 Видеоҳои табрикотӣ бо AI", callback_data="extra_svc_ai_videos")],
        [InlineKeyboardButton("📢 Таҳияи роликҳои рекламавӣ", callback_data="extra_svc_promo_clips")],
        [InlineKeyboardButton("🎥 Наворбардории реклама", callback_data="extra_svc_ad_filming")],
        [InlineKeyboardButton("🎤 Клип ва консертҳо", callback_data="extra_svc_clips_concerts")],
        [InlineKeyboardButton("🎬 Ҳама намудҳои монтажи видео", callback_data="extra_svc_video_editing")],
        [InlineKeyboardButton(b["back"], callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(kb)

def prices_menu_kb(lang: str):
    b = BTN[lang]
    kb = [
        [InlineKeyboardButton("🎥 STANDARD — 1500 сомонӣ", callback_data="pkg_standard")],
        [InlineKeyboardButton("👑 VIP — 2000 сомонӣ", callback_data="pkg_vip")],
        [InlineKeyboardButton("💎 VIP PREMIUM — 3000 сомонӣ", callback_data="pkg_vip_premium")],
        [InlineKeyboardButton(b["back"], callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(kb)

def back_to_main_kb(lang: str):
    return InlineKeyboardMarkup([[InlineKeyboardButton(BTN[lang]["back"], callback_data="menu_main")]])

# ==================== ХЭНДЛЕРҲОИ АСОСӢ ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    user = update.effective_user
    context.bot_data.setdefault("all_users", {})[user.id] = {"name": user.full_name, "username": user.username}

    try:
        await update.message.reply_photo(
            photo=WELCOME_IMAGE_URL,
            caption=t("welcome", lang),
            reply_markup=main_menu_kb(lang),
            parse_mode="HTML",
        )
    except Exception:
        await update.message.reply_text(t("welcome", lang), reply_markup=main_menu_kb(lang), parse_mode="HTML")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    lang = get_lang(context)

    if data == "toggle_lang":
        new_lang = "ru" if lang == "tj" else "tj"
        context.user_data["lang"] = new_lang
        await query.edit_message_caption(caption=t("welcome", new_lang), reply_markup=main_menu_kb(new_lang), parse_mode="HTML")

    elif data == "menu_main":
        await query.edit_message_caption(caption=t("welcome", lang), reply_markup=main_menu_kb(lang), parse_mode="HTML")

    elif data == "menu_extra_services":
        await query.edit_message_caption(caption="🎬 <b>Хизматрасониҳои иловагии SIMO.MEDIA</b>\n\nЯке аз бахшҳоро интихоб кунед:", reply_markup=extra_services_kb(lang), parse_mode="HTML")

    elif data.startswith("extra_svc_"):
        svc_key = data[len("extra_svc_"):]
        svc_text = EXTRA_SERVICES_TEXTS.get(svc_key, "")
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✍️ Фармоиш диҳед", callback_data=f"order_extra_{svc_key}")],
            [InlineKeyboardButton("⬅️ Бозгашт", callback_data="menu_extra_services")]
        ])
        await query.edit_message_caption(caption=svc_text, reply_markup=kb, parse_mode="HTML")

    elif data.startswith("order_extra_"):
        await query.edit_message_caption(caption=f"✅ <b>Фармоиши шумо қабул шуд!</b>\n\nБарои тасдиқ бо мо дар тамос шавед:\n📞 {CONTACT_PHONE_DISPLAY}", reply_markup=back_to_main_kb(lang), parse_mode="HTML")

    elif data == "menu_prices":
        await query.edit_message_caption(caption=t("prices_title", lang), reply_markup=prices_menu_kb(lang), parse_mode="HTML")

    elif data.startswith("pkg_"):
        pkg_key = data[len("pkg_"):]
        pkg = PACKAGES.get(pkg_key)
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Ин пакетро фармоиш медиҳам", callback_data=f"choose_{pkg_key}")],
            [InlineKeyboardButton("⬅️ Ба прайс-лист", callback_data="menu_prices")]
        ])
        await query.edit_message_caption(caption=pkg["text"][lang], reply_markup=kb, parse_mode="HTML")

    elif data == "menu_availability":
        now = datetime.now()
        booked = context.bot_data.get("booked_dates", {})
        kb = generate_calendar_keyboard(now.year, now.month, booked)
        await query.edit_message_caption(caption="📅 <b>Календари санҷиши сана:</b>\n\nРақамҳо (1, 2, 3...) — Санаи озод\n🔴 — Санаи банд", reply_markup=kb, parse_mode="HTML")

    elif data.startswith("cal_nav_"):
        _, _, y, m = data.split("_")
        booked = context.bot_data.get("booked_dates", {})
        kb = generate_calendar_keyboard(int(y), int(m), booked)
        await query.edit_message_reply_markup(reply_markup=kb)

    elif data.startswith("cal_date_"):
        selected_date = data.split("_")[2]
        booked = context.bot_data.get("booked_dates", {})
        if selected_date in booked:
            await query.answer(f"⚠️ Санаи {selected_date} аллакай банд аст!", show_alert=True)
        else:
            await query.answer(f"✅ Санаи {selected_date} озод аст!", show_alert=True)

    elif data == "menu_track":
        context.user_data["awaiting"] = "track"
        await query.edit_message_caption(caption=t("ask_track_number", lang), reply_markup=back_to_main_kb(lang), parse_mode="HTML")

    elif data == "menu_stats":
        await query.edit_message_caption(caption=t("stats", lang), reply_markup=back_to_main_kb(lang), parse_mode="HTML")

    elif data == "menu_about":
        await query.edit_message_caption(caption=t("about", lang), reply_markup=back_to_main_kb(lang), parse_mode="HTML")

    elif data == "menu_why":
        await query.edit_message_caption(caption=t("why", lang), reply_markup=back_to_main_kb(lang), parse_mode="HTML")

    elif data == "menu_faq":
        await query.edit_message_caption(caption=t("faq", lang), reply_markup=back_to_main_kb(lang), parse_mode="HTML")

    elif data == "menu_contact":
        await query.edit_message_caption(caption=t("contact", lang), reply_markup=back_to_main_kb(lang), parse_mode="HTML")

    elif data.startswith("rev_"):
        index = int(data[len("rev_"):])
        custom_revs = context.bot_data.get("custom_reviews", [])
        all_revs = DEFAULT_REVIEWS + custom_revs
        total = len(all_revs)
        r = all_revs[index % total]
        
        text = f"⭐ <b>ТАВСИФҲОИ МУШТАРИЁН</b> ({index + 1}/{total})\n━━━━━━━━━━━━━━━━━━\n\n{r.get('stars', '⭐⭐⭐⭐⭐')}\n<i>«{r.get(lang, r.get('tj', ''))}»</i>\n\n— <b>{r['name']}</b>"
        
        nav = [
            InlineKeyboardButton("⬅️ Қаблӣ", callback_data=f"rev_{(index - 1) % total}"),
            InlineKeyboardButton("Баъдӣ ➡️", callback_data=f"rev_{(index + 1) % total}")
        ]
        kb = InlineKeyboardMarkup([nav, [InlineKeyboardButton("⬅️ Меню", callback_data="menu_main")]])
        await query.edit_message_caption(caption=text, reply_markup=kb, parse_mode="HTML")

# ==================== ПАЙГИРИИ ФАРМОИШ БО ПРОГРЕСС-БАР ====================

async def handle_tracking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting") == "track":
        context.user_data.pop("awaiting", None)
        order_num = update.message.text.strip().upper()
        orders = context.bot_data.get("orders", {})
        order = orders.get(order_num)
        
        if not order:
            await update.message.reply_text(t("track_not_found", get_lang(context)), reply_markup=back_to_main_kb(get_lang(context)))
            return

        p1, p2, p3, p4 = order.get("p1", 100), order.get("p2", 0), order.get("p3", 0), order.get("p4", 0)

        def icon(p): return "🟩" if p == 100 else ("🟨" if p > 0 else "⬜")

        text = (
            f"📈 <b>Пайгирии фармоиши {order_num}</b>\n━━━━━━━━━━━━━━━━━━\n\n"
            f"{icon(p1)} Наворбардорӣ ва воридсозӣ — <b>{p1}%</b>\n"
            f"{icon(p2)} Интихоби мусиқӣ ва садо — <b>{p2}%</b>\n"
            f"{icon(p3)} Монтаж ва Color Grading — <b>{p3}%</b>\n"
            f"{icon(p4)} Сабт ба флешка ва албом — <b>{p4}%</b>\n\n"
            f"📌 <b>Ҳолати умумӣ:</b> {order.get('status', 'Дар ҳоли коркард')}"
        )
        await update.message.reply_text(text, reply_markup=back_to_main_kb(get_lang(context)), parse_mode="HTML")

# ==================== РАВАНДИ ФАРМОИШ ====================

async def choose_package_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_lang(context)
    pkg_key = query.data[len("choose_"):]
    context.user_data["order_pkg"] = PACKAGES.get(pkg_key)
    await query.message.reply_text(t("ask_name", lang), parse_mode="HTML")
    return ASK_NAME

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order_name"] = update.message.text
    await update.message.reply_text(t("ask_phone", get_lang(context)), parse_mode="HTML")
    return ASK_PHONE

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not validate_phone(update.message.text):
        await update.message.reply_text(t("phone_invalid", get_lang(context)))
        return ASK_PHONE
    context.user_data["order_phone"] = update.message.text
    
    now = datetime.now()
    booked = context.bot_data.get("booked_dates", {})
    kb = generate_calendar_keyboard(now.year, now.month, booked)
    await update.message.reply_text(t("ask_date_cal", get_lang(context)), reply_markup=kb, parse_mode="HTML")
    return ASK_DATE

async def date_calendar_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data.startswith("cal_date_"):
        selected_date = data.split("_")[2]
        booked = context.bot_data.get("booked_dates", {})
        if selected_date in booked:
            await query.answer("⚠️ Ин сана банд аст, лутфан санаи дигарро интихоб кунед!", show_alert=True)
            return ASK_DATE
        
        context.user_data["order_date"] = selected_date
        context.user_data["order_number"] = f"SM-{random.randint(1000, 9999)}"
        
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎟 Доштани Промокод", callback_data="use_promo")],
            [InlineKeyboardButton("✅ Ҳоло пардохт мекунам", callback_data="pay_now")],
            [InlineKeyboardButton("⏳ Дертар пардохт мекунам", callback_data="pay_later")]
        ])
        await query.message.reply_text(f"📅 Санаи интихобшуда: <b>{selected_date}</b>\n\n" + t("ask_payment", get_lang(context)), reply_markup=kb, parse_mode="HTML")
        return PAYMENT_CHOICE

async def promo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("🎟 Лутфан <b>Промокоди худро</b> ворид кунед:", parse_mode="HTML")
    return ASK_PROMO

async def process_promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip().upper()
    promos = context.bot_data.get("promos", {})
    if code in promos:
        discount = promos[code]
        context.user_data["discount"] = discount
        await update.message.reply_text(f"🎉 Промокод қабул шуд! Шумо <b>{discount}%</b> чегирма гирифтед.", parse_mode="HTML")
    else:
        await update.message.reply_text("❌ Промокоди нодуруст.")
    
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Ҳоло пардохт мекунам", callback_data="pay_now")],
        [InlineKeyboardButton("⏳ Дертар пардохт мекунам", callback_data="pay_later")]
    ])
    await update.message.reply_text(t("ask_payment", get_lang(context)), reply_markup=kb, parse_mode="HTML")
    return PAYMENT_CHOICE

async def payment_choice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "pay_now":
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Ман пардохт кардам", callback_data="pay_continue")]])
        await query.message.reply_text(t("payment_link_text", get_lang(context)), reply_markup=kb, parse_mode="HTML")
        return PAYMENT_CHOICE
    elif query.data == "pay_continue":
        await query.message.reply_text(t("ask_receipt", get_lang(context)), parse_mode="HTML")
        return ASK_RECEIPT
    else:
        context.user_data["prepay"] = False
        return await finalize_order(query.message, context, update.effective_user.id)

async def receipt_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["prepay"] = True
    await update.message.reply_text(t("receipt_received", get_lang(context)))
    return await finalize_order(update.message, context, update.effective_user.id)

async def finalize_order(message_obj, context: ContextTypes.DEFAULT_TYPE, user_id=None):
    lang = get_lang(context)
    pkg = context.user_data.get("order_pkg", {})
    name = context.user_data.get("order_name", "—")
    phone = context.user_data.get("order_phone", "—")
    date = context.user_data.get("order_date", "—")
    order_number = context.user_data.get("order_number", "—")
    prepay = context.user_data.get("prepay", False)
    
    price = pkg.get("price", 1500)
    discount = context.user_data.get("discount", 0)
    final_price = price - (price * discount / 100)

    pdf_buffer = create_contract_pdf(order_number, name, phone, date, pkg.get("short", ""), final_price, "Пардохт шуд" if prepay else "Интизори пардохт", user_id)

    context.bot_data.setdefault("booked_dates", {})[date] = order_number
    context.bot_data.setdefault("orders", {})[order_number] = {
        "chat_id": message_obj.chat.id, "pkg_short": pkg.get("short"),
        "name": name, "phone": phone, "date": date, "status": "🆕 Қабул шуд",
        "p1": 100, "p2": 0, "p3": 0, "p4": 0
    }

    await message_obj.reply_document(
        document=InputFile(pdf_buffer, filename=f"Contract_{order_number}.pdf"),
        caption=f"{t('order_accepted', lang)}\n\n{t('order_thanks', lang)}",
        parse_mode="HTML",
        reply_markup=back_to_main_kb(lang)
    )

    for admin_id in ADMIN_IDS:
        try:
            pdf_buffer.seek(0)
            await context.bot.send_document(
                chat_id=admin_id,
                document=InputFile(pdf_buffer, filename=f"Contract_{order_number}.pdf"),
                caption=f"🆕 <b>ФАРМОИШИ НАВ!</b>\n\n🔖 Рақам: {order_number}\n👤 Ном: {name}\n📱 Тел: {phone}\n📅 Сана: {date}\n💰 Нарх: {final_price} сомонӣ",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Хабар ба админ нарафт: {e}")

    return ConversationHandler.END

# ==================== КОМАНДАҲОИ АДМИН ВА БЭКАПӢ ====================

async def admin_only(update: Update) -> bool:
    return update.effective_user and update.effective_user.id in ADMIN_IDS

async def cmd_exportdb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await admin_only(update): return
    db_path = get_persistence_path()
    if os.path.exists(db_path):
        with open(db_path, "rb") as f:
            await update.message.reply_document(
                document=InputFile(f, filename="bot_data.pkl"),
                caption="💾 <b>Файли захиравии маълумотҳои бот (Бэкап).</b>",
                parse_mode="HTML"
            )

async def cmd_importdb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await admin_only(update): return
    if update.message.document and update.message.document.file_name.endswith(".pkl"):
        db_path = get_persistence_path()
        file = await update.message.document.get_file()
        await file.download_to_drive(db_path)
        await update.message.reply_text("✅ <b>Маълумотҳо бомуваффақият барқарор шуданд!</b>", parse_mode="HTML")

async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await admin_only(update): return
    all_users = context.bot_data.get("all_users", {})
    orders = context.bot_data.get("orders", {})
    booked = context.bot_data.get("booked_dates", {})

    lines = [
        "📊 <b>ОМОРИ ПУРРАИ БОТ (SIMO.MEDIA)</b>",
        "━━━━━━━━━━━━━━━━━━",
        f"👥 Ҳамагӣ корбарони бот: <b>{len(all_users)}</b>",
        f"🔖 Ҳамагӣ фармоишҳо: <b>{len(orders)}</b>",
        f"📅 Санаҳои бандшуда: <b>{len(booked)}</b>",
    ]
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

async def cmd_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await admin_only(update): return
    if not context.args: return
    text = " ".join(context.args)
    all_users = context.bot_data.get("all_users", {})
    sent, failed = 0, 0
    broadcast_caption = f"📢 <b>ХАБАРИ МУҲИМ АЗ SIMO.MEDIA</b>\n━━━━━━━━━━━━━━━━━━\n\n{text}"
    
    for chat_id in list(all_users.keys()):
        try:
            await context.bot.send_message(chat_id=chat_id, text=broadcast_caption, parse_mode="HTML")
            sent += 1
        except Exception:
            failed += 1
    await update.message.reply_text(f"✅ Паём ба {sent} корбар фиристода шуд. Хатогӣ: {failed}.")

# ==================== MAIN ====================

def main():
    persistence_file = get_persistence_path()
    persistence = PicklePersistence(filepath=persistence_file)
    application = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

    order_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(choose_package_start, pattern="^choose_")],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
            ASK_DATE: [CallbackQueryHandler(date_calendar_handler, pattern="^cal_")],
            PAYMENT_CHOICE: [
                CallbackQueryHandler(promo_handler, pattern="^use_promo$"),
                CallbackQueryHandler(payment_choice_handler, pattern="^pay_"),
            ],
            ASK_PROMO: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_promo)],
            ASK_RECEIPT: [MessageHandler(filters.PHOTO, receipt_photo_handler)],
        },
        fallbacks=[],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", start))
    application.add_handler(CommandHandler("stats", cmd_stats))
    application.add_handler(CommandHandler("exportdb", cmd_exportdb))
    application.add_handler(MessageHandler(filters.Document.ALL & filters.User(user_id=ADMIN_IDS), cmd_importdb))
    application.add_handler(CommandHandler("broadcast", cmd_broadcast))
    
    application.add_handler(order_conv)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tracking))
    application.add_handler(CallbackQueryHandler(button_handler))

    print(f"🤖 SIMO.MEDIA Master bot фаъол гашт...")
    application.run_polling()

if __name__ == "__main__":
    main()
