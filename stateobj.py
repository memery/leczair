class State(dict):

    """
    A state container which allows OOP-style selector access of its
    contents. Essentially works like the fixpoint of defaultdict, i.e.
    defaultdict(defaultdict(defaultdict(...

    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            new = State()
            self[name] = new
            return new

    def __setattr__(self, name, value):
        self[name] = value

    def __repr__(self):
        return 'from_dict({})'.format(repr(to_dict(self)))


def from_dict(d):

    """
    Create a State object recursively from a dict.
    Should satisfy to_dict(from_dict(d)) == d

    """

    state = State()

    for k, v in d.items():
        if isinstance(v, dict):
            v = from_dict(v)
        state.__setattr__(k, v)

    return state


def to_dict(state):

    """
    Recursively create a dict from a State object
    Should satisfy to_dict(from_dict(d)) == d

    """

    return {
        k: to_dict(v) if isinstance(v, State) else v
        for k, v in state.items()
    }


