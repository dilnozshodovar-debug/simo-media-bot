# -*- coding: utf-8 -*-
"""
SIMO.MEDIA — Telegram bot (нусхаи касбӣ v5)
Ду забон, санҷиши вуруд, идоракунии хатогиҳо, соатҳои корӣ, банер, оморҳо,
тавсифҳо, тасдиқи фармоиш, санҷиши дастрасии сана, пайгирии фармоиш,
ёдоварии худкор, паёми умумӣ ба мизоҷон, даъвати дӯстон.

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
BOT_USERNAME = "simoo129_bot"

CONTACT_PHONE_DISPLAY = "+992 93 882 97 96"
CONTACT_PHONE_RAW = "992938829796"
WHATSAPP_LINK = f"https://wa.me/{CONTACT_PHONE_RAW}"
TELEGRAM_USERNAME = "@editor2202"
TELEGRAM_LINK = "https://t.me/editor2202"
INSTAGRAM_LINK = "https://www.instagram.com/iam_shodovar?igsh=Z3g1NHhrOXM5NGdl"

WELCOME_IMAGE_URL = "https://raw.githubusercontent.com/dilnozshodovar-debug/simo-media-bot/main/logo.png"
ABOUT_IMAGE_URL = "https://raw.githubusercontent.com/dilnozshodovar-debug/simo-media-bot/main/about.jpg"

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

WORK_START_HOUR = 9
WORK_END_HOUR = 20
DUSHANBE_TZ = timezone(timedelta(hours=5))
REMINDER_HOURS = 24
REFERRAL_DISCOUNT_PERCENT = 5
DEPOSIT_AMOUNT = "100 сомонӣ"
PAYMENT_LINK = "http://pay.expresspay.tj/?A=5058270376098736&s=100&c=&f1=133&FIELD2=&FIELD3="

# ==================== МАТНҲО (ду забон) ====================

BTN = {
    "tj": {
        "urgent": "🔥 Фармоиши фаврӣ", "prices": "💰 Прайс-лист", "portfolio": "🎬 Портфолио",
        "reviews": "⭐ Тавсифҳо", "stats": "📊 Дар рақамҳо", "why": "✨ Чаро маҳз мо?",
        "faq": "❓ FAQ", "about": "ℹ️ Дар бораи мо", "contact": "📞 Тамос",
        "availability": "📅 Санҷиши сана", "track": "📋 Пайгирии фармоиш",
        "referral": "🎁 Даъвати дӯстон", "compare": "📊 Муқоисаи пакетҳо", "lang": "🇷🇺 На русском",
        "back": "⬅️ Ба меню асосӣ", "back_prices": "⬅️ Ба прайс-лист",
        "order": "✅ Ин пакетро фармоиш медиҳам", "confirm": "✅ Тасдиқ ва фиристодан",
        "restart": "✏️ Аз нав пур кардан", "prev": "⬅️ Қаблӣ", "next": "Баъдӣ ➡️",
        "whatsapp": "💬 WhatsApp", "telegram": "✈️ Telegram", "instagram": "📷 Instagram",
    },
    "ru": {
        "urgent": "🔥 Быстрый заказ", "prices": "💰 Прайс-лист", "portfolio": "🎬 Портфолио",
        "reviews": "⭐ Отзывы", "stats": "📊 В цифрах", "why": "✨ Почему мы?",
        "faq": "❓ FAQ", "about": "ℹ️ О нас", "contact": "📞 Контакты",
        "availability": "📅 Проверить дату", "track": "📋 Отследить заказ",
        "referral": "🎁 Пригласить друзей", "compare": "📊 Сравнить пакеты", "lang": "🇹🇯 Тоҷикӣ",
        "back": "⬅️ Главное меню", "back_prices": "⬅️ К прайс-листу",
        "order": "✅ Заказать этот пакет", "confirm": "✅ Подтвердить и отправить",
        "restart": "✏️ Заполнить заново", "prev": "⬅️ Пред.", "next": "След. ➡️",
        "whatsapp": "💬 WhatsApp", "telegram": "✈️ Telegram", "instagram": "📷 Instagram",
    },
}

TEXT = {
    "welcome": {
        "tj": ("🎥 <b>SIMO.MEDIA</b>\n<i>✨ Хотираҳоро ба филмҳои ҷовидона табдил медиҳем ✨</i>\n"
               "━━━━━━━━━━━━━━━━━━\n\n🤍 Хуш омадед!\n\n"
               "Рӯзи арӯсӣ яке аз муҳимтарин ва фаромӯшнашавандатарин рӯзҳои зиндагист. Мо ҳар табассум, "
               "ҳар ашки шодӣ ва ҳар лаҳзаи пур аз эҳсосоти ин рӯзи махсусро бо сифати баланд ва услуби "
               "касбӣ сабт намуда, онҳоро ба филме табдил медиҳем, ки солҳои дароз хотираҳои ширини "
               "шуморо зинда нигоҳ медорад.\n\n"
               "🎬 <b>Аз имкониятҳои боти мо истифода баред!</b>\nДар ин ҷо шумо метавонед:\n"
               "📂 Намунаҳои корҳои моро тамошо кунед;\n💰 Бо нархнома шинос шавед;\n"
               "📅 Барои санаи худ дастрасиро санҷед;\n📝 Фармоиш диҳед ё бо мо дар тамос шавед.\n\n"
               "👇 Лутфан аз менюи поён яке аз бахшҳоро интихоб намоед. Мо ҳамеша омодаем, ки беҳтарин "
               "лаҳзаҳои шуморо ҷовидона гардонем! 🤍"),
        "ru": ("🎥 <b>SIMO.MEDIA</b>\n<i>✨ Превращаем воспоминания в вечные фильмы ✨</i>\n"
               "━━━━━━━━━━━━━━━━━━\n\n🤍 Добро пожаловать!\n\n"
               "Свадебный день — один из важнейших и незабываемых дней в жизни. Мы снимаем каждую улыбку, "
               "каждую слезу радости и каждый эмоциональный момент этого особенного дня в высоком качестве "
               "и с профессиональным стилем, превращая их в фильм, который долгие годы будет хранить ваши "
               "тёплые воспоминания.\n\n"
               "🎬 <b>Воспользуйтесь возможностями нашего бота!</b>\nЗдесь вы можете:\n"
               "📂 Посмотреть примеры наших работ;\n💰 Ознакомиться с прайс-листом;\n"
               "📅 Проверить доступность на вашу дату;\n📝 Оформить заказ или связаться с нами.\n\n"
               "👇 Пожалуйста, выберите один из разделов в меню ниже. Мы всегда готовы сделать ваши "
               "лучшие моменты вечными! 🤍"),
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
    "compare_table": {
        "tj": ("📊 <b>МУҚОИСАИ ПАКЕТҲО</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               "💰 <b>Нарх</b>\n🎥 STANDARD: 1500 сомонӣ\n👑 VIP: 2000 сомонӣ\n💎 VIP PREMIUM: 3000 сомонӣ\n\n"
               "📸 <b>Наворбардорӣ ва аксбардории касбӣ</b>\n✅ Дар ҳар се пакет\n\n"
               "💿 <b>Диски аслӣ (DVD)</b>\n🎥 1 ҷуфт | 👑 1 ҷуфт | 💎 2 ҷуфт\n\n"
               "💾 <b>Флешкаи аслӣ (64GB)</b>\n🎥 ❌ | 👑 ✅ | 💎 ✅\n\n"
               "📖 <b>Албоми Wedding Day</b>\n🎥 ❌ | 👑 ✅ | 💎 ✅\n\n"
               "🖼️ <b>Албом барои аксҳо</b>\n🎥 ❌ | 👑 ❌ | 💎 ✅\n\n"
               "🎬 <b>Клипи тӯёна</b>\n🎥 ❌ | 👑 ❌ | 💎 ✅\n\n"
               "💕 <b>Love Story</b>\n🎥 ❌ | 👑 ❌ | 💎 ✅\n\n"
               "🎥 <b>Крани наворбардорӣ</b>\n🎥 ❌ | 👑 ❌ | 💎 ✅\n\n"
               "🎁 <b>Тӯҳфаи акси чопшуда</b>\n🎥 10 дона | 👑 30 дона | 💎 50 дона\n\n"
               "⏳ <b>Омодасозии мавод</b>\n🎥 25–30 рӯз | 👑 15–20 рӯз | 💎 7–10 рӯз\n\n"
               "👇 Пакетро интихоб кунед:"),
        "ru": ("📊 <b>СРАВНЕНИЕ ПАКЕТОВ</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               "💰 <b>Цена</b>\n🎥 STANDARD: 1500 сомони\n👑 VIP: 2000 сомони\n💎 VIP PREMIUM: 3000 сомони\n\n"
               "📸 <b>Профессиональная видео- и фотосъёмка</b>\n✅ Во всех трёх пакетах\n\n"
               "💿 <b>Оригинальный DVD-диск</b>\n🎥 1 шт | 👑 1 шт | 💎 2 шт\n\n"
               "💾 <b>Оригинальная флешка (64GB)</b>\n🎥 ❌ | 👑 ✅ | 💎 ✅\n\n"
               "📖 <b>Альбом Wedding Day</b>\n🎥 ❌ | 👑 ✅ | 💎 ✅\n\n"
               "🖼️ <b>Фотоальбом</b>\n🎥 ❌ | 👑 ❌ | 💎 ✅\n\n"
               "🎬 <b>Свадебный клип</b>\n🎥 ❌ | 👑 ❌ | 💎 ✅\n\n"
               "💕 <b>Love Story</b>\n🎥 ❌ | 👑 ❌ | 💎 ✅\n\n"
               "🎥 <b>Операторский кран</b>\n🎥 ❌ | 👑 ❌ | 💎 ✅\n\n"
               "🎁 <b>Подарок — печатные фото</b>\n🎥 10 шт | 👑 30 шт | 💎 50 шт\n\n"
               "⏳ <b>Готовность материала</b>\n🎥 25–30 дней | 👑 15–20 дней | 💎 7–10 дней\n\n"
               "👇 Выберите пакет:"),
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
        "tj": "📝 <b>Қадами 1/4</b> — Лутфан <b>номи худро</b> нависед:",
        "ru": "📝 <b>Шаг 1/4</b> — Пожалуйста, напишите <b>ваше имя</b>:",
    },
    "ask_phone": {
        "tj": "📱 <b>Қадами 2/4</b> — Лутфан рақами телефони худро нависед (масалан 93 882 97 96):",
        "ru": "📱 <b>Шаг 2/4</b> — Напишите ваш номер телефона (например 93 882 97 96):",
    },
    "phone_invalid": {
        "tj": "⚠️ Рақами телефон нодуруст аст. Лутфан танҳо рақамҳо нависед (масалан 93 882 97 96 ё +992 93 882 97 96):",
        "ru": "⚠️ Неверный номер телефона. Пожалуйста, укажите только цифры (например 93 882 97 96 или +992 93 882 97 96):",
    },
    "ask_date": {
        "tj": "📅 <b>Қадами 3/4</b> — Лутфан санаи тӯйро нависед (масалан 15.08.2026):",
        "ru": "📅 <b>Шаг 3/4</b> — Напишите дату свадьбы (например 15.08.2026):",
    },
    "date_invalid": {
        "tj": "⚠️ Формати сана нодуруст аст. Лутфан бо ин формат нависед: РӮЗ.МОҲ.СОЛ (масалан 15.08.2026):",
        "ru": "⚠️ Неверный формат даты. Пожалуйста, укажите в формате ДЕНЬ.МЕСЯЦ.ГОД (например 15.08.2026):",
    },
    "ask_payment": {
        "tj": (f"💳 <b>Қадами 4/4</b> — Оё ҳоло мехоҳед пешпардохт кунед?\n\n"
               f"Барои мустаҳкам кардани ҷои шумо дар санаи интихобшуда, тавсия медиҳем "
               f"{DEPOSIT_AMOUNT} пешпардохт кунед ва чек (скриншоти пардохт)-ро фиристед. Ин ихтиёрист."),
        "ru": (f"💳 <b>Шаг 4/4</b> — Хотите внести предоплату сейчас?\n\n"
               f"Чтобы закрепить за собой выбранную дату, рекомендуем внести предоплату "
               f"{DEPOSIT_AMOUNT} и отправить скриншот чека оплаты. Это по желанию."),
    },
    "pay_now_btn": {"tj": "✅ Ҳоло мехоҳам пардохт кунам", "ru": "✅ Хочу оплатить сейчас"},
    "pay_later_btn": {"tj": "⏳ Дертар пардохт мекунам", "ru": "⏳ Оплачу позже"},
    "payment_link_text": {
        "tj": (f"💳 <b>Пешпардохти {DEPOSIT_AMOUNT}</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               f"1️⃣ Тавассути линки зерин {DEPOSIT_AMOUNT} пардохт кунед:\n\n🔗 {PAYMENT_LINK}\n\n"
               "2️⃣ Тугмаи «Ман пардохт кардам»-ро занед\n"
               "3️⃣ Чек (скриншоти пардохт)-ро фиристед 👇"),
        "ru": (f"💳 <b>Предоплата {DEPOSIT_AMOUNT}</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               f"1️⃣ Внесите предоплату {DEPOSIT_AMOUNT} по ссылке ниже:\n\n🔗 {PAYMENT_LINK}\n\n"
               "2️⃣ Нажмите «Я оплатил(а)»\n"
               "3️⃣ Отправьте скриншот чека оплаты 👇"),
    },
    "pay_continue_btn": {"tj": "✅ Ман пардохт кардам", "ru": "✅ Я оплатил(а)"},
    "ask_receipt": {
        "tj": ("📸 <b>Чеки пардохт</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               "Лутфан расми чек (скриншоти пардохт)-ро фиристед.\n"
               "Метавонед дар зери акс маблағи пардохтшударо низ нависед."),
        "ru": ("📸 <b>Чек оплаты</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               "Пожалуйста, отправьте скриншот чека оплаты.\n"
               "Вы можете указать оплаченную сумму в подписи к фото."),
    },
    "receipt_invalid": {
        "tj": "⚠️ Лутфан расми чекро (акс) фиристед, на матн.",
        "ru": "⚠️ Пожалуйста, отправьте фото чека, а не текст.",
    },
    "receipt_received": {
        "tj": "✅ Чек гирифта шуд! Ба зудӣ санҷида мешавад.",
        "ru": "✅ Чек получен! Скоро будет проверен.",
    },
    "prepay_status": {
        "tj": {True: "✅ Чек фиристод (дар ҳоли санҷиш)", False: "⏳ Пешпардохт накард"},
        "ru": {True: "✅ Отправил(а) чек (на проверке)", False: "⏳ Без предоплаты"},
    },
    "order_prepay": {"tj": "💳 Пешпардохт", "ru": "💳 Предоплата"},
    "confirm_title": {"tj": "🔎 <b>ЛУТФАН ТАСДИҚ КУНЕД</b>", "ru": "🔎 <b>ПОЖАЛУЙСТА, ПОДТВЕРДИТЕ</b>"},
    "confirm_ok": {"tj": "Ҳама дуруст аст?", "ru": "Всё верно?"},
    "order_pkg": {"tj": "📦 Пакет", "ru": "📦 Пакет"},
    "order_name": {"tj": "👤 Ном", "ru": "👤 Имя"},
    "order_phone": {"tj": "📱 Телефон", "ru": "📱 Телефон"},
    "order_date": {"tj": "📅 Санаи тӯй", "ru": "📅 Дата свадьбы"},
    "order_number": {"tj": "🔖 Рақами фармоиш", "ru": "🔖 Номер заказа"},
    "order_accepted": {
        "tj": "🎉 <b>Дархости шумо бомуваффақият сабт гардид!</b>",
        "ru": "🎉 <b>Ваша заявка успешно сохранена!</b>",
    },
    "order_thanks": {
        "tj": ("Ташаккур, ки SIMO.MEDIA-ро интихоб намудед. 🤍\n\n"
               "Дар наздиктарин вақт яке аз намояндагони мо бо шумо тамос гирифта, тамоми маълумоти "
               "заруриро пешниҳод ва фармоиши шуморо тасдиқ мекунад.\n\n"
               "🎥 Мо ифтихор дорем, ки дар муҳимтарин рӯзи зиндагии шумо ҳамроҳатон бошем ва ҳар як "
               "лаҳзаи зеборо ба хотираи ҷовидона табдил диҳем.\n\n"
               "✨ SIMO.MEDIA — сифати баланд, муносибати касбӣ ва хотираҳое, ки ҳамеша зинда мемонанд.\n\n"
               "Аз боварӣ ва интихоби шумо самимона сипосгузорем! 🌹"),
        "ru": ("Спасибо, что выбрали SIMO.MEDIA. 🤍\n\n"
               "В ближайшее время наш представитель свяжется с вами, предоставит всю необходимую "
               "информацию и подтвердит ваш заказ.\n\n"
               "🎥 Мы гордимся тем, что можем быть рядом с вами в самый важный день вашей жизни и "
               "превратить каждый прекрасный момент в вечное воспоминание.\n\n"
               "✨ SIMO.MEDIA — высокое качество, профессиональный подход и воспоминания, которые "
               "останутся навсегда.\n\n"
               "Искренне благодарим за ваше доверие и выбор! 🌹"),
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
    "referral_note": {
        "tj": f"\n\n🎁 <i>Ин мизоҷ тавассути даъвати дӯст омадааст — {REFERRAL_DISCOUNT_PERCENT}% тахфифро дар назар гиред.</i>",
        "ru": f"\n\n🎁 <i>Клиент пришёл по приглашению друга — учтите скидку {REFERRAL_DISCOUNT_PERCENT}%.</i>",
    },
    "error_generic": {
        "tj": "⚠️ Мутаассифона хатогӣ рух дод. Лутфан аз нав кӯшиш кунед ё /start-ро занед.",
        "ru": "⚠️ Произошла ошибка. Пожалуйста, попробуйте снова или нажмите /start.",
    },
    "ask_avail_date": {
        "tj": "📅 <b>Санҷиши дастрасии сана</b>\n━━━━━━━━━━━━━━━━━━\n\nЛутфан санаи мавриди назарро нависед (масалан 15.08.2026):",
        "ru": "📅 <b>Проверка доступности даты</b>\n━━━━━━━━━━━━━━━━━━\n\nПожалуйста, напишите интересующую дату (например 15.08.2026):",
    },
    "date_available": {
        "tj": "✅ <b>Хушхабар!</b> Санаи {date} ҳоло озод аст.\n\nМетавонед ҳозир фармоиш диҳед, то ҷояшро мустаҳкам кунед 👇",
        "ru": "✅ <b>Отличная новость!</b> Дата {date} свободна.\n\nМожете оформить заказ прямо сейчас 👇",
    },
    "date_taken": {
        "tj": "⚠️ Мутаассифона, санаи {date} аллакай банд аст.\n\nЛутфан бо мо тамос гиред то санаҳои алтернативиро муҳокима кунем.",
        "ru": "⚠️ К сожалению, дата {date} уже занята.\n\nСвяжитесь с нами, чтобы обсудить альтернативные даты.",
    },
    "ask_track_number": {
        "tj": "📋 <b>Пайгирии фармоиш</b>\n━━━━━━━━━━━━━━━━━━\n\nЛутфан рақами фармоиши худро нависед (масалан SM-4821):",
        "ru": "📋 <b>Отслеживание заказа</b>\n━━━━━━━━━━━━━━━━━━\n\nПожалуйста, напишите номер вашего заказа (например SM-4821):",
    },
    "track_not_found": {
        "tj": "❌ Фармоише бо ин рақам ёфт нашуд. Лутфан рақамро санҷед ва дубора кӯшиш кунед.",
        "ru": "❌ Заказ с таким номером не найден. Проверьте номер и попробуйте снова.",
    },
    "referral_text": {
        "tj": ("🎁 <b>ДӮСТОНРО ДАЪВАТ КУНЕД</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               f"Линки шахсии худро ба дӯстонатон фиристед — агар онҳо тавассути ин линк фармоиш диҳанд, "
               f"шумо {REFERRAL_DISCOUNT_PERCENT}% тахфиф мегиред!\n\n🔗 <code>{{link}}</code>\n\n"
               "Линкро нусхабардорӣ карда, ба дӯстони худ фиристед 👆"),
        "ru": ("🎁 <b>ПРИГЛАСИТЕ ДРУЗЕЙ</b>\n━━━━━━━━━━━━━━━━━━\n\n"
               f"Отправьте свою персональную ссылку друзьям — если они закажут по этой ссылке, "
               f"вы получите скидку {REFERRAL_DISCOUNT_PERCENT}%!\n\n🔗 <code>{{link}}</code>\n\n"
               "Скопируйте ссылку и отправьте друзьям 👆"),
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

def payment_choice_kb(lang: str):
    b_pay = t("pay_now_btn", lang)
    b_later = t("pay_later_btn", lang)
    kb = [
        [InlineKeyboardButton(b_pay, callback_data="pay_now")],
        [InlineKeyboardButton(b_later, callback_data="pay_later")],
    ]
    return InlineKeyboardMarkup(kb)


def payment_link_kb(lang: str):
    kb = [
        [InlineKeyboardButton(t("pay_continue_btn", lang), callback_data="pay_continue")],
        [InlineKeyboardButton(t("pay_later_btn", lang), callback_data="pay_later")],
    ]
    return InlineKeyboardMarkup(kb)


def receipt_wait_kb(lang: str):
    return InlineKeyboardMarkup([[InlineKeyboardButton(t("pay_later_btn", lang), callback_data="pay_later")]])


ASK_NAME, ASK_PHONE, ASK_DATE, PAYMENT_CHOICE, ASK_RECEIPT, CONFIRM = range(6)

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


def normalize_date(text: str):
    m = re.match(r"^(\d{1,2})[./](\d{1,2})[./](\d{2,4})$", text.strip())
    if not m:
        return None
    day, month, year = m.groups()
    if len(year) == 2:
        year = "20" + year
    try:
        d = datetime(int(year), int(month), int(day))
    except ValueError:
        return None
    return d.strftime("%d.%m.%Y")


def validate_date(text: str) -> bool:
    return normalize_date(text) is not None


# ==================== КЛАВИАТУРАҲО ====================

def main_menu_kb(lang: str):
    b = BTN[lang]
    kb = [
        [InlineKeyboardButton(b["urgent"], callback_data="menu_prices")],
        [InlineKeyboardButton(b["prices"], callback_data="menu_prices"),
         InlineKeyboardButton(b["portfolio"], callback_data="menu_portfolio")],
        [InlineKeyboardButton(b["compare"], callback_data="menu_compare")],
        [InlineKeyboardButton(b["availability"], callback_data="menu_availability"),
         InlineKeyboardButton(b["track"], callback_data="menu_track")],
        [InlineKeyboardButton(b["reviews"], callback_data="rev_0"),
         InlineKeyboardButton(b["stats"], callback_data="menu_stats")],
        [InlineKeyboardButton(b["why"], callback_data="menu_why"),
         InlineKeyboardButton(b["faq"], callback_data="menu_faq")],
        [InlineKeyboardButton(b["about"], callback_data="menu_about"),
         InlineKeyboardButton(b["referral"], callback_data="menu_referral")],
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
    user = update.effective_user
    context.bot_data.setdefault("all_users", {})[user.id] = {
        "name": user.full_name,
        "username": user.username,
    }

    if context.args:
        arg = context.args[0]
        if arg.startswith("ref_"):
            try:
                referrer_id = int(arg[len("ref_"):])
            except ValueError:
                referrer_id = None
            referrals = context.bot_data.setdefault("referrals", {})
            if referrer_id and referrer_id != user.id and user.id not in referrals:
                referrals[user.id] = referrer_id
                context.user_data["referred_by"] = referrer_id
                try:
                    await context.bot.send_message(
                        chat_id=referrer_id,
                        text=(f"🎉 Шахсе тавассути линки даъвати шумо ба SIMO.MEDIA ворид шуд! "
                              f"Агар онҳо фармоиш диҳанд, шумо {REFERRAL_DISCOUNT_PERCENT}% тахфиф мегиред 🎁"),
                    )
                except Exception:
                    pass

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


async def safe_edit(query, text, reply_markup=None, media_url=None):
    try:
        if media_url:
            from telegram import InputMediaPhoto
            await query.edit_message_media(
                media=InputMediaPhoto(media=media_url, caption=text, parse_mode="HTML"),
                reply_markup=reply_markup,
            )
        elif query.message.photo:
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
        context.user_data.pop("awaiting", None)
        await safe_edit(query, t("welcome", lang), main_menu_kb(lang), media_url=WELCOME_IMAGE_URL)

    elif data == "menu_prices":
        await safe_edit(query, t("prices_title", lang), prices_menu_kb(lang))

    elif data == "menu_compare":
        await safe_edit(query, t("compare_table", lang), prices_menu_kb(lang))

    elif data == "menu_why":
        await safe_edit(query, t("why", lang), back_to_main_kb(lang))

    elif data == "menu_stats":
        await safe_edit(query, t("stats", lang), back_to_main_kb(lang))

    elif data == "menu_faq":
        await safe_edit(query, t("faq", lang), back_to_main_kb(lang))

    elif data == "menu_about":
        await safe_edit(query, t("about", lang), back_to_main_kb(lang), media_url=ABOUT_IMAGE_URL)

    elif data == "menu_portfolio":
        await safe_edit(query, t("portfolio_title", lang), portfolio_kb(lang))

    elif data == "menu_contact":
        await safe_edit(query, t("contact", lang), contact_kb(lang))

    elif data == "menu_availability":
        context.user_data["awaiting"] = "availability"
        await safe_edit(query, t("ask_avail_date", lang), back_to_main_kb(lang))

    elif data == "menu_track":
        context.user_data["awaiting"] = "track"
        await safe_edit(query, t("ask_track_number", lang), back_to_main_kb(lang))

    elif data == "menu_referral":
        link = f"https://t.me/{BOT_USERNAME}?start=ref_{query.from_user.id}"
        text = t("referral_text", lang).format(link=link)
        await safe_edit(query, text, back_to_main_kb(lang))

    elif data.startswith("rev_"):
        index = int(data[len("rev_"):])
        await safe_edit(query, review_render(index, lang), reviews_kb(index, lang))

    elif data.startswith("pkg_"):
        pkg_key = data[len("pkg_"):]
        pkg = PACKAGES.get(pkg_key)
        if pkg:
            await safe_edit(query, pkg["text"][lang], package_detail_kb(pkg_key, lang))


async def awaiting_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Идора мекунад агар корбар дар ҳолати интизории вуруд (сана/рақами фармоиш) бошад.
    True бармегардонад агар паём идора шуда бошад."""
    awaiting = context.user_data.get("awaiting")
    if not awaiting:
        return False

    lang = get_lang(context)
    text = update.message.text

    if awaiting == "availability":
        norm = normalize_date(text)
        if not norm:
            await update.message.reply_text(t("date_invalid", lang), parse_mode="HTML")
            return True
        booked = context.bot_data.get("booked_dates", {})
        context.user_data.pop("awaiting", None)
        if norm in booked:
            await update.message.reply_text(
                t("date_taken", lang).format(date=norm), reply_markup=back_to_main_kb(lang), parse_mode="HTML"
            )
        else:
            await update.message.reply_text(
                t("date_available", lang).format(date=norm), reply_markup=prices_menu_kb(lang), parse_mode="HTML"
            )
        return True

    if awaiting == "track":
        order_num = text.strip().upper()
        orders = context.bot_data.get("orders", {})
        context.user_data.pop("awaiting", None)
        order = orders.get(order_num)
        if not order:
            await update.message.reply_text(
                t("track_not_found", lang), reply_markup=back_to_main_kb(lang), parse_mode="HTML"
            )
        else:
            status = order.get("status", "🆕 Нав")
            info = (
                f"📋 <b>{order_num}</b>\n━━━━━━━━━━━━━━━━━━\n\n"
                f"{t('order_pkg', lang)}: {order.get('pkg_short', '—')}\n"
                f"{t('order_date', lang)}: {order.get('date', '—')}\n\n"
                f"📌 <b>Ҳолат:</b> {status}"
            )
            await update.message.reply_text(info, reply_markup=back_to_main_kb(lang), parse_mode="HTML")
        return True

    return False


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
    norm = normalize_date(date_text)
    if not norm:
        await update.message.reply_text(t("date_invalid", lang), parse_mode="HTML")
        return ASK_DATE

    context.user_data["order_date"] = norm
    context.user_data["order_number"] = f"SM-{random.randint(1000, 9999)}"

    await update.message.reply_text(t("ask_payment", lang), reply_markup=payment_choice_kb(lang), parse_mode="HTML")
    return PAYMENT_CHOICE


