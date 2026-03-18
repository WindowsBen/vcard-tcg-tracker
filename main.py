#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║         VCard TCG  ·  Pull Tracker  ·  main.py          ║
╚══════════════════════════════════════════════════════════╝
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sqlite3, os
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

APP_TITLE      = "VCard TCG  ·  Pull Tracker"
APP_W, APP_H   = 1080, 720
CARDS_PER_PACK = 10
PACKS_PER_BOX  = 24
TOPPERS_PER_SET = {
    "Rising Stars":    2,
    "Awakened Worlds": 1,
    "Divine Chaos":    2,
}
DB_FILE        = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vcard_tracker.db")
SETS           = ["Rising Stars", "Awakened Worlds", "Divine Chaos"]

RARITIES = [
    "Mascot", "Mascot Holo",
    "World", "World Holo",
    "Support", "Support Holo", "Secret Rare",
    "8", "8 Holo",
    "9", "9 Holo",
    "10",
    "God Rare",
    "Box Topper",
]

RARITY_COLORS = {
    "Mascot":       "#9e9e9e",
    "Mascot Holo":  "#d4d4d4",
    "World":        "#42a5f5",
    "World Holo":   "#90caf9",
    "Support":      "#66bb6a",
    "Support Holo": "#a5d6a7",
    "Secret Rare":  "#00e5ff",
    "8":            "#ff7043",
    "8 Holo":       "#ffab91",
    "9":            "#ef5350",
    "9 Holo":       "#ef9a9a",
    "10":           "#ffd54f",
    "God Rare":     "#e040fb",
    "Box Topper":   "#ff80ab",
}

RARITY_RANK = {
    "Mascot": 0,      "Mascot Holo": 1,
    "World": 2,       "World Holo": 3,
    "Support": 4,     "Support Holo": 5,  "Secret Rare": 5,
    "8": 6,           "8 Holo": 7,
    "9": 8,           "9 Holo": 9,
    "10": 10,
    "God Rare": 11,
    "Box Topper": 12,
}

NOTABLE_RANK = 8

# ═══════════════════════════════════════════════════════════════════════════════
#  CARD DATABASE
# ═══════════════════════════════════════════════════════════════════════════════

def _build_aw():
    cards = []
    aw_89 = [
        "COTTONTAILVA","CYYU (SHARK MODE)","FREAM","CAPTAIN HANNAH","LAIMU",
        "POSEIDON","RAINHOE","SPITE","YENKO","AKUMI",
        "YUZU, LADY OF THE LAKE","DEME","FEFE","HEAVENLY","KOKONUTS",
        "OBKATIEKAT","EGG","SHYLILY","SQUCHAN","TOTLESS",
        "GHOST TRICKYWI","SPRING BAO","FROGGYLOCH","JUNIPER ACTIAS","GARDEN KEEPER SKY",
        "MILKY","ONIKANZEI","PORCELAINMAID","SANSIN","GARDENER SHOTO",
        "SUKO","TOMA","CAMPFIRE BUFFPUP","CAMILA","CHACHAYOURVMOM",
        "GAMBLER DYA RIKKU","ELLY","IKUMI","LUCY PYRE","NANOLESS",
        "SUN GODDESS SILVERVALE","VEI","VEXORIA THE SUN EATER","AICANDII","AMALEE",
        "ARIELLE","CROWKI","EIN","LORD AETHELSTAN","NUMI 4.0",
        "NYANNERS","SARUEI","VIENNA",
    ]
    for name in aw_89:
        for r in ("8", "8 Holo", "9", "9 Holo"):
            cards.append((name, r))
    aw_10 = [
        "COTTONTAILVA","CYYU (SHARK MODE)","FREAM","CAPTAIN HANNAH","LAIMU",
        "POSEIDON","RAINHOE","SPITE","YENKO","YOCLESH",
        "YUZU, LADY OF THE LAKE","DEME","FEFE","HEAVENLY","KOKONUTS",
        "OBKATIEKAT","EGG","SHYLILY","SQUCHAN","KINETIC TOTLESS",
        "ALIEN DRAGON NEPHASIS","THE BAOBERRY","FROGGYLOCH","JUNIPER, USURPER OF LUNE","GARDEN KEEPER SKY",
        "MILKY","ONIKANZEI","PORCELAINMAID","SANSIN","SAKURA SHOTO",
        "SUKO","TOMA","FERAL BUFFPUP","CAMILA","CHACHAYOURVMOM",
        "GAMBLER DYA RIKKU","ELLY","IKUMI","LUCY PYRE","NANOLESS",
        "SUN GODDESS SILVERVALE","VEI","VEXORIA THE SUN EATER","AICANDII","MAFIA-BOSS AMALEE",
        "ARIELLE","DOKIBIRD","EIN","LORD AETHELSTAN","THE NUMIVERSE",
        "NYANNERS","SARUEI","PINK VIENNA",
    ]
    for name in aw_10:
        cards.append((name, "10"))
    aw_mascots = [
        "FLUFFER","B (SHARK MODE)","SPIKE","FIRST MATE OLLIE","LIMON",
        "IKAMARU","POOL PARTY DROID","RAWR XD","BUNNERD","ONIFAN",
        "KOGA","BOOMI","FEET FEET","FREAKBOT","AXEL",
        "KATTENS","YOLK","SPOOF","POKATTO","SHOCKED MIMI",
        "TRICKSTER","BAOBBLE BUDDY","FROGLODYTES","BABY MOTH","HAZE",
        "ASTRO","NOBU","BLOCKHEADS","FOREST OLLIE","GUILDIE",
        "SUKOPATH","TOMANIAC","BURNT PUP","CIMP","CUTIE PIE",
        "GIGA GAMBLIN","BANDIT & ACE","GUUMI","DARK DEMONITE","YAKIMONO",
        "PETAL PALS","GARY","CLEO","LABCHAT","SCUFFLING",
        "GLOWSTICK","D.A.D (DOKI AMBER DOGE)","BRO","METAL BRADLEY","BENSON",
        "GORO","CERBERUS","NOODLE",
    ]
    for name in aw_mascots:
        for r in ("Mascot", "Mascot Holo"):
            cards.append((name, r))
    aw_supports = [
        "PRESS YOUR LUCK","PYRO BADDIE","BIBIMBAP","BRICK BY BRICK","CYANIDE-CHAN'S REVENGE",
        "SOAKED IN HAPPINESS","CATATONIC","WORLD PREMIERE","FOURPLAY","UNDERWORLD",
        "PRETTY PRIVILEGE","HOT POT","OUT TO PASTURE","MASSIVE LEGEND","TIT FOR TAT",
        "ACADEMIC ADVISOR","RESTRAINING ORDER","CRITICAL CONDITION","GG EZ","LET'S PLAY",
        "GASSING UP","SPLASH DAMAGE","SWAGGER'S HELMET",
    ]
    for name in aw_supports:
        for r in ("Support", "Support Holo", "Secret Rare"):
            cards.append((name, r))
    aw_worlds = [
        "SHIMMERING DEPTHS","CRYSTAL COVE","COSMIC LIGHTHOUSE","POWER GRID","SACRED GROVE",
        "SPRING PATH","CRIMSON FESTIVAL","STROMBOLIAN CRADLE","SERVICE CORRIDOR","VAULTED TREASURY",
        "GRAND QUARTER","VELVET CONCORD","SPORELIT CAVERN","SWEET DOUGHMAIN","KONBINI",
    ]
    for name in aw_worlds:
        for r in ("World", "World Holo"):
            cards.append((name, r))
    for name in aw_10 + aw_supports:
        cards.append((f"GOD {name}", "God Rare"))
    aw_toppers = [
        "Vexoria","Porcelainmaid","Suko","Sansin","Bao","Silvervale","FeFe",
        "Obkatiekat","Nanoless","Limealicious","Skyaboveme","Squchan","Yuzu","Nyanners",
        "CottontailVA","Camila","AICandii","Akuma Nihmune","FroggyLoch","Shoto",
        "Rainhoe","Arielle","Deme","Onikanzei","AmaLee","Fream","Yenko",
        "Saruei","Shylily","Yoclesh","Hannah Hyrule","Milky","Yuniper Actias",
        "Spite","Trickywi","Heavenly Father","Dokibird","Dya Rikku","Poseidon",
        "Kokonuts","Vienna","Toma","Overezeggs","FoxyReine","Lord Aethelstan",
        "CyYu","Buffpup","Elly","Vei","Ikumi","ChaChaYourVmom","Lucy Pyre",
        "Totless","MeatCanyon","BBno$","Cyanide & Happiness","Maxmoefoe","JSchlatt",
        "Clooless","Swaggersouls","TheRussianBadger","MoistCr1TiKaL","Ray","DEMONDICE",
        "SMii7Y","CaseOh","Nagzz","FlorkOfCows","TheAnimeMen","Meru","CDawG",
        "Baddie","PaymoneyWubby","Bricky","Trashmob",
    ]
    for name in aw_toppers:
        cards.append((name, "Box Topper"))
    return cards


