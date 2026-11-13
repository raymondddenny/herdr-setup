# Cozy pixel art for pixel-agents: 24x24 scenes (one per machine) and 16x16 chibi
# adventurers (one per space), drawn over each other in the card.
# Run: python3 sprites.py [docs_dir] -> writes scenes/*.svg and chars/*.svg next to
# this file; given a folder, also README images there: sprites.svg (every char on
# every scene), chars/<name>.svg (each char on a scene) and chars/soon.svg.
#
# The drawings (SCENES, CHARS and their palettes) are art: CC BY-NC 4.0.
# The code around them is Apache License 2.0. See NOTICE in the repo.
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
# Warm plum outline instead of black, soft skin, blush.
K, SKIN, NOSE, BLUSH = "#3b2433", "#f8cfa8", "#e0a07c", "#f28a8a"

def band(rows):  # [(height, color)] top to bottom -> full-width rects
    y, out = 0, []
    for h, c in rows:
        out.append((0, y, 24, h, c)); y += h
    return out

def glow(x, y, w, h, c="#ffb84a", a=0.14):  # a soft light pool
    return (x, y, w, h, c, a)

# Each rect: (x, y, w, h, color[, opacity]). Keep the middle (x 4..19, y 4..19) calm:
# the character stands there.
SCENES = {
  # Porch at sunset: lantern, railing, potted plant.
  "dusk": band([(4, "#3d2a5c"), (3, "#6a3f6e"), (3, "#a85a72"), (3, "#e08a78"), (7, "#f4b38a")])
    + [(4, 1, 1, 1, "#f2d2ff"), (15, 2, 1, 1, "#f2d2ff"), (10, 0, 1, 1, "#f2d2ff")]
    + [(0, 15, 24, 1, "#8a5a3a")] + [(x, 15, 1, 5, "#8a5a3a") for x in (0, 6, 12, 18, 23)]
    + [(x, 16, 1, 4, "#9a6a46") for x in (3, 9, 15, 21)]
    + [(2, 0, 1, 2, "#5a3a2a"), (1, 2, 3, 3, "#5a3a2a"), (2, 3, 1, 1, "#ffd27a"), glow(0, 1, 5, 5, "#ffd27a", 0.25)]
    + [(20, 17, 3, 3, "#c0643a"), (20, 17, 3, 1, "#d8784a"), (19, 14, 2, 2, "#6aa84f"), (21, 12, 2, 3, "#7fc060"), (20, 15, 3, 2, "#6aa84f")]
    + [(0, 20, 24, 1, "#b07a4a"), (0, 21, 24, 3, "#7a4e2e"), (5, 21, 1, 3, "#5e3a22"), (14, 21, 1, 3, "#5e3a22"), (20, 22, 1, 2, "#5e3a22")],
  # Fireplace, bookshelf, rug, string lights.
  "den": [(0, 0, 24, 20, "#5a3a2a")] + [(x, 0, 1, 20, "#63412f") for x in (2, 6, 10, 14, 18, 22)]
    + [(0, 1, 24, 1, "#3a2418")] + [(x, 2, 1, 1, ["#ffd27a", "#f28a8a", "#7fc060", "#8ab4f0"][x // 3 % 4]) for x in range(1, 24, 3)]
    + [glow(x - 1, 1, 3, 3, "#ffd27a", 0.15) for x in range(1, 24, 3)]
    + [(0, 8, 6, 1, "#8a5a3a"), (0, 9, 5, 11, "#7a6a68"), (1, 12, 3, 8, "#2a1a1a"), (1, 17, 3, 3, "#ff8c42"), (2, 15, 1, 2, "#ffd27a"), (1, 16, 1, 1, "#ffb84a"), (3, 16, 1, 1, "#ffb84a"), glow(0, 10, 10, 13, "#ff9a4a", 0.18)]
    + [(19, 4, 5, 16, "#6a4428"), (19, 8, 5, 1, "#4a2e1a"), (19, 12, 5, 1, "#4a2e1a"), (19, 16, 5, 1, "#4a2e1a")]
    + [(20, 5, 1, 3, "#d8504a"), (21, 6, 1, 2, "#6a8ac0"), (22, 5, 1, 3, "#e0a03a"), (20, 10, 2, 2, "#7fc060"), (22, 9, 1, 3, "#c792ea"), (20, 13, 1, 3, "#f28a8a"), (21, 14, 2, 2, "#e0a03a"), (20, 17, 3, 3, "#8a5a3a")]
    + [(0, 20, 24, 1, "#8a5a3a"), (0, 21, 24, 3, "#6a4428"), (3, 21, 18, 2, "#c8504a"), (3, 21, 18, 1, "#d8644e"), (5, 22, 2, 1, "#f2b34a"), (11, 22, 2, 1, "#f2b34a"), (17, 22, 2, 1, "#f2b34a")],
  # Cottage garden at golden hour: tree, lit window, smoke, mushroom, flowers.
  "grove": band([(5, "#4a3a5e"), (5, "#7a5a72"), (5, "#c88a72"), (5, "#e8b07a")])
    + [(17, 10, 6, 7, "#8a5a4a"), (16, 8, 8, 2, "#b0443c"), (17, 7, 6, 1, "#b0443c"), (19, 12, 2, 2, "#ffd27a"), (21, 4, 1, 3, "#6a4a4a"), (22, 2, 1, 1, "#e8d8e8"), (21, 1, 1, 1, "#e8d8e8"), glow(17, 10, 6, 6, "#ffd27a", 0.15)]
    + [(1, 12, 2, 8, "#6a4428"), (0, 6, 5, 6, "#5a8a4a"), (1, 5, 3, 1, "#5a8a4a"), (1, 7, 2, 2, "#7fb060")]
    + [(6, 4, 1, 1, "#ffe08a"), (13, 6, 1, 1, "#ffe08a"), (9, 2, 1, 1, "#ffe08a")]
    + [(0, 20, 24, 1, "#7fb060"), (0, 21, 24, 3, "#5a8a4a"), (4, 19, 1, 1, "#f28a8a"), (2, 20, 1, 1, "#f2d27a"), (14, 20, 1, 1, "#f2f0ff"), (8, 21, 1, 1, "#f28a8a")]
    + [(20, 17, 3, 1, "#d8504a"), (21, 17, 1, 1, "#f2e6d0"), (21, 18, 1, 2, "#f2e6d0")],
  # Candlelit stone nook: candles, tapestry, cushion.
  "keep": [(0, 0, 24, 20, "#6a5a5e")]
    + [(0, y, 24, 1, "#5a4a50") for y in (4, 9, 14, 19)]
    + [(x + (3 if (y // 5) % 2 else 0), y, 1, 4, "#5a4a50") for y in (0, 5, 10, 15) for x in (5, 11, 17)]
    + [(19, 1, 4, 10, "#8a3a4a"), (19, 1, 4, 1, "#e0a03a"), (20, 4, 2, 2, "#e0a03a"), (19, 11, 1, 1, "#e0a03a"), (22, 11, 1, 1, "#e0a03a")]
    + [(0, 10, 5, 1, "#6a4428"), (1, 7, 1, 3, "#f2e6d0"), (3, 8, 1, 2, "#f2e6d0"), (1, 6, 1, 1, "#ffb84a"), (3, 7, 1, 1, "#ffb84a"), glow(0, 4, 6, 8, "#ffb84a", 0.22)]
    + [(0, 0, 24, 20, "#ff9a4a", 0.07)]
    + [(0, 20, 24, 1, "#8a7a7a"), (0, 21, 24, 3, "#6a5a5e"), (5, 21, 14, 2, "#6a8ac0"), (5, 21, 14, 1, "#8aa8d8")],
  # Campfire grotto: warm crystals, glowing mushrooms, a little fire.
  "cave": [(0, 0, 24, 20, "#2e2236"), (0, 0, 24, 2, "#3e2e46"), (2, 2, 3, 2, "#3e2e46"), (16, 2, 5, 2, "#3e2e46")]
    + [glow(3, 9, 18, 11, "#ff9a4a", 0.12), glow(13, 13, 9, 8, "#ffb84a", 0.16)]
    + [(1, 13, 2, 7, "#f28aa0"), (0, 16, 1, 4, "#c8607a"), (3, 16, 1, 4, "#c8607a"), (1, 13, 1, 2, "#ffc0d0")]
    + [(5, 17, 2, 1, "#5fd3e0"), (5, 18, 1, 2, "#d8d0e0"), (2, 11, 1, 1, "#5fd3e0"), (8, 5, 1, 1, "#f2b34a"), (19, 6, 1, 1, "#f28aa0")]
    + [(15, 20, 5, 1, "#6a4428"), (16, 18, 3, 2, "#ff8c42"), (17, 17, 1, 1, "#ffd27a"), (17, 18, 1, 1, "#ffd27a")]
    + [(21, 12, 2, 8, "#f2b34a"), (23, 15, 1, 5, "#c88a2a"), (21, 12, 1, 2, "#ffe08a")]
    + [(0, 20, 24, 1, "#4a3a52"), (0, 21, 24, 3, "#382a40")],
}

CHARS = {
  # Off-duty knight: messy hair, red knit scarf, mug of cocoa.
  "knight": ({"H": "#e07a3a", "R": "#d8504a", "r": "#f2d2a0", "T": "#6a8ac0", "B": "#6a4428", "M": "#f2e6d0", "m": "#8a5a3a"}, """
................
.....KKKKKK.....
...KKHHHHHHKK...
..KHHHHHHHHHHK..
..KHHSHHHHSHHK..
..KHSSSSSSSSHK..
..KSSKSSSSKSSK..
..KScSSSSSScSK..
...KSSSppSSSK...
...KKRrRRrRKK...
..KRRRRRRRRRRK..
..KTTRRTTTTTKKKK
..KSTRrTTTTSKMmK
...KTTTTTTTTKMMK
....KBBKKBBK.KK.
....KKK..KKK...."""),
  # Sleepy wizard: floppy knit hat, white beard, mustard sweater.
  "wizard": ({"G": "#7a68c8", "Y": "#f2d27a", "W": "#f2eef8", "O": "#e0a03a", "o": "#c8862a"}, """
........KK......
.......KGGK.....
......KGGGK.....
.....KGGGGGK....
....KGGGYGGGK...
..KKGGGGGGGGGKK.
.KGGGGGGGGGGGGGK
..KKSSSSSSSSKK..
..KSKKSSSSKKSK..
..KScSSSSSScSK..
..KWWWSppSWWWK..
..KWWWWWWWWWWK..
.KSKWWWWWWWWKSK.
..KOOKWWWWKOOK..
..KOoOOoOOoOOK..
...KKKKKKKKKK..."""),
  # Ranger in a leaf-sprout beanie and a warm poncho.
  "ranger": ({"L": "#7fc060", "G": "#5a8a4a", "g": "#4a7a3e", "H": "#8a5a3a", "P": "#c8864a", "Y": "#f2d27a", "N": "#6a4428"}, """
.......LL.......
........L.......
.....KKKKKK.....
...KKGGGGGGKK...
..KGGgGGgGGgGK..
..KKKKKKKKKKKK..
..KHSSSSSSSSHK..
..KSSKSSSSKSSK..
..KScSSSSSScSK..
...KSSSppSSSK...
...KKPPPPPPKK...
..KPPPPYYPPPPK..
..KPPPPPPPPPPK..
..KSPPPPPPPPSK..
...KKNNKKNNKK...
....KKK..KKK...."""),
  # Dwarf in a pompom beanie with a big ginger beard and a mug.
  "dwarf": ({"W": "#f2e6d0", "C": "#d8504a", "c": "#b83c38", "H": "#e8833a", "A": "#6a8ac0", "M": "#f2e6d0", "m": "#8a5a3a"}, """
.......WW.......
.....KKWWKK.....
....KCCCCCCK....
...KCCcCCcCCK...
..KWWWWWWWWWWK..
..KSSSSSSSSSSK..
..KSKSSSSSSKSK..
..KcSSSppSSScK..
..KHHHHHHHHHHK..
.KHHHHHHHHHHHHK.
.KHHHHHHHHHHHHK.
..KHHHHHHHHHHKKK
.KSKHHHHHHHHKMmK
.KAAKKHHHHKKAMMK
..KAAAAAAAAAAKK.
..KKKK....KKKK.."""),
  # Cleric bundled in a patchwork quilt, holding a candle.
  "cleric": ({"Q": "#a8c4a0", "q": "#f28a8a", "W": "#f2e6d0", "Y": "#ffb84a", "c": BLUSH}, """
................
.....KKKKKK.....
...KKQQQQQQKK...
..KQQqQQQQqQQK..
..KQQSSSSSSQQK..
..KQSSSSSSSSQK..
..KQSKKSSKKSQK..
..KQScSSSScSQK..
..KQQSSppSSQQK..
..KQQQQKYKQQQK..
.KQQqQQKWKQqQQK.
.KQQQQSKWKSQQQK.
.KQQQQQQQQQQQQK.
.KQqQQQQQQQQqQK.
..KQQQQQQQQQQK..
...KKKKKKKKKK..."""),
  # Bard in a beret and striped sweater, strumming a ukulele.
  "bard": ({"B": "#c8504a", "H": "#5a3a2a", "V": "#f2e6d0", "v": "#6a8ac0", "D": "#c8864a", "Y": "#3b2433", "N": "#6a4428"}, """
................
......KKKKK.....
....KKBBBBBKK...
...KBBBBBBBBBK..
..KBBBBBBBBBBBK.
..KKHKKKKKKKHK..
..KHSSSSSSSSHK..
..KSSKSSSSKSSK..
..KScSSSSSScSK..
...KSSSppSSSK...
...KKKKKKKKKK...
..KVVVVKDDDK....
..KvvvKDDYDDK...
.KSVVVKDDDDDKKK.
..KvvvvKDDDKKSK.
...KKNNKKKKNNK..
"""),
  # Grey tabby in a mustard scarf, napping with a ball of yarn.
  "cat": ({"G": "#9aa3c0", "g": "#7a82a0", "e": "#f2a0a8", "n": "#f28a8a", "W": "#f2eef8", "R": "#e0a03a", "r": "#f2d27a", "Y": "#f28aa0"}, """
................
..KK.......KK...
..KGK.....KGK...
..KGeKKKKKeGK...
..KGGGGgGGGGK...
.KGGgGGGGGgGGK..
.KGGGGGGGGGGGK..
.KGKKGGGGGKKGK..
.KGcGGGnGGGcGK..
.KGGGGKGKGGGGK..
..KGGGGGGGGGK...
..KRRRRRRRRRK...
.KGRRrRRRRRRGK..
.KGGWWWWWWGGGKYK
..KGWWWWWWGGKYYK
..KKKKKKKKKKKKK."""),
  # Fox in a green scarf, bushy white-tipped tail.
  "fox": ({"O": "#e8833a", "d": "#8a4a2a", "W": "#fbeedd", "n": K, "G": "#4caf50", "g": "#3a8a3e"}, """
................
.KK.........KK..
.KOK.......KOK..
.KOdK.....KdOK..
.KOOKKKKKKKOOK..
.KOOOOOOOOOOOK..
KOOOOOOOOOOOOOK.
KOOKOOOOOOOKOOK.
KWWcOOOOOOOcWWK.
.KWWWWWnWWWWWK..
..KWWWWWWWWWK...
...KKGGGGGKK....
..KOGGgGGGGOK...
.KOOOWWWWOOOKOOK
.KOOWWWWWWOOKOWK
..KKKKKKKKKKKKK."""),
  # Bunny in a blue knit sweater, hugging a carrot.
  "bunny": ({"W": "#f4ecf0", "e": "#f2a0a8", "n": "#f28a8a", "V": "#8ab4f0", "v": "#6a94d0", "C": "#f08a3a", "G": "#7fc060"}, """
...KK.....KK....
..KWeK...KeWK...
..KWeK...KeWK...
..KWeK...KeWK...
...KWKKKKKWK....
..KWWWWWWWWWK...
.KWWWWWWWWWWWK..
.KWWKWWWWWKWWK..
.KWcWWWnWWWcWK..
.KWWWWKWKWWWWK..
..KWWWWWWWWWK...
..KVVVVVVVVVKGK.
.KWVVvVVvVVKCCK.
.KWVVVVVVVKCCK..
..KVVvVVvVVKCK..
..KKKKKKKKKKKK.."""),
  # Little scholar owl with big eyes, reading a red book.
  "owl": ({"B": "#8a5a3a", "W": "#fbeedd", "F": "#e8c89a", "f": "#c8a070", "Y": "#f2b34a", "R": "#c8504a", "r": "#f2e6d0"}, """
................
..KK.......KK...
..KBK.....KBK...
..KBBKKKKKBBK...
.KBBBBBBBBBBBK..
.KBWWWBBBWWWBK..
KBWWKWWBWWKWWBK.
KBWWWWWBWWWWWBK.
KBBWWWBYBWWWBBK.
.KBBBBBYBBBBBK..
.KBFFFFFFFFFBK..
KBBFfFFfFFfFBBK.
KBKFFFFFFFFFKBK.
KBBKRRRRRRRKBBK.
.KBKRrrrrrRKBK..
..KYYKKKKKYYK..."""),
  # Frog in a yellow raincoat, big happy grin.
  "frog": ({"G": "#7fc060", "W": "#f4f4ea", "Y": "#f2c23a", "y": "#d8a428"}, """
................
..KKKK...KKKK...
.KWWWWK.KWWWWK..
.KWKKWKKKWKKWK..
.KGWWGGGGGWWGK..
KGGGGGGGGGGGGGK.
KGGGGGGGGGGGGGK.
KGcGGGGGGGGGcGK.
KGGKGGGGGGGKGGK.
.KGGKKKKKKKGGK..
..KGGGGGGGGGK...
..KYYYYYYYYYK...
.KGYYyYKYyYYGK..
.KGYYYYYYYYYGK..
..KYYYYKYYYYK...
..KGGKK.KKGGK..."""),
  # Brown bear in a red scarf, holding a honey pot.
  "bear": ({"B": "#9a6a44", "b": "#c8946a", "M": "#e8c8a0", "R": "#c8504a", "r": "#f2d2a0", "H": "#f2b34a", "h": "#d88a2a"}, """
................
.KKK.......KKK..
.KBbK.....KbBK..
.KBBKKKKKKKBBK..
.KBBBBBBBBBBBK..
KBBBBBBBBBBBBBK.
KBBKBBBBBBBKBBK.
KBcBBMMMMMBBcBK.
KBBBBMMKMMBBBBK.
.KBBBMKMKMBBBK..
..KBBBMMMBBBK...
..KRRRRRRRRRK...
.KBRrRRRRRrRBK..
.KBBKHHHHHKBBK..
..KBKHhHHHKBK...
..KKKKKKKKKKK..."""),
  # Raccoon in a teal hoodie, sneaking a chocolate-chip cookie.
  "raccoon": ({"G": "#9a9aa8", "W": "#f2eef8", "D": "#4a4a58", "n": K, "T": "#5fb3a8", "C": "#c8864a", "h": "#5a3a22"}, """
................
..KK.......KK...
..KGK.....KGK...
..KGGKKKKKGGK...
.KGGGGGGGGGGGK..
.KWWGGGGGGGWWK..
KWDDDDWWWDDDDWK.
KWDWDDWWWDDWDWK.
KWWDDWWnWWDDWWK.
.KWcWWWWWWWcWK..
..KWWWWWWWWWK...
..KTTTTTTTTTKKK.
.KGTTTTTTTTKCCK.
.KGTTTTTTTKChCK.
..KTTTTTTTTKCCK.
..KKKKKKKKKKKK.."""),
  # Christmas pack.
  "santa": ({"W": "#f4f6fb", "R": "#d8504a", "B": "#3b2433", "Y": "#f2c23a"}, """
..........WW....
........KKWWK...
......KKRRKK....
....KKRRRRRK....
...KRRRRRRRRK...
..KWWWWWWWWWWK..
..KSSSSSSSSSSK..
..KSKSSSSSSKSK..
..KcSSSppSSScK..
..KWWWWWWWWWWK..
.KWWWWWWWWWWWWK.
.KRKWWWWWWWWKRK.
.KSRKWWWWWWKRSK.
..KRRRRRRRRRRK..
..KBBBBYYBBBBK..
..KKKK....KKKK.."""),
  "elf": ({"G": "#4caf50", "R": "#d8504a", "Y": "#f2c23a"}, """
................
..........KK....
.........KYYK...
........KGGK....
......KKGGGK....
....KKGGGGGGK...
...KGGGGGGGGGK..
..KRRRRRRRRRRK..
KSKSSSSSSSSSSKSK
.KSSKSSSSSSKSSK.
..KcSSSppSSScK..
...KKKSSSSKKK...
..KGGGRRRRGGGK..
.KSKGGGYYGGGKSK.
..KGGGGGGGGGGK..
..KRRKK..KKRRK.."""),
  "reindeer": ({"A": "#c8a070", "B": "#9a6a44", "M": "#e8c8a0", "R": "#ff5e6c", "G": "#4caf50", "g": "#f4f6fb"}, """
.KK.KK....KK.KK.
.KAKAK....KAKAK.
..KAAK....KAAK..
...KAKKKKKKAK...
..KBBBBBBBBBBK..
.KBBBBBBBBBBBBK.
.KBBKBBBBBBKBBK.
.KBcBBMMMMBBcBK.
.KBBBMMRRMMBBBK.
..KBBMMRRMMBBK..
...KBBMMMMBBK...
..KGGGGGGGGGGK..
.KBGgGGGGGGgGBK.
.KBBBBBBBBBBBBK.
..KBBKKKKKKBBK..
..KKK......KKK.."""),
  "snowman": ({"W": "#f4f6fb", "w": "#c8d2e8", "R": "#d8504a", "r": "#f2a0a8", "O": "#f08a3a", "G": "#4caf50", "g": "#2e6a3a"}, """
.......WW.......
.....KKWWKK.....
....KRRRRRRK....
...KRRrRRrRRK...
...KrrrrrrrrK...
..KWWWWWWWWWWK..
..KWWKWWWWKWWK..
..KWcWWOOWWcWK..
..KWWWWWOOWWWK..
...KWWKKKKWWK...
..KGGGGGGGGGGK..
.KWWGgGWWWWWWWK.
KWWWWGGWKWWWWWWK
KwWWWWWWWWWWWWwK
KwWWWWWWKWWWWWwK
.KKKKKKKKKKKKKK."""),
  "gingerbread": ({"D": "#c8864a", "W": "#f8f4ee", "R": "#d8504a", "G": "#4caf50"}, """
................
.....KKKKKK.....
....KDDDDDDK....
...KDDDDDDDDK...
...KDKDDDDKDK...
...KDcDDDDcDK...
...KDDWWWWDDK...
....KDDDDDDK....
..KKKDDDDDDKKK..
.KDWDDDDRDDDWDK.
.KDDKDDDDDDKDDK.
..KK.KDDGDDK.KK.
.....KDDDDDK....
....KDDDRDDDK...
...KDWDKKKDWDK..
...KKKK...KKKK.."""),
}
# Which characters belong to the festive pack (mirrors PACKS in main.js), so the README
# images show them on the `-xmas` scenes.
XMAS = ["santa", "elf", "reindeer", "snowman", "gingerbread"]
OUTDOOR = {"dusk", "grove"}

def festive(name):  # a scene's Christmas version: a garland of lights; snow outdoors
    rects = list(SCENES[name])
    rects += [(0, 0, 24, 1, "#2e6a3a")] + [(x, 1, 1, 1, ["#ff5e6c", "#f2c23a", "#8ab4f0"][x // 3 % 3]) for x in range(1, 24, 3)]
    if name in OUTDOOR:
        rects += [(x, y, 1, 1, "#f4f6fb") for x, y in [(2, 4), (7, 3), (20, 5), (15, 3), (1, 11), (22, 10), (11, 5)]]
        rects += [(0, 20, 24, 1, "#eef2fa"), (3, 21, 2, 1, "#eef2fa"), (12, 21, 3, 1, "#eef2fa"), (19, 21, 2, 1, "#eef2fa")]
    return rects

def rect(x, y, w, h, c, a=None):
    op = f' fill-opacity="{a}"' if a is not None else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"{op}/>'

def svg(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="96" height="96" shape-rendering="crispEdges">{body}</svg>\n'

def scene_body(name):  # "den", or "den-xmas" for its festive version
    rects = festive(name[:-5]) if name.endswith("-xmas") else SCENES[name]
    return "".join(rect(*r) for r in rects)

def char_body(name, ox=4, oy=4):
    pal, art = CHARS[name]
    pal = {"K": K, "S": SKIN, "p": NOSE, "c": BLUSH, **pal}
    rows = [r for r in art.split("\n") if r]
    assert len(rows) == 16 and all(len(r) <= 16 for r in rows), (name, len(rows))
    return "".join(rect(ox + x, oy + y, 1, 1, pal[c]) for y, row in enumerate(rows) for x, c in enumerate(row) if c != ".")

def write(kind, name, body):
    os.makedirs(f"{HERE}/{kind}", exist_ok=True)
    open(f"{HERE}/{kind}/{name}.svg", "w").write(svg(body))

# A pixel question mark (5x8, drawn at 2x) for characters not drawn yet.
SOON = [".###.", "#...#", "....#", "...#.", "..#..", "..#..", ".....", "..#.."]

def soon_body():
    mark = "".join(rect(7 + 2 * x, 4 + 2 * y, 2, 2, "#f2e6d0") for y, row in enumerate(SOON) for x, c in enumerate(row) if c == "#")
    return scene_body("dusk") + rect(0, 0, 24, 24, "#10131b", 0.6) + mark

def sheet(path, chars, scenes):
    cells = [f'<g transform="translate({i * 25},{j * 25})">{scene_body(s)}{char_body(c)}</g>'
             for j, s in enumerate(scenes) for i, c in enumerate(chars)]
    w, h = len(chars) * 25, len(scenes) * 25
    open(path, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w * 5}" height="{h * 5}" shape-rendering="crispEdges">{"".join(cells)}</svg>\n')

def docs(out):
    os.makedirs(f"{out}/chars", exist_ok=True)
    cozy = [c for c in CHARS if c not in XMAS]
    plain, xmas = list(SCENES), [f"{s}-xmas" for s in SCENES]
    for i, c in enumerate(cozy):  # each char on the next scene in turn
        open(f"{out}/chars/{c}.svg", "w").write(svg(scene_body(plain[i % len(plain)]) + char_body(c)))
    for i, c in enumerate(XMAS):
        open(f"{out}/chars/{c}.svg", "w").write(svg(scene_body(xmas[i % len(xmas)]) + char_body(c)))
    open(f"{out}/chars/soon.svg", "w").write(svg(soon_body()))
    sheet(f"{out}/sprites.svg", cozy, plain)
    sheet(f"{out}/sprites-christmas.svg", XMAS, xmas)

if __name__ == "__main__":
    for s in SCENES: write("scenes", s, scene_body(s)); write("scenes", f"{s}-xmas", scene_body(f"{s}-xmas"))
    for c in CHARS: write("chars", c, char_body(c))
    if len(sys.argv) > 1: docs(sys.argv[1])
    print(sorted(SCENES), sorted(CHARS))