def build_confirm_summary(context: ContextTypes.DEFAULT_TYPE, lang: str) -> str:
    pkg = context.user_data.get("order_pkg", {})
    name = context.user_data.get("order_name", "—")
    phone = context.user_data.get("order_phone", "—")
    date = context.user_data.get("order_date", "—")
    order_number = context.user_data.get("order_number", "—")
    prepay = context.user_data.get("prepay", False)
    prepay_label = t("prepay_status", lang)[prepay]

    return (
        f"{t('confirm_title', lang)}\n━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('order_number', lang)}: <b>{order_number}</b>\n"
        f"{t('order_pkg', lang)}: {pkg.get('short', '—')}\n"
        f"{t('order_name', lang)}: {name}\n"
        f"{t('order_phone', lang)}: {phone}\n"
        f"{t('order_date', lang)}: {date}\n"
        f"{t('order_prepay', lang)}: {prepay_label}\n\n"
        f"{t('confirm_ok', lang)}"
    )


async def payment_choice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_lang(context)

    if query.data == "pay_now":
        await safe_edit(query, t("payment_link_text", lang), payment_link_kb(lang))
        return PAYMENT_CHOICE

    context.user_data["prepay"] = False
    await safe_edit(query, build_confirm_summary(context, lang), confirm_kb(lang))
    return CONFIRM


