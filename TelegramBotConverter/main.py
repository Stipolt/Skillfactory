import json
import telebot
import requests

from config import token_
from utils import ConvertionException, APIException

bot = telebot.TeleBot(token_)


class StartInfo:
    @staticmethod
    @bot.message_handler(commands=["start", "help"])
    def start_func(message: telebot.types.Message):
        hi_ = f'Hi {message.chat.username}' \
              f"\nIt's a simple currency converter" \
              f"\nTo use, enter:" \
              f"\n<name from the list of currencies> " \
              f"<the currency to which you want to transfer>, " \
              f"<the amount of currency> " \
              f"\n" \
              f"\nexample: USD EUR 1" \
              f"\n" \
              f"\nprint /value to see 3 of all list currency"\

        bot.send_message(message.chat.id, hi_)


class Value:
    @staticmethod
    @bot.message_handler(commands=["value"])
    def info_(message: telebot.types.Message):
        value_list = f"\nUSD : Доллар" \
                     f"\nEUR : Евро" \
                     f"\nRUB : Рубль" \
                     f"\nДа и в принципе какую угодно)"
        bot.send_message(message.chat.id, value_list)


class Converter:
    @staticmethod
    @bot.message_handler(content_types=["text"])
    def get_price(message: telebot.types.Message):
        try:
            elem_quant = message.text.split()

            if len(elem_quant) !=3:
                raise ConvertionException(f"Incorrect number of variables"
                                          f"\n check Example")

            base, quote, amount = elem_quant
            if quote == base:
                raise ConvertionException("Same currencies")

            if len(quote) or len(base) != 3:
                raise APIException("NOT 3 LETTER in currency!")

        except ConvertionException as e:
            bot.reply_to(message, f"Oops, you take a mistake\n{e}")
        except APIException as e:
            bot.reply_to(message, f'Oops, you take a mistake\n{e}')
        except Exception as e:
            bot.reply_to(message, f"Try again\n{e}")

        else:
            r = requests.get(f"https://api.exchangerate.host/convert?from={base}&to={quote}&amount={amount}")
            ans = json.loads(r.content)["result"]
            bot.reply_to(message, ans)

bot.polling(none_stop=True)