def _build_rs():
    cards = []
    rs_89 = [
        "MONARCH","BAO THE WHALE","EBIKO","FOXYREINE","FROGGYLOCH",
        "MEGALODONVT","NYANNERS","SHYLILY","BUFFPUP","COQUI",
        "DOKI'S TRUE FORM","LAIMU","MEAT","SILVERVALE","TOB",
        "FARMER VIENNA","FEFE","LORD AETHELSTAN","UNIVERSITY NUMI","PUNKALOPI",
        "AKUMI","PIRATE TRICKYWI","SINDER","YUZU","CIDEMIKO",
        "COTTONTAILVA","CYYU","YUNIPER ACTIAS","LUCY PYRE","QUINN BENET",
        "RAINHOE","SKY","SHOTO","CAMILA","DYA RIKKU",
        "FREAM","HEAVENLY FATHER","LAYNA LAZAR","NANOLESS","SANSIN",
        "TOTLESS","VEI",
    ]
    for name in rs_89:
        for r in ("8", "8 Holo", "9", "9 Holo"):
            cards.append((name, r))
    rs_10 = [
        "MULTIVERSE MONARCH","BAO THE WHALE","EBIKO","FOXYREINE","FROGGYLOCH",
        "MEGALODONVT","NYANNERS","SHYLILY","BUFFPUP","COQUI",
        "DOKIBIRD","LAIMU","MEAT","SILVERVALE","TOB",
        "FARMER VIENNA","FEFE","LORD AETHELSTAN","NIHMUNE","PUNKALOPI",
        "AKUMI","PHARAOH NEPHASIS","SINDER","YUZU","CIDEMIKO",
        "COTTONTAILVA","CYYU","YUNIPER ACTIAS","LUCY PYRE","QUINN BENET",
        "RAINHOE","SKY","SHOTO","CAMILA","DYANTE",
        "FREAM","HEAVENLY FATHER","LAYNA LAZAR","NANOLESS","SANSIN",
        "TOTLESS","VEI",
    ]
    for name in rs_10:
        cards.append((name, "10"))
    rs_mascots = [
        "MONARCH'S MESSENGER CLONE","PESTONINI","GRUB","BRO","FROGLODYTE",
        "SASHIMI","GORO","ORCA PUP","PUP","TAD & CANNOLI",
        "DRAGOONS","LIMON","MEATHEAD","PETAL PALS","BATSARD CAT",
        "FARMER COSMATE","RANCID","BRADLES","BENSON","CHABBIT",
        "SMOLCCI","TRICKY","PYRO PUP","LAMPCHAMP","POTAT",
        "FLUFFER","B","BABY MOTH","DEMONITE","ELECTROBYTES",
        "DROID","HAZE","GUILDIE","CIMP","CHATBLIN",
        "SPIKE","EVILBOT","CHIBI LAYNA","NANOMONO","OLLIE",
        "MIMI","TENKI",
    ]
    for name in rs_mascots:
        for r in ("Mascot", "Mascot Holo"):
            cards.append((name, r))
    rs_shields_guardians = [
        "FIRE SHIELD","WATER SHIELD","GRASS SHIELD","ELECTRIC SHIELD","PLATINUM SHIELD",
        "FIRE GUARDIAN","WATER GUARDIAN","GRASS GUARDIAN","ELECTRIC GUARDIAN","PLATINUM GUARDIAN",
    ]
    for name in rs_shields_guardians:
        for r in ("Support", "Support Holo"):
            cards.append((name, r))
    rs_supports = [
        "HARPOON","EXPOSED","CYANIDE-CHAN","HAPPINESS-CHAN","SNACK CAT",
        "WORK-LIFE BALANCE","WHITE KNIGHT","BUTCHER'S BLADE","DOPPELGANGER","DOUBLE DOWN",
        "BATTLE CRY","REAPER",
    ]
    for name in rs_supports:
        for r in ("Support", "Support Holo", "Secret Rare"):
            cards.append((name, r))
    for name in rs_10 + rs_supports:
        cards.append((f"GOD {name}", "God Rare"))
    rs_toppers = [
        "Nihmune","Totless","Fream","Fefe","CodeMiko","Layna Lazar","FroggyLoch",
        "CyYu","Shylily","Nyanners","Nanoless","Pharaoh Nephasis","Vei","Lord Aethelstan",
        "Ebiko","Buffpup","Lucy Pyre","Silvervale","Camila","Quinn Benet",
        "Akumi","MegalodonVT","Coqui","Yuzu","Bao The Whale","Sky","FoxyReine",
        "CottontailVA","Sinder","Shoto","Juniper Actias","Dokibird","Punkalopi",
        "Laimu","Rainhoe","Sansin","Multiverse Monarch","Farmer Vienna","Tob",
        "Heavenly Father","Meat","Dyante",
    ]
    for name in rs_toppers:
        cards.append((name, "Box Topper"))
    return cards


