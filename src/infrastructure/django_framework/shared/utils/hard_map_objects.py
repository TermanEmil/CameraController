def hard_map_objects(src, dest):
    for atr, value in src.__dict__.items():
        if atr in dest.__dict__:
            setattr(dest, atr, value)

    try:
        dest.pk = src.pk
    except:
        # Ignore if it doesn't have pk
        pass