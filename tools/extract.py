"""Exporta o texto dos .arc de uma pasta para JSON (um arquivo por .msbt).

    python3 tools/extract.py <pasta com os .arc> <pasta de saída>
"""
import json
import os
import sys

import msbt
import u8


def main(src, dst):
    total = 0
    for arc in sorted(f for f in os.listdir(src) if f.endswith(".arc")):
        with open(os.path.join(src, arc), "rb") as f:
            nodes = u8.read(f.read())
        folder = os.path.join(dst, arc[:-4])
        os.makedirs(folder, exist_ok=True)
        for node in nodes:
            if node["dir"] or not node["name"].endswith(".msbt"):
                continue
            secs = dict(msbt.sections(node["data"]))
            names = msbt.labels(secs[b"LBL1"])
            texts = {names[i]: msbt.decode(raw) for i, raw in enumerate(msbt.raw_strings(secs[b"TXT2"]))}
            total += len(texts)
            with open(os.path.join(folder, node["name"][:-5] + ".json"), "w", encoding="utf-8") as f:
                json.dump(texts, f, ensure_ascii=False, indent=1)
                f.write("\n")
    print("%d textos exportados" % total)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
