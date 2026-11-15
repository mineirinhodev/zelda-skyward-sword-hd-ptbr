"""Monta o mod aplicando texto/ sobre os .arc originais do seu dump.

    python3 tools/build.py <romfs do jogo> <pasta do mod>

<romfs do jogo> é a pasta que contém US/Object/en_US e/ou EU/Object/en_GB.
O resultado é gravado em <pasta do mod>/romfs/...
"""
import json
import os
import sys

import msbt
import u8

HERE = os.path.dirname(os.path.abspath(__file__))
TEXT = os.path.join(os.path.dirname(HERE), "texto")
REGIONS = ["US/Object/en_US", "EU/Object/en_GB"]


def patch(data, texts, where):
    """Troca os textos de um .msbt pelos de `texts` ({rótulo: texto})."""
    secs = msbt.sections(data)
    names = msbt.labels(dict(secs)[b"LBL1"])
    missing = 0
    out = []
    for magic, content in secs:
        if magic == b"TXT2":
            items = msbt.raw_strings(content)
            for i in range(len(items)):
                if names.get(i) in texts:
                    items[i] = msbt.encode(texts[names[i]])
                else:
                    missing += 1
            content = msbt.pack_strings(items)
        out.append((magic, content))
    if missing:
        print("aviso: %s: %d texto(s) sem tradução, mantidos como no original" % (where, missing))
    return msbt.join(data[:0x20], out)


def main(romfs, mod):
    done = 0
    for region in REGIONS:
        src = os.path.join(romfs, region)
        if not os.path.isdir(src):
            continue
        dst = os.path.join(mod, "romfs", region)
        os.makedirs(dst, exist_ok=True)
        for arc in sorted(os.listdir(TEXT)):
            path = os.path.join(src, arc + ".arc")
            if not os.path.isfile(path):
                print("aviso: %s não encontrado" % path)
                continue
            with open(path, "rb") as f:
                nodes = u8.read(f.read())
            for node in nodes:
                source = os.path.join(TEXT, arc, node["name"][:-5] + ".json")
                if node["dir"] or not node["name"].endswith(".msbt") or not os.path.isfile(source):
                    continue
                with open(source, encoding="utf-8") as f:
                    node["data"] = patch(node["data"], json.load(f), "%s/%s" % (arc, node["name"]))
            with open(os.path.join(dst, arc + ".arc"), "wb") as f:
                f.write(u8.write(nodes))
            done += 1
    if not done:
        sys.exit("nenhum .arc encontrado em %s (esperado: %s)" % (romfs, " ou ".join(REGIONS)))
    print("%d arquivo(s) gravados em %s" % (done, os.path.join(mod, "romfs")))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