async def payment_continue_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_lang(context)
    await safe_edit(query, t("ask_receipt", lang), receipt_wait_kb(lang))
    return ASK_RECEIPT


async def receipt_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    user = update.message.from_user
    context.user_data["prepay"] = True

    order_number = context.user_data.get("order_number", "—")
    pkg = context.user_data.get("order_pkg", {})
    caption = (
        f"🧾 <b>Чеки пардохт — {order_number}</b>\n"
        f"👤 {context.user_data.get('order_name', '—')} | 📱 {context.user_data.get('order_phone', '—')}\n"
        f"📦 {pkg.get('short', '—')}\n"
    )
    if update.message.caption:
        caption += f"\n💬 {update.message.caption}"

    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_photo(
                chat_id=admin_id,
                photo=update.message.photo[-1].file_id,
                caption=caption,
                parse_mode="HTML",
            )
        except Exception as e:
            logger.error(f"Чек ба админ нарафт: {e}")

    await update.message.reply_text(t("receipt_received", lang))
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    await update.message.reply_text(build_confirm_summary(context, lang), reply_markup=confirm_kb(lang), parse_mode="HTML")
    return CONFIRM


async def receipt_wrong_type_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    await update.message.reply_text(t("receipt_invalid", lang))
    return ASK_RECEIPT


