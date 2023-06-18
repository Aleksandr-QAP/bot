#!/usr/bin/env python

import telebot
from config import keys, TOKEN
from utils import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате: \n<название валюты> ' \
           '<название валюты перевода> <количество переводимой валюты>\n Названия валют вводить ' \
           'с большой буквы, с использованием запятых и пробелов\nУвидеть список всех доступных ' \
           'валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for value in keys.values():
        text = '\n'.join((text, value[1]))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        if ', ' in message.text:
            values = message.text.split(', ')
        elif ',' in message.text:
            values = message.text.split(',')
        else:
            values = message.text.split(' ')
        if 3 < len(values) > 4:
            raise ConvertionException('Слишком много параметров.')
        if 'в' in values:
            values.remove('в')
        amount = []
        i = 0
        while i < len(values):
            try:
                amount.append(float(values[i]))
            except ValueError:
                pass
            i += 1
        if amount[0] <= 0:
            raise ConvertionException('Введено отрицательное число или ноль.')
        try:
            values.remove(str(int(amount[0])))
        except ValueError:
            values.remove(str(amount[0]))
        quote, base = values
        amount = str(amount[0])
        if quote[0].isupper():
            quote = quote[0].lower()
        else:
            quote = quote[0]
        if base[0].isupper():
            base = base[0].lower()
        else:
            base = base[0]
        total_base = CryptoConverter.convert(quote, base, amount)

        for k, v in keys.items():
            if v[0] == quote:
                quote = k
        for k, v in keys.items():
            if v[0] == base:
                base = k

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:

        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
