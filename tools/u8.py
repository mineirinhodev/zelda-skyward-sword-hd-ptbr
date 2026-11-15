"""Leitor / gravador de arquivos U8 (.arc) do Skyward Sword HD."""
import struct

MAGIC = b"U\xaa8-"
ALIGN = 32


def _align(n, a=ALIGN):
    return (n + a - 1) // a * a


def read(data):
    """Devolve a lista de nós: dicts com dir, name, e data (arquivo) ou parent/end (pasta)."""
    if data[:4] != MAGIC:
        raise ValueError("não é um arquivo U8")
    root, _hsize, _doff = struct.unpack(">III", data[4:16])
    count = struct.unpack(">I", data[root + 8:root + 12])[0]
    names = root + count * 12
    nodes = []
    for i in range(count):
        kind, a, b = struct.unpack(">III", data[root + i * 12:root + i * 12 + 12])
        start = names + (kind & 0xFFFFFF)
        name = data[start:data.index(b"\0", start)].decode("ascii")
        if kind >> 24:
            nodes.append({"dir": True, "name": name, "parent": a, "end": b})
        else:
            nodes.append({"dir": False, "name": name, "data": data[a:a + b]})
    return nodes


def write(nodes):
    """Monta o arquivo U8 a partir da lista de nós devolvida por read()."""
    names = b""
    name_offs = []
    for node in nodes:
        name_offs.append(len(names))
        names += node["name"].encode("ascii") + b"\0"
    root = 0x20
    hsize = len(nodes) * 12 + len(names)
    doff = _align(root + hsize)
    table = b""
    blob = b""
    for node, noff in zip(nodes, name_offs):
        if node["dir"]:
            table += struct.pack(">III", 0x01000000 | noff, node["parent"], node["end"])
        else:
            blob += b"\0" * (_align(len(blob)) - len(blob))
            table += struct.pack(">III", noff, doff + len(blob), len(node["data"]))
            blob += node["data"]
    head = MAGIC + struct.pack(">III", root, hsize, doff) + b"\0" * 16
    out = head + table + names
    out += b"\0" * (doff - len(out))
    return out + blob
