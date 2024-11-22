from collections.abc import Iterable

from loader import attributes
from plugin import load_plugin
from src import DATASOURCE, PLUGIN, ARGUMENT


def each_bundle(binding: dict[str, Iterable], sources: list[str]|tuple[str]):
    yield from (v for s in sources for v in binding[s])

def run_policy(policy: dict[str, dict], binding: dict[str, Iterable], policy_name: str, acc_name: str) -> dict[str, Iterable]:
    data = dict()

    for (key, attr) in attributes(policy):
        try:
            assert attr, f"账户-{acc_name} 策略-{policy_name} 未指定插件。"
            if PLUGIN not in attr or not attr[PLUGIN]:
                data[key] = each_bundle(binding, attr[DATASOURCE])
                continue

            plugin_name = attr[PLUGIN]
            fn = load_plugin(plugin_name)

            if ARGUMENT in attr:
                arguments = attr[ARGUMENT]
                assert arguments, f"策略项 {key} 插件不能使用参数 '{str(arguments)}'"
                data[key] = fn(zip(*(binding[source] for source in attr[DATASOURCE])), arguments)
            else:
                data[key] = fn(zip(*(binding[source] for source in attr[DATASOURCE])))
        except KeyError as kerr:
            raise BaseException(f"账户-{acc_name} 策略-{policy_name} 要求的数据源 {kerr.args[0]} 在银行账号配置中没有呈现。")
        except RuntimeError as e:
            if ''.join(e.args).startswith('generator raised StopIteration'):
                continue
            else:
                raise e

    return data