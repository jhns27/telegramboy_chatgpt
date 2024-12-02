#!/usr/bin/python3
import logging
import ipaddress
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import puresnmp
import constant
import datetime
import allowed_users


# Проверка, является ли пользователь разрешенным
def is_allowed_user(user_id):
    return user_id in allowed_users.ALLOWED_USERS


# Состояния для обработки
(MENU, CHECK_DEVICE, CHECK_PORTS) = range(3)

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename=constant.LOG_STABLE,
)
logger = logging.getLogger(__name__)

# Проверка корректности IP-адреса
def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

# Получение модели устройства
def get_device_model(host):
    try:
        sys_descr = puresnmp.get(host, constant.ro_switchs, ".1.3.6.1.2.1.1.1.0").decode("utf-8")
        logger.info(f"sysDescr от устройства {host}: {sys_descr}")

        for model in constant.MODELS_OID_CONFIG.keys():
            if model in sys_descr:
                logger.info(f"Модель устройства определена как {model}")
                return model

        logger.warning(f"Модель устройства {host} не найдена. Используем Default.")
        return "Default"
    except Exception as e:
        logger.error(f"Ошибка определения модели устройства {host}: {e}")
        return "Default"

# Получение базовой информации об устройстве
def get_basic_info(host):
    try:
        model = get_device_model(host)
        oids = constant.MODELS_OID_CONFIG.get(model, constant.MODELS_OID_CONFIG["Default"])

        sysname = puresnmp.get(host, constant.ro_switchs, oids["sysname"]).decode("utf-8")
        uptime_ticks = puresnmp.get(host, constant.ro_switchs, oids["uptime"])

        # Обработка времени работы
        if isinstance(uptime_ticks, datetime.timedelta):
            uptime_seconds = uptime_ticks.total_seconds()
        else:
            uptime_seconds = int(uptime_ticks) / 100  # Учитываем, что значение SNMP может быть в сотых долях секунд

        days, rem = divmod(uptime_seconds, 86400)
        hours, rem = divmod(rem, 3600)
        minutes = rem // 60
        uptime = f"{int(days)} дн. {int(hours)} ч. {int(minutes)} мин."

        return f"✅✅✅ Имя устройства: {sysname}\nВремя работы: {uptime}"
    except Exception as e:
        logger.error(f"Ошибка при запросе базовой информации {host}: {e}")
        return "❌❌❌ Ошибка при запросе информации."

# Получение состояния портов
def get_port_status(host):
    try:
        model = get_device_model(host)
        oids = constant.MODELS_OID_CONFIG.get(model, constant.MODELS_OID_CONFIG["Default"])
        port_range = constant.PORT_RANGES.get(model, constant.PORT_RANGES["Default"])

        results = []
        for port_index in port_range:
            try:
                port_description = puresnmp.get(host, constant.ro_switchs, oids["port_description"] + f".{port_index}").decode("utf-8")
            except:
                port_description = "Без описания"
            try:
                oper_status = "UP" if int(puresnmp.get(host, constant.ro_switchs, oids["oper_status"] + f".{port_index}")) == 1 else "DOWN"
                oper_status_icon = "🟢" if oper_status == "UP" else "🔴"
            except:
                oper_status = "Неизвестно"
                oper_status_icon = "🔴"
            try:
                admin_status = "UP" if int(puresnmp.get(host, constant.ro_switchs, oids["admin_status"] + f".{port_index}")) == 1 else "DOWN"
            except:
                admin_status = "Неизвестно"
            try:
                port_speed = f"{int(puresnmp.get(host, constant.ro_switchs, oids['port_speed'] + f'.{port_index}'))} Mbps"
            except:
                port_speed = "0 Mbps"

            results.append(
                f"{oper_status_icon} Порт: {port_index} | Описание: {port_description} | "
                f"Статус: {oper_status} | Админ статус: {admin_status} | Скорость: {port_speed}"
            )
        return "\n".join(results)
    except Exception as e:
        logger.error(f"Ошибка при запросе состояния портов {host}: {e}")
        return "Ошибка при запросе портов."

# Обработчик команды /start
def start(update, context):
    user = update.message.from_user
    reply_keyboard = [["💥 Проверить устройство"]]
    update.message.reply_text(
        f"✌ Добро пожаловать, {user.full_name}! Выберите действие.",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True),
    )
    return MENU

# Обработчик проверки устройства
def check_device(update, context):
    host = update.message.text.strip()
    if not is_valid_ip(host):
        update.message.reply_text("Некорректный IP-адрес. Попробуйте снова.")
        return CHECK_DEVICE

    logger.info(f"Пользователь ввел IP: {host}")
    context.user_data["host"] = host

    result = get_basic_info(host)
    update.message.reply_text(result)

    # Сброс при ошибке
    if "Ошибка" in result:
        context.user_data.clear()
        update.message.reply_text("Введите IP-адрес нового устройства:")
        return CHECK_DEVICE

    reply_keyboard = [["Состояние портов", "Сброс"]]
    update.message.reply_text(
        "Выберите действие:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    )
    return MENU

# Обработчик меню
def menu(update, context):
    message = update.message.text.strip()

    if "💥 Проверить устройство" in message:
        update.message.reply_text("Введите IP-адрес устройства:", reply_markup=ReplyKeyboardRemove())
        return CHECK_DEVICE

    elif "Состояние портов" in message or "Повторно проверить порты" in message:
        host = context.user_data.get("host", "")
        if not host:
            update.message.reply_text("Сначала проверьте устройство и введите его IP-адрес.")
            return MENU

        result = get_port_status(host)
        update.message.reply_text(result)

        reply_keyboard = [["Повторно проверить порты", "Сброс"]]
        update.message.reply_text(
            "Что бы вы хотели сделать дальше?",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        )
        return MENU

    elif "Сброс" in message:
        context.user_data.clear()
        update.message.reply_text("Введите IP-адрес нового устройства:")
        return CHECK_DEVICE

    update.message.reply_text("Команда не распознана. Попробуйте снова.")
    return MENU

# Основная функция
def main():
    updater = Updater(constant.TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [MessageHandler(Filters.text & ~Filters.command, menu)],
            CHECK_DEVICE: [MessageHandler(Filters.text & ~Filters.command, check_device)],
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: update.message.reply_text("Прощайте!"))],
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
