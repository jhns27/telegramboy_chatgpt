from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd
import telebot

# Создание экземпляра класса TeleBot
bot = telebot.TeleBot('7800153533:AAF6mO5uw8YcOt_gHAAIqXjBDGd3dSJgg0A')

def send_data_to_telegram(data):
    # Отправка данных в телеграм-бот
    bot.send_message(chat_id='489271584', text=data)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Запрос IP-адреса у пользователя
    bot.send_message(message.chat.id, "Пожалуйста, отправьте IP-адрес коммутатора.")
    
    @bot.message_handler(func=lambda m: True)  # Для обработки следующего сообщения
    def get_ip(message):
        snmp_host = message.text
        print("IP-адрес коммутатора: " + snmp_host)

        # Подключение к коммутатору через SNMP
        iterator = getCmd(SnmpEngine(),
                          CommunityData('public'),  # Замените на нужное сообщество
                          UdpTransportTarget((snmp_host, 161)),
                          ContextData(),
                          ObjectType(ObjectIdentity('IF-MIB', 'ifDescr')))  # Запрос дескрипторов интерфейсов
        
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication:
            print("Ошибка при получении данных: ", errorIndication)
        elif errorStatus:
            print("Статус ошибки: ", errorStatus)
        else:
            # Отправка данных в телеграм-бот
            send_data_to_telegram(str(varBinds))

# Запуск бота
bot.polling()
