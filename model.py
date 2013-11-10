from random import randrange

class State(object):
    def __init__(self, state):
        self._state = state
        self._wrd = {}
        self._total_cnt = 0
        super(State, self).__init__()
#     def __str__(self):
#        return str(self._state)
#     def __hash__(self):
#         return hash(state)

    def add_next(self, next):
        self._total_cnt += 1
        if next not in self._wrd:
            self._wrd[next] = 1
        else:
            self._wrd[next] += 1
    def get_next(self):
        rnd = randrange(self._total_cnt)
        for i in self._wrd.items():
            if rnd <= 0:
                return i[0]
            rnd -= i[1]


class Model(object):
    _model = {}

    def train(self, current, next):
        """
        Train model by adding new states in Markov chain
        """
        if current not in self._model:
            self._model[current] = State(current)

        st = self._model[current]
        st.add_next(next)
    
    def get_next(self, current):
        if current not in self._model:
            return None
        st = self._model[current]
        return st.get_next()
