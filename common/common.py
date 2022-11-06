import base64
import copy
import hashlib
import itertools
import json
import os
import random
import re
import shlex
import subprocess
import uuid
from collections import defaultdict
from datetime import date, datetime
from typing import Any, Dict, Hashable, List, Optional, Sequence, Tuple

import requests

__all__ = [
    "dict_to_base64",
    "base64_to_dict",
    "str_to_base64",
    "base64_to_str",
    "is_legal_json",
    "str_to_dict",
    "utcnow",
    "now",
    "now_s",
    "dttm_to_str",
    "str_to_dttm",
    "underscore_to_classname",
    "open_subprocess",
    "deepcopy",
    "safe_remove_file",
    "get_uuid",
    "is_http_url",
    "is_local_path",
    "is_uuid",
    "smart_get_bytes",
    "request_get_ha",
    "request_get",
    "http_get_bytes",
    "request_post",
    "request_delete",
    "request_put",
    "rows_to_records",
    "md5",
    "read_excel",
    "random_color",
    "random_grey",
    "find_continous_one_from_bits",
    "chinese2int",
    "num2chinese",
    "floor_number_compress",
    "str_floor_number_to_int_list",
    "deduce_floor_number_from_drawing_name",
    "read_path",
    "write_content_to_path",
]


def dict_to_base64(d: Dict) -> str:
    s = json.dumps(d, ensure_ascii=False)
    return str_to_base64(s)


def base64_to_dict(s: str) -> Dict:
    s = base64_to_str(s)
    assert is_legal_json(s), "非法json"
    return str_to_dict(s)


def str_to_base64(s: str) -> str:
    return base64.b64encode(s.encode()).decode()


def base64_to_str(s: str) -> str:
    return base64.b64decode(s.encode()).decode()


def is_legal_json(s: str) -> bool:
    try:
        json.loads(s)
        return True
    except Exception as e:
        return False


def str_to_dict(s: str) -> Dict:
    return json.loads(s)


def now():
    """
    now
    :return:
    """
    return datetime.now()


def utcnow():
    """
    utcnow
    :return:
    """
    return datetime.utcnow()


def dttm_to_str(dttm):
    """
    datetime->字符串
    :return:
    """
    return dttm.strftime("%Y-%m-%d %H:%M:%S")


def str_to_dttm(s):
    """
    字符串->datetime
    :param s:
    :return:
    """
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        pass
    return None


def now_s():
    return dttm_to_str(now())


def seconds_since(dttm):
    return (now() - dttm).total_seconds()


def underscore_to_classname(s):
    """
    下划线-->类名
    :param s:
    :return:
    """
    arr = s.split("_")
    return "".join(_[:1].upper() + _[1:] for _ in arr)


def open_subprocess(
    cmd: str,
    split: bool = True,
    shell: bool = False,
    raise_exc: bool = True,
    timeout=None,
    **kwargs,
) -> Tuple[int, str, str]:
    """
    同步打开子进程，等待子进程执行结果
    :param cmd: 命令
    :param split:
    :param shell:
    :param raise_exc: raise异常
    :return: tuple(程序退出码, 标准输出, 标出错误)
    """
    proc = subprocess.Popen(
        shlex.split(cmd) if split else cmd,
        stdout=kwargs.get("stdout", 0) or subprocess.PIPE,
        stderr=kwargs.get("stderr", 0) or subprocess.PIPE,
        shell=shell,
    )

    timeout_triggered = False
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as e:
        stdout, stderr = proc.communicate()
        proc.kill()
        timeout_triggered = True

    stdout = stdout or b""
    stderr = stderr or b""

    rc = proc.returncode
    if timeout_triggered:
        rc = -1
    if rc != 0 and raise_exc:
        raise Exception(stderr.decode())

    stdout = stdout.decode()
    if timeout_triggered:
        stdout = f"{stdout}\n运行超时，超时时间: {timeout}秒"
    stderr = stderr.decode()
    return rc, stdout, stderr


def deepcopy(d: Dict) -> Dict:
    """深拷贝"""
    return copy.deepcopy(d)


def rows_to_records(
    rows: Sequence[Sequence[Any]], keys: Sequence[Hashable], utc_convert: bool = True
) -> List[Dict]:
    """
    行数据转化为字典
    :param rows:
    :param keys:
    :param utc_convert:
    :return:
    """
    return [map_row_to_object(row, keys) for row in rows]


