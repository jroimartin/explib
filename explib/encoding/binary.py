"""Helpers for binary encoding."""

import struct


__all__ = [
    'pack',
    'unpack',
    'p16',
    'u16',
    'p32',
    'u32',
    'p64',
    'u64'
]


def _genfmt(size, endian, sign):
    """
    Generates a format string that can be used with struct.pack()
    and struct.unpack().
    """
    if sign not in [True, False]:
        raise ValueError('sign must be either True or False')

    if endian == 'little':
        fmt = '<'
    elif endian == 'big':
        fmt = '>'
    else:
        raise ValueError('endianness must be either "little" or "big"')

    if size == 16:
        fmt += 'h' if sign else 'H'
    elif size == 32:
        fmt += 'i' if sign else 'I'
    elif size == 64:
        fmt += 'q' if sign else 'Q'
    else:
        raise ValueError('supported sizes are 16, 32 and 64')

    return fmt


def pack(value, size=64, endian='little', sign=False):
    """Packs arbitrary size integer."""
    fmt = _genfmt(size, endian, sign)
    return struct.pack(fmt, value)


def unpack(buf, size=64, endian='little', sign=False):
    """Unpacks arbitrary size integer."""
    fmt = _genfmt(size, endian, sign)
    return struct.unpack(fmt, buf)[0]


def p16(value, endian='little', sign=False):
    """Packs 16-bit integer."""
    return pack(value, size=16, endian=endian, sign=sign)


def u16(buf, endian='little', sign=False):
    """Unpacks 16-bit integer."""
    return unpack(buf, size=16, endian=endian, sign=sign)


def p32(value, endian='little', sign=False):
    """Packs 32-bit integer."""
    return pack(value, size=32, endian=endian, sign=sign)


def u32(buf, endian='little', sign=False):
    """Unpacks 32-bit integer."""
    return unpack(buf, size=32, endian=endian, sign=sign)


def p64(value, endian='little', sign=False):
    """Packs 64-bit integer."""
    return pack(value, size=64, endian=endian, sign=sign)


def u64(buf, endian='little', sign=False):
    """Unpacks 64-bit integer."""
    return unpack(buf, size=64, endian=endian, sign=sign)
