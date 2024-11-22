from re import match
from time import strptime
from typing import Iterable


def strf_time_ts(*ts: tuple|list, format: str= r"%Y-%m-%d %H:%M:%S") -> float:

    assert any(ts), f"联合时间表示期望日期：时间均有有效值，实际: {str(ts)}"
    fds = ' '.join(part for sub in ts for part in sub)
    if not fds:
        raise ValueError()

    try:
        return strptime(fds, format)
    except ValueError:
        raise


def str_capture_draw(ts: tuple | list, rgexp: str=None):
    if not any(t for t in ts):
        raise ValueError()

    return tuple(' '.join(g for g in match(rgexp, str(t)).groups()) for t in ts)


def str_union(ts: tuple|list, cs: tuple|list, concat_mod: str=None, format_mod: str=None) -> Iterable:
    def non_blanks_str(ts: tuple|list):
        for t in ts:
            if t:
                yield t

    if format_mod:
        return (format_mod.format(**dict(zip(cs, ts))),)
    elif concat_mod:
        return (concat_mod.join(non_blanks_str(ts)),)
    else:
        return (''.join(ts),)

