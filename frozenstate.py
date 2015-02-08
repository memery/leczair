from functools import partial, reduce
from collections import namedtuple


def mkfs(fields, *args, **kwargs):
    """
    Factory for creating an FS object. An FS object differs from a namedtuple
    only in that it has a magic __getattr__ which produces empty FS objects if
    they don't exist yet.
    
    """

    class FS(namedtuple('FS', fields)):
        def __getattr__(self, name):
            return empty()

        def __contains__(self, name):
            return name in self._fields

    return FS(*args, **kwargs)


def empty():
    """Returns an empty frozenstate object. Probably not very useful for normal
    applications."""
    return mkfs([])


def single(path, value):
    """
    Creates a frozenstate object out of a single value, such that if

        fs_obj = single('foo.bar.baz', 17)

    then

        fs_obj.foo.bar.baz = 17

    """

    try:
        this, rest = path.split('.', 1)
        deeper = partial(single, rest)
    except ValueError:
        this = path
        deeper = lambda x: x

    return mkfs([this], deeper(value))


def append(fsa, fsb):
    """
    Takes two frozenstate objects and combines them into one. Where their
    values differ, the latter one will be used. For example, if

        a = frozenstate.single('foo.bar', 3)
        b = frozenstate.single('foo.baz', 5)
        c = frozenstate.append(a, b)

    then

        c.foo.bar = 3
        c.foo.baz = 5

    If we continue with

        d = frozenstate.single('foo.baz', 7)
        e = frozenstate.append(c, d)

    then

        e.foo.bar == 3
        e.foo.baz == 7

    From this you might realise that we can fake mutable state by doing

        fs = frozenstate.append(fs, frozenstate.single(path, v))

    which will overwrite the fs object with the result you get if you take the
    fs object and change one of its members to a new value. Doing this might
    not be a good idea.

    My recommendation is to aggregate changes to the state (in, say, a list or
    a generator) and then apply them all atomically. This will make your state
    easier to reason about since at any point in your program it will be either
    in state A or state B, never will it be halfway between the two states.
    Aggregating changes before applying them might also be useful for logging
    and transactional purposes – you can keep a record of all changes applied
    to the state, and roll them back if you need to.

    """

    keys = set(fsa._fields) | set(fsb._fields)

    d = {}
    for k in keys:
        # If the key isn't in one of them...
        if k not in fsa._fields:
            d[k] = getattr(fsb, k)
            continue

        # ...it's guaranteed to be in the other
        if k not in fsb._fields:
            d[k] = getattr(fsa, k)
            continue

        # At this point both are guaranteed to have the key
        va, vb = getattr(fsa, k), getattr(fsb, k)

        # If the keys exist in both FSs, we try to join their values together
        try:
            d[k] = append(va, vb)
        except AttributeError:
            # ...but if we can't do that, we just overwrite the old value
            d[k] = vb

    return mkfs(keys, **d)


def concat(fss):
    """Convenience function to join a bunch of states simultaneously instead of
    two at a time."""
    return reduce(append, fss, empty())


def to_dict(fs):
    d = {}
    for k in fs._fields:
        v = getattr(fs, k)
        try:
            d[k] = to_dict(v)
        except AttributeError:
            d[k] = v
    return d


def from_dict(d, path=()):
    def get_changeset(d):
        for k, v in d.items():
            try:
                r = from_dict(v, path=path)
            except AttributeError:
                r = v

            yield single('.'.join(path+(k,)), r)

    return concat(get_changeset(d))
