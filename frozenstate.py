
import copy
import functools


class State:
    def __init__(self, *states):
        self.__path__ = ''
        self.__store__ = {}

        # TODO: Check somewhere here that we are retaning the biggest possible
        # path intact (and creating the minimal possible state object)
        ds = [type(state).to_dict(state) for state in states]
        if ds:
            combined = functools.reduce(lambda d, u: dict(d, **u), ds, {})
            new = type(self).from_dict(combined)
            self.__store__ = new.__store__

    @classmethod
    def get(cls, state, path):
        *sections, name = path.split('.')
        try:
            target = state
            for node in sections:
                target = target.__store__[node]
            return target.__store__[name]
        except KeyError:
            new = cls()
            new.__path__ = state.__path__ + '.' + path
            return new

    @classmethod
    def set(cls, state, path, value):
        *sections, name = path.split('.')

        new = copy.copy(state)
        target = new
        for node in sections:
            print(node)
            try:
                target.__store__[node] = copy.copy(target.__store__[node])
            except KeyError:
                target.__store__[node] = cls()
            target = target.__store__[node]
        target.__store__[name] = value

        return new

    @classmethod
    def to_dict(cls, state, include_path=True):
        d = { k: cls.to_dict(v, include_path=False)
              if isinstance(v, cls) else v
              for k, v in state }

        if include_path:
            for node in reversed(state.__path__.split('.')):
                d = {node: d}

        return d

    @classmethod
    def from_dict(cls, d, path=''):
        state = cls()
        state.__path__ = path
        for k, v in d.items():
            if isinstance(v, cls):
                v = cls.from_dict(v.__store__, path=path+'.'+k)
            if isinstance(v, dict):
                v = cls.from_dict(v, path=path+'.'+k)
            state.__store__[k] = v

        return state

    def __copy__(self):
        new = type(self)()
        new.__path__ = self.__path__
        new.__store__ = dict(self.__store__) 
        return new

    def __iter__(self):
        return zip(self.__store__.keys(), self.__store__.values())

    def __contains__(self, key):
        return key in self.__store__.keys()

    def __repr__(self):
        return '{}.from_dict({}{})'.format(
            type(self).__name__,
            type(self).to_dict(self, include_path=False),
            ', path=' + repr(self.__path__) if self.__path__ else ''
        )