def map_row_to_object(row: Sequence[Any], fields: Sequence[Hashable]) -> Dict:
    """
    row -> object list
    :param row: 行
    :param fields: 列名
    :return:
    """
    assert len(fields) == len(row)
    d = {}
    for i in range(len(row)):
        if isinstance(row[i], date):
            d[fields[i]] = str(row[i])
        elif isinstance(row[i], datetime):
            d[fields[i]] = row[i].strftime("%Y-%m-%d %H:%M:%S")
        else:
            d[fields[i]] = row[i]
    return d


def md5(s: str) -> str:
    x = hashlib.md5()
    x.update(s.encode())
    return x.hexdigest()


def is_http_url(url: str) -> bool:
    """
    是否是http(s)路径
    Args:
        url:

    Returns:

    """
    return url.startswith("http://") or url.startswith("https://")


def is_local_path(url: str) -> bool:
    """
    是否是本地磁盘路径
    Args:
        url:

    Returns:

    """
    return url.startswith("/")


def is_uuid(url: str) -> bool:
    """
    是否是32位uuid
    Args:
        url:

    Returns:

    """
    return re.fullmatch(r"^[a-z0-9]{32}$", url) is not None


def safe_remove_file(path: str) -> None:
    """
    安全移除文件
    Args:
        path:

    Returns:

    """
    try:
        os.remove(path)
    except Exception as e:
        pass


def get_uuid() -> str:
    """
    uuid生成
    Returns:

    """
    return uuid.uuid4().hex


def request_get_ha(urls, **kwargs) -> Tuple[int, Any]:
    """
    高可用的get，支持url列表
    :param urls:
    :param kwargs:
    :return:
    """
    if isinstance(urls, str):
        return request_get(urls, **kwargs)

    for url in urls:
        status_code, data = request_get(url, **kwargs)
        if status_code == 200:
            return status_code, data
    return 500, None


def request_get(url, headers=None, auth=None, **kwargs) -> Tuple[int, Any]:
    try:
        res = requests.get(url, headers=headers, auth=auth, **kwargs)
    except Exception as e:
        return 500, str(e)
    try:
        return res.status_code, res.json()
    except:
        return res.status_code, res.text


def http_get_bytes(
    url, headers=None, auth=None, raise_exception=False, **kwargs
) -> Tuple[int, Any]:
    try:
        res = requests.get(url, headers=headers, auth=auth, **kwargs)
        return res.status_code, res.content
    except Exception as e:
        status_code, data = 500, str(e)
        if raise_exception:
            raise Exception(f"获取{url}失败 {status_code} {data}")
        return status_code, data


def smart_get_bytes(url):
    """
    智能下载
    Args:
        url: url、本地路径、32位uuid都支持

    Returns: 文件的字节流

    """
    if is_http_url(url):
        _, data = http_get_bytes(url, raise_exception=True)
        return data
    elif is_local_path(url):
        if os.path.exists(url):
            f = open(url, "rb")
            data = f.read()
            f.close()
            return data
    # elif is_uuid(url):
    #     return FileServiceClient().download_file(url)
    return None


def request_post(url, headers=None, payload=None, **kwargs) -> Tuple[int, Any]:
    if not headers:
        headers = {"content-type": "application/json;charset=UTF-8"}
    else:
        headers.update({"content-type": "application/json;charset=UTF-8"})

    try:
        res = requests.post(url, json=payload, headers=headers, **kwargs)
    except Exception as e:
        return 500, str(e)
    try:
        return res.status_code, res.json()
    except:
        return res.status_code, res.text


def request_delete(url, headers=None, payload=None, **kwargs) -> Tuple[int, Any]:
    if not headers:
        headers = {"content-type": "application/json;charset=UTF-8"}
    else:
        headers.update({"content-type": "application/json;charset=UTF-8"})

    try:
        res = requests.delete(url, json=payload, headers=headers, **kwargs)
    except Exception as e:
        return 500, str(e)
    try:
        return res.status_code, res.json()
    except:
        return res.status_code, res.text


def request_put(url, headers=None, payload=None, **kwargs) -> Tuple[int, Any]:
    if not headers:
        headers = {"content-type": "application/json;charset=UTF-8"}
    else:
        headers.update({"content-type": "application/json;charset=UTF-8"})

    try:
        res = requests.put(url, json=payload, headers=headers, **kwargs)
    except Exception as e:
        return 500, str(e)
    try:
        return res.status_code, res.json()
    except:
        return res.status_code, res.text


def read_excel(file_path) -> Tuple[List[str], List[List[Any]]]:
    """读取excel的第一个sheet，返回列名和行数据"""
    import pandas as pd

    df = pd.read_excel(file_path)
    columns = list(df.columns)
    rows = [[_ for _ in row] for row in df.values]
    return columns, rows


def random_color() -> Tuple[int, int, int]:
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def random_grey() -> Tuple[int, int, int]:
    x = random.randint(0, 255)
    return (x, x, x)


def find_continous_one_from_bits(bits: Sequence[bool]) -> List[List[bool]]:
    """
    从一个true/false的数组中获取连续的true
    """
    ret = []
    cur = None
    for i, v in enumerate(bits):
        if v:
            if cur:
                cur.append(i)
            else:
                cur = [i]
        else:
            if cur:
                ret.append(cur)
                cur = None
    if cur:
        ret.append(cur)

    if len(ret) >= 2 and bits[0] and bits[-1]:
        ret[-1].extend(ret[0])
        return ret[1:]
    return ret


def strict_dict_get(d, key, *args):
    """严格的字典get，缺key默认抛异常"""
    if isinstance(d, defaultdict):
        return d[key]

    if args:
        return d.get(key, args[0])

    # 暂时不做严格检查
    if key not in d:
        raise Exception(f'找不到key: "{key}"且get()没指定默认值')

    return d.get(key)


chinese_digit_d = {
    "零": 0,
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
    "百": 100,
    "千": 1000,
    "万": 10000,
    "亿": 100000000,
}


def chinese2int(chinese):
    if not re.match(r"^负?[零一二两三四五六七八九十百千万亿]+$", chinese):
        return None

    negative = chinese.startswith("负")
    if negative:
        chinese = chinese[1:]

    total = 0
    r = 1  # 表示单位: 个十百千...
    for i in range(len(chinese) - 1, -1, -1):
        val = chinese_digit_d.get(chinese[i])
        if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
            if val > r:
                r = val
                total = total + val
            else:
                r = r * val
        elif val >= 10:
            r = val if val > r else r * val
        else:
            total = total + r * val
    return -total if negative else total


def num2chinese(num, big=False, simp=True, o=False, twoalt=False):
    """
    Converts numbers to Chinese representations.
    `big`   : use financial characters.
    `simp`  : use simplified characters instead of traditional characters.
    `o`     : use 〇 for zero.
    `twoalt`: use 两/兩 for two when appropriate.
    Note that `o` and `twoalt` is ignored when `big` is used,
    and `twoalt` is ignored when `o` is used for formal representations.
    """
    # check num first
    nd = str(num)
    if abs(float(nd)) >= 1e48:
        raise ValueError("number out of range")
    elif "e" in nd:
        raise ValueError("scientific notation is not supported")
    c_symbol = "正负点" if simp else "正負點"
    if o:  # formal
        twoalt = False
    if big:
        c_basic = "零壹贰叁肆伍陆柒捌玖" if simp else "零壹貳參肆伍陸柒捌玖"
        c_unit1 = "拾佰仟"
        c_twoalt = "贰" if simp else "貳"
    else:
        c_basic = "〇一二三四五六七八九" if o else "零一二三四五六七八九"
        c_unit1 = "十百千"
        if twoalt:
            c_twoalt = "两" if simp else "兩"
        else:
            c_twoalt = "二"
    c_unit2 = "万亿兆京垓秭穰沟涧正载" if simp else "萬億兆京垓秭穰溝澗正載"
    revuniq = lambda l: "".join(k for k, g in itertools.groupby(reversed(l)))
    nd = str(num)
    result = []
    if nd[0] == "+":
        result.append(c_symbol[0])
    elif nd[0] == "-":
        result.append(c_symbol[1])
    if "." in nd:
        integer, remainder = nd.lstrip("+-").split(".")
    else:
        integer, remainder = nd.lstrip("+-"), None
    if int(integer):
        splitted = [integer[max(i - 4, 0) : i] for i in range(len(integer), 0, -4)]
        intresult = []
        for nu, unit in enumerate(splitted):
            # special cases
            if int(unit) == 0:  # 0000
                intresult.append(c_basic[0])
                continue
            elif nu > 0 and int(unit) == 2:  # 0002
                intresult.append(c_twoalt + c_unit2[nu - 1])
                continue
            ulist = []
            unit = unit.zfill(4)
            for nc, ch in enumerate(reversed(unit)):
                if ch == "0":
                    if ulist:  # ???0
                        ulist.append(c_basic[0])
                elif nc == 0:
                    ulist.append(c_basic[int(ch)])
                elif nc == 1 and ch == "1" and unit[1] == "0":
                    # special case for tens
                    # edit the 'elif' if you don't like
                    # 十四, 三千零十四, 三千三百一十四
                    ulist.append(c_unit1[0])
                elif nc > 1 and ch == "2":
                    ulist.append(c_twoalt + c_unit1[nc - 1])
                else:
                    ulist.append(c_basic[int(ch)] + c_unit1[nc - 1])
            ustr = revuniq(ulist)
            if nu == 0:
                intresult.append(ustr)
            else:
                intresult.append(ustr + c_unit2[nu - 1])
        result.append(revuniq(intresult).strip(c_basic[0]))
    else:
        result.append(c_basic[0])
    if remainder:
        result.append(c_symbol[2])
        result.append("".join(c_basic[int(ch)] for ch in remainder))
    return "".join(result)


