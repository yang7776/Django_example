# -*- coding: utf-8 -*-
import os
import json


"""
    #这个脚本是用来生成发布json的，以解决json容易写错且不能添加注释的问题。
    ## 使用方法：
    在这个文件中，第一行写singnal_mod，如果没有就写英文减号“-”。下面写要发布的文件名，不带引号。
    空行以及“#”号后面的内容被忽略。执行main.py，会在fab_json中生成json文件。
    ## 注意事项！
    　　1、文件列表需要手动去重复
    　　2、文件名中含有通配符或正则表达式的时候，会生成错误结果
   　　 3、文件名中含有common文件或静态文件，可能会生成错误结果

    务必手动检查！
    务必手动检查！
    务必手动检查！
"""

SOURCE_FILE_DIR = "source_files"
OUT_PUT_DIR = "fab_json"
STATIC_FILE_EX_NAME = ("js", "css", "png", "gif", "jpg", "jpeg", 'json', 'map', 'eot', 'woff', 'ttf', 'svg')


def parse_fab_file(source_file, target_file):
    with open(source_file) as f:
        lines = f.readlines()

    content = [_ for _ in [f_n.strip(" \r\n").split("#")[0].replace("\\", "/").strip(" \r\n") for f_n in lines] if _]
    fab_json = {
        "type": "filelist",
        "signal_mods": [],
        "statics_cdn": [],
        "spec_files": [],
        "apps": [],
        "djapps": [],
        "common": [],
        "fix_common": []
    }
    print(source_file)
    signal_mods = content[0]
    fab_json["signal_mods"] = list(filter(lambda y: y, map(lambda x: x.strip(), [] if signal_mods == "-" else signal_mods.split(" "))))
    content = list(set(content[1:]))

    # pick spec_files
    fab_json["spec_files"].extend(content)

    # pick statics files
    for file_name in content:
        base, ex = os.path.splitext(file_name)
        if ex.lower()[1:] in STATIC_FILE_EX_NAME and file_name not in fab_json["statics_cdn"]:
            fab_json["statics_cdn"].append(file_name)

    # pick apps and djapps
    for file_name in content:
        s = file_name.split("/")
        if s[0] == "apps":
            if s[1] not in fab_json["apps"]:
                fab_json["apps"].append(s[1])
        elif s[0] == "djapps":
            if s[1] not in fab_json["djapps"]:
                fab_json["djapps"].append(s[1])
        else:
            if s[0] not in fab_json["common"]:
                fab_json["common"].append(s[0])
            if file_name not in fab_json["fix_common"]:
                fab_json["fix_common"].append(file_name)
            fab_json["spec_files"].pop(fab_json["spec_files"].index(file_name))

    with open(target_file, "w") as f:
        f.write(json.dumps(fab_json, indent=4, ensure_ascii=False))
    print("gen: %s" % target_file)


if __name__ == "__main__":
    source_files = os.listdir(SOURCE_FILE_DIR)
    gen_file_list = {}
    for f_name in source_files:
        base_name, ex_name = os.path.splitext(f_name)
        gen_file_list[f_name] = base_name + ".json"

    existed_json_files = os.listdir(OUT_PUT_DIR)
    need_gen_files = {k: v for k, v in gen_file_list.items()}  # if v not in existed_json_files}

    for src in need_gen_files:
        parse_fab_file(os.path.join(SOURCE_FILE_DIR, src), os.path.join(OUT_PUT_DIR, need_gen_files[src]))
    print("Done")


def encode_ascii(bytes_str):
    return "".join(["\\0x%0x" % ord(c) for c in bytes_str])
