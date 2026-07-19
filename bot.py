# -*- coding: utf-8 -*-
"""
SIMO.MEDIA — Telegram bot (нусхаи касбӣ v4)
Ду забон (Тоҷикӣ/Русӣ), санҷиши рақами телефон, идоракунии хатогиҳо,
соатҳои корӣ, банер, оморҳо, тавсифҳо, тасдиқи фармоиш бо рақами беназир.

Барои иҷро:
1) pip install -r requirements.txt
2) Токени ботро аз @BotFather гиред
3) Дар поён BOT_TOKEN-ро гузоред
4) python bot.py
"""

import os
import re
import random
import logging
from datetime import datetime, timezone, timedelta

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

WELCOME_IMAGE_URL = "https://images.unsplash.com/photo-1519741497674-611481863552?w=1200&q=80"

PORTFOLIO_LINKS = [
    ("🎬 Намунаи клип — Reel", "https://www.instagram.com/reel/DYJFY9MoYnJ/?igsh=MWc4ZHNua2xyMzdkaw=="),
    ("📷 Instagram — намунаи бештар", "https://www.instagram.com/iam_shodovar?igsh=Z3g1NHhrOXM5NGdl"),
]

REVIEWS = [
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

# Соатҳои корӣ (вақти Душанбе, UTC+5)
WORK_START_HOUR = 9
WORK_END_HOUR = 20
DUSHANBE_TZ = timezone(timedelta(hours=5))

# ==================== МАТНҲО (ду забон) ====================

BTN = {
    "tj": {
        "urgent": "🔥 Фармоиши фаврӣ", "prices": "💰 Прайс-лист", "portfolio": "🎬 Портфолио",
        "reviews": "⭐ Тавсифҳо", "stats": "📊 Дар рақамҳо", "why": "✨ Чаро маҳз мо?",
        "faq": "❓ FAQ", "about": "ℹ️ Дар бораи мо", "contact": "📞 Тамос",
        "lang": "🇷🇺 На русском", "back": "⬅️ Ба меню асосӣ", "back_prices": "⬅️ Ба прайс-лист",
        "order": "✅ Ин пакетро фармоиш медиҳам", "confirm": "✅ Тасдиқ ва фиристодан",
        "restart": "✏️ Аз нав пур кардан", "prev": "⬅️ Қаблӣ", "next": "Баъдӣ ➡️",
        "whatsapp": "💬 WhatsApp", "telegram": "✈️ Telegram", "instagram": "📷 Instagram",
    },
    "ru": {
        "urgent": "🔥 Быстрый заказ", "prices": "💰 Прайс-лист", "portfolio": "🎬 Портфолио",
        "reviews": "⭐ Отзывы", "stats": "📊 В цифрах", "why": "✨ Почему мы?",
        "faq": "❓ FAQ", "about": "ℹ️ О нас", "contact": "📞 Контакты",
        "lang": "🇹🇯 Тоҷикӣ", "back": "⬅️ Главное меню", "back_prices": "⬅️ К прайс-листу",
        "order": "✅ Заказать этот пакет", "confirm": "✅ Подтвердить и отправить",
        "restart": "✏️ Заполнить заново", "prev": "⬅️ Пред.", "next": "След. ➡️",
        "whatsapp": "💬 WhatsApp", "telegram": "✈️ Telegram", "instagram": "📷 Instagram",
    },
}

TEXT = {
    "welcome": {
        "tj": ("🎥 <b>SIMO.MEDIA</b>\n<i>✨ Хотираҳоро ба филмҳои ҷовидона табдил медиҳем ✨</i>\n"
               "━━━━━━━━━━━━━━━━━━\n\nХуш омадед! 🤍\n\n"
               "Рӯзи арӯсӣ танҳо як бор такрор мешавад. Мо ҳар табассум, ҳар ашки шодӣ ва "
               "ҳар лаҳзаи зебои ин рӯзи фаромӯшнашавандаро бо сифати баланд сабт мекунем.\n\n"
               "👇 <b>Лутфан аз менюи поён интихоб кунед:</b>"),
        "ru": ("🎥 <b>SIMO.MEDIA</b>\n<i>✨ Превращаем воспоминания в вечные фильмы ✨</i>\n"
               "━━━━━━━━━━━━━━━━━━\n\nДобро пожаловать! 🤍\n\n"
               "Свадебный день бывает только один раз. Мы снимаем каждую улыбку и каждый "
               "прекрасный момент этого незабываемого дня в высоком качестве.\n\n"
               "👇 <b>Пожалуйста, выберите из меню ниже:</b>"),
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
               "🎥 Мо аз камераҳои касбӣ, DJI Ronin, дронҳои муосир ва сабти садои касбӣ истифода мебарем.\n\n"
               "💻 Коркарди видео бо <b>Adobe Premiere Pro, After Effects</b> ва <b>DaVinci Resolve</b> "
               "анҷом дода мешавад, бо кӯмаки AI барои сифати беҳтари ранг.\n\n"
               "<b>SIMO.MEDIA — хотираҳоро ба филмҳои ҷовидона табдил медиҳем.</b> 💍"),
        "ru": ("ℹ️ <b>О SIMO.MEDIA</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               "SIMO.MEDIA — профессиональная студия свадебной видеосъёмки под руководством "
               "<b>Шодовара Нуриддинова</b>.\n\n"
               "📅 Студия официально работает с 20 февраля 2023 года.\n\n"
               "🎥 Мы используем профессиональные камеры, DJI Ronin, современные дроны и "
               "профессиональный звук.\n\n"
               "💻 Монтаж выполняется в <b>Adobe Premiere Pro, After Effects</b> и <b>DaVinci Resolve</b>, "
               "с использованием AI для улучшения цвета.\n\n"
               "<b>SIMO.MEDIA — превращаем воспоминания в вечные фильмы.</b> 💍"),
    },
    "why": {
        "tj": ("✨ <b>ЧАРО МАҲЗ SIMO.MEDIA?</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               "📸 Таҷҳизоти муосир ва сифати баланд\n🎬 Монтажи касбӣ бо услуби замонавӣ\n"
               "🚁 Наворбардорӣ бо дрон\n💍 Сабти тамоми лаҳзаҳои муҳими тӯй\n"
               "⚡ Омодасозии зуд ва саривақтӣ\n🤖 Истифодаи AI барои сифати беҳтари ранг\n"
               "🤝 Муносибати масъулиятнок"),
        "ru": ("✨ <b>ПОЧЕМУ ИМЕННО SIMO.MEDIA?</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               "📸 Современное оборудование и высокое качество\n🎬 Профессиональный монтаж\n"
               "🚁 Съёмка с дрона\n💍 Съёмка всех важных моментов свадьбы\n"
               "⚡ Быстрая и своевременная подготовка\n🤖 Использование AI для улучшения цвета\n"
               "🤝 Ответственный подход"),
    },
    "faq": {
        "tj": ("❓ <b>САВОЛҲОИ МАЪМУЛ</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               "🔹 <b>Оё пеш аз тӯй вохӯрӣ мешавад?</b>\nҲа, тамоми ҷузъиётро пеш муҳокима мекунем.\n\n"
               "🔹 <b>Пеш-пардохт лозим аст?</b>\nҲа, барои мустаҳкам кардани фармоиш.\n\n"
               "🔹 <b>Оё берун аз шаҳр меравед?</b>\nҲа, бо шартҳои иловагӣ.\n\n"
               "🔹 <b>То кай мавод омода мешавад?</b>\nАз 7 то 30 рӯз, вобаста ба пакет."),
        "ru": ("❓ <b>ЧАСТЫЕ ВОПРОСЫ</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               "🔹 <b>Есть ли встреча перед свадьбой?</b>\nДа, мы обсуждаем все детали заранее.\n\n"
               "🔹 <b>Нужна ли предоплата?</b>\nДа, для подтверждения заказа.\n\n"
               "🔹 <b>Выезжаете за город?</b>\nДа, при дополнительных условиях.\n\n"
               "🔹 <b>Когда будет готов материал?</b>\nОт 7 до 30 дней, в зависимости от пакета."),
    },
    "contact": {
        "tj": ("📞 <b>Барои машварат ва фармоиш</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               f"☎️ Телефон: {CONTACT_PHONE_DISPLAY}\n💬 WhatsApp: {CONTACT_PHONE_DISPLAY}\n"
               f"✈️ Telegram: {TELEGRAM_USERNAME}\n📷 Instagram: намуна дар боло\n\n"
               "SIMO.MEDIA — Хотираҳоро ба вақт насупоред 🤍"),
        "ru": ("📞 <b>Для консультации и заказа</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               f"☎️ Телефон: {CONTACT_PHONE_DISPLAY}\n💬 WhatsApp: {CONTACT_PHONE_DISPLAY}\n"
               f"✈️ Telegram: {TELEGRAM_USERNAME}\n📷 Instagram: см. выше\n\n"
               "SIMO.MEDIA — Не откладывайте воспоминания 🤍"),
    },
    "prices_title": {
        "tj": "💰 <b>ПРАЙС-ЛИСТИ SIMO.MEDIA</b>\n━━━━━━━━━━━━━━━━━━\n\nЛутфан пакетро интихоб кунед 👇",
        "ru": "💰 <b>ПРАЙС-ЛИСТ SIMO.MEDIA</b>\n━━━━━━━━━━━━━━━━━━\n\nВыберите пакет 👇",
    },
    "portfolio_title": {
        "tj": ("🎬 <b>ПОРТФОЛИО</b>\n━━━━━━━━━━━━━━━━━━\n\nНамунаи баъзе корҳои мо дар поён 👇\n\n"
               "📷 Барои намунаи бештар, ба саҳифаи Instagram-и мо гузаред."),
        "ru": ("🎬 <b>ПОРТФОЛИО</b>\n━━━━━━━━━━━━━━━━━━\n\nНекоторые наши работы ниже 👇\n\n"
               "📷 Для большего количества примеров посетите наш Instagram."),
    },
    "reviews_title": {"tj": "ТАВСИФҲОИ МУШТАРИЁН", "ru": "ОТЗЫВЫ КЛИЕНТОВ"},
    "unknown": {
        "tj": "Лутфан аз тугмаҳои меню истифода баред 👇",
        "ru": "Пожалуйста, используйте кнопки меню 👇",
    },
    "ask_name": {
        "tj": "📝 <b>Қадами 1/3</b> — Лутфан <b>номи худро</b> нависед:",
        "ru": "📝 <b>Шаг 1/3</b> — Пожалуйста, напишите <b>ваше имя</b>:",
    },
    "ask_phone": {
        "tj": "📱 <b>Қадами 2/3</b> — Лутфан рақами телефони худро нависед (масалан 93 882 97 96):",
        "ru": "📱 <b>Шаг 2/3</b> — Напишите ваш номер телефона (например 93 882 97 96):",
    },
    "phone_invalid": {
        "tj": "⚠️ Рақами телефон нодуруст аст. Лутфан танҳо рақамҳо нависед (масалан 93 882 97 96 ё +992 93 882 97 96):",
        "ru": "⚠️ Неверный номер телефона. Пожалуйста, укажите только цифры (например 93 882 97 96 или +992 93 882 97 96):",
    },
    "ask_date": {
        "tj": "📅 <b>Қадами 3/3</b> — Лутфан санаи тӯйро нависед (масалан 15.08.2026):",
        "ru": "📅 <b>Шаг 3/3</b> — Напишите дату свадьбы (например 15.08.2026):",
    },
    "date_invalid": {
        "tj": "⚠️ Формати сана нодуруст аст. Лутфан бо ин формат нависед: РӮЗ.МОҲ.СОЛ (масалан 15.08.2026):",
        "ru": "⚠️ Неверный формат даты. Пожалуйста, укажите в формате ДЕНЬ.МЕСЯЦ.ГОД (например 15.08.2026):",
    },
    "confirm_title": {"tj": "🔎 <b>ЛУТФАН ТАСДИҚ КУНЕД</b>", "ru": "🔎 <b>ПОЖАЛУЙСТА, ПОДТВЕРДИТЕ</b>"},
    "confirm_ok": {"tj": "Ҳама дуруст аст?", "ru": "Всё верно?"},
    "order_pkg": {"tj": "📦 Пакет", "ru": "📦 Пакет"},
    "order_name": {"tj": "👤 Ном", "ru": "👤 Имя"},
    "order_phone": {"tj": "📱 Телефон", "ru": "📱 Телефон"},
    "order_date": {"tj": "📅 Санаи тӯй", "ru": "📅 Дата свадьбы"},
    "order_number": {"tj": "🔖 Рақами фармоиш", "ru": "🔖 Номер заказа"},
    "order_accepted": {"tj": "🎉 <b>Фармоиши шумо қабул шуд!</b>", "ru": "🎉 <b>Ваш заказ принят!</b>"},
    "order_thanks": {
        "tj": "Ходими мо ба наздикӣ бо шумо тамос мегирад. Ташаккур! 🙏",
        "ru": "Наш сотрудник свяжется с вами в ближайшее время. Спасибо! 🙏",
    },
    "order_keep_number": {
        "tj": "Рақами фармоишро нигоҳ доред — ҳангоми муроҷиат метавонед истифода баред.",
        "ru": "Сохраните номер заказа — вы можете использовать его при обращении.",
    },
    "after_hours_note": {
        "tj": (f"\n\n⏰ <i>Диққат: ҳозир берун аз соатҳои кории мо ({WORK_START_HOUR}:00–{WORK_END_HOUR}:00) аст. "
               "Ходими мо пагоҳ бо шумо тамос мегирад.</i>"),
        "ru": (f"\n\n⏰ <i>Внимание: сейчас нерабочее время ({WORK_START_HOUR}:00–{WORK_END_HOUR}:00). "
               "Наш сотрудник свяжется с вами позже.</i>"),
    },
    "error_generic": {
        "tj": "⚠️ Мутаассифона хатогӣ рух дод. Лутфан аз нав кӯшиш кунед ё /start-ро занед.",
        "ru": "⚠️ Произошла ошибка. Пожалуйста, попробуйте снова или нажмите /start.",
    },
}

