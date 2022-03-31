import telebot
import requests
import json
from CurrencyBotExtensions import ConversionException, CurrencyConverter
from CurrencyConfig import keys

TOKEN = '5214431120:AAH-RNOmCkMm_XwH7xqoZdsX9uigx7N7iTU'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'To convert the currency, please enter command in the following order: \n<currency you want to convert> \
<currency you want to get> \
<amount>\n Available currencies please click or enter /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Available currencies:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConversionException('Wrong input order. The number of parameters should be 3 /help')

        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'User mistake \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Could not process the command \n{e}')

    else:
        text = f'Price of {amount} {quote} in {base} is equal to {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()