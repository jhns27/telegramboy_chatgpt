from dotenv import load_dotenv
import os

# Загрузка переменных из .env файла
load_dotenv()

# Telegram Bot Configuration
TOKEN = os.getenv("TOKEN")  # Токен Telegram-бота
MAIN_ADMIN = os.getenv("MAIN_ADMIN", "489271584")  # Telegram CHAT_ID администратора
MAIN_ADMIN_NIK = os.getenv("MAIN_ADMIN_NIK", "@admin_nickname")  # Ник администратора
WORK_DIR = os.getenv("WORK_DIR", "/root/telegrambot/telegrambot/gemine")  # Рабочая директория

# SNMP Configuration
LOG_STABLE = os.getenv("LOG_STABLE", "bot.log")  # Имя файла для логов
MO_switchs = ["10.39.64.0/25", "10.39.65.0/25", "10.39.87.0/25", "10.39.0.0/16"]
#MO_switchs = os.getenv("MO_switchs", "10.39.64.0/25,10.39.65.0/25,10.39.87.0/25")  # Подсеть устройств
ro_switchs = os.getenv("ro_switchs", "eriwpirt")  # SNMP Read-Only Community

# Default OIDs
oid_sysname = "1.3.6.1.2.1.1.5.0"  # OID для имени устройства
oid_uptime = "1.3.6.1.2.1.1.3.0"  # OID для времени работы устройства

