def hard_map_objects(obj1, obj2):
    for atr, value in obj1.__dict__.items():
        if atr in obj2.__dict__:
            setattr(obj2, atr, value)

    try:
        obj2.pk = obj1.pk
    except:
        pass