"""
Text filters and replacements.

Replaces or otherwise filters strings of text. All commands can be used without
a parameter, where they will use the last line spoken in the channel.
"""

import functools
import random
import re
import unicodedata

from kochira.service import Service

service = Service(__name__, __doc__)


def benisify(s):
    return functools.reduce(lambda acc, f: f(acc), [
        lambda s: s.lower(),
        lambda s: unicodedata.normalize('NFKD', s),
        lambda s: s.replace('x', 'cks'),
        lambda s: re.sub(r'ing','in', s),
        lambda s: re.sub(r'you', 'u', s),
        lambda s: re.sub(r'oo', 'u', s),
        lambda s: re.sub(r'ck\b', 'g', s),
        lambda s: re.sub(r'ck', 'gg', s),
        lambda s: re.sub(r'\bthe\b', 'da', s),
        lambda s: re.sub(r'(t+)', lambda x: 'd' * len(x.group(1)), s),
        lambda s: s.replace('p', 'b'),
        lambda s: re.sub(r'\bc', 'g', s),
        lambda s: re.sub(r'\bis\b', 'are', s),
        lambda s: re.sub(r'c+(?![eiy])', 'g', s),
        lambda s: re.sub(r'know', 'no', s),
        lambda s: re.sub(r'kn', 'n', s),
        lambda s: re.sub(r'[qk]', 'g', s),
        lambda s: re.sub(r'([?!.]|$)+', lambda x: (x.group(0) * random.randint(2, 5)) + " " + "".join((":" * random.randint(1, 2)) + ("D" * random.randint(1, 4)) for _ in range(random.randint(2, 5))), s),
    ], s)



FABULOUS_COLORS = [4, 5, 8, 9, 10, 12, 13, 6]

def fabulousify(s):
    buf = ""

    for i, x in enumerate(s):
        if x == " ":
            buf += x
        else:
            buf += "\x03{:02}{}".format(FABULOUS_COLORS[i % len(FABULOUS_COLORS)], x)

    return buf


ASCII_TO_WIDE = {i: chr(i + 0xfee0) for i in range(0x21, 0x7f)}
ASCII_TO_WIDE.update({0x20: "\u3000", 0x2D: "\u2212"})

def wide(s):
    return s.translate(ASCII_TO_WIDE)


def run_filter(f, ctx, text=None):
    if text is None:
        if not ctx.client.backlogs.get(ctx.target, []):
            return

        if len(ctx.client.backlogs[ctx.target]) < 2:
            return

        _, text = ctx.client.backlogs[ctx.target][1]

    text = f(text)

    ctx.respond(text)


def bind_filter(name, f, doc):
    @service.command(r"!{}(?: (?P<text>.+))?$".format(name))
    @service.command(r"{}(?: (?P<text>.+))?$".format(name), mention=True)
    def benis(ctx, text=None):
        run_filter(f, ctx, text)
    benis.__doc__ = doc


bind_filter("benis", benisify,
"""
Benis.

You're going to have to figure this one out for yourself.
""")

bind_filter("fabulous", fabulousify,
"""
Fabulous.

Rainbow text!
""")

bind_filter("wide", wide,
"""
Widen.

Convert text to fullwidth.
""")
