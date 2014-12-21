
class State:

    """
    A state container which allows OOP-style selector access of its
    contents. Essentially works like the fixpoint of defaultdict, i.e.
    defaultdict(defaultdict(defaultdict(...

    """

    def __getattr__(self, name):
        new = State()
        # Avoid a circular definition by tapping into the superclass
        super(State, self).__getattribute__('__dict__')[name] = new
        return new



