from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Основное меню
def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🗂 Создать файл"),
                KeyboardButton(text="💳 Создать банковскую карту"),
            ],
            [
                KeyboardButton(text="🧪 Создать Pairwise тест"),
                KeyboardButton(text="📑 Проверить JSON")
            ],
            [
                KeyboardButton(text="📋 Создать тест-кейс"),
                KeyboardButton(text="🐞 Создать баг-репорт")
            ],
            [
                KeyboardButton(text="👥 Создать тестовые данные")
            ],
            [
                KeyboardButton(text="Информация")
            ]
        ],
        resize_keyboard=True
    )

# Меню с кнопкой Назад
def get_back_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Назад в меню")]
        ],
        resize_keyboard=True
    )

# Текстовые сообщения
WELCOME_MSG = "Привет!👋 Я QA Ai Assistant 🤖\n\nВыбери, что нужно сделать:"
MENU_MSG = "Выбери, что нужно сделать:"
HELP_MSG = (
    "Доступные команды:\n"
    "/file - 🗂 Создать файл\n"
    "/payment - 💳 Создать банковскую карту\n"
    "/pairwise - 🧪 Создать Pairwise тест\n"
    "/json - 📑 Проверить JSON\n"
    "/testcase - 📋 Создать тест-кейс\n"
    "/bug - 🐞 Создать баг-репорт\n"
    "/testdata - 👥 Создать тестовые данные\n"
    "/cancel - отмена текущей операции\n"
    "/help - вызов справки\n\n"
    "ℹ️ Или используй кнопки меню ниже 👇"
)
