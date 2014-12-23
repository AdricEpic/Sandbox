from itertools import izip_longest


def chunker(iterable, n, pad_value=None):
    """Group iterable into tuples of n length. If not enough values present,
    pad_value is appended to fill."""
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=pad_value)


def txt2rgb(text):
    """Convert ASCII to RGB tuples"""
    rgb = [ord(i) for i in text]
    return list(chunker(rgb, 3, 0))


def rgb2txt(rgb):
    """Convert RGB to ASCII. Strips trailing nulls."""
    return "".join([chr(value) for pixel in rgb for value in pixel]).rstrip(chr(0))


if __name__ == '__main__':
    # Simple test for all values that fit in 8-bit range
    all_chars = "".join([chr(i) for i in xrange(0 , 256)])
    trailing_nulls = all_chars + chr(0)

    # General test case should pass
    assert (all_chars == rgb2txt(txt2rgb(all_chars)))
    # Trailing nulls should fail
    assert(not (trailing_nulls == rgb2txt(txt2rgb(trailing_nulls))))