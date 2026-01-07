# Transmute

[![PyPI version](https://badge.fury.io/py/transmute-mtg.svg)](https://badge.fury.io/py/transmute-mtg)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CLI tool for converting Magic: The Gathering collection CSV files between formats.

## Features

- Convert collections between 16 different formats
- Auto-detect input format from CSV headers
- Optional Scryfall API integration to fill missing card data
- Simple command-line interface

## Installation

```bash
pip install transmute-mtg
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install transmute-mtg
```

## Usage

### Convert between formats

```bash
# Basic conversion (auto-detect input format)
transmute convert my-collection.csv output.csv -o manabox

# Specify both input and output formats
transmute convert goldfish-export.csv moxfield-import.csv -i mtggoldfish -o moxfield

# Fill missing card data via Scryfall API
transmute convert collection.csv output.csv -o helvault --scryfall
```

### List supported formats

```bash
transmute formats
```

### Auto-detect a file's format

```bash
transmute detect mystery-file.csv
```

## Supported Formats

| Format | CLI Name | Notes |
|--------|----------|-------|
| Archidekt | `archidekt` | Flexible columns, Scryfall ID support |
| Card Kingdom | `cardkingdom` | Simple 4-column format for selling |
| Cardsphere | `cardsphere` | Trading platform with Scryfall ID |
| Deckbox | `deckbox` | Uses full set names |
| Decked Builder | `deckbuilder` | Separate regular/foil quantities |
| Deckstats | `deckstats` | 0/1 for foil status |
| DragonShield | `dragonshield` | Card scanner app with folder support |
| Helvault | `helvault` | Requires Scryfall IDs |
| ManaBox | `manabox` | Popular mobile app |
| Moxfield | `moxfield` | Popular deck builder |
| MTGGoldfish | `mtggoldfish` | Supports FOIL/REGULAR/FOIL_ETCHED |
| MTG Manager | `mtgmanager` | Numeric codes for condition |
| MTGO | `mtgo` | Magic Online format |
| MTGStocks | `mtgstocks` | Price tracking site |
| MTG Studio | `mtgstudio` | Simple Yes/No foil format |
| TCGPlayer | `tcgplayer` | Includes Product ID/SKU |

## Python API

You can also use transmute as a library:

```python
from pathlib import Path
from transmute.converter import Converter
from transmute.formats import FormatRegistry

# Convert a file
converter = Converter(use_scryfall=True)
converter.convert(
    input_path=Path("collection.csv"),
    output_path=Path("output.csv"),
    input_format="mtggoldfish",
    output_format="manabox",
)

# Read a collection
handler = FormatRegistry.get("helvault")
collection = handler.read(Path("helvault-export.csv"))

for entry in collection:
    print(f"{entry.quantity}x {entry.card.name} ({entry.card.set_code})")
```

## CSV Format Examples

<details>
<summary>Helvault</summary>

```csv
collector_number,extras,language,name,oracle_id,quantity,scryfall_id,set_code,set_name
"136","foil","en","Goblin Arsonist","c1177f22-...","4","c24751fd-...","m12","Magic 2012"
```
</details>

<details>
<summary>MTGGoldfish</summary>

```csv
Card,Set ID,Set Name,Quantity,Foil,Variation
Aether Vial,MMA,Modern Masters,1,REGULAR,""
Anax and Cymede,THS,Theros,4,FOIL,""
```
Foil values: `FOIL`, `REGULAR`, `FOIL_ETCHED`
</details>

<details>
<summary>ManaBox</summary>

```csv
Name,Set code,Set name,Collector number,Foil,Rarity,Quantity,Scryfall ID,Condition,Language
Lightning Bolt,m10,Magic 2010,146,foil,Common,4,abc123...,NM,en
```
</details>

<details>
<summary>Moxfield</summary>

```csv
Count,Tradelist Count,Name,Edition,Condition,Language,Foil,Alter,Proxy,Purchase Price
4,2,Lightning Bolt,m10,NM,English,foil,,,
```
</details>

<details>
<summary>DragonShield</summary>

```csv
Folder Name,Quantity,Trade Quantity,Card Name,Set Code,Set Name,Card Number,Condition,Printing,Language
Binder,4,0,Lightning Bolt,M10,Magic 2010,146,NearMint,Foil,English
```
</details>

<details>
<summary>TCGPlayer</summary>

```csv
Quantity,Name,Simple Name,Set,Card Number,Set Code,Printing,Condition,Language,Rarity,Product ID,SKU
1,Verdant Catacombs,Verdant Catacombs,Zendikar,229,ZEN,Normal,Near Mint,English,Rare,33470,315319
```
</details>

<details>
<summary>Deckbox</summary>

```csv
Count,Tradelist Count,Name,Edition,Card Number,Condition,Language,Foil,Signed
4,4,Angel of Serenity,Return to Ravnica,1,Near Mint,English,,,
```
Edition is the **full set name** (not code). Foil is `foil` or empty.
</details>

<details>
<summary>MTGO</summary>

```csv
Card Name,Quantity,ID #,Rarity,Set,Collector #,Premium
Banisher Priest,1,51909,Uncommon,PRM,1136/1158,Yes
```
Premium is `Yes` for foils, `No` otherwise.
</details>

<details>
<summary>MTGStocks</summary>

```csv
"Card","Set","Quantity","Price","Condition","Language","Foil","Signed"
"Advent of the Wurm","Modern Masters 2017",1,0.99,M,en,Yes,No
```
</details>

<details>
<summary>Deckstats</summary>

```csv
amount,card_name,is_foil,is_pinned,set_id,set_code
1,"Abandon Reason",0,0,147,"EMN"
```
</details>

<details>
<summary>MTG Manager</summary>

```csv
Quantity,Name,Code,PurchasePrice,Foil,Condition,Language,PurchaseDate
1,"Amulet of Vigor",WWK,18.04,0,0,0,5/6/2018
```
Condition and Language use numeric codes.
</details>

## Development

```bash
# Clone and install
git clone https://github.com/oflannabhra/transmute.git
cd transmute
uv sync

# Run tests
uv run pytest

# Lint
uv run ruff check src/ tests/

# Format
uv run ruff format src/ tests/
```

## License

MIT License - see [LICENSE](LICENSE) for details.
