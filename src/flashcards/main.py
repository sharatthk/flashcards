import csv
import json
import uuid
import argparse
from collections import defaultdict

# Constants
DECK_CONFIG_UUID = "c901a6ec-1234-48a5-9e56-ccfb0b0a1111"
NOTE_MODEL_UUID = "b1b1b1b1-2345-4b4b-b4b4-b1b1b1b1b1b1"
NOTE_DESC = "Covers core features like 1-1 chat, group chat, message sending and receiving"

def generate_guid():
    return uuid.uuid4().hex

def generate_uuid():
    return str(uuid.uuid4())

def build_note(front, back):
    return {
        "__type__": "Note",
        "fields": [front.strip(), back.strip()],
        "guid": generate_guid(),
        "note_model_uuid": NOTE_MODEL_UUID,
        "tags": []
    }

def build_deck(name, notes):
    return {
        "__type__": "Deck",
        "name": name,
        "crowdanki_uuid": generate_uuid(),
        "deck_config_uuid": DECK_CONFIG_UUID,
        "desc": NOTE_DESC,
        "dyn": 0,
        "extendNew": 10,
        "extendRev": 50,
        "media_files": [],
        "children": [],
        "notes": notes
    }

def create_json(csv_file_path, parent_deck_name):
    decks = defaultdict(list)

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        for row in reader:
            front, back, deck = row["Front"], row["Back"], row["Deck"]
            decks[deck.strip()].append(build_note(front, back))

    # Build child decks
    children = [build_deck(deck_name, notes) for deck_name, notes in decks.items()]

    # Compose full deck
    deck_json = {
        "__type__": "Deck",
        "name": parent_deck_name,
        "crowdanki_uuid": generate_uuid(),
        "deck_config_uuid": DECK_CONFIG_UUID,
        "desc": "Deck covering Facebook Messenger System Design",
        "dyn": 0,
        "extendNew": 10,
        "extendRev": 50,
        "media_files": [],
        "notes": [],
        "children": children,
        "deck_configurations": [
            {
                "__type__": "DeckConfig",
                "crowdanki_uuid": DECK_CONFIG_UUID,
                "name": "Default",
                "autoplay": True,
                "dyn": False,
                "lapse": {
                    "delays": [10],
                    "leechAction": 0,
                    "leechFails": 8,
                    "minInt": 1,
                    "mult": 0.0
                },
                "maxTaken": 60,
                "new": {
                    "bury": True,
                    "delays": [1, 10],
                    "initialFactor": 2500,
                    "ints": [1, 4, 7],
                    "order": 1,
                    "perDay": 20,
                    "separate": True
                },
                "replayq": True,
                "rev": {
                    "bury": True,
                    "ease4": 1.3,
                    "fuzz": 0.05,
                    "ivlFct": 1.0,
                    "maxIvl": 36500,
                    "minSpace": 1,
                    "perDay": 100
                },
                "timer": 0
            }
        ],
        "note_models": [
            {
                "__type__": "NoteModel",
                "crowdanki_uuid": NOTE_MODEL_UUID,
                "name": "Basic",
                "css": ".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}",
                "flds": [
                    {
                        "name": "Front",
                        "ord": 0,
                        "font": "Arial",
                        "size": 20,
                        "rtl": False,
                        "sticky": False,
                        "media": []
                    },
                    {
                        "name": "Back",
                        "ord": 1,
                        "font": "Arial",
                        "size": 20,
                        "rtl": False,
                        "sticky": False,
                        "media": []
                    }
                ],
                "req": [[0, "all", [0]]],
                "sortf": 0,
                "tags": [],
                "tmpls": [
                    {
                        "name": "Card 1",
                        "ord": 0,
                        "qfmt": "{{Front}}",
                        "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}"
                    }
                ],
                "type": 0,
                "vers": [],
                "latexPre": "\\documentclass[12pt]{article}\\special{papersize=3in,5in}\\usepackage[utf8]{inputenc}\\usepackage{amssymb,amsmath}\\pagestyle=empty}\\setlength{\\parindent}{0in}\\begin{document}",
                "latexPost": "\\end{document}"
            }
        ]
    }

    return deck_json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CSV to CrowdAnki JSON format")
    parser.add_argument("csv_path", nargs="?", default="src/flashcards/cards.csv", help="Path to the CSV file (default: cards.csv)")
    parser.add_argument("deck_name", nargs="?", default="Books::Refactoring improving design of Existing Code::Chapter 1", help="Parent deck name, e.g., 'Sys Design::Code Cat::Facebook Messenger'")
    parser.add_argument("--output", default="flashcards.json", help="Output JSON file name")

    args = parser.parse_args()
    result_json = create_json(args.csv_path, args.deck_name)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result_json, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON file generated: {args.output}")