def str_to_int(s):
    if s in ("标准", "屋顶", "机房"):
        return s

    try:
        return int(round(float(s)))
    except Exception:
        pass
    return chinese2int(s)


def str_floor_number_to_int_list(s):
    if not s:
        return []
    try:
        return sorted([int(_) for _ in s.split(",")])
    except Exception as e:
        pass
    return []


def floor_number_compress(int_list):
    if not int_list:
        return None
    int_list = sorted(list(set(int_list)))

    res = []
    left = None
    right = None
    for i, v in enumerate(int_list):
        if not left:
            left = right = v
        else:
            if v == right + 1:
                right = v
            else:
                res.append((left, right))
                left = right = v
    res.append((left, right))

    for i, v in enumerate(res):
        l, r = v
        if l == r:
            res[i] = "{}层".format(num2chinese(l))
        else:
            res[i] = "{}～{}层".format(num2chinese(l), num2chinese(r))

    return "、".join(res)


def deduce_floor_number_from_drawing_name(s):
    """
        根据图框名推断楼层名
    五、七、九层平面图	[5,7,9]
    五、七-九层平面图	[5,7,8,9]
    七至九层平面图	[7,8,9]
    七到九层平面图	[7,8,9]
    七~九层平面图	[7,8,9]
    七～九层平面图	[7,8,9]
    """
    s = re.sub(r"^.+(楼|栋|宅)", "", s)  # 去掉楼、栋
    m = re.match(r"^(?P<floor>.+)层.*平面图", s)
    floor = m.group("floor") if m else None
    if not floor:
        return None
    floor = floor.replace("首", "1")
    floor = floor.replace("地下", "负")
    floor = re.sub(r"[第层\s]", "", floor)  # 去掉空格、层
    floor = re.sub(r"[至到~～\-]", "|", floor)  # 区间分隔符替换为|
    floor = [_ for _ in re.split(r"[、,，；。]", floor) if _]

    ret = set()
    for x in floor:
        arr = [str(_) for _ in x.split("|") if _]
        if len(arr) == 2:
            a, b = str_to_int(arr[0]), str_to_int(arr[1])
            if a is not None and b is not None:
                for i in range(a, b + 1):
                    ret.add(i)
        elif len(arr) == 1:
            a = str_to_int(arr[0])
            if a is not None:
                ret.add(a)

    for _ in ("标准", "屋顶", "机房"):
        if _ in ret:
            return _

    return ",".join(str(_) for _ in ret) or None


def read_path(path: str) -> str:
    if not os.path.exists(path):
        return ""

    f = open(path, "r", encoding="UTF-8")
    ret = "".join(f.readlines())
    f.close()
    return ret


def write_content_to_path(content: str, path: str):
    """
    写内容到指定路径
    """
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    f = open(path, "w", encoding="UTF-8")
    f.write(content)
    f.close()