async def order_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_lang(context)
    await safe_edit(query, t("ask_name", lang))
    return ASK_NAME


async def reminder_job(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    order_number = job_data["order_number"]
    orders = context.bot_data.get("orders", {})
    order = orders.get(order_number)
    if not order or order.get("status") != "🆕 Нав":
        return
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=(
                    f"⏰ <b>ЁДОВАРӢ!</b>\n━━━━━━━━━━━━━━━━━━\n\n"
                    f"Фармоиши <b>{order_number}</b> зиёда аз {REMINDER_HOURS} соат ҷавоб намондааст!\n\n"
                    f"👤 {order.get('name', '—')} | 📱 {order.get('phone', '—')}\n"
                    f"📦 {order.get('pkg_short', '—')} | 📅 {order.get('date', '—')}"
                ),
                parse_mode="HTML",
            )
        except Exception as e:
            logger.error(f"Ёдоварӣ фиристода нашуд: {e}")


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
    prepay = context.user_data.get("prepay", False)
    prepay_label = t("prepay_status", lang)[prepay]

    hours_note = "" if is_within_work_hours() else t("after_hours_note", lang)

    await safe_edit(
        query,
        f"{t('order_accepted', lang)}\n━━━━━━━━━━━━━━━━━━\n\n"
        f"{t('order_number', lang)}: <b>{order_number}</b>\n"
        f"{t('order_pkg', lang)}: {pkg.get('short', '—')}\n"
        f"{t('order_name', lang)}: {name}\n"
        f"{t('order_phone', lang)}: {phone}\n"
        f"{t('order_date', lang)}: {date}\n"
        f"{t('order_prepay', lang)}: {prepay_label}\n\n"
        f"{t('order_thanks', lang)}\n\n<i>{t('order_keep_number', lang)}</i>{hours_note}",
        after_order_kb(lang),
    )

    context.bot_data.setdefault("known_customers", {})[user.id] = lang
    context.bot_data.setdefault("customer_last_order", {})[user.id] = order_number
    context.bot_data.setdefault("booked_dates", {})[date] = order_number
    context.bot_data.setdefault("orders", {})[order_number] = {
        "chat_id": user.id, "lang": lang, "pkg_short": pkg.get("short", "—"),
        "name": name, "phone": phone, "date": date, "status": "🆕 Нав", "prepay": prepay,
    }

    is_referred = bool(context.user_data.get("referred_by"))
    referral_extra = t("referral_note", lang) if is_referred else ""
    prepay_extra = f"\n💳 Пешпардохт: {'Ҳа' if prepay else 'Не'}"
    verify_note = ("\n\n⚠️ <b>Диққат:</b> Мизоҷ гуфт, ки пардохт кардааст — лутфан "
                    "тавассути ExpressPay санҷед, пеш аз идомаи кор!") if prepay else ""

    for admin_id in ADMIN_IDS:
        try:
            sent_msg = await context.bot.send_message(
                chat_id=admin_id,
                text=(
                    "🆕 <b>ФАРМОИШИ НАВ!</b>\n━━━━━━━━━━━━━━━━━━\n\n"
                    f"🔖 Рақами фармоиш: <b>{order_number}</b>\n"
                    f"📦 Пакет: {pkg.get('short', '—')}\n"
                    f"👤 Ном: {name}\n📱 Телефон: {phone}\n📅 Санаи тӯй: {date}"
                    f"{prepay_extra}{verify_note}\n\n"
                    f"Telegram: @{user.username if user.username else '—'}\n"
                    f"User ID: {user.id}"
                    f"{referral_extra}\n\n"
                    "💬 <i>Барои ҷавоб додан ба мизоҷ, ба ҳамин паём Reply кунед.</i>"
                ),
                parse_mode="HTML",
            )
            context.bot_data.setdefault("order_chats", {})[sent_msg.message_id] = {
                "chat_id": user.id,
                "lang": lang,
            }
        except Exception as e:
            logger.error(f"Хабар ба админ нарафт: {e}")

    if context.job_queue:
        context.job_queue.run_once(
            reminder_job, when=timedelta(hours=REMINDER_HOURS), data={"order_number": order_number}
        )

    context.user_data.pop("order_pkg", None)
    context.user_data.pop("order_name", None)
    context.user_data.pop("order_phone", None)
    context.user_data.pop("order_date", None)
    context.user_data.pop("order_number", None)
    context.user_data.pop("prepay", None)
    return ConversationHandler.END


