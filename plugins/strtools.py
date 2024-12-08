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


def str_matching(ts: tuple | list, rgexp: str=None):
    for t in ts:
        if t:
            m = match(rgexp, str(t))
            if m:
                break
        else:
            continue
    else:
        return False

    return True

def str_capture_draw(ts: tuple | list, rgexp: str=None):
    result = list()
    for t in ts:
        if t:
            m = match(rgexp, str(t))
            if m:
                rt = ''.join(gt if gt else '' for gt in m.groups())
            else:
                rt = ''
        else:
            rt = ''
        result.append(rt)

    if not any(t for t in ts):
        raise ValueError()

    return tuple(result)


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