# Models and their specific OIDs
MODELS_OID_CONFIG = {
    "MES2428": {
        "sysname": oid_sysname,
        "uptime": oid_uptime,
        "port_index": " 1.3.6.1.2.1.31.1.1.1.1",
        "port_description": "1.3.6.1.2.1.31.1.1.1.18",
        "port_speed": "1.3.6.1.2.1.31.1.1.1.15",
        "oper_status": "1.3.6.1.2.1.2.2.1.8",
        "admin_status": "1.3.6.1.2.1.2.2.1.7",
        "cable_test_start": "1.3.6.1.4.1.35265.52.1.2.1.1.1.1",
        "cable_test_status": "1.3.6.1.4.1.35265.52.1.2.1.2.1.2",
        "cable_test_length": "1.3.6.1.4.1.35265.52.1.2.1.2.1.3",
        "cable_test_short_circuit": "1.3.6.1.4.1.35265.52.1.2.1.2.1.3",
    },
    "MES2408": {
        "sysname": oid_sysname,
        "uptime": oid_uptime,
        "port_index": "1.3.6.1.2.1.2.2.1.1",
        "port_description": "1.3.6.1.2.1.31.1.1.1.18",
        "port_speed": "1.3.6.1.2.1.31.1.1.1.15",
        "oper_status": "1.3.6.1.2.1.2.2.1.8",
        "admin_status": "1.3.6.1.2.1.2.2.1.7",
        "cable_test_start": "1.3.6.1.4.1.35265.52.1.2.1.1.1.1",
        "cable_test_status": "1.3.6.1.4.1.35265.52.1.2.1.2.1.2",
        "cable_test_length": "1.3.6.1.4.1.35265.52.1.2.1.2.1.3",
        "cable_test_short_circuit": "1.3.6.1.4.1.35265.52.1.2.1.2.1.3",
    },
    "MES2308": {
        "sysname": oid_sysname,  # Убедитесь, что эти OID правильные для устройства MES2308
        "uptime": oid_uptime,
        "port_index": "1.3.6.1.2.1.2.2.1.1",
        "port_description": "1.3.6.1.2.1.31.1.1.1.18",
        "port_speed": "1.3.6.1.2.1.31.1.1.1.15",
        "oper_status": "1.3.6.1.2.1.2.2.1.8",
        "admin_status": "1.3.6.1.2.1.2.2.1.7",
        "cable_test_start": "1.3.6.1.4.1.35265.52.1.2.1.1.1.1",
        "cable_test_status": "1.3.6.1.4.1.35265.52.1.2.1.2.1.2",
        "cable_test_length": "1.3.6.1.4.1.35265.52.1.2.1.2.1.3",
        "cable_test_short_circuit": "1.3.6.1.4.1.35265.52.1.2.1.2.1.3",
    },
    "JetStream": {
        "sysname": oid_sysname,
        "uptime": oid_uptime,
        "port_index": "1.3.6.1.2.1.2.2.1.1",
        "port_description": "1.3.6.1.2.1.31.1.1.1.18",
        "port_speed": "1.3.6.1.2.1.31.1.1.1.15",
        "oper_status": "1.3.6.1.2.1.2.2.1.8",
        "admin_status": "1.3.6.1.2.1.2.2.1.7",
        "cable_test_start": "1.3.6.1.4.1.35265.52.1.2.1.1.1.1",
        "cable_test_status": "1.3.6.1.4.1.35265.52.1.2.1.2.1.2",
        "cable_test_length": "1.3.6.1.4.1.35265.52.1.2.1.2.1.3",
        "cable_test_short_circuit": "1.3.6.1.4.1.35265.52.1.2.1.2.1.3",
    },
    "MES1124MB": {
        "sysname": oid_sysname,
        "uptime": oid_uptime,
        "port_index": "1.3.6.1.2.1.2.2.1.2",
        "port_description": "1.3.6.1.2.1.31.1.1.1.18",
        "port_speed": "1.3.6.1.2.1.2.2.1.5",
        "oper_status": "1.3.6.1.2.1.2.2.1.8",
        "admin_status": "1.3.6.1.2.1.2.2.1.7",
        "cable_test_start": "1.3.6.1.4.1.35265.52.1.2.1.1.1.1",
        "cable_test_status": "1.3.6.1.4.1.35265.52.1.2.1.2.1.2",
        "cable_test_length": "1.3.6.1.4.1.35265.52.1.2.1.2.1.3",
        "cable_test_short_circuit": "1.3.6.1.4.1.35265.52.1.2.1.2.1.3",
    },
    "MES3500-24": {
        "sysname": oid_sysname,
        "uptime": oid_uptime,
        "port_index": "1.3.6.1.2.1.2.2.1.1",
        "port_description": "1.3.6.1.2.1.31.1.1.1.18",
        "port_speed": "1.3.6.1.2.1.31.1.1.1.15",
        "oper_status": "1.3.6.1.2.1.2.2.1.8",
        "admin_status": "1.3.6.1.2.1.2.2.1.7",
        "cable_test_start": "1.3.6.1.4.1.35265.52.1.2.1.1.1.1",
        "cable_test_status": "1.3.6.1.4.1.35265.52.1.2.1.2.1.2",
        "cable_test_length": "1.3.6.1.4.1.35265.52.1.2.1.2.1.3",
        "cable_test_short_circuit": "1.3.6.1.4.1.35265.52.1.2.1.2.1.3",
    },
    "Default": {  # Дефолтная конфигурация для неизвестных моделей
        "sysname": oid_sysname,
        "uptime": oid_uptime,
        "port_index": "1.3.6.1.2.1.2.2.1.1",
        "port_description": "1.3.6.1.2.1.31.1.1.1.18",
        "port_speed": "1.3.6.1.2.1.31.1.1.1.15",
        "oper_status": "1.3.6.1.2.1.2.2.1.8",
        "admin_status": "1.3.6.1.2.1.2.2.1.7",
        "cable_test_start": "1.3.6.1.4.1.35265.52.1.2.1.1.1.1",
        "cable_test_status": "1.3.6.1.4.1.35265.52.1.2.1.2.1.2",
        "cable_test_length": "1.3.6.1.4.1.35265.52.1.2.1.2.1.3",
        "cable_test_short_circuit": "1.3.6.1.4.1.35265.52.1.2.1.2.1.3",
    },

}



# Диапазоны портов для каждой модели
PORT_RANGES = {
    "MES2408": range(1, 11),  # Порты 1-10
    "MES2428": range(1, 29),  # Порты 1-28
    "MES1124MB": range(1, 25),  # Порты 1-28
    "MES3500-24": range(1, 29),  # Порты 1-28
    "MES1124": range(1, 29),  # Порты 1-28
    "Default": range(1, 11),  # Дефолтные порты (например, для неизвестных моделей)
}





















# Symbols for Status
UP = "\U00002705 "  # Зелёная галочка
DOWN = "\U0000274C "  # Красный крест
CRITICAL = "\U0001F525 "  # Пламя (критическая ошибка)
VICTORY = "\U0000270C "  # Победа
MAGIC = "\U0001F4A5 "  # Магия
