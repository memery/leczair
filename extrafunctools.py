
identity = lambda x: x
succ = lambda x: x+1
pred = lambda x: x-1

def modattr(obj, name, fn):
    setattr(obj, name, fn(getattr(obj, name)))

