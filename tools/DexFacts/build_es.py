#!/usr/bin/env python3
"""Spanish offline Pokédex facts for the PKForge community translation.

Uses PokeAPI's licensed CSV tables, retaining numerical data and English item keys
from PKForge's existing (English) reference file. The descriptions are selected
from Spanish prose or the most recent Spanish in-game flavor text; English
remains as fallback for data that PokeAPI has not translated.

PokeAPI contributors © 2014; BSD-3-Clause (https://github.com/PokeAPI/pokeapi).
Only generated data is embedded in the APK, no HTTP requests happen in-app.
"""
import csv
import gzip
import io
import os
import sys
from collections import defaultdict

from build import BASE, clean, normalise_name, load

LANG_ES = "7"
LANG_EN = "9"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOURCE = os.path.join(ROOT, "src", "PKForge.Domain", "Resources", "dexfacts.tsv.gz")
OUTPUT = os.path.join(ROOT, "src", "PKForge.Domain", "Resources", "dexfacts.es.tsv.gz")
FILES = [
    "moves.csv", "move_effect_prose.csv", "move_flavor_text.csv",
    "ability_prose.csv", "ability_flavor_text.csv",
    "item_prose.csv", "item_flavor_text.csv", "item_names.csv",
    "pokemon_species_names.csv", "pokemon_species_flavor_text.csv",
    "version_names.csv",
]


def latest_flavor(rows, key):
    best = {}
    for row in rows:
        if row["language_id"] != LANG_ES or not row["flavor_text"].strip():
            continue
        version = int(row["version_group_id"])
        item_id = row[key]
        if item_id not in best or version > best[item_id][0]:
            best[item_id] = (version, clean(row["flavor_text"]))
    return {k: v[1] for k, v in best.items()}


def lookup_effects(rows, key):
    return {r[key]: clean(r["short_effect"]) for r in rows
            if r["local_language_id"] == LANG_ES and r["short_effect"].strip()}


def main():
    data = {name: load(None, name) for name in FILES}

    move_effects = lookup_effects(data["move_effect_prose.csv"], "move_effect_id")
    move_flavor = latest_flavor(data["move_flavor_text.csv"], "move_id")
    by_move = {row["id"]: row for row in data["moves.csv"]}
    ability_effects = lookup_effects(data["ability_prose.csv"], "ability_id")
    ability_flavor = latest_flavor(data["ability_flavor_text.csv"], "ability_id")
    item_effects = lookup_effects(data["item_prose.csv"], "item_id")
    item_flavor = latest_flavor(data["item_flavor_text.csv"], "item_id")

    en_item = {r["item_id"]: r["name"] for r in data["item_names.csv"]
               if r["local_language_id"] == LANG_EN}
    es_item = {r["item_id"]: r["name"] for r in data["item_names.csv"]
               if r["local_language_id"] == LANG_ES}
    en_item_id = {}
    for item_id in sorted(en_item, key=int):
        en_item_id.setdefault(normalise_name(en_item[item_id]), item_id)

    genus = {r["pokemon_species_id"]: clean(r["genus"]) for r in data["pokemon_species_names.csv"]
             if r["local_language_id"] == LANG_ES and r["genus"].strip()}
    version_es = {r["version_id"]: r["name"] for r in data["version_names.csv"]
                  if r["local_language_id"] == LANG_ES}
    version_en = {r["version_id"]: r["name"] for r in data["version_names.csv"]
                  if r["local_language_id"] == LANG_EN}

    pokedex = defaultdict(dict)
    for row in sorted(data["pokemon_species_flavor_text.csv"],
                      key=lambda x: (int(x["species_id"]), int(x["version_id"]))):
        if row["language_id"] != LANG_ES or not row["flavor_text"].strip():
            continue
        version = version_es.get(row["version_id"], version_en.get(row["version_id"]))
        if not version:
            continue
        species = row["species_id"]
        text = clean(row["flavor_text"].replace("\f", " "))
        if text:
            pokedex[species].setdefault(normalise_name(text), (version, text))

    with gzip.open(SOURCE, "rt", encoding="utf-8") as f:
        english = [line.rstrip("\n") for line in f]

    translated = []
    count = defaultdict(int)
    seen_sp = set()
    spanish_items = {}
    for line in english:
        row = line.split("\t")
        kind = row[0]
        if kind == "M" and len(row) >= 7:
            details = by_move.get(row[1], {})
            result = clean(move_effects.get(details.get("effect_id"), ""),
                           details.get("effect_chance", ""))
            result = result or move_flavor.get(row[1], "")
            if result:
                row[6] = result
                count["move"] += 1
        elif kind == "A" and len(row) >= 3:
            result = ability_effects.get(row[1]) or ability_flavor.get(row[1], "")
            if result:
                row[2] = result
                count["ability"] += 1
        elif kind == "I" and len(row) >= 3:
            item_id = en_item_id.get(row[1])
            if item_id:
                result = item_effects.get(item_id) or item_flavor.get(item_id, "")
                if result:
                    row[2] = result
                    count["item"] += 1
                # Aliases support localized names while the English lookups
                # used by older saves continue to work.
                if item_id in es_item:
                    alias = normalise_name(es_item[item_id])
                    if alias and alias != row[1]:
                        spanish_items.setdefault(alias, row[2])
        elif kind == "S" and len(row) >= 3:
            result = genus.get(row[1])
            if result:
                row[2] = result
                count["genus"] += 1
        elif kind == "F" and len(row) >= 4:
            species = row[1]
            if species in pokedex:
                if species not in seen_sp:
                    for version, flavor in pokedex[species].values():
                        translated.append("\t".join(["F", species, version, flavor]))
                        count["entry"] += 1
                    seen_sp.add(species)
                continue
        translated.append("\t".join(row))

    for alias, effect in sorted(spanish_items.items()):
        translated.append("\t".join(["I", alias, effect]))

    # Stable gzip output for repeatable CI and reproducible source attribution.
    translated.insert(0, "#\tPKForge Spanish dex facts: PokeAPI BSD-3-Clause © 2014 contributors; English fallback")
    payload = ("\n".join(translated) + "\n").encode("utf-8")
    with open(OUTPUT, "wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as z:
            z.write(payload)

    print("Spanish dex data:", dict(count), "aliases:", len(spanish_items),
          "bytes:", os.path.getsize(OUTPUT), flush=True)
    if count["entry"] < 500 or count["move"] < 100:
        raise SystemExit("PokeAPI Spanish data unexpectedly incomplete")


if __name__ == "__main__":
    main()
