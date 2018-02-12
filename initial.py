#инициализация
#запуст после продакшена череват отрывом дето и кодородных органов
import pickle
a = []
b = [['DOGE',[[0.00000050,1]],0.0000004]]
with open('subs.pickle', 'wb') as f:
    pickle.dump(a,f)
f.close()
with open('signals.pickle', 'wb') as f:
    pickle.dump(b, f)
f.close()