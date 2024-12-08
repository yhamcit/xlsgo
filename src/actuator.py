from collections.abc import Iterable
from functools import reduce
from operator import add

from loader import attributes
from plugin import load_plugin
from src import DATASOURCE, PLUGIN, ARGUMENT


def each_bundle(binding: dict[str, Iterable], sources: list[str]|tuple[str]):
    yield from (v for s in sources for v in binding[s])

def run_policy(policy: dict[str, dict], binding: dict[str, Iterable], policy_name: str, acc_name: str) -> dict[str, Iterable]:
    data = dict()

    binding = dict(zip(binding.keys(), (tuple(v) for v in binding.values())))
    for (key, attr) in attributes(policy):
        try:
            assert attr and attr[DATASOURCE], f"账户-{acc_name} 策略-{policy_name} 未指定 '{key}' 属性或 '{DATASOURCE}'。"
            data_src = attr[DATASOURCE]

            data[key] = (reduce(add, line) for line in zip(*(binding[s] for s in data_src)))
            if PLUGIN not in attr or not attr[PLUGIN]:
                continue

            plugin_name = attr[PLUGIN]
            fn = load_plugin(plugin_name)

            arguments = None
            if ARGUMENT in attr:
                arguments = attr[ARGUMENT]
                assert arguments, f"策略项 {key} 插件不能使用参数 '{str(arguments)}'"

            data[key] = fn(zip(*(binding[source] for source in data_src)), data_src, arguments)

        except KeyError as kerr:
            raise BaseException(f"账户-{acc_name} 策略-{policy_name} 指定的数据源不存在：'{kerr.args[0]}'。")
        except RuntimeError as e:
            if ''.join(e.args).startswith('generator raised StopIteration'):
                continue
            else:
                raise e

    return data