from random import randrange
import string

def remove_punct(text):
    return text.translate(string.maketrans("", ""), string.punctuation)


class State(object):
    def __init__(self, state):
        self._state = state
        self._wrd = {}
        self._total_cnt = 0
        super(State, self).__init__()

    def add_next(self, next):
        self._total_cnt += 1
        if next not in self._wrd:
            self._wrd[next] = 1
        else:
            self._wrd[next] += 1

    def get_next(self):
        rnd = randrange(self._total_cnt)
        for i in self._wrd.items():
            rnd -= i[1]
            if rnd < 0:
                return i[0]
        raise Exception('Random index out of range')


class Model(object):
    def __init__(self, n):
        self._n = n
        self._model = {}
        super(Model, self).__init__()

    def train_model(self, text):
        # remove punctuation
        text = remove_punct(text)
        text = text.decode('utf-8').lower()
        words = text.split()

        # building model
        if len(words) < self._n:
            return

        prev = words[:self._n]
        words = words[self._n:]
        for i in words:
            self._train(tuple(prev), i)
            prev.pop(0)
            prev.append(i)

    def _train(self, current, next):
        """
        Train model by adding new states in Markov chain
        """
        if current not in self._model:
            self._model[current] = State(current)
        st = self._model[current]
        st.add_next(next)
    
    def get_next(self, current):
        tpl = tuple(current)
        if tpl not in self._model:
            return None
        st = self._model[tpl]
        next = st.get_next()
        current.pop(0)
        current.append(next)
        return current, next