async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    context.user_data.clear()
    await update.message.reply_text("Бекор карда шуд / Отменено", reply_markup=main_menu_kb(lang))
    return ConversationHandler.END


async def relay_customer_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    handled = await awaiting_input_handler(update, context)
    if handled:
        return

    user = update.message.from_user
    known = context.bot_data.get("known_customers", {})

    if user.id not in known:
        lang = get_lang(context)
        await update.message.reply_text(t("unknown", lang), reply_markup=main_menu_kb(lang))
        return

    lang = known[user.id]
    order_num = context.bot_data.get("customer_last_order", {}).get(user.id, "")
    label = f" ({order_num})" if order_num else ""
    username_part = f" (@{user.username})" if user.username else ""

    text_for_admin = (
        f"💬 <b>Паём аз мизоҷ{label}</b>\n━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 {user.full_name}{username_part}\n\n"
        f"{update.message.text}\n\n"
        "<i>Барои ҷавоб додан, ба ин паём Reply кунед.</i>"
    )

    for admin_id in ADMIN_IDS:
        try:
            sent = await context.bot.send_message(chat_id=admin_id, text=text_for_admin, parse_mode="HTML")
            context.bot_data.setdefault("order_chats", {})[sent.message_id] = {
                "chat_id": user.id,
                "lang": lang,
            }
        except Exception as e:
            logger.error(f"Паёми мизоҷ ба админ нарафт: {e}")

    ack = ("🙏 Паёми шумо гирифта шуд. Ба наздикӣ ҷавоб медиҳем."
           if lang == "tj" else "🙏 Ваше сообщение получено. Скоро ответим.")
    await update.message.reply_text(ack)


