from os.path import join as joinpath
from time import strftime, localtime

from tomli import load as loadconf

from src import METADATA, MERGE_POLICY, POLICYNAME, WRITETO, VALUESET


def load (path: str, name: str='accounts.txt'):
    with open(f"{path}/{name}", "rb") as f:
        toml_dict = loadconf(f)

        return toml_dict


def find_matching_policy(pol_name: str, pols: list) -> dict|None:
    for pol in pols:
        assert METADATA in pol, f" {METADATA} 元数据缺失的策略"
        pol_meta = pol[METADATA]

        assert POLICYNAME in pol_meta, f" {POLICYNAME} 是必要的配置。"
        if pol_name == pol_meta[POLICYNAME]:
            return pol

    return None


def get_meta(conf: dict) -> dict:
    assert METADATA in conf, f" {METADATA} 是必要的配置。"
    return conf[METADATA]


def get_valueset(conf: dict) -> list:
    assert VALUESET in conf, f" {VALUESET} 是必要的配置。"
    return conf[VALUESET]


def get_policies(conf: dict) -> list:
    assert MERGE_POLICY in conf, f" {MERGE_POLICY} 是必要的配置。"
    return conf.pop(MERGE_POLICY)


def get_out_uri(meta: dict, dir: str) -> str:
    if WRITETO in meta and meta[WRITETO]:
        fn = meta[WRITETO]
    else:
        fn = strftime("%a_%b_%Y%m%d %H:%M:%S", localtime())
    return joinpath(dir, fn)

def attributes(conf: dict):
    for k, v in conf.items():
        if k == METADATA:
            continue
        yield (k, v)
