import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot("6085176296:AAF9xUSRIxsKkIUNLJxSXg6WIFZj031UC4Y")
currency = CurrencyConverter()

amount = 0


@bot.message_handler(commands=['start'])
def main(mess):
    bot.send_message(mess.chat.id, "Enter amount of currency")
    bot.register_next_step_handler(mess, num)


def num(mess):
    global amount
    try:
        amount = int(mess.text.strip())
    except ValueError:
        bot.send_message(mess.chat.id, "Wrong format! Enter amount of currency")
        bot.register_next_step_handler(mess, num)
        return
    if amount >= 0:
        markup = types.InlineKeyboardMarkup(row_width=3)
        btn1 = types.InlineKeyboardButton("USD/EUR", callback_data="USD/EUR")
        btn2 = types.InlineKeyboardButton("USD/GBP", callback_data="USD/GBP")
        btn3 = types.InlineKeyboardButton("EUR/USD", callback_data="EUR/USD")
        btn4 = types.InlineKeyboardButton("EUR/GBP", callback_data="EUR/GBP")
        btn5 = types.InlineKeyboardButton("GBP/USD", callback_data="GBP/USD")
        btn6 = types.InlineKeyboardButton("GBP/EUR", callback_data="GBP/EUR")
        btn7 = types.InlineKeyboardButton("Enter another pair", callback_data="Else")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
        bot.reply_to(mess, "Choose pair of currencies", reply_markup=markup)
    else:
        bot.send_message(mess.chat.id, "Amount can`t be less then 0! Enter amount of currency")
        bot.register_next_step_handler(mess, num)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != "Else":
        values = call.data.split("/")
        result = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f"{amount} {values[0]} = {round(result, 2)} {values[1]}\n"
                                               f"/start - enter new amount of currency")
    else:
        bot.send_message(call.message.chat.id,
                         "Enter your currency pair in format:\n"
                         "(first currency code)/(second currency code).\n"
                         "Example: 'usd/jpy'")
        bot.register_next_step_handler(call.message, else_pair)


def else_pair(mess):
    try:
        values = mess.text.upper().split('/')
        result = currency.convert(amount, values[0], values[1])
        bot.send_message(mess.chat.id, f"{amount} {values[0]} = {round(result, 2)} {values[1]}\n"
                                       f"/start - enter new amount of currency")
    except Exception:
        bot.send_message(mess.chat.id, "Something went wrong. Enter amount of currency again")
        bot.register_next_step_handler(mess, num)


bot.infinity_polling()