PACKAGES = {
    "standard": {
        "short": "STANDARD (1500 сомонӣ)",
        "text": {
            "tj": ("🎥 <b>STANDARD — 1500 сомонӣ</b>\n━━━━━━━━━━━━━━━━━━\n\n"
                   "Интихоби беҳтарин барои сабти лаҳзаҳои муҳими тӯй.\n\n"
                   "✔️ Наворбардории касбӣ\n✔️ Аксбардории касбӣ\n✔️ 1 адад камера\n"
                   "✔️ 1 ҷуфт диски аслӣ (Original DVD)\n\n🎁 Тӯҳфа: 10 дона акси чопшуда\n"
                   "⏳ Омодасозии мавод: 25–30 рӯз"),
            "ru": ("🎥 <b>STANDARD — 1500 сомони</b>\n━━━━━━━━━━━━━━━━━━\n\n"
                   "Лучший выбор для съёмки важных моментов свадьбы.\n\n"
                   "✔️ Профессиональная видеосъёмка\n✔️ Профессиональная фотосъёмка\n✔️ 1 камера\n"
                   "✔️ 1 оригинальный DVD-диск\n\n🎁 Подарок: 10 печатных фото\n"
                   "⏳ Готовность материала: 25–30 дней"),
        },
    },
    "vip": {
        "short": "VIP (2000 сомонӣ)",
        "text": {
            "tj": ("👑 <b>VIP — 2000 сомонӣ</b>\n━━━━━━━━━━━━━━━━━━\n\n"
                   "Сифати бештар, хотираҳои бештар.\n\n"
                   "✔️ Наворбардории касбӣ\n✔️ Аксбардории касбӣ\n✔️ 1 адад камера\n"
                   "✔️ 1 ҷуфт диски аслӣ\n✔️ Флешкаи аслӣ (64 GB)\n✔️ 1 адад албоми Wedding Day\n\n"
                   "🎁 Тӯҳфа: 30 дона акси чопшуда\n⏳ Омодасозии мавод: 15–20 рӯз"),
            "ru": ("👑 <b>VIP — 2000 сомони</b>\n━━━━━━━━━━━━━━━━━━\n\n"
                   "Больше качества, больше воспоминаний.\n\n"
                   "✔️ Профессиональная видеосъёмка\n✔️ Профессиональная фотосъёмка\n✔️ 1 камера\n"
                   "✔️ 1 оригинальный DVD-диск\n✔️ Оригинальная флешка (64 GB)\n✔️ Альбом Wedding Day\n\n"
                   "🎁 Подарок: 30 печатных фото\n⏳ Готовность материала: 15–20 дней"),
        },
    },
    "vip_premium": {
        "short": "VIP PREMIUM (3000 сомонӣ)",
        "text": {
            "tj": ("💎 <b>VIP PREMIUM — 3000 сомонӣ</b>\n━━━━━━━━━━━━━━━━━━\n\n"
                   "Интихоби беҳтарин барои онҳое, ки беҳтаринро мехоҳанд.\n\n"
                   "✔️ Наворбардории касбӣ\n✔️ Аксбардории касбӣ\n✔️ 1 адад камера\n"
                   "✔️ 1 адад крани наворбардорӣ\n✔️ Клипи тӯёна\n✔️ Love Story\n"
                   "✔️ 2 ҷуфт диски аслӣ\n✔️ Флешкаи аслӣ (64 GB)\n✔️ Албоми Wedding Day\n"
                   "✔️ Албом барои аксҳо\n\n🎁 Тӯҳфа: 50 дона акси чопшуда\n⏳ Омодасозии мавод: 7–10 рӯз"),
            "ru": ("💎 <b>VIP PREMIUM — 3000 сомони</b>\n━━━━━━━━━━━━━━━━━━\n\n"
                   "Лучший выбор для тех, кто хочет самое лучшее.\n\n"
                   "✔️ Профессиональная видеосъёмка\n✔️ Профессиональная фотосъёмка\n✔️ 1 камера\n"
                   "✔️ Операторский кран\n✔️ Свадебный клип\n✔️ Love Story\n"
                   "✔️ 2 оригинальных DVD-диска\n✔️ Оригинальная флешка (64 GB)\n✔️ Альбом Wedding Day\n"
                   "✔️ Фотоальбом\n\n🎁 Подарок: 50 печатных фото\n⏳ Готовность материала: 7–10 дней"),
        },
    },
}

