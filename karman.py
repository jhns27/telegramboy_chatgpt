#!/usr/bin/python3
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import puresnmp
import constant
import datetime

# Состояния для обработки
(MENU, CHECK_DEVICE) = range(2)

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename=constant.LOG_STABLE,
)
logger = logging.getLogger(__name__)

# Функция для получения базовой информации об устройстве через SNMP
import datetime

def get_basic_info(host):
    try:
        logger.info(f"Пытаемся подключиться к устройству {host} через SNMP...")

        # Запрашиваем имя устройства (sysName)
        sysname = puresnmp.get(host, constant.ro_switchs, constant.oid_sysname).decode("utf-8")
        logger.info(f"sysName устройства: {sysname}")

        # Запрашиваем Uptime устройства
        uptime_ticks = puresnmp.get(host, constant.ro_switchs, constant.oid_uptime)

        # Если uptime_ticks это объект timedelta, то извлекаем количество секунд
        if isinstance(uptime_ticks, datetime.timedelta):
            uptime_seconds = uptime_ticks.total_seconds()  # Получаем общее количество секунд
            logger.info(f"Uptime устройства: {uptime_seconds} секунд")

            # Преобразуем в дни, часы, минуты, секунды
            days = int(uptime_seconds // 86400)  # 1 день = 86400 секунд
            hours = int((uptime_seconds % 86400) // 3600)  # 1 час = 3600 секунд
            minutes = int((uptime_seconds % 3600) // 60)  # 1 минута = 60 секунд
            seconds = int(uptime_seconds % 60)

            uptime = f"{days} дн. {hours} ч. {minutes} мин. {seconds} сек."
            logger.info(f"Время работы устройства: {uptime}")
        else:
            uptime = "неизвестно"
            logger.warning(f"Не удалось извлечь uptime: {uptime_ticks}")

        result = f"{constant.UP} Имя устройства: {sysname}\nВремя работы: {uptime}"
        return result

    except Exception as e:
        # Логируем подробности ошибки
        logger.error(f"Ошибка при запросе SNMP данных у {host}: {e}")
        return f"{constant.CRITICAL} Устройство не доступно или неверный IP."



# Обработчики команд
def start(update, context):
    user = update.message.from_user
    reply_keyboard = [[f"{constant.MAGIC} Проверить устройство"]]
    update.message.reply_text(
        f"{constant.VICTORY} Добро пожаловать, {user.full_name}!",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
    )
    logger.info(f"Пользователь {user.full_name} запустил бота.")
    return MENU

def menu(update, context):
    message = update.message.text
    if "Проверить устройство" in message:
        update.message.reply_text("Введите IP-адрес устройства:", reply_markup=ReplyKeyboardRemove())
        return CHECK_DEVICE
    else:
        update.message.reply_text("Команда не распознана. Попробуйте снова.")
        return MENU

def check_device(update, context):
    host = update.message.text.strip()  # Убираем лишние пробелы
    logger.info(f"Пользователь ввел IP: {host}")
    
    # Получаем данные об устройстве
    result = get_basic_info(host)
    update.message.reply_text(result)

    # Возвращаемся в меню для ожидания следующего ввода
    reply_keyboard = [[f"{constant.MAGIC} Проверить устройство"]]
    update.message.reply_text(
        "Что бы вы хотели сделать дальше?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    )
    return MENU  # Возвращаемся в меню, чтобы бот снова ждал команды


def cancel(update, context):
    user = update.message.from_user
    logger.info(f"Пользователь {user.full_name} завершил работу с ботом.")
    update.message.reply_text("До свидания!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Основная функция
def main():
    updater = Updater(constant.TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [MessageHandler(Filters.text, menu)],
            CHECK_DEVICE: [MessageHandler(Filters.text, check_device)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
