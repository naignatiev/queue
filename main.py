import random
import telebot
from telebot import types
bot = telebot.TeleBot('2112586716:AAHI-SASvl5Bf18rwsQNJOWtfE0TrGuGJM4')

from data import names, adj


users_data = {}


class UserData:
    def __init__(self):
        self.a = [(random.choice(adj), random.choice(names)) for i in range(5)]

    def __getitem__(self, item):
        return self.a[item][0] + ' ' + self.a[item][1]

    def refresh(self, x):
        self.a[x] = (random.choice(adj), random.choice(names))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.from_user not in users_data:
        users_data[message.chat.id] = UserData()
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    print(message.chat.id)
    print('\n' * 2)
    for i in range(5):
        print(users_data[message.chat.id][i])
        button = types.InlineKeyboardButton(text=users_data[message.chat.id][i], callback_data=str(i))
        keyboard.add(button)
    bot.send_message(message.from_user.id, text='s', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    for i in range(5):
        if call.data == str(i):
            users_data[call.message.chat.id].refresh(i)
    bot.send_message(call.message.chat.id, text='Принято!')


bot.polling(none_stop=True, interval=0)
