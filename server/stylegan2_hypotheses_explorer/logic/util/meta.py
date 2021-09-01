def subclasses(cls):
    return set(cls.__subclasses__()).union([s
                                            for c in cls.__subclasses__()
                                            for s in subclasses(c)])


def subclasses_dict(cls):
    return {cls.__name__: cls for cls in subclasses(cls)}
