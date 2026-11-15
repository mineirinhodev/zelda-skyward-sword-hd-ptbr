"""Leitor / gravador do texto de arquivos .msbt (MsgStdBn, UTF-16 big-endian).

No JSON, cada texto é uma string comum. O que não é texto vira marcação:
  [[G:T:HEX]]  comando 0x0E (grupo G, tipo T, parâmetros em hexadecimal)
  [[/G:T]]     comando 0x0F (fim de um efeito)
  [[u:XXXX]]   unidade UTF-16 sem representação direta
"""
import re
import struct

MAGIC = b"MsgStdBn"
TOKEN = re.compile(r"\[\[(/?)([0-9A-Fa-f]+):([0-9A-Fa-f]+)(?::([0-9A-Fa-f]*))?\]\]|\[\[u:([0-9A-Fa-f]{4})\]\]")


def sections(data):
    """Devolve [(magic, conteúdo)] na ordem do arquivo."""
    if data[:8] != MAGIC or data[8:10] != b"\xfe\xff":
        raise ValueError("não é um .msbt big-endian")
    count = struct.unpack(">H", data[14:16])[0]
    pos = 0x20
    out = []
    for _ in range(count):
        magic = data[pos:pos + 4]
        size = struct.unpack(">I", data[pos + 4:pos + 8])[0]
        out.append((magic, data[pos + 16:pos + 16 + size]))
        pos = (pos + 16 + size + 15) // 16 * 16
    return out


def join(header, secs):
    """Remonta o arquivo a partir do cabeçalho original e das seções."""
    body = b""
    for magic, content in secs:
        body += magic + struct.pack(">I", len(content)) + b"\0" * 8 + content
        body += b"\xab" * (-len(body) % 16)
    return header[:18] + struct.pack(">I", 0x20 + len(body)) + header[22:0x20] + body


def labels(content):
    """LBL1 -> {índice: rótulo}."""
    slots = struct.unpack(">I", content[:4])[0]
    out = {}
    for i in range(slots):
        n, off = struct.unpack(">II", content[4 + i * 8:12 + i * 8])
        for _ in range(n):
            size = content[off]
            name = content[off + 1:off + 1 + size].decode("ascii")
            out[struct.unpack(">I", content[off + 1 + size:off + 5 + size])[0]] = name
            off += 5 + size
    return out


def raw_strings(content):
    """TXT2 -> lista de bytes, um item por texto (com o terminador)."""
    count = struct.unpack(">I", content[:4])[0]
    offs = list(struct.unpack(">%dI" % count, content[4:4 + count * 4])) + [len(content)]
    return [content[offs[i]:offs[i + 1]] for i in range(count)]


def pack_strings(items):
    """Lista de bytes -> TXT2."""
    off = 4 + len(items) * 4
    table = struct.pack(">I", len(items))
    for item in items:
        table += struct.pack(">I", off)
        off += len(item)
    return table + b"".join(items)


def decode(raw):
    """Bytes de um texto -> string com marcações."""
    units = struct.unpack(">%dH" % (len(raw) // 2), raw)
    out = []
    i = 0
    while i < len(units):
        u = units[i]
        if u == 0x0E:
            group, kind, size = units[i + 1:i + 4]
            params = raw[(i + 4) * 2:(i + 4) * 2 + size]
            out.append("[[%X:%X:%s]]" % (group, kind, params.hex().upper()))
            i += 4 + size // 2
        elif u == 0x0F:
            out.append("[[/%X:%X]]" % (units[i + 1], units[i + 2]))
            i += 3
        elif u == 0 and i == len(units) - 1:
            i += 1
        elif u == 0x0A or (u >= 0x20 and not 0xD800 <= u <= 0xDFFF):
            out.append(chr(u))
            i += 1
        else:
            out.append("[[u:%04X]]" % u)
            i += 1
    return "".join(out)


def encode(text):
    """String com marcações -> bytes de um texto (com o terminador)."""
    out = b""
    pos = 0
    for m in TOKEN.finditer(text):
        out += text[pos:m.start()].encode("utf-16-be")
        pos = m.end()
        if m.group(5):
            out += struct.pack(">H", int(m.group(5), 16))
        elif m.group(1):
            out += struct.pack(">HHH", 0x0F, int(m.group(2), 16), int(m.group(3), 16))
        else:
            params = bytes.fromhex(m.group(4) or "")
            out += struct.pack(">HHHH", 0x0E, int(m.group(2), 16), int(m.group(3), 16), len(params)) + params
    return out + text[pos:].encode("utf-16-be") + b"\0\0"