ASK_NAME, ASK_PHONE, ASK_DATE, CONFIRM = range(4)

# ==================== ФУНКСИЯҲОИ КӮМАКӣ ====================

def get_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("lang", "tj")


def t(key: str, lang: str) -> str:
    return TEXT[key][lang]


def is_within_work_hours() -> bool:
    now = datetime.now(DUSHANBE_TZ)
    return WORK_START_HOUR <= now.hour < WORK_END_HOUR


def validate_phone(text: str) -> bool:
    digits = re.sub(r"[^\d]", "", text)
    return 7 <= len(digits) <= 15


def validate_date(text: str) -> bool:
    return bool(re.match(r"^\d{1,2}[./]\d{1,2}[./]\d{2,4}$", text.strip()))


# ==================== КЛАВИАТУРАҲО ====================

def main_menu_kb(lang: str):
    b = BTN[lang]
    kb = [
        [InlineKeyboardButton(b["urgent"], callback_data="menu_prices")],
        [InlineKeyboardButton(b["prices"], callback_data="menu_prices"),
         InlineKeyboardButton(b["portfolio"], callback_data="menu_portfolio")],
        [InlineKeyboardButton(b["reviews"], callback_data="rev_0"),
         InlineKeyboardButton(b["stats"], callback_data="menu_stats")],
        [InlineKeyboardButton(b["why"], callback_data="menu_why"),
         InlineKeyboardButton(b["faq"], callback_data="menu_faq")],
        [InlineKeyboardButton(b["about"], callback_data="menu_about")],
        [InlineKeyboardButton(b["contact"], callback_data="menu_contact")],
        [InlineKeyboardButton(b["lang"], callback_data="toggle_lang")],
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


def package_detail_kb(pkg_key: str, lang: str):
    b = BTN[lang]
    kb = [
        [InlineKeyboardButton(b["order"], callback_data=f"choose_{pkg_key}")],
        [InlineKeyboardButton(b["back_prices"], callback_data="menu_prices")],
    ]
    return InlineKeyboardMarkup(kb)


def back_to_main_kb(lang: str):
    return InlineKeyboardMarkup([[InlineKeyboardButton(BTN[lang]["back"], callback_data="menu_main")]])


def contact_kb(lang: str):
    b = BTN[lang]
    kb = [
        [InlineKeyboardButton(b["whatsapp"], url=WHATSAPP_LINK)],
        [InlineKeyboardButton(b["telegram"], url=TELEGRAM_LINK)],
        [InlineKeyboardButton(b["instagram"], url=INSTAGRAM_LINK)],
        [InlineKeyboardButton(b["back"], callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(kb)


def portfolio_kb(lang: str):
    kb = [[InlineKeyboardButton(name, url=link)] for name, link in PORTFOLIO_LINKS]
    kb.append([InlineKeyboardButton(BTN[lang]["back"], callback_data="menu_main")])
    return InlineKeyboardMarkup(kb)


def reviews_kb(index: int, lang: str):
    b = BTN[lang]
    total = len(REVIEWS)
    nav = []
    if total > 1:
        prev_i = (index - 1) % total
        next_i = (index + 1) % total
        nav = [
            InlineKeyboardButton(b["prev"], callback_data=f"rev_{prev_i}"),
            InlineKeyboardButton(b["next"], callback_data=f"rev_{next_i}"),
        ]
    kb = []
    if nav:
        kb.append(nav)
    kb.append([InlineKeyboardButton(b["back"], callback_data="menu_main")])
    return InlineKeyboardMarkup(kb)


def after_order_kb(lang: str):
    b = BTN[lang]
    kb = [
        [InlineKeyboardButton(b["whatsapp"], url=WHATSAPP_LINK)],
        [InlineKeyboardButton(b["back"], callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(kb)


def confirm_kb(lang: str):
    b = BTN[lang]
    kb = [
        [InlineKeyboardButton(b["confirm"], callback_data="order_confirm")],
        [InlineKeyboardButton(b["restart"], callback_data="order_restart")],
    ]
    return InlineKeyboardMarkup(kb)


def review_render(index: int, lang: str) -> str:
    r = REVIEWS[index]
    return (
        f"⭐ <b>{t('reviews_title', lang)}</b>\n━━━━━━━━━━━━━━━━━━\n\n"
        f"{r['stars']}\n<i>«{r[lang]}»</i>\n\n— <b>{r['name']}</b>\n\n({index + 1}/{len(REVIEWS)})"
    )


# ==================== ХЭНДЛЕРҲОИ АСОСӢ ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    try:
        await update.message.reply_photo(
            photo=WELCOME_IMAGE_URL,
            caption=t("welcome", lang),
            reply_markup=main_menu_kb(lang),
            parse_mode="HTML",
        )
    except Exception as e:
        logger.warning(f"Акс фиристода нашуд: {e}")
        await update.message.reply_text(t("welcome", lang), reply_markup=main_menu_kb(lang), parse_mode="HTML")


async def safe_edit(query, text, reply_markup=None):
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
    lang = get_lang(context)
    await context.bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.TYPING)

    if data == "toggle_lang":
        new_lang = "ru" if lang == "tj" else "tj"
        context.user_data["lang"] = new_lang
        await safe_edit(query, t("welcome", new_lang), main_menu_kb(new_lang))
        return

    if data == "menu_main":
        await safe_edit(query, t("welcome", lang), main_menu_kb(lang))

    elif data == "menu_prices":
        await safe_edit(query, t("prices_title", lang), prices_menu_kb(lang))

    elif data == "menu_why":
        await safe_edit(query, t("why", lang), back_to_main_kb(lang))

    elif data == "menu_stats":
        await safe_edit(query, t("stats", lang), back_to_main_kb(lang))

    elif data == "menu_faq":
        await safe_edit(query, t("faq", lang), back_to_main_kb(lang))

    elif data == "menu_about":
        await safe_edit(query, t("about", lang), back_to_main_kb(lang))

    elif data == "menu_portfolio":
        await safe_edit(query, t("portfolio_title", lang), portfolio_kb(lang))

    elif data == "menu_contact":
        await safe_edit(query, t("contact", lang), contact_kb(lang))

    elif data.startswith("rev_"):
        index = int(data[len("rev_"):])
        await safe_edit(query, review_render(index, lang), reviews_kb(index, lang))

    elif data.startswith("pkg_"):
        pkg_key = data[len("pkg_"):]
        pkg = PACKAGES.get(pkg_key)
        if pkg:
            await safe_edit(query, pkg["text"][lang], package_detail_kb(pkg_key, lang))


async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    await update.message.reply_text(t("unknown", lang), reply_markup=main_menu_kb(lang))


# ==================== ФАРМОИШИ ПУРРА (Conversation) ====================

async def choose_package_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_lang(context)
    pkg_key = query.data[len("choose_"):]
    pkg = PACKAGES.get(pkg_key)
    if not pkg:
        return ConversationHandler.END

    context.user_data["order_pkg"] = pkg
    await safe_edit(query, t("ask_name", lang))
    return ASK_NAME


async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    context.user_data["order_name"] = update.message.text
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    await update.message.reply_text(t("ask_phone", lang), parse_mode="HTML")
    return ASK_PHONE


async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    phone_text = update.message.text
    if not validate_phone(phone_text):
        await update.message.reply_text(t("phone_invalid", lang), parse_mode="HTML")
        return ASK_PHONE
    context.user_data["order_phone"] = phone_text
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    await update.message.reply_text(t("ask_date", lang), parse_mode="HTML")
    return ASK_DATE


async def ask_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    date_text = update.message.text
    if not validate_date(date_text):
        await update.message.reply_text(t("date_invalid", lang), parse_mode="HTML")
        return ASK_DATE

    context.user_data["order_date"] = date_text
    context.user_data["order_number"] = f"SM-{random.randint(1000, 9999)}"
    pkg = context.user_data.get("order_pkg", {})
    name = context.user_data.get("order_name", "—")
    phone = context.user_data.get("order_phone", "—")
    date = context.user_data.get("order_date", "—")
    order_number = context.user_data.get("order_number", "—")

    summary = (
        f"{t('confirm_title', lang)}\n━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('order_number', lang)}: <b>{order_number}</b>\n"
        f"{t('order_pkg', lang)}: {pkg.get('short', '—')}\n"
        f"{t('order_name', lang)}: {name}\n"
        f"{t('order_phone', lang)}: {phone}\n"
        f"{t('order_date', lang)}: {date}\n\n"
        f"{t('confirm_ok', lang)}"
    )
    await update.message.reply_text(summary, reply_markup=confirm_kb(lang), parse_mode="HTML")
    return CONFIRM


async def order_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_lang(context)
    await safe_edit(query, t("ask_name", lang))
    return ASK_NAME


async def order_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_lang(context)
    user = query.from_user
    pkg = context.user_data.get("order_pkg", {})
    name = context.user_data.get("order_name", "—")
    phone = context.user_data.get("order_phone", "—")
    date = context.user_data.get("order_date", "—")
    order_number = context.user_data.get("order_number", "—")

    hours_note = "" if is_within_work_hours() else t("after_hours_note", lang)

    await safe_edit(
        query,
        f"{t('order_accepted', lang)}\n━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('order_number', lang)}: <b>{order_number}</b>\n"
        f"{t('order_pkg', lang)}: {pkg.get('short', '—')}\n"
        f"{t('order_name', lang)}: {name}\n"
        f"{t('order_phone', lang)}: {phone}\n"
        f"{t('order_date', lang)}: {date}\n\n"
        f"{t('order_thanks', lang)}\n\n<i>{t('order_keep_number', lang)}</i>{hours_note}",
        after_order_kb(lang),
    )

    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=(
                    "🆕 <b>ФАРМОИШИ НАВ!</b>\n━━━━━━━━━━━━━━━━━━\n\n"
                    f"🔖 Рақами фармоиш: <b>{order_number}</b>\n"
                    f"📦 Пакет: {pkg.get('short', '—')}\n"
                    f"👤 Ном: {name}\n📱 Телефон: {phone}\n📅 Санаи тӯй: {date}\n\n"
                    f"Telegram: @{user.username if user.username else '—'}\n"
                    f"User ID: {user.id}"
                ),
                parse_mode="HTML",
            )
        except Exception as e:
            logger.error(f"Хабар ба админ нарафт: {e}")

    context.user_data.pop("order_pkg", None)
    context.user_data.pop("order_name", None)
    context.user_data.pop("order_phone", None)
    context.user_data.pop("order_date", None)
    context.user_data.pop("order_number", None)
    return ConversationHandler.END


async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    context.user_data.clear()
    await update.message.reply_text("Бекор карда шуд / Отменено", reply_markup=main_menu_kb(lang))
    return ConversationHandler.END


# ==================== ИДОРАКУНИИ ХАТОГИҲО ====================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Хатогии дар полинг рух дод:", exc_info=context.error)
    try:
        if isinstance(update, Update) and update.effective_chat:
            lang = get_lang(context) if hasattr(context, "user_data") and context.user_data else "tj"
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=t("error_generic", lang),
            )
    except Exception:
        pass


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
    application.add_error_handler(error_handler)

    print("🤖 SIMO.MEDIA bot кор карда истодааст...")
    application.run_polling()


if __name__ == "__main__":
    main()
