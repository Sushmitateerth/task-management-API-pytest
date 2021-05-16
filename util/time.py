import dateutil.parser as dp


def num_seconds(days=1):
    """
    converts days to seconds
    """
    return 86400 * days


def to_epoch(iso):
    """
    converts ISO date string to epoch in seconds
    :param iso: date in ISO8601 format
    """
    parsed = dp.parse(iso)
    secs = parsed.strftime('%s')

    return int(secs)