def _build_dc():
    cards = []
    dc_89 = [
        "AQUWA","BIKINI IKUMI","MOMOTE","SUTO","WET FEFE",
        "ALLUUX","HEAVENLY","KAIRYU CROCODILE","ROSEDOODLE","SYKKUNO",
        "FREAM","FROGGYLOCH","K9KURO","SMUGALANA","SPITE",
        "GX AURA","ARIELLE","BAO THE WHALE","IDOL YENKO","RAIJIN YOCCI",
        "ZENTREYA","DIAMOND HEIST ELLY","GEEGA","GRIMMI","SPACE INVADER JUNIPER",
        "TOB","CAMILA","CHAOS QUEEN TRICKYWI","CLUMSY TOTLESS","COTTONTAILVA",
        "CRIMSON BLOOM","DOKIBIRD","EVIL BUFFPUP","GIWI","MICHI MOCHIEVEE",
        "NIHMUNE","NYANNERS","RAINHOE","SAIREN","SARUEI",
        "SHOTO","SHYLILY","VEXORIA THE SUN EATER","AMALEE","CHIBIDOKI",
        "CYFY","DREAMER VIENNA","GOLDEN HOUR DYARIKKU","LAIMU","LORD AETHELSTAN",
        "LUCIEL","MAIDEN IN HEAVEN","MILKY","NYANNIE","REINE OF THE SACRED LIGHT",
        "SAKURA DRAGON SILVERVALE","SHIABUN","SQUCHAN","VEI","YUZU",
    ]
    for name in dc_89:
        for r in ("8", "8 Holo", "9", "9 Holo"):
            cards.append((name, r))
    dc_10 = [
        "AQUWA","BIKINI IKUMI","MOMOTE","SUTO","WET FEFE",
        "ALLUUX","HEAVENLY","KAIRYU CROCODILE","ROSEDOODLE","SYKKUNO",
        "FREAM","FROGGYLOCH","K9KURO","SMUGALANA","SPITE",
        "GX AURA","ARIELLE","BAO THE WHALE","IDOL YENKO","RAIJIN YOCCI",
        "ZENTREYA","DIAMOND HEIST ELLY","GEEGA","GRIMMI","SPACE INVADER JUNIPER",
        "TOB","CAMILA","CHAOS QUEEN TRICKYWI","CLUMSY TOTLESS","COTTONTAILVA",
        "CRIMSON BLOOM","DOKIBIRD","EVIL BUFFPUP","GIWI","MICHI MOCHIEVEE",
        "NIHMUNE","NYANNERS","RAINHOE","SAIREN","SARUEI",
        "SHOTO","SHYLILY","VEXORIA THE SUN EATER","AMALEE","CHIBIDOKI",
        "CYFY","DREAMER VIENNA","GOLDEN HOUR DYARIKKU","LAIMU","LORD AETHELSTAN",
        "LUCIEL","MAIDEN IN HEAVEN","MILKY","NYANNIE","REINE OF THE SACRED LIGHT",
        "SAKURA DRAGON SILVERVALE","SHIABUN","SQUCHAN","VEI","YUZU",
    ]
    for name in dc_10:
        cards.append((name, "10"))
    dc_mascots = [
        "ATLAS","ABYSSAL GUUMI","WOODCHAT","TONIE","RANCID & GLITCHY",
        "TOANY","CHILLBOT","LITTLE CROC","BEEPU","SYKKCAT",
        "SPIKE","FROGLODYTES","WHISPER","SMUGGLER","RAWR XD",
        "RAMBIT","GLOWSTICKS","BAOBBLE BUDDY","BUNNERD","ONIFAN",
        "GECKOS","BANDIT & ACE","BORIS","GASPAR & SKELTER","UNIDENTIFIED FLYING MOTH",
        "BATSARD CAT","CIMP","TRICKYWI'S GHOSTS","CLUMSY MIMI","FLUFFER",
        "h4ND-0325","JOVIAL DOKIMENT","EVIL PUP","WIGGLER","JARED",
        "BENSON","GORO","MEGACORP DROID","SQUISHIES","GZ-MG0 HARBINGER",
        "THE GUILDIES","SPOOF","CLEO","SCUFFLING","CHAT",
        "BEE","DREAMER COSMATE","GOLDEN BLIN","LIMON","CHERUB BRADLEY",
        "HEAVENITE","MONOWAY TO HEAVEN","ASTRO","GOONIE","FOXCALIBUR",
        "DRAGON PALS","BUN","POKATTOS & L","GARY","LAMPCHAMPS",
    ]
    for name in dc_mascots:
        for r in ("Mascot", "Mascot Holo"):
            cards.append((name, r))
    dc_supports = [
        "SHIFT D","TWO FACED","THE PASS","PLAYBACK ERROR","LUCKY PULL",
        "SINFUL SEARCH","LOOKING (RESPECTFULLY)","STORYBOARD","DREAMSCAPE","SECRET RECIPE",
        "CHAOS GUARDIAN","DIVINE GUARDIAN","FOR THE ALLIANCE","NARRATOR","NEAPOLITAN",
        "FROUGE AMBUSH","MEDICINAL HERBS","GREEN GANG","LESSON LEARNED","BARD'S FAVOR",
    ]
    for name in dc_supports:
        for r in ("Support", "Support Holo", "Secret Rare"):
            cards.append((name, r))
    dc_worlds = [
        "JADE REFLECTION","NEON CLAWCADE","MORNING WOOD","CHARRED DOMINION","CHESTPLATE CHAMBER",
        "HOLY GRAIL","GUILDED PARADOX","STREAM ROOM","GOON CAVE","A KITCHEN",
        "SHITPOSTERS HQ",
    ]
    for name in dc_worlds:
        for r in ("World", "World Holo"):
            cards.append((name, r))
    for name in dc_10 + dc_supports:
        cards.append((f"GOD {name}", "God Rare"))
    dc_toppers = [
        "Shift D","Two Faced","The Pass","Playback Error","Lucky Pull",
        "Sinful Search","Looking (Respectfully)","Storyboard","Dreamscape","Secret Recipe",
        "Chaos Guardian","Divine Guardian","For the Alliance","Narrator","Neapolitan",
        "Frouge Ambush","Medicinal Herbs","Green Gang","Lesson Learned","Bard's Favor",
        "Zentreya","Yuzu","Raijin Yocci","Idol Yenko","Dreamer Vienna",
        "Vexoria The Sun Eater","Vei","Chaos Queen Trickywi","Clumsy Totless","Tob",
        "Sykkuno","Suto","SquChan","Spite","SmugAlana",
        "Sakura Dragon Silvervale","Shylily","Shoto","ShiaBun","Saruei",
        "Saiiren","Rosedoodle","Rainhoe","Nyannie","Nyanners",
        "Nihmune","Maiden in Heaven","Momote","Milky","Michi Mochievee",
        "Luciel","Lord Aethelstan","Crimson Bloom","Laimu","K9KURO",
        "Space Invader Juniper","Bikini Ikumi","Heavenly","Grimmi","Giwi",
        "Geega","FroggyLoch","Fream","Reine of the Sacred Light","Wet FeFe",
        "Diamond Heist Elly","Golden Hour DyaRikku","Dokibird","CyFy","Kairyu Crocodile",
        "CottontailVA","Chibidoki","Camila","Evil Buffpup","Bao The Whale",
        "GX Aura","Arielle","Aquwa","AmaLee","Alluux",
    ]
    for name in dc_toppers:
        cards.append((name, "Box Topper"))
    return cards


CARD_DB: dict = {
    "Awakened Worlds": _build_aw(),
    "Rising Stars":    _build_rs(),
    "Divine Chaos":    _build_dc(),
}

# ═══════════════════════════════════════════════════════════════════════════════
#  SEARCH
# ═══════════════════════════════════════════════════════════════════════════════

def search_cards(query: str, cards: list, limit: int = 8,
                 rarity_filter=None) -> list:
    q = query.strip().lower()
    if not q:
        return []
    tokens = q.split()
    pool   = [(n, r) for n, r in cards if rarity_filter is None or r == rarity_filter]
    hits   = []
    for name, rarity in pool:
        combined = f"{name.lower()} {rarity.lower()}"
        if all(t in combined for t in tokens):
            hits.append((len(combined), name, rarity))
    hits.sort(key=lambda x: x[0])
    return [(n, r) for _, n, r in hits[:limit]]

# ═══════════════════════════════════════════════════════════════════════════════
#  DATABASE
# ═══════════════════════════════════════════════════════════════════════════════

def init_db():
    con = sqlite3.connect(DB_FILE)
    con.executescript("""
        CREATE TABLE IF NOT EXISTS boxes (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            set_name       TEXT NOT NULL,
            opened_at      TEXT NOT NULL,
            topper_name    TEXT NOT NULL,
            topper_rarity  TEXT NOT NULL,
            topper2_name   TEXT,
            topper2_rarity TEXT
        );
        CREATE TABLE IF NOT EXISTS packs (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            box_id    INTEGER NOT NULL,
            set_name  TEXT NOT NULL,
            opened_at TEXT NOT NULL,
            FOREIGN KEY (box_id) REFERENCES boxes(id)
        );
        CREATE TABLE IF NOT EXISTS pulls (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            pack_id   INTEGER NOT NULL,
            card_name TEXT NOT NULL,
            rarity    TEXT NOT NULL,
            set_name  TEXT NOT NULL,
            pulled_at TEXT NOT NULL,
            FOREIGN KEY (pack_id) REFERENCES packs(id)
        );
    """)
    con.commit(); con.close()

def _con():
    return sqlite3.connect(DB_FILE)

def db_new_box(set_name, topper_name, topper_rarity, topper2_name=None, topper2_rarity=None):
    con = _con()
    cur = con.execute(
        "INSERT INTO boxes (set_name,opened_at,topper_name,topper_rarity,topper2_name,topper2_rarity) VALUES (?,?,?,?,?,?)",
        (set_name, datetime.now().isoformat(), topper_name, topper_rarity, topper2_name, topper2_rarity))
    bid = cur.lastrowid; con.commit(); con.close(); return bid

