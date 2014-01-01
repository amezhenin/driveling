[![Build Status](https://travis-ci.org/amezhenin/driveling.png?branch=master)](https://travis-ci.org/amezhenin/driveling)
[![Coverage Status](https://coveralls.io/repos/amezhenin/driveling/badge.png)](https://coveralls.io/r/amezhenin/driveling)

driveling
=========
Тестовое задание для ТАРГЕТ.Mail.Ru

Описание
========

Требуется построить марковcкий генератор текстов n-го порядка (http://ru.wikipedia.org/wiki/Цепь_Маркова). 
Логически состоит из двух компонент - обучающей и эксплуатирующей.

**Обучающей части** на вход подается список урлов, ведущих на текстовые
файлы. Она должна скачать их, вызывая внутри curl и получая от него
данные через пайп. Файлы содержат текст на естественном языке.
Пунктуацию откидываем, морфологию учитывать не нужно, стоит лишь
привести текcт к одному регистру, чтобы повысить заполняемость цепи.
Также задается параметр n - порядок цепи. По входному тексту строится
марковская цепь, и сохраняется в файл (можно выдавать в стандартный
вывод).

**Эксплуатирующей части** на вход подаются начальный отрывок из n слов и
число - количество слов, которые надо достроить по начальному отрывку и
построенной обучающей частью марковской цепи, которую надо загрузить из
файла. Если в какой-то момент программа не знает какую-то
последовательность слов (не встречалась при построении марковской цепи),
то на этом можно построение текста завершить. Вывод надо выдавать в
поток стандартного вывода. Вход можно принимать как со стандартного
потока ввода, так и указанием файлов и параметров в командной
строке, но не хардкодить имена в тексте программы.

Разумеется, ни на каких входных данных программа не должна падать,
вместо этого при ошибке писать текст ошибки и корректно завершаться.
Писать код надо принимая во внимание возможный большой объем данных
и высокую скорость выполнения эксплуатирующей (а желательно и обучающей) части.

Реализация
==========
* **trainer.py** - обучающий модуль
* **generator.py** - эксплуатирующий модуль
* **model.py** - классы модели и состояния цепи Маркова

trainer.py
==========
    usage: trainer.py [-h] [-f FILE [FILE ...]] [-u URL [URL ...]] -n N -o O
    
    optional arguments:
      -h, --help            show this help message and exit
      -f FILE [FILE ...], --file FILE [FILE ...]
                            local files to train model
      -u URL [URL ...], --url URL [URL ...]
                            url of remote files to train model
      -n N                  order of markov chain
      -o O                  file to save model
    
    Examples:
        python trainer.py -n 1 -o save.p -f text.txt 
        python trainer.py -n 2 -o save2.p -f text.txt
        python trainer.py -n 2 -o save3.p -u https://raw.github.com/amezhenin/driveling/master/text.txt
        python trainer.py -n 1 -o save4.p -u http://www.gnu.org/licenses/gpl-2.0.txt
        
generator.py
============
    usage: generator.py [-h] -m MODEL -s START [START ...] -k K
    
    optional arguments:
      -h, --help            show this help message and exit
      -m MODEL, --model MODEL
                            file with trained model
      -s START [START ...], --start START [START ...]
                            beginning of text(initial state)
      -k K                  order of markov chain
    
    Examples:
        python generator.py -m save2.p -k 100 -s не мысля
        python generator.py -m save2.p -k 100 -s не мысля гордый
        python generator.py -m save2.p -k 100 -s asdf ff
        python generator.py -m save4.p -k 100 -s gnu
    

Оптимизация
===========
При обучении модели есть несколько неоптимальных операций:

    Line #      Hits         Time  Per Hit   % Time  Line Contents
    ==============================================================
        52                                               def train_model(self, text):
        53                                                   """
        54                                                   Train model by given text. Initial state is taken from beginning of 
        55                                                   text.
        56                                                   """
        57                                                   # remove punctuation
        58         1         1078   1078.0      0.5          text = remove_punct(text)
        59         1         3381   3381.0      1.5          text = text.decode('utf-8').lower()
        60         1         3791   3791.0      1.7          words = text.split()
        61                                           
        62                                                   # not enough words
        63         1            3      3.0      0.0          if len(words) < self._n:
        64                                                       return
        65                                           
        66                                                   # building model
        67         1            2      2.0      0.0          prev = words[:self._n]
        68         1          415    415.0      0.2          words = words[self._n:]
        69     25886        14694      0.6      6.4          for i in words:
        70     25885       164796      6.4     72.2              self._train(tuple(prev), i)
        71     25885        22845      0.9     10.0              prev.pop(0)
        72     25885        17136      0.7      7.5              prev.append(i)
    Line #      Hits         Time  Per Hit   % Time  Line Contents
    ==============================================================
        74                                               def _train(self, current, next):
        75                                                   """
        76                                                   Train model by adding new states in Markov chain
        77                                                   """
        78     25885        18608      0.7     11.4          if current not in self._model:
        79     23490        84242      3.6     51.4              self._model[current] = State(current)
        80     25885        15465      0.6      9.4          st = self._model[current]
        81     25885        45566      1.8     27.8          st.add_next(next)


В строках `prev.pop(0)` и `prev.append(i)` интерпретатору приходится перестраивать индекс. 
Много времени уходит на выделение памяти под новые объекты `State`. 

При генерации текста, самой нагрузной операцией является цикл в `State.get_next`:

    Line #      Hits         Time  Per Hit   % Time  Line Contents
    ==============================================================
        31                                               def get_next(self):
        32                                                   """
        33                                                   Get next random state
        34                                                   """
        35       100          645      6.5      5.1          rnd = randrange(self._total_cnt)
        36      3782         3852      1.0     30.6          for i in self._wrd.items():
        37      3782         4127      1.1     32.8              rnd -= i[1]
        38      3782         3466      0.9     27.5              if rnd < 0:
        39       100          494      4.9      3.9                  return i[0]
        40                                                   raise Exception('Random index out of range')

При большом количествет возможных состояний это может быть критично. Для оптимизации 
этой операции можно использовать (модифицированный) бинарный поиск. Бинарный поиск 
нужно выполнять по кумулятивной сумме хитов(self._wrd.values()), поэтому этап обучения
станет "дороже", но этап генерации станет "дешевле"( O(logN) вместо O(N) в `State.get_next`) 

**UPD.** Method `Model.train_model` was slightly optimised to use `deque` for iterating through words. 