async def admin_reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_to = update.message.reply_to_message
    order_chats = context.bot_data.get("order_chats", {})
    mapping = order_chats.get(reply_to.message_id) if reply_to else None

    if not mapping:
        await update.message.reply_text(
            "⚠️ Ин паём ба ягон фармоиш алоқаманд нест — лутфан ба худи паёми "
            "\"ФАРМОИШИ НАВ!\" Reply кунед."
        )
        return

    target_chat_id = mapping["chat_id"]
    try:
        await context.bot.send_message(
            chat_id=target_chat_id,
            text=f"💬 <b>SIMO.MEDIA:</b>\n\n{update.message.text}",
            parse_mode="HTML",
        )
        await update.message.reply_text("✅ Ба мизоҷ фиристода шуд.")
    except Exception as e:
        logger.error(f"Ҷавоб ба мизоҷ нарафт: {e}")
        await update.message.reply_text("⚠️ Фиристодан ба мизоҷ муяссар нашуд (шояд боти моро блок кардааст).")


# ==================== КОМАНДАҲОИ АДМИН ====================

async def admin_only(update: Update) -> bool:
    return update.effective_user and update.effective_user.id in ADMIN_IDS


async def cmd_booked(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await admin_only(update):
        return
    booked = context.bot_data.get("booked_dates", {})
    if not booked:
        await update.message.reply_text("Ягон сана банд нест.")
        return
    lines = [f"📅 {date} — {order}" for date, order in sorted(booked.items())]
    await update.message.reply_text("📋 <b>Санаҳои банд:</b>\n\n" + "\n".join(lines), parse_mode="HTML")


async def cmd_freedate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await admin_only(update):
        return
    if not context.args:
        await update.message.reply_text("Истифода: /freedate 15.08.2026")
        return
    norm = normalize_date(context.args[0])
    if not norm:
        await update.message.reply_text("Формати сана нодуруст. Мисол: /freedate 15.08.2026")
        return
    booked = context.bot_data.get("booked_dates", {})
    if norm in booked:
        del booked[norm]
        await update.message.reply_text(f"✅ Санаи {norm} озод карда шуд.")
    else:
        await update.message.reply_text(f"Санаи {norm} дар рӯйхати банд нест.")


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await admin_only(update):
        return
    if len(context.args) < 2:
        await update.message.reply_text("Истифода: /status SM-1234 Тасдиқшуда")
        return
    order_number = context.args[0].upper()
    new_status = " ".join(context.args[1:])
    orders = context.bot_data.get("orders", {})
    order = orders.get(order_number)
    if not order:
        await update.message.reply_text(f"Фармоиши {order_number} ёфт нашуд.")
        return
    order["status"] = new_status
    await update.message.reply_text(f"✅ Ҳолати {order_number} иваз шуд ба: {new_status}")
    try:
        lang = order.get("lang", "tj")
        note = (f"📌 Ҳолати фармоиши шумо ({order_number}) иваз шуд:\n<b>{new_status}</b>"
                if lang == "tj" else
                f"📌 Статус вашего заказа ({order_number}) изменён:\n<b>{new_status}</b>")
        await context.bot.send_message(chat_id=order["chat_id"], text=note, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Огоҳии тағйири ҳолат ба мизоҷ нарафт: {e}")


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await admin_only(update):
        return
    all_users = context.bot_data.get("all_users", {})
    known_customers = context.bot_data.get("known_customers", {})
    orders = context.bot_data.get("orders", {})
    referrals = context.bot_data.get("referrals", {})

    status_counts = {}
    for o in orders.values():
        s = o.get("status", "🆕 Нав")
        status_counts[s] = status_counts.get(s, 0) + 1

    lines = [
        "📊 <b>ОМОРИ БОТ</b>",
        "━━━━━━━━━━━━━━━━━━",
        "",
        f"👥 Ҳамагӣ кушодаанд ботро: <b>{len(all_users)}</b> нафар",
        f"📝 Фармоиш додаанд: <b>{len(known_customers)}</b> нафар",
        f"🔖 Ҳамагӣ фармоишҳо: <b>{len(orders)}</b>",
        f"🎁 Тавассути даъвати дӯст омадаанд: <b>{len(referrals)}</b> нафар",
    ]
    if status_counts:
        lines.append("")
        lines.append("<b>Ҳолати фармоишҳо:</b>")
        for status, count in status_counts.items():
            lines.append(f"• {status}: {count}")

    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


async def cmd_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await admin_only(update):
        return
    if not context.args:
        await update.message.reply_text("Истифода: /broadcast Матни паём барои ҳама мизоҷон")
        return
    text = " ".join(context.args)
    known = context.bot_data.get("known_customers", {})
    sent, failed = 0, 0
    for chat_id in list(known.keys()):
        try:
            await context.bot.send_message(chat_id=chat_id, text=f"📢 <b>SIMO.MEDIA</b>\n\n{text}", parse_mode="HTML")
            sent += 1
        except Exception:
            failed += 1
    await update.message.reply_text(f"✅ Фиристода шуд ба {sent} мизоҷ. Хато: {failed}.")


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
            PAYMENT_CHOICE: [
                CallbackQueryHandler(payment_choice_handler, pattern="^pay_(now|later)$"),
                CallbackQueryHandler(payment_continue_handler, pattern="^pay_continue$"),
            ],
            ASK_RECEIPT: [
                CallbackQueryHandler(payment_choice_handler, pattern="^pay_later$"),
                MessageHandler(filters.PHOTO, receipt_photo_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, receipt_wrong_type_handler),
            ],
            CONFIRM: [
                CallbackQueryHandler(order_confirm, pattern="^order_confirm$"),
                CallbackQueryHandler(order_restart, pattern="^order_restart$"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_order)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", start))
    application.add_handler(CommandHandler("booked", cmd_booked))
    application.add_handler(CommandHandler("freedate", cmd_freedate))
    application.add_handler(CommandHandler("status", cmd_status))
    application.add_handler(CommandHandler("stats", cmd_stats))
    application.add_handler(CommandHandler("broadcast", cmd_broadcast))
    application.add_handler(
        MessageHandler(
            filters.REPLY & filters.User(user_id=ADMIN_IDS) & filters.TEXT & ~filters.COMMAND,
            admin_reply_handler,
        )
    )
    application.add_handler(order_conv)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.User(user_id=ADMIN_IDS), relay_customer_message)
    )
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.ALL, unknown_message))
    application.add_error_handler(error_handler)

    print("🤖 SIMO.MEDIA bot кор карда истодааст...")
    application.run_polling()


if __name__ == "__main__":
    main()
