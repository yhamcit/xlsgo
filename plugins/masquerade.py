from typing import Iterable

from strtools import str_capture_draw, str_matching


def NonSpaceZeroEithePositive(sources: tuple[Iterable], names: tuple[Iterable], arguments: dict=None) -> Iterable:

    try:
        for l, r in (field for row in sources for field in row):

            try:
                lv = float(l.replace(',', '') if isinstance(l, str) else float(l)) if l else 0
            except ValueError:
                lv = 0
            except:
                raise

            try:
                rv = float(r.replace(',', '') if isinstance(r, str) else float(r)) if r else 0
            except ValueError:
                rv = 0
            except:
                raise

            assert any((lv, rv)) or not all((lv, rv)), f"非空二选一插件传入数据有且仅有一个非空非零值，接受 {l} ： {r}"

            yield (f"{lv:.2f}" if lv else f"{rv:.2f}", )
    except ValueError:
        assert False, f"非空二选一插件只接受两列数据输入，传入数据数量不正确。"



def AbsoluteValue(sources: tuple[Iterable], names: tuple[Iterable], arguments: dict=None) -> Iterable:
    ns = tuple(names)
    n_names = len(ns)
    for field in (tuple(fields) for row in sources for fields in row):
        sum_value = 0
        assert len(field) == n_names, f"绝对值插件应接受 {ns} 字段，与实际收到的值： {field} 数量不匹配"
        for value in field:
            try:
                sum_value = sum_value + float(value) if value else 0
            except ValueError:
                assert False, f"绝对值插件期望传入数字类的数据，实际 {value}。"
            except:
                raise

            yield (f"{sum_value:.2f}" if sum_value > 0 else f"{-sum_value:.2f}", )



def ClearPeerAsPerDes(sources: tuple[Iterable], names: tuple[Iterable], arguments: dict=None) -> Iterable:
    MATCHCOL = "匹配列"
    KEYWORDS = "匹配清理关键词列表"

    assert arguments and MATCHCOL in arguments and KEYWORDS in arguments, f"清除对手插件应传入'{MATCHCOL}'和'{KEYWORDS}' 参数。"

    col_name = arguments[MATCHCOL]
    keywords = arguments[KEYWORDS]
    lst = list(sources)
    if len(lst) == 0:
        yield ('', )
    else:
        for line in lst:
            cols_d = dict(zip(names, line))
            col_word = cols_d.pop(col_name)

            for kword in keywords:
                if str_matching(col_word, kword):
                    break
            else:
                yield tuple(cols_d.values())
                continue

            yield ('', )
