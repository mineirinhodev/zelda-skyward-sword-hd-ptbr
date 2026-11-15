# The Legend of Zelda: Skyward Sword HD — Tradução PT-BR (não oficial)

Tradução dos textos de **The Legend of Zelda: Skyward Sword HD** (Nintendo Switch, title ID `01002DA013484000`)
para **português do Brasil**. O jogo não tem português; a tradução entra no lugar do texto em inglês.

- Interface, menus, itens, tutoriais, dicas, mapas e os diálogos da história.
- 8.103 textos em 84 arquivos (cerca de 168 mil palavras em português).
- Vozes, vídeos e textos desenhados em imagens continuam como no original.

> **Aviso:** a tradução **ainda não foi testada dentro do jogo** nem revisada linha a linha. Espere inconsistências,
> frases estranhas e linhas que não cabem na caixa de texto. Correções são bem-vindas: veja
> [Como contribuir](#como-contribuir).

## O que há neste repositório

Este repositório **não contém arquivos do jogo**. Ele guarda só o texto traduzido e os scripts que o aplicam sobre o
seu próprio dump:

```
texto/      texto em português, um JSON por arquivo .msbt do jogo
tools/      scripts em Python para montar o mod e exportar texto
```

Os arquivos de texto do jogo (`.arc`) também carregam dados originais que não são texto (roteiros de eventos
`.msbf`, `zev.dat`), por isso o mod já montado não é distribuído aqui.

## Como montar o mod

Você precisa do Python 3 (sem dependências) e do RomFS do seu próprio jogo, extraído do seu dump.

1. Localize no RomFS as pastas `US/Object/en_US` e/ou `EU/Object/en_GB`. Cada uma tem seis arquivos:
   `0-Common.arc`, `1-Town.arc`, `2-Forest.arc`, `3-Mountain.arc`, `4-Desert.arc` e `5-CenterField.arc`.
2. Rode, apontando para a raiz do RomFS:

   ```
   python3 tools/build.py "caminho/para/romfs" "Traducao PT-BR"
   ```

O resultado é uma pasta de mod pronta:

```
Traducao PT-BR/
└── romfs/
    ├── US/Object/en_US/*.arc
    └── EU/Object/en_GB/*.arc
```

Só são geradas as regiões que existirem no seu dump. Textos do jogo que não tiverem tradução (por exemplo, numa
versão mais nova) ficam em inglês e o script avisa quantos são.

## Instalação

Em qualquer caso, **deixe o idioma do jogo em inglês**: o português aparece no lugar dele.

### NX Library (Mac)

1. Copie a pasta `Traducao PT-BR` para
   `/Applications/NxNative_Data/AppSupport/01002DA013484000/mods/`
2. Abra o NX Library, entre em Skyward Sword HD → **Mods** e ligue `Traducao PT-BR`.
3. Inicie o jogo.

### Switch com Atmosphère

Copie o conteúdo da pasta `romfs` do mod para o cartão SD em

```
atmosphere/contents/01002DA013484000/romfs/
```

Não testado.

### Outros emuladores

Emuladores que aceitam mods no formato `romfs` costumam ter uma pasta de mods por jogo: abra-a pelo menu do
emulador e copie a pasta `Traducao PT-BR` inteira para lá. Não testado.

### Desinstalar

Desligue o mod ou apague a pasta. Nada no jogo nem no save é alterado.

## Escolhas de tradução

- Nomes de personagens, lugares e criaturas ficam como no original (Skyloft, Loftwing, Faron, Eldin, Lanayru,
  Ghirahim, Triforce, Bokoblin…).
- Termos comuns são traduzidos (Rupia, Deusa, Espada Mestra, Coração…), assim como itens, interface, tutoriais e
  diálogos.

## Limitações conhecidas

- Nenhuma parte foi conferida dentro do jogo. A única verificação feita foi automática: o texto deste repositório,
  aplicado pelos scripts, reproduz byte a byte o mod que foi montado originalmente.
- O script de montagem não foi testado sobre um dump limpo da região europeia (`en_GB`); se ela tiver textos que a
  americana não tem, eles ficam em inglês.
- Linhas podem ficar mais largas que a caixa de texto.
- O gênero de quem fala ou de quem ouve foi deduzido pelo contexto e pode estar errado em algumas falas.

## Como contribuir

Achou um erro? Abra uma [issue](../../issues) com a frase como aparece no jogo (uma captura de tela ajuda) ou mande
um pull request.

A tradução fica em `texto/<arquivo .arc>/<arquivo .msbt>.json`. Cada arquivo é um objeto
`{"RÓTULO": "texto em português"}`, em que o rótulo é o nome que o próprio jogo dá àquele texto. Para corrigir uma
frase, procure-a nesses arquivos e edite o valor, mantendo:

- as marcações entre colchetes duplos exatamente iguais. Elas são comandos do jogo (cor, pausa, nome do jogador,
  ícone de botão, opções de resposta…):
  - `[[G:T:HEX]]` — comando do grupo `G`, tipo `T`, com parâmetros em hexadecimal;
  - `[[/G:T]]` — fim de um efeito;
  - `[[u:XXXX]]` — caractere especial;
- as quebras de linha (`\n`) em posições que caibam na caixa de texto.

## Scripts

| Script | Função |
|---|---|
| `tools/build.py` | aplica `texto/` sobre os `.arc` do seu dump e grava a pasta do mod |
| `tools/extract.py` | exporta o texto dos `.arc` de uma pasta para JSON, no mesmo formato de `texto/` |
| `tools/msbt.py` | leitor / gravador do texto de arquivos `.msbt` (UTF-16 big-endian) |
| `tools/u8.py` | leitor / gravador de arquivos U8 (`.arc`) |

### Detalhe técnico

Cada `.arc` é um arquivo U8 sem compressão com pares `.msbf` (fluxo dos eventos) e `.msbt` (texto). O `build.py`
troca apenas a seção `TXT2` de cada `.msbt`, casando os textos pelo rótulo da seção `LBL1`; todo o resto do arquivo é
copiado do seu dump sem alteração.

## Aviso legal

Projeto de fã, sem fins lucrativos, sem vínculo com a Nintendo. The Legend of Zelda e Skyward Sword são marcas e
propriedade de seus respectivos donos. Este repositório não inclui o jogo nem seus arquivos originais e só funciona
com uma cópia sua, obtida legalmente. Os scripts em `tools/` estão sob a licença MIT (veja [`LICENSE`](LICENSE)).
