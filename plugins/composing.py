from random import sample
from time import mktime
from typing import Iterable

from hashlib import shake_256
from strtools import strf_time_ts


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




def TimestampNonceFromDate(sources: tuple[Iterable], arguments: dict=None) -> Iterable:
    DIGESTLENG = "摘要长度"
    DIGESTFROM = "摘要字段"
    # PRECISION  = "时间戳精度"
    # NONCEDIGITS = "随机数位数"  :== 7  0

    assert arguments and DIGESTLENG in arguments and DIGESTFROM in arguments, "时间戳和随机数需要指定精度及随机数长度。"

    diglen, digsrc = arguments[DIGESTLENG], arguments[DIGESTFROM]
    assert diglen and len(digsrc) == 2, f"{DIGESTLENG}: {diglen}; {DIGESTFROM}: {digsrc} 应为非空非零的有效值。"

    src_lst = list(sources)
    if len(src_lst) == 0:
        yield tuple(), tuple()
    else:
        for record in src_lst:
            fields = tuple(pair[-1] for pair in record)
            ts = strf_time_ts(fields[0])

            mono_str = str(fields[slice(*digsrc)])
            diger = shake_256()
            diger.update(mono_str.encode(encoding='utf-8'))
            digest = diger.hexdigest(diglen//2)

            yield (f"{int(mktime(ts))}{digest}",), *fields