def db_new_pack(box_id, set_name):
    con = _con()
    cur = con.execute("INSERT INTO packs (box_id,set_name,opened_at) VALUES (?,?,?)",
                      (box_id, set_name, datetime.now().isoformat()))
    pid = cur.lastrowid; con.commit(); con.close(); return pid

def db_add_pull(pack_id, card_name, rarity, set_name):
    con = _con()
    con.execute("INSERT INTO pulls (pack_id,card_name,rarity,set_name,pulled_at) VALUES (?,?,?,?,?)",
                (pack_id, card_name, rarity, set_name, datetime.now().isoformat()))
    con.commit(); con.close()

def db_delete_pack(pack_id):
    con = _con()
    con.execute("DELETE FROM pulls WHERE pack_id=?", (pack_id,))
    con.execute("DELETE FROM packs  WHERE id=?",     (pack_id,))
    con.commit(); con.close()

def db_delete_box(box_id):
    con = _con()
    pack_ids = [r[0] for r in con.execute("SELECT id FROM packs WHERE box_id=?", (box_id,)).fetchall()]
    for pid in pack_ids:
        con.execute("DELETE FROM pulls WHERE pack_id=?", (pid,))
    con.execute("DELETE FROM packs WHERE box_id=?", (box_id,))
    con.execute("DELETE FROM boxes WHERE id=?",     (box_id,))
    con.commit(); con.close()

def db_get_boxes(set_filter=None):
    con  = _con()
    base = ("SELECT b.id, b.set_name, b.opened_at, b.topper_name, b.topper_rarity, "
            "b.topper2_name, b.topper2_rarity, COUNT(DISTINCT p.id) "
            "FROM boxes b LEFT JOIN packs p ON p.box_id=b.id")
    if set_filter and set_filter != "All Sets":
        rows = con.execute(base+" WHERE b.set_name=? GROUP BY b.id ORDER BY b.opened_at DESC",
                           (set_filter,)).fetchall()
    else:
        rows = con.execute(base+" GROUP BY b.id ORDER BY b.opened_at DESC").fetchall()
    con.close(); return rows

def db_get_box_packs(box_id):
    con  = _con()
    rows = con.execute(
        "SELECT p.id, p.opened_at, COUNT(pu.id) "
        "FROM packs p LEFT JOIN pulls pu ON pu.pack_id=p.id "
        "WHERE p.box_id=? GROUP BY p.id ORDER BY p.opened_at",
        (box_id,)).fetchall()
    con.close(); return rows

def db_get_pack_pulls(pack_id):
    con  = _con()
    rows = con.execute("SELECT card_name,rarity FROM pulls WHERE pack_id=? ORDER BY id",
                       (pack_id,)).fetchall()
    con.close(); return rows

def db_get_collection(set_filter=None):
    con  = _con()
    base = "SELECT card_name,rarity,set_name,COUNT(*) FROM pulls"
    grp  = " GROUP BY card_name,rarity,set_name"
    if set_filter and set_filter != "All Sets":
        rows = con.execute(base+" WHERE set_name=?"+grp, (set_filter,)).fetchall()
    else:
        rows = con.execute(base+grp).fetchall()
    con.close(); return rows

def db_get_stats(set_filter=None):
    con  = _con()
    filt = set_filter and set_filter != "All Sets"
    w    = " WHERE set_name=?" if filt else ""
    a    = (set_filter,) if filt else ()
    boxes  = con.execute("SELECT COUNT(*) FROM boxes"+w, a).fetchone()[0]
    packs  = con.execute("SELECT COUNT(*) FROM packs"+w, a).fetchone()[0]
    pulls  = con.execute("SELECT COUNT(*) FROM pulls"+w, a).fetchone()[0]
    rc     = dict(con.execute("SELECT rarity,COUNT(*) FROM pulls"+w+" GROUP BY rarity", a).fetchall())
    con.close(); return boxes, packs, pulls, rc

def db_count_box_packs(box_id):
    con = _con()
    n   = con.execute("SELECT COUNT(*) FROM packs WHERE box_id=?", (box_id,)).fetchone()[0]
    con.close(); return n

# ═══════════════════════════════════════════════════════════════════════════════
#  AUTOCOMPLETE ENTRY
# ═══════════════════════════════════════════════════════════════════════════════

