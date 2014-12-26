class State:

    """
    A state container which allows OOP-style selector access of its
    contents. Essentially works like the fixpoint of defaultdict, i.e.
    defaultdict(defaultdict(defaultdict(...

    """

    # This thing calls super a lot to avoid circular definitions
    def __init__(self):
        # The special member field __dict_repr__ is used to keep track
        # of the information necessary to convert a State object to a
        # dict
        super(State, self).__setattr__('__dict_repr__', {})

    def __getattr__(self, name):
        if name != '__dict_repr__':
            new = State()
            super(State, self).__getattribute__('__dict__')[name] = new
            self.__dict_repr__[name] = new
            return new

    def __setattr__(self, name, value):
        super(State, self).__setattr__(name, value)
        super(State, self).__getattribute__('__dict_repr__')[name] = value


    def __repr__(self):
        return 'from_dict({})'.format(repr(to_dict(self)))



# from_dict and to_dict should satisfy the property
#     to_dict(from_dict(d)) == d


def from_dict(d):

    """
    Create a State object recursively from a dict.

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

    """

    return {
        k: to_dict(v) if isinstance(v, State) else v
        for k, v in state.__dict_repr__.items()
    }


