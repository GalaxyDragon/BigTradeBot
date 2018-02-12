#part reciving message
import random
import pickle
import telebot
import config
from cryptocompare import *
subscribers = []
signals = []
with open('subs.pickle', 'rb') as f:
    subscribers = pickle.load(f)
f.close()
def zeros(str):
    while str[-1]=="0":
        str = str[:-1]
    return str

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def new_member(message):
        if ( subscribers.count(message.chat.id)==0):
         subscribers.append(message.chat.id)
        with open('subs.pickle', 'wb') as f:
            pickle.dump(subscribers, f)
        f.close()
        bot.send_message(message.chat.id, """Thank you for signing up for us! With this bot you will be able to instantly learn about the execution of signals from the channel @BigCryptotrade.
To find out the exchange rate of the currency you are interested in send /price %coin name% (/price ETH)\n
To unsubscribe from us enter /go_away\n
Expect more interesting things soon :)\nСпасибо, что подписались на нас! С помощью этого бота вы сможете моментально узнавать о выполнении сигналов из канала @BigCryptotrade.
\nЧтобы узнать курс интересующей вас валюты отправьте /price %название монеты% (/price ETH)
\nЧтобы отписаться от нас введите /go_away\n
Ожидайте больше интересностей скоро :)""")

@bot.message_handler(commands=['go_away'])
def new_member(message):
    if ( subscribers.count(message.chat.id)!=0):
        subscribers.remove(message.chat.id)
        with open('subs.pickle', 'wb') as f:
            pickle.dump(subscribers, f)
        f.close()

@bot.message_handler(commands=['price'])
def new_member(message):
    name = message.text[7:]
    name = name.upper()
    y = get_price(name, curr='USD')
    if y == None:
        bot.send_message(message.chat.id, "Sorry, no this coin. Please, check name\n Нет монеты с таким именем. Пожалуйста, проверьте правильность написания")
        return
    answer = name+":\n"
    if name != "BTC":
        x = get_price(name, curr='BTC')
        answer+=zeros(str('{:.10f}'.format(x[name]['BTC'])))
        answer+=" BTC\n"

    answer += zeros(str('{:.10f}'.format(y[name]["USD"])))
    answer += "$ USD\n"
    bot.send_message(message.chat.id,answer)
@bot.message_handler(commands=['add'])
def add_sygnal(message):
    try:
        if (message.chat.id in config.admins):
            a = []
            with open('signals.pickle', 'rb') as f:
                a = pickle.load(f)
            f.close()
            new_sig = message.text.split(':')
            new_sig[0] = new_sig[0][5:]
            aa = new_sig[1]
            new_sig[1] = new_sig[2]
            new_sig[2] = aa
            print(new_sig)
            new_sig[2] = float(new_sig[2])
            new_sig[1] = new_sig[1].split('-')
            for i in range(len(new_sig[1])):
                print(new_sig[1][i])
                new_sig[1][i] = [float(new_sig[1][i]), i]
            print('sygnal_added')
            print(new_sig)
            a.append(new_sig)
            with open('signals.pickle', 'wb') as f:
                pickle.dump(a, f)
            f.close()
            bot.send_message(message.chat.id, str(new_sig))
    except:
        print("да пошли вы нахуй!")
        pass

@bot.message_handler(commands=['list'])
def list(message):
    if (message.chat.id in config.admins):
        a = []
        res = 'Signals'
        with open('signals.pickle', 'rb') as f:
            a = pickle.load(f)
        f.close()
        cnt = 0
        for r in a:
            res = res +'\n'+str(cnt)+":" + str(r)
            cnt+=1
        res += '\n' + str(len(subscribers)) + " subs"
        bot.send_message(message.chat.id,res)
@bot.message_handler(commands=['delete'])
def list(message):
    try:
        if (message.chat.id in config.admins):
            a = []
            with open('signals.pickle', 'rb') as f:
                a = pickle.load(f)
            f.close()
            num = message.text[8:]
            num = int(num)
            a.pop(num)
            with open('signals.pickle','wb') as f:
                pickle.dump(a,f)
            f.close()
    except:
        print("Админ дэбэл")
        pass
@bot.message_handler(commands=['rand'])
def list(message):
    try:
        if (message.chat.id in config.admins) and message.text != "/rand" and message.tet != "/rand ":
            txt = message.text[6:]
            rand = random.randint(0, len(subscribers))
            try:
                bot.send_message(subscribers[rand], txt)
            except:
                bot.send_message(message.chat.id, "Oops... try again")
    except:
        pass

@bot.message_handler(commands=['all'])
def list(message):
    try:
        if (message.chat.id in config.admins) and message.text != "/rand" and message.tet != "/rand ":
            txt = message.text[6:]
            for i in subscribers:
                try:
                    bot.send_message(i, txt)
                except:
                    pass
    except:
        pass

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            pass