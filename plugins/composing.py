from random import sample
from time import mktime
from typing import Iterable

from strtools import strf_time_ts, str_capture_draw


def PermutePeersAsCreditDebit(sources: tuple[Iterable], arguments: dict=None) -> Iterable:
    PRKEY = "收支字段"
    PRACT = "标识行为"
    PRSQU = "交换序列"

    assert arguments and PRKEY in arguments and PRACT in arguments and PRSQU in arguments, \
        f"重新排列收支双方插件，要求必须指定: {PRKEY}, {PRACT}, {PRSQU} 参数。"

    key, act = arguments[PRKEY], arguments[PRACT]
    assert key and act, f"{PRKEY}: {key}; {PRACT}: {act} 应为非空值。"

    prsqu = arguments[PRSQU]
    assert isinstance(prsqu, list) and \
           all(isinstance(p,list) for p in prsqu) and \
           all(len(p) == 2 for p in prsqu), \
        f"{PRSQU} 的合法参数为(N x 2)的二维数组，当前：{prsqu}。"

    for record in (dict(r) for r in sources):
        try:
            if act[''.join(record.pop(key))]:
                for r, p in prsqu:
                    record[r], record[p] = record[p], record[r]
        except KeyError:
            assert False, f"数据记录 {str(record)} 中不存在 {PRKEY}: {key} 的对应值或该值不正确。"

        yield list(record.values())



def ClearPeerAsPerDes(sources: tuple[Iterable], arguments: dict=None) -> Iterable:
    MATCHCOL = "匹配列"
    KEYWORDS = "匹配清理关键词列表"
    DATASOURCE = "数据源"

    assert arguments and MATCHCOL in arguments and KEYWORDS in arguments, f"清除对手插件应传入'{MATCHCOL}'和'{KEYWORDS}' 参数。"

    fields = arguments[DATASOURCE]
    m_col = arguments[MATCHCOL]
    keywords = arguments[KEYWORDS]
    lst = list(sources)
    if len(lst) == 0:
        yield tuple(), tuple(), tuple()
    else:
        for l in lst:
            cols_d = dict(zip(fields, l))
            col_k = cols_d[m_col]

            for k in keywords:
                if str_capture_draw((col_k, ), k):
                    yield tuple(), tuple(), col_k
                else:
                    yield tuple(cols_d.values())


def TimestampNonceFromDate(sources: tuple[Iterable], arguments: dict=None) -> Iterable:
    PRECISION = "时间戳精度"
    NONCEDIGITS = "随机数位数"

    assert arguments and PRECISION in arguments and NONCEDIGITS in arguments, "时间戳和随机数需要指定精度及随机数长度。"

    prec, ndigtc = arguments[PRECISION], arguments[NONCEDIGITS]
    assert prec and ndigtc, f"{PRECISION}: {prec}; {NONCEDIGITS}: {ndigtc} 应为非空非零的有效值。"

    lst = list(sources)
    if len(lst) == 0:
        yield tuple(), tuple()
    else:
        for k, v in (p for l in lst for p in l):
            nonce = sample(tuple('0123456789'), ndigtc)
            ts = strf_time_ts(v)
            yield (f"{int(mktime(ts) * prec)}{''.join(nonce)}",), v

