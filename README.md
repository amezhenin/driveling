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
* **generator.py** - эксплуатирующей модуль
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