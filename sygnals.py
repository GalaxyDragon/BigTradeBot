
from cryptocompare import *
import pickle
import telebot
import config
import time

sygnals = []
with open('signals.pickle', 'rb') as f:
    sygnals = pickle.load(f)
f.close()



def zeros(str):
    while str[-1]=="0":
        str = str[:-1]
    return str




def sig():
    try:
        was = False
        delete = []
        with open('signals.pickle', 'rb') as f:
            sygnals = pickle.load(f)
        f.close()
        res = []
        for i in sygnals:
            try:
                time.sleep(config.sleep_between_ask)
                x = get_price(i[0], curr='BTC')
                print(i[0], x)
                if (float(x[i[0]]['BTC']) >= i[1][0][0]):
                    was = True
                    res.append('''#{} \n\nPrise touch {} \n{} target done! \n{} % profit
                        '''.format(i[0],
                                   zeros(str('{:.10f}'.format(i[1][0][0]))),
                                   i[1][0][1] + 1, int((i[1][0][0] - i[2]) / i[2] * 100)))
                    i[1].pop(0)
                    if len(i[1]) == 0:
                        xx = sygnals.index(i)
                        delete.append(xx)
            except:
                pass
        for i in range(len(delete)):
            sygnals.pop(delete[len(delete) - 1 - i])
        if was:
            with open('signals.pickle', 'wb') as f:
                pickle.dump(sygnals, f)
            f.close()
        return res
    except:
        return []

while True:
    a = sig()
    print(a)
    subscribers = []
    bot = None
    if len(a)!=0:
        with open('subs.pickle', 'rb') as f:
            subscribers = pickle.load(f)
        f.close()
        bot = telebot.TeleBot(config.token)
    for i in a:
        for j in subscribers:
            try:
                bot.send_message(j, i)
            except:
                pass