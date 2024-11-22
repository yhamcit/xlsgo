from importlib import import_module


def load_plugin(plugin_name: str) :
    slices = plugin_name.split('.')

    assert len(slices) > 1, f"插件名称格式应为：'模块'.'函数名'， 指定名称为： {plugin_name}。"
    module: str = '.'.join(slices[:-1])
    func: str = slices[-1]
    try:
        plugin_module = import_module(module)
        return getattr(plugin_module, func)
    except BaseException as err:
        assert False, f"'{module}'模块使用的插件 '{func}' 不能被加载，原因{err.args}。"
