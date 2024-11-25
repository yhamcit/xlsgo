from typing import Iterable



def NonSpaceZeroEithePositive(sources: tuple[Iterable], arguments: dict=None) -> Iterable:

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



def AbsoluteValue(sources: tuple[Iterable], arguments: dict=None) -> Iterable:
    for field in (field for row in sources for field in row):
        sum_value = 0
        for value in field:
            try:
                sum_value = sum_value + float(value) if value else 0
            except ValueError:
                assert False, f"绝对值插件期望传入数字类的数据，实际 {value}。"
            except:
                raise

            yield (f"{sum_value:.2f}" if sum_value > 0 else f"{-sum_value:.2f}", )


