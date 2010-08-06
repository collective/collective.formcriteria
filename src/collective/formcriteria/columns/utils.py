SIZE_SUFFIXES = [('GB', 1024 * 1024 * 1024), ('MB', 1024 * 1024), ('kB', 1024)]


def format_number(number, format='%.1f %s', suffixes=SIZE_SUFFIXES):
    """Format a number acording to suffixes defaulting to byte sizes"""
    smaller, min_ = suffixes[-1]

    # if the number is a float, then make it an int
    # happens for large files
    try:
        number = int(number)
    except (ValueError, TypeError):
        pass

    if not number:
        return '0 %s' % smaller

    if isinstance(number, (int, long)):
        if number < min_:
            return '1 %s' % smaller
        for c, factor in suffixes:
            if number / factor > 0:
                break
        return format % (float(number / float(factor)), c)
    return number