class AutocompleteEntry(ctk.CTkFrame):
    def __init__(self, parent, get_cards_fn, on_select_fn,
                 placeholder="Type card name…", rarity_filter=None, keep_text=False, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self._get_cards     = get_cards_fn
        self._on_select     = on_select_fn
        self._rarity_filter = rarity_filter
        self._keep_text     = keep_text
        self._results       = []
        self._sel           = 0
        self._dropdown      = None
        self._dd_btns       = []

        self._entry = ctk.CTkEntry(self, placeholder_text=placeholder,
                                    height=44, font=ctk.CTkFont(size=14))
        self._entry.pack(fill="x")
        self._entry.bind("<KeyRelease>", self._on_key)
        self._entry.bind("<Return>",     self._confirm)
        self._entry.bind("<Up>",         self._nav_up)
        self._entry.bind("<Down>",       self._nav_down)
        self._entry.bind("<Escape>",     lambda _: self._hide())
        self._entry.bind("<FocusOut>",   lambda _: self.after(200, self._hide))

    def focus(self):                self._entry.focus_set()
    def clear(self):                self._entry.delete(0, "end"); self._hide()
    def set_rarity_filter(self, r): self._rarity_filter = r

    def _on_key(self, e):
        if e.keysym in ("Return","Up","Down","Escape","Tab",
                        "Shift_L","Shift_R","Control_L","Control_R","Alt_L","Alt_R"):
            return
        self._results = search_cards(self._entry.get(), self._get_cards(),
                                      limit=8, rarity_filter=self._rarity_filter)
        self._sel = 0
        self._show_dropdown()

    def _confirm(self, _=None):
        if self._results and self._entry.get().strip():
            n, r = self._results[max(0, self._sel)]
            self._hide()
            if self._keep_text:
                self._entry.delete(0, "end")
                self._entry.insert(0, f"{n}  [{r}]")
            else:
                self._entry.delete(0, "end")
            self._on_select(n, r)

    def _nav_up(self, _):
        if self._results:
            self._sel = max(0, self._sel - 1); self._highlight()

    def _nav_down(self, _):
        if self._results:
            self._sel = min(len(self._results)-1, self._sel + 1); self._highlight()

    def _show_dropdown(self):
        self._hide()
        if not self._results: return
        self._entry.update_idletasks()
        x  = self._entry.winfo_rootx()
        y  = self._entry.winfo_rooty() + self._entry.winfo_height() + 2
        w  = self._entry.winfo_width()
        h  = len(self._results) * 36
        dd = tk.Toplevel(self)
        dd.overrideredirect(True)
        dd.geometry(f"{w}x{h}+{x}+{y}")
        dd.configure(bg="#161616")
        dd.attributes("-topmost", True)
        self._dropdown = dd; self._dd_btns = []
        for name, rarity in self._results:
            color = RARITY_COLORS.get(rarity, "#888")
            btn   = tk.Button(dd, text=f"  ● {name}   [{rarity}]", anchor="w",
                              bg="#161616", fg="#dddddd", activebackground="#1e3a5f",
                              relief="flat", bd=0, padx=6, font=("Segoe UI", 11),
                              command=lambda n=name, r=rarity: self._select(n, r))
            btn.pack(fill="x", ipady=3)
            self._dd_btns.append((btn, color))
        self._highlight()

    def _highlight(self):
        for i, (btn, color) in enumerate(self._dd_btns):
            btn.configure(bg="#1e3a5f" if i==self._sel else "#161616",
                          fg=color      if i==self._sel else "#dddddd")

    def _select(self, name, rarity):
        self._hide()
        if self._keep_text:
            self._entry.delete(0, "end")
            self._entry.insert(0, f"{name}  [{rarity}]")
        else:
            self._entry.delete(0, "end")
        self._on_select(name, rarity)

    def _hide(self):
        if self._dropdown:
            try: self._dropdown.destroy()
            except: pass
        self._dropdown = None; self._dd_btns = []

# ═══════════════════════════════════════════════════════════════════════════════
#  BOX TOPPER DIALOG  (returns result via callback)
# ═══════════════════════════════════════════════════════════════════════════════

class BoxTopperDialog(ctk.CTkToplevel):
    """Shown when opening a new box. Supports 1 or 2 toppers depending on set."""

    def __init__(self, parent, set_name: str, on_confirm):
        super().__init__(parent)
        self._on_confirm  = on_confirm
        self._set_name    = set_name
        self._num_toppers = TOPPERS_PER_SET.get(set_name, 1)
        self._t1          = (None, None)
        self._t2          = (None, None)

        h = 290 if self._num_toppers == 2 else 210
        self.title("Open Box — Log Box Topper(s)")
        self.geometry(f"540x{h}")
        self.resizable(False, False)
        self.grab_set()
        self.attributes("-topmost", True)

        ctk.CTkLabel(self, text=f"Opening a box from  {set_name}",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(18, 4))
        ctk.CTkLabel(self, text="Select the Box Topper(s) before opening packs:",
                     text_color="#aaa", font=ctk.CTkFont(size=11)).pack(pady=(0, 10))

        # Topper 1
        ctk.CTkLabel(self, text="Box Topper 1:" if self._num_toppers == 2 else "Box Topper:",
                     font=ctk.CTkFont(size=12), anchor="w").pack(fill="x", padx=20)
        self._ac1 = AutocompleteEntry(
            self,
            get_cards_fn=lambda: CARD_DB.get(self._set_name, []),
            on_select_fn=self._selected1,
            placeholder="Search Box Topper…",
            rarity_filter="Box Topper",
            keep_text=True,
        )
        self._ac1.pack(fill="x", padx=20, pady=(2, 8))

        # Topper 2 (only for 2-topper sets)
        if self._num_toppers == 2:
            ctk.CTkLabel(self, text="Box Topper 2:",
                         font=ctk.CTkFont(size=12), anchor="w").pack(fill="x", padx=20)
            self._ac2 = AutocompleteEntry(
                self,
                get_cards_fn=lambda: CARD_DB.get(self._set_name, []),
                on_select_fn=self._selected2,
                placeholder="Search Box Topper…",
                rarity_filter="Box Topper",
                keep_text=True,
            )
            self._ac2.pack(fill="x", padx=20, pady=(2, 8))

        self._confirm_btn = ctk.CTkButton(
            self, text="Confirm & Open Box", height=38,
            state="disabled", command=self._confirm)
        self._confirm_btn.pack(padx=20, fill="x", pady=(4, 4))
        ctk.CTkButton(self, text="Cancel", fg_color="#444", hover_color="#666",
                      command=self._cancel, width=100).pack(pady=(2, 0))
        self.protocol("WM_DELETE_WINDOW", self._cancel)
        self.after(100, self._ac1.focus)

    def _selected1(self, name, rarity):
        self._t1 = (name, rarity)
        self._check_ready()

    def _selected2(self, name, rarity):
        self._t2 = (name, rarity)
        self._check_ready()

    def _check_ready(self):
        ready = self._t1[0] is not None
        if self._num_toppers == 2:
            ready = ready and self._t2[0] is not None
        self._confirm_btn.configure(state="normal" if ready else "disabled")

    def _confirm(self):
        self._on_confirm(self._t1[0], self._t1[1], self._t2[0], self._t2[1])
        self.destroy()

    def _cancel(self):
        self._on_confirm(None, None, None, None)
        self.destroy()

# ═══════════════════════════════════════════════════════════════════════════════
#  SHARED HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def card_row(parent, index, card_name, rarity, extra=None):
    color = RARITY_COLORS.get(rarity, "#888")
    row   = ctk.CTkFrame(parent, fg_color="#252525", corner_radius=6)
    row.pack(fill="x", padx=4, pady=2)
    ctk.CTkLabel(row, text=f"#{index}", width=32, text_color="#555",
                 font=ctk.CTkFont(size=11)).pack(side="left", padx=(8,2), pady=6)
    ctk.CTkLabel(row, text="●", text_color=color,
                 font=ctk.CTkFont(size=14)).pack(side="left", padx=(0,6))
    ctk.CTkLabel(row, text=card_name, anchor="w",
                 font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", fill="x", expand=True)
    if extra:
        ctk.CTkLabel(row, text=extra, text_color="#777",
                     font=ctk.CTkFont(size=11)).pack(side="right", padx=(0,8))
    ctk.CTkLabel(row, text=rarity, text_color=color,
                 font=ctk.CTkFont(size=11)).pack(side="right", padx=10)

# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN APP
# ═══════════════════════════════════════════════════════════════════════════════

class VCardTracker(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title(APP_TITLE)
        self.geometry(f"{APP_W}x{APP_H}")
        self.minsize(900, 600)
        self._build_ui()

    def _build_ui(self):
        self.tabs = ctk.CTkTabview(self, anchor="nw")
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)
        self.t_log   = self.tabs.add("📦  Log")
        self.t_stats = self.tabs.add("📊  Stats")
        self.t_coll  = self.tabs.add("📋  Collection")
        self.t_hist  = self.tabs.add("🕓  History")
        self._build_log_tab()
        self._build_stats_tab()
        self._build_collection_tab()
        self._build_history_tab()

    # ══════════════════════════════════════════════════════════════════════════
    #  TAB 1  —  LOG
    # ══════════════════════════════════════════════════════════════════════════

    def _build_log_tab(self):
        # State
        self._box_id:    int | None = None
        self._pack_id:   int | None = None
        self._set_name:  str        = SETS[0]
        self._pack_cards: list      = []
        self._packs_in_box: int     = 0

        # ── Left panel ───────────────────────────────────────────────────────
        left = ctk.CTkFrame(self.t_log, width=320)
        left.pack(side="left", fill="y", padx=(0,8))
        left.pack_propagate(False)

        ctk.CTkLabel(left, text="Set:", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=16, pady=(16,2))
        self._log_set_var = ctk.StringVar(value=SETS[0])
        ctk.CTkOptionMenu(left, values=SETS, variable=self._log_set_var,
                          command=self._on_set_change, width=280).pack(padx=16, pady=(0,10))

        # Box section
        box_sec = ctk.CTkFrame(left, fg_color="#1a2a1a", corner_radius=8)
        box_sec.pack(padx=16, fill="x")

        self._open_box_btn = ctk.CTkButton(
            box_sec, text="🎁  Open New Box",
            command=self._open_box, height=40,
            fg_color="#2a5a2a", hover_color="#3a7a3a")
        self._open_box_btn.pack(padx=10, pady=(10,6), fill="x")

        self._box_prog_label = ctk.CTkLabel(
            box_sec, text="No box open", text_color="#555",
            font=ctk.CTkFont(size=11))
        self._box_prog_label.pack(pady=(0,2))

        self._box_prog_bar = ctk.CTkProgressBar(box_sec, width=270, progress_color="#3a7a3a")
        self._box_prog_bar.pack(padx=10, pady=(0,6))
        self._box_prog_bar.set(0)

        self._cancel_box_btn = ctk.CTkButton(
            box_sec, text="✕  Cancel Box", height=28,
            fg_color="#3a1a1a", hover_color="#5a2a2a",
            state="disabled", command=self._cancel_box)
        self._cancel_box_btn.pack(padx=10, pady=(0,10), fill="x")

        ctk.CTkFrame(left, height=1, fg_color="#333").pack(fill="x", padx=16, pady=10)

        # Pack section
        pack_sec = ctk.CTkFrame(left, fg_color="#1a1a2a", corner_radius=8)
        pack_sec.pack(padx=16, fill="x")

        self._open_pack_btn = ctk.CTkButton(
            pack_sec, text="📦  Open Pack",
            command=self._open_pack, height=38,
            state="disabled")
        self._open_pack_btn.pack(padx=10, pady=(10,6), fill="x")

        self._pack_prog_label = ctk.CTkLabel(
            pack_sec, text="No pack open", text_color="#555",
            font=ctk.CTkFont(size=11))
        self._pack_prog_label.pack(pady=(0,2))

        self._pack_prog_bar = ctk.CTkProgressBar(pack_sec, width=270)
        self._pack_prog_bar.pack(padx=10, pady=(0,6))
        self._pack_prog_bar.set(0)

        self._cancel_pack_btn = ctk.CTkButton(
            pack_sec, text="✕  Cancel Pack", height=28,
            fg_color="#3a1a1a", hover_color="#5a2a2a",
            state="disabled", command=self._cancel_pack)
        self._cancel_pack_btn.pack(padx=10, pady=(0,10), fill="x")

        ctk.CTkFrame(left, height=1, fg_color="#333").pack(fill="x", padx=16, pady=10)

        # Card entry
        ctk.CTkLabel(left, text="Card Name + Rarity:",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=16)
        self._ac = AutocompleteEntry(
            left,
            get_cards_fn=lambda: [(n, r) for n, r in CARD_DB.get(self._log_set_var.get(), [])
                                   if r != "Box Topper"],
            on_select_fn=self._add_card,
            placeholder="e.g.  totless 8 h",
        )
        self._ac.pack(padx=16, fill="x", pady=(4,16))

        # ── Right panel ───────────────────────────────────────────────────────
        right = ctk.CTkFrame(self.t_log)
        right.pack(side="right", fill="both", expand=True)
        ctk.CTkLabel(right, text="Current Pack",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(14,6))
        self._preview = ctk.CTkScrollableFrame(right)
        self._preview.pack(fill="both", expand=True, padx=8, pady=(0,8))
        self._refresh_preview()

    # ── Log helpers ───────────────────────────────────────────────────────────

    def _on_set_change(self, _=None):
        self._set_name = self._log_set_var.get()

    def _open_box(self):
        if self._box_id is not None:
            messagebox.showwarning("Box In Progress", "Finish or cancel the current box first.")
            return
        self._set_name = self._log_set_var.get()
        BoxTopperDialog(self, self._set_name, self._on_topper_selected)

    def _on_topper_selected(self, name, rarity, name2, rarity2):
        if name is None:
            return  # user cancelled
        self._box_id       = db_new_box(self._set_name, name, rarity, name2, rarity2)
        self._packs_in_box = 0
        self._sync_log_ui()
        t2_line = f"\nBox Topper 2: {name2}" if name2 else ""
        messagebox.showinfo("Box Opened!",
                            f"Box Topper 1: {name}{t2_line}\n\nNow open your first pack.")

    def _open_pack(self):
        if self._box_id is None:
            messagebox.showinfo("No Box Open", "Open a box first.")
            return
        if self._pack_id is not None:
            messagebox.showwarning("Pack In Progress", "Finish or cancel the current pack first.")
            return
        self._pack_id    = db_new_pack(self._box_id, self._set_name)
        self._pack_cards = []
        self._sync_log_ui()
        self._refresh_preview()

    def _add_card(self, name: str, rarity: str):
        if self._pack_id is None:
            messagebox.showinfo("No Pack Open", "Open a pack first.")
            return
        db_add_pull(self._pack_id, name, rarity, self._set_name)
        self._pack_cards.append((name, rarity))
        self._refresh_preview()
        self._sync_log_ui()
        if len(self._pack_cards) >= CARDS_PER_PACK:
            self._finish_pack()
        else:
            self._ac.focus()

    def _finish_pack(self):
        notable = [f"  • {n}  [{r}]" for n, r in self._pack_cards
                   if RARITY_RANK.get(r, 0) >= NOTABLE_RANK]
        msg = f"Pack complete!  {CARDS_PER_PACK} cards logged."
        if notable:
            msg += "\n\n✨  Notable pulls:\n" + "\n".join(notable)
        self._packs_in_box += 1
        self._pack_id    = None
        self._pack_cards = []
        if self._packs_in_box >= PACKS_PER_BOX:
            msg += f"\n\n🎉  Box complete! All {PACKS_PER_BOX} packs opened."
            messagebox.showinfo("Pack & Box Complete!", msg)
            self._box_id       = None
            self._packs_in_box = 0
        else:
            messagebox.showinfo("Pack Complete!", msg)
        self._sync_log_ui()
        self._refresh_preview()

    def _cancel_pack(self):
        if self._pack_id is None: return
        if messagebox.askyesno("Cancel Pack", "Delete this pack and all entered cards?"):
            db_delete_pack(self._pack_id)
            self._pack_id = None; self._pack_cards = []
            self._sync_log_ui(); self._refresh_preview()

    def _cancel_box(self):
        if self._box_id is None: return
        if messagebox.askyesno("Cancel Box",
                               "Delete this entire box, all its packs, and all cards?"):
            if self._pack_id:
                db_delete_pack(self._pack_id)
                self._pack_id = None; self._pack_cards = []
            db_delete_box(self._box_id)
            self._box_id = None; self._packs_in_box = 0
            self._sync_log_ui(); self._refresh_preview()

    def _remove_card(self, index: int):
        if self._pack_id is None: return
        con  = sqlite3.connect(DB_FILE)
        rows = con.execute("SELECT id FROM pulls WHERE pack_id=? ORDER BY id",
                           (self._pack_id,)).fetchall()
        if index < len(rows):
            con.execute("DELETE FROM pulls WHERE id=?", (rows[index][0],))
            con.commit()
        con.close()
        self._pack_cards.pop(index)
        self._sync_log_ui(); self._refresh_preview(); self._ac.focus()

    def _sync_log_ui(self):
        box_open  = self._box_id is not None
        pack_open = self._pack_id is not None

        self._open_box_btn.configure(state="disabled" if box_open else "normal")
        self._cancel_box_btn.configure(state="normal" if box_open else "disabled")
        self._open_pack_btn.configure(
            state="disabled" if (not box_open or pack_open) else "normal")
        self._cancel_pack_btn.configure(state="normal" if pack_open else "disabled")

        if box_open:
            self._box_prog_label.configure(
                text=f"Pack {self._packs_in_box + 1} of {PACKS_PER_BOX}  in current box",
                text_color="white")
            self._box_prog_bar.set(self._packs_in_box / PACKS_PER_BOX)
        else:
            self._box_prog_label.configure(text="No box open", text_color="#555")
            self._box_prog_bar.set(0)

        if pack_open:
            done = len(self._pack_cards)
            self._pack_prog_label.configure(
                text=f"Card {done + 1} of {CARDS_PER_PACK}", text_color="white")
            self._pack_prog_bar.set(done / CARDS_PER_PACK)
            self._ac.focus()
        else:
            self._pack_prog_label.configure(text="No pack open", text_color="#555")
            self._pack_prog_bar.set(0)
            self._ac.clear()

    def _refresh_preview(self):
        for w in self._preview.winfo_children(): w.destroy()
        if not self._pack_cards:
            if self._pack_id is None and self._box_id is None:
                msg = "Open a box to get started."
            elif self._pack_id is None:
                msg = "Open a pack to start logging cards."
            else:
                msg = f"Enter card #{len(self._pack_cards)+1} on the left ↑"
            ctk.CTkLabel(self._preview, text=msg, text_color="#555").pack(pady=40)
            return
        for i, (n, r) in enumerate(self._pack_cards):
            self._preview_row(i, n, r)

    def _preview_row(self, index, card_name, rarity):
        color = RARITY_COLORS.get(rarity, "#888")
        row   = ctk.CTkFrame(self._preview, fg_color="#252525", corner_radius=6)
        row.pack(fill="x", padx=4, pady=2)
        ctk.CTkLabel(row, text=f"#{index+1}", width=32, text_color="#555",
                     font=ctk.CTkFont(size=11)).pack(side="left", padx=(8,2), pady=6)
        ctk.CTkLabel(row, text="●", text_color=color,
                     font=ctk.CTkFont(size=14)).pack(side="left", padx=(0,6))
        ctk.CTkLabel(row, text=card_name, anchor="w",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(row, text=rarity, text_color=color,
                     font=ctk.CTkFont(size=11)).pack(side="right", padx=(0,4))
        ctk.CTkButton(row, text="✕", width=28, height=24,
                      fg_color="#3a1a1a", hover_color="#5a2a2a",
                      command=lambda i=index: self._remove_card(i)
                      ).pack(side="right", padx=(0,6))

    # ══════════════════════════════════════════════════════════════════════════
    #  TAB 2  —  STATS
    # ══════════════════════════════════════════════════════════════════════════

    def _build_stats_tab(self):
        top = ctk.CTkFrame(self.t_stats, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(10,0))
        ctk.CTkLabel(top, text="Filter:").pack(side="left", padx=(0,8))
        self._stats_set_var = ctk.StringVar(value="All Sets")
        ctk.CTkOptionMenu(top, values=["All Sets"]+SETS, variable=self._stats_set_var,
                          command=lambda _: self._refresh_stats(), width=200).pack(side="left")
        ctk.CTkButton(top, text="↺  Refresh", command=self._refresh_stats,
                      width=95).pack(side="right")

        self._stats_summary = ctk.CTkFrame(self.t_stats, fg_color="transparent")
        self._stats_summary.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(self.t_stats, text="Rarity Breakdown",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#ccc").pack(anchor="w", padx=14, pady=(0,4))
        self._stats_scroll = ctk.CTkScrollableFrame(self.t_stats)
        self._stats_scroll.pack(fill="both", expand=True, padx=10, pady=(0,10))
        self._refresh_stats()

    def _refresh_stats(self):
        sf = self._stats_set_var.get()
        boxes, packs, pulls, rc = db_get_stats(sf)
        unique = len(db_get_collection(sf))

        for w in self._stats_summary.winfo_children(): w.destroy()
        for lbl, val in [("Boxes Opened", boxes), ("Packs Opened", packs),
                          ("Cards Pulled", pulls), ("Unique Cards", unique)]:
            box = ctk.CTkFrame(self._stats_summary, fg_color="#252525", corner_radius=8)
            box.pack(side="left", expand=True, fill="x", padx=5)
            ctk.CTkLabel(box, text=str(val),
                         font=ctk.CTkFont(size=26, weight="bold")).pack(pady=(12,0))
            ctk.CTkLabel(box, text=lbl, text_color="#777",
                         font=ctk.CTkFont(size=11)).pack(pady=(0,12))

        for w in self._stats_scroll.winfo_children(): w.destroy()
        if pulls == 0:
            ctk.CTkLabel(self._stats_scroll, text="No pulls recorded yet.",
                         text_color="#555").pack(pady=20)
            return
        for rarity in RARITIES:
            if rarity == "Box Topper": continue
            count = rc.get(rarity, 0)
            pct   = count / pulls * 100 if pulls else 0
            color = RARITY_COLORS[rarity]
            row   = ctk.CTkFrame(self._stats_scroll, fg_color="#252525", corner_radius=6)
            row.pack(fill="x", padx=4, pady=3)
            ctk.CTkLabel(row, text="●", text_color=color,
                         font=ctk.CTkFont(size=13)).pack(side="left", padx=(10,4), pady=7)
            ctk.CTkLabel(row, text=rarity, width=130, anchor="w",
                         font=ctk.CTkFont(size=12)).pack(side="left", padx=(0,8))
            wrap = ctk.CTkFrame(row, fg_color="transparent")
            wrap.pack(side="left", fill="x", expand=True, padx=(0,8))
            bar = ctk.CTkProgressBar(wrap, height=13, corner_radius=4, progress_color=color)
            bar.pack(fill="x", pady=10); bar.set(pct / 100)
            ctk.CTkLabel(row, text=f"{count}  ({pct:.1f}%)", width=120, anchor="e",
                         text_color="#999", font=ctk.CTkFont(size=11)).pack(side="right", padx=10)

    # ══════════════════════════════════════════════════════════════════════════
    #  TAB 3  —  COLLECTION
    # ══════════════════════════════════════════════════════════════════════════

    def _build_collection_tab(self):
        top = ctk.CTkFrame(self.t_coll, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(10,0))
        ctk.CTkLabel(top, text="Set:").pack(side="left", padx=(0,4))
        self._coll_set_var = ctk.StringVar(value="All Sets")
        ctk.CTkOptionMenu(top, values=["All Sets"]+SETS, variable=self._coll_set_var,
                          command=lambda _: self._refresh_collection(), width=165).pack(side="left")
        ctk.CTkLabel(top, text="Search:").pack(side="left", padx=(12,4))
        self._coll_search = ctk.StringVar()
        self._coll_search.trace_add("write", lambda *_: self._refresh_collection())
        ctk.CTkEntry(top, textvariable=self._coll_search,
                     placeholder_text="Card name…", width=170).pack(side="left")
        ctk.CTkLabel(top, text="Sort:").pack(side="left", padx=(12,4))
        self._coll_sort_var = ctk.StringVar(value="Rarity ↑")
        ctk.CTkOptionMenu(top, values=["Rarity ↑","Rarity ↓","Name A–Z","Copies ↓"],
                          variable=self._coll_sort_var,
                          command=lambda _: self._refresh_collection(), width=120).pack(side="left")
        ctk.CTkButton(top, text="↺", command=self._refresh_collection, width=40).pack(side="right")

        hdr = ctk.CTkFrame(self.t_coll, fg_color="#1c1c1c", corner_radius=0)
        hdr.pack(fill="x", padx=10, pady=(8,0))
        for txt, w in [("Card Name",0),("Rarity",150),("Set",175),("×",55)]:
            ctk.CTkLabel(hdr, text=txt, font=ctk.CTkFont(size=11, weight="bold"),
                         text_color="#666", width=w,
                         anchor="w" if txt=="Card Name" else "center"
                         ).pack(side="left", padx=(10 if txt=="Card Name" else 0, 0),
                                pady=5, fill="x" if txt=="Card Name" else "none",
                                expand=(txt=="Card Name"))

        self._coll_scroll = ctk.CTkScrollableFrame(self.t_coll)
        self._coll_scroll.pack(fill="both", expand=True, padx=10, pady=(0,10))
        self._refresh_collection()

    def _refresh_collection(self):
        sf     = self._coll_set_var.get()
        search = self._coll_search.get().strip().lower()
        sort   = self._coll_sort_var.get()
        rows   = db_get_collection(sf)
        if search:
            rows = [r for r in rows if search in r[0].lower()]
        if sort   == "Rarity ↑": rows.sort(key=lambda r: (RARITY_RANK.get(r[1],0), r[0]))
        elif sort == "Rarity ↓": rows.sort(key=lambda r: (-RARITY_RANK.get(r[1],0), r[0]))
        elif sort == "Name A–Z": rows.sort(key=lambda r: r[0].lower())
        elif sort == "Copies ↓": rows.sort(key=lambda r: -r[3])

        for w in self._coll_scroll.winfo_children(): w.destroy()
        if not rows:
            ctk.CTkLabel(self._coll_scroll, text="No cards found.",
                         text_color="#555").pack(pady=30); return
        for card_name, rarity, set_name, copies in rows:
            color = RARITY_COLORS.get(rarity, "#888")
            row   = ctk.CTkFrame(self._coll_scroll, fg_color="#252525", corner_radius=5)
            row.pack(fill="x", padx=4, pady=2)
            ctk.CTkLabel(row, text="●", text_color=color,
                         font=ctk.CTkFont(size=12)).pack(side="left", padx=(8,4), pady=5)
            ctk.CTkLabel(row, text=card_name, anchor="w",
                         font=ctk.CTkFont(size=12)).pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(row, text=rarity, text_color=color, width=150,
                         font=ctk.CTkFont(size=11), anchor="center").pack(side="left")
            ctk.CTkLabel(row, text=set_name, width=175, text_color="#888",
                         font=ctk.CTkFont(size=11), anchor="center").pack(side="left")
            ctk.CTkLabel(row, text=f"×{copies}", width=55, anchor="center",
                         font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")

    # ══════════════════════════════════════════════════════════════════════════
    #  TAB 4  —  HISTORY
    # ══════════════════════════════════════════════════════════════════════════

    def _build_history_tab(self):
        top = ctk.CTkFrame(self.t_hist, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(10,4))
        ctk.CTkLabel(top, text="Filter:").pack(side="left", padx=(0,8))
        self._hist_set_var = ctk.StringVar(value="All Sets")
        ctk.CTkOptionMenu(top, values=["All Sets"]+SETS, variable=self._hist_set_var,
                          command=lambda _: self._refresh_history(), width=200).pack(side="left")
        ctk.CTkButton(top, text="↺  Refresh", command=self._refresh_history,
                      width=95).pack(side="right")

        pane = ctk.CTkFrame(self.t_hist, fg_color="transparent")
        pane.pack(fill="both", expand=True, padx=10, pady=(4,8))

        # ── Column 1: boxes ──────────────────────────────────────────────────
        self._hist_box_list = ctk.CTkScrollableFrame(pane, width=240)
        self._hist_box_list.pack(side="left", fill="y", padx=(0,6))

        # ── Column 2: packs in selected box ──────────────────────────────────
        col2 = ctk.CTkFrame(pane, width=220)
        col2.pack(side="left", fill="y", padx=(0,6))
        col2.pack_propagate(False)
        ctk.CTkLabel(col2, text="Packs in Box",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#ccc").pack(anchor="w", padx=8, pady=(8,4))
        self._hist_pack_list = ctk.CTkScrollableFrame(col2)
        self._hist_pack_list.pack(fill="both", expand=True, padx=4, pady=(0,4))

        # ── Column 3: cards in selected pack ─────────────────────────────────
        col3 = ctk.CTkFrame(pane)
        col3.pack(side="left", fill="both", expand=True)
        hdr3 = ctk.CTkFrame(col3, fg_color="transparent")
        hdr3.pack(fill="x", padx=8, pady=(8,4))
        ctk.CTkLabel(hdr3, text="Pack Contents",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#ccc").pack(side="left")
        self._hist_del_box_btn = ctk.CTkButton(
            hdr3, text="🗑 Delete Box", width=110, height=26,
            fg_color="#4a1a1a", hover_color="#6a2a2a", state="disabled",
            command=self._delete_selected_box)
        self._hist_del_box_btn.pack(side="right")

        self._hist_card_list = ctk.CTkScrollableFrame(col3)
        self._hist_card_list.pack(fill="both", expand=True, padx=4, pady=(0,4))
        ctk.CTkLabel(self._hist_card_list,
                     text="Select a box, then a pack.",
                     text_color="#555").pack(pady=30)

        self._sel_box_id  = None
        self._sel_pack_id = None
        self._hist_box_btns  = {}
        self._hist_pack_btns = {}
        self._refresh_history()

    def _refresh_history(self):
        sf    = self._hist_set_var.get()
        boxes = db_get_boxes(sf)
        self._hist_box_btns = {}
        for w in self._hist_box_list.winfo_children(): w.destroy()

        if not boxes:
            ctk.CTkLabel(self._hist_box_list, text="No boxes yet.",
                         text_color="#555").pack(pady=20)
        else:
            ctk.CTkLabel(self._hist_box_list, text=f"{len(boxes)} box(es)",
                         text_color="#555", font=ctk.CTkFont(size=11)
                         ).pack(anchor="w", padx=4, pady=(0,4))
            for bid, sname, opened_at, tname, trarity, tname2, trarity2, pack_cnt in boxes:
                try:    ds = datetime.fromisoformat(opened_at).strftime("%b %d  %H:%M")
                except: ds = opened_at[:16]
                is_sel = (bid == self._sel_box_id)
                btn = ctk.CTkButton(
                    self._hist_box_list,
                    text=f"{sname}  •  {pack_cnt}/{PACKS_PER_BOX} packs\n{ds}",
                    anchor="w", height=50, font=ctk.CTkFont(size=11),
                    fg_color="#1e3a5f" if is_sel else "#252525",
                    hover_color="#2a4a7f" if is_sel else "#323232",
                    border_width=2 if is_sel else 0,
                    border_color="#4a8adf" if is_sel else "#252525",
                    command=lambda b=bid: self._show_box(b),
                )
                btn.pack(fill="x", pady=2, padx=2)
                self._hist_box_btns[bid] = btn

                # Box Topper sub-line(s)
                for tn, tr in [(tname, trarity), (tname2, trarity2)]:
                    if not tn: continue
                    tc  = RARITY_COLORS.get(tr, "#ff80ab")
                    sub = ctk.CTkFrame(self._hist_box_list, fg_color="transparent")
                    sub.pack(fill="x", padx=6, pady=(0,2))
                    ctk.CTkLabel(sub, text="●", text_color=tc,
                                 font=ctk.CTkFont(size=10)).pack(side="left")
                    ctk.CTkLabel(sub, text=f" {tn}  [{tr}]",
                                 text_color="#888", font=ctk.CTkFont(size=10),
                                 anchor="w").pack(side="left")

    def _show_box(self, box_id):
        self._sel_box_id  = box_id
        self._sel_pack_id = None
        self._hist_del_box_btn.configure(state="normal")

        # Highlight box buttons
        for bid, btn in self._hist_box_btns.items():
            sel = (bid == box_id)
            btn.configure(fg_color="#1e3a5f" if sel else "#252525",
                          hover_color="#2a4a7f" if sel else "#323232",
                          border_width=2 if sel else 0,
                          border_color="#4a8adf" if sel else "#252525")

        # Populate packs column
        self._hist_pack_btns = {}
        for w in self._hist_pack_list.winfo_children(): w.destroy()
        for w in self._hist_card_list.winfo_children(): w.destroy()
        ctk.CTkLabel(self._hist_card_list, text="Select a pack.",
                     text_color="#555").pack(pady=30)

        packs = db_get_box_packs(box_id)
        if not packs:
            ctk.CTkLabel(self._hist_pack_list, text="No packs logged.",
                         text_color="#555").pack(pady=10)
            return

        for i, (pid, opened_at, cnt) in enumerate(packs):
            try:    ds = datetime.fromisoformat(opened_at).strftime("%b %d  %H:%M")
            except: ds = opened_at[:16]
            btn = ctk.CTkButton(
                self._hist_pack_list,
                text=f"Pack {i+1}  •  {cnt} cards\n{ds}",
                anchor="w", height=44, font=ctk.CTkFont(size=11),
                fg_color="#252525", hover_color="#323232",
                command=lambda p=pid, n=i+1: self._show_pack(p, n),
            )
            btn.pack(fill="x", pady=2, padx=2)
            self._hist_pack_btns[pid] = btn

    def _show_pack(self, pack_id, pack_num=None):
        self._sel_pack_id = pack_id

        # Highlight pack buttons
        for pid, btn in self._hist_pack_btns.items():
            sel = (pid == pack_id)
            btn.configure(fg_color="#1e3a5f" if sel else "#252525",
                          hover_color="#2a4a7f" if sel else "#323232",
                          border_width=2 if sel else 0,
                          border_color="#4a8adf" if sel else "#252525")

        for w in self._hist_card_list.winfo_children(): w.destroy()
        pulls = db_get_pack_pulls(pack_id)
        if not pulls:
            ctk.CTkLabel(self._hist_card_list, text="No cards.",
                         text_color="#555").pack(pady=20); return
        for i, (n, r) in enumerate(pulls):
            card_row(self._hist_card_list, i+1, n, r)

    def _delete_selected_box(self):
        if self._sel_box_id is None: return
        if messagebox.askyesno("Delete Box",
                               "Permanently delete this box, all its packs, and all cards?"):
            db_delete_box(self._sel_box_id)
            self._sel_box_id  = None
            self._sel_pack_id = None
            self._hist_del_box_btn.configure(state="disabled")
            for w in self._hist_pack_list.winfo_children(): w.destroy()
            for w in self._hist_card_list.winfo_children(): w.destroy()
            ctk.CTkLabel(self._hist_card_list, text="Box deleted.",
                         text_color="#555").pack(pady=30)
            self._refresh_history()

# ═══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    init_db()
    app = VCardTracker()
    app.mainloop()