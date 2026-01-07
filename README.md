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

| Format | CLI Name | Documentation | Notes |
|--------|----------|---------------|-------|
| Archidekt | `archidekt` | [Help](https://archidekt.com/help/faq) | Flexible columns, Scryfall ID support |
| Card Kingdom | `cardkingdom` | [Buylist](https://www.cardkingdom.com/purchasing/mtg_singles) | Simple 4-column format for selling |
| Cardsphere | `cardsphere` | [FAQ](https://www.cardsphere.com/faq) | Trading platform with Scryfall ID |
| Deckbox | `deckbox` | [Help](https://deckbox.org/help/importing) | Uses **full set names** (not codes) |
| Decked Builder | `deckbuilder` | — | Separate regular/foil quantities |
| Deckstats | `deckstats` | [Import](https://deckstats.net/decks/) | 0/1 for foil status |
| DragonShield | `dragonshield` | [App Guide](https://mtg.dragonshield.com/) | Card scanner app with folder support |
| Helvault | `helvault` | [App](https://apps.apple.com/app/helvault-mtg-card-scanner/id1466963201) | **Requires Scryfall IDs** |
| ManaBox | `manabox` | [Guide](https://www.manabox.app/guide) | Popular mobile app |
| Moxfield | `moxfield` | [Import/Export](https://www.moxfield.com/help/importing-and-exporting) | Popular deck builder |
| MTGGoldfish | `mtggoldfish` | [Export Help](https://www.mtggoldfish.com/help/import_export) | Supports FOIL/REGULAR/FOIL_ETCHED |
| MTG Manager | `mtgmanager` | — | **Numeric codes** for condition/language |
| MTGO | `mtgo` | [Support](https://www.mtgo.com/help) | Magic Online format |
| MTGStocks | `mtgstocks` | [Site](https://www.mtgstocks.com/) | Price tracking site |
| MTG Studio | `mtgstudio` | [Site](https://www.mtgstudio.com/) | Simple Yes/No foil format |
| TCGPlayer | `tcgplayer` | [Bulk Entry](https://help.tcgplayer.com/hc/en-us/articles/360056778454) | Includes Product ID/SKU |

## Data Considerations

When converting between formats, some data may be lost or unavailable depending on the source and target formats.

### Missing Data Without Scryfall

Without the `--scryfall` flag, transmute only uses data present in the source file. This means:

- **Set names** may be missing if the source only has set codes (or vice versa)
- **Scryfall IDs** required by Helvault won't be populated unless present in the source
- **Collector numbers** may be absent, causing some apps to show generic card images
- **Oracle IDs** needed for some advanced features won't be available

Using `--scryfall` enables API lookups to fill these gaps, but adds processing time and requires internet access.

### Format-Specific Limitations

| Target Format | Limitation |
|---------------|------------|
| **Helvault** | Requires `scryfall_id` - use `--scryfall` if source lacks it |
| **Deckbox** | Needs full set names, not codes |
| **TCGPlayer** | Product ID/SKU only preserved if present in source |
| **MTG Manager** | Condition/language converted to numeric codes (may lose precision) |

### Recommended Workflow

For best results when converting to formats that require rich metadata:

```bash
# Use Scryfall to fill missing data
transmute convert collection.csv output.csv -o helvault --scryfall
```

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

**Unique aspects:**
- Requires `scryfall_id` for each card (use `--scryfall` flag when converting to this format)
- Foil status stored in `extras` field as "foil" string
- Language uses ISO codes (`en`, `de`, `ja`, etc.)
</details>

<details>
<summary>MTGGoldfish</summary>

```csv
Card,Set ID,Set Name,Quantity,Foil,Variation
Aether Vial,MMA,Modern Masters,1,REGULAR,""
Anax and Cymede,THS,Theros,4,FOIL,""
```

**Unique aspects:**
- Foil is an enum with three values: `FOIL`, `REGULAR`, `FOIL_ETCHED`
- One of few formats that distinguishes etched foils
- `Variation` field for special printings (extended art, showcase, etc.)
</details>

<details>
<summary>ManaBox</summary>

```csv
Name,Set code,Set name,Collector number,Foil,Rarity,Quantity,Scryfall ID,Condition,Language
Lightning Bolt,m10,Magic 2010,146,foil,Common,4,abc123...,NM,en
```

**Unique aspects:**
- Includes both set code and set name
- Has optional Scryfall ID (useful for preserving exact printings)
- Foil is simply "foil" or empty string
</details>

<details>
<summary>Moxfield</summary>

```csv
Count,Tradelist Count,Name,Edition,Condition,Language,Foil,Alter,Proxy,Purchase Price
4,2,Lightning Bolt,m10,NM,English,foil,,,
```

**Unique aspects:**
- Separate `Tradelist Count` column for cards available for trade
- Tracks altered and proxy cards
- `Edition` uses lowercase set codes
</details>

<details>
<summary>DragonShield</summary>

```csv
Folder Name,Quantity,Trade Quantity,Card Name,Set Code,Set Name,Card Number,Condition,Printing,Language
Binder,4,0,Lightning Bolt,M10,Magic 2010,146,NearMint,Foil,English
```

**Unique aspects:**
- Supports folder organization via `Folder Name`
- Condition uses concatenated format: `NearMint`, `LightlyPlayed` (no spaces)
- Includes price columns: `LOW`, `MID`, `MARKET`
</details>

<details>
<summary>TCGPlayer</summary>

```csv
Quantity,Name,Simple Name,Set,Card Number,Set Code,Printing,Condition,Language,Rarity,Product ID,SKU
1,Verdant Catacombs,Verdant Catacombs,Zendikar,229,ZEN,Normal,Near Mint,English,Rare,33470,315319
```

**Unique aspects:**
- Has both `Name` (with variant info) and `Simple Name` (base card name)
- Includes TCGPlayer-specific `Product ID` and `SKU` for marketplace integration
- `Set` is full name, `Set Code` is abbreviation
</details>

<details>
<summary>Deckbox</summary>

```csv
Count,Tradelist Count,Name,Edition,Card Number,Condition,Language,Foil,Signed
4,4,Angel of Serenity,Return to Ravnica,1,Near Mint,English,,,
```

**Unique aspects:**
- `Edition` must be the **full set name** (e.g., "Return to Ravnica", not "RTR")
- Foil column uses "foil" or empty string
- Supports signed card tracking
</details>

<details>
<summary>MTGO</summary>

```csv
Card Name,Quantity,ID #,Rarity,Set,Collector #,Premium
Banisher Priest,1,51909,Uncommon,PRM,1136/1158,Yes
```

**Unique aspects:**
- Magic Online format with unique `ID #` for digital cards
- `Premium` uses `Yes`/`No` for foil status
- Collector numbers may include `/` notation (e.g., "1136/1158")
</details>

<details>
<summary>MTGStocks</summary>

```csv
"Card","Set","Quantity","Price","Condition","Language","Foil","Signed"
"Advent of the Wurm","Modern Masters 2017",1,0.99,M,en,Yes,No
```

**Unique aspects:**
- Price tracking site format with embedded price data
- Foil and Signed use `Yes`/`No` strings
- Condition uses single letters (`M`, `NM`, `LP`, etc.)
</details>

<details>
<summary>Deckstats</summary>

```csv
amount,card_name,is_foil,is_pinned,set_id,set_code
1,"Abandon Reason",0,0,147,"EMN"
```

**Unique aspects:**
- Uses `0`/`1` integers for boolean fields (`is_foil`, `is_pinned`)
- Has both `set_id` (Deckstats internal ID) and `set_code`
- `is_pinned` marks cards locked to specific printings
</details>

<details>
<summary>MTG Manager</summary>

```csv
Quantity,Name,Code,PurchasePrice,Foil,Condition,Language,PurchaseDate
1,"Amulet of Vigor",WWK,18.04,0,0,0,5/6/2018
```

**Unique aspects:**
- Uses **numeric codes** for Condition: 0=Mint, 1=NM, 2=LP, 3=MP, 4=HP, 5=Damaged
- Uses **numeric codes** for Language: 0=English, 1=German, 2=French, etc.
- Tracks purchase history with `PurchasePrice` and `PurchaseDate`
</details>

<details>
<summary>Archidekt</summary>

```csv
Quantity,Name,Scryfall ID,Condition,Language,Foil
4,Lightning Bolt,e3285e6b-...,NM,en,false
```

**Unique aspects:**
- Very flexible column format (minimal required columns)
- Supports Scryfall ID for precise card identification
- Boolean foil field accepts various formats
</details>

<details>
<summary>Cardsphere</summary>

```csv
Count,Name,Edition,Edition Code,Scryfall ID,Condition,Language,Foil
1,Lightning Bolt,Magic 2010,m10,e3285e6b-...,NM,English,false
```

**Unique aspects:**
- Trading platform format with both edition name and code
- Includes Scryfall ID for precise matching
- Used primarily for offer/want list management
</details>

<details>
<summary>Card Kingdom</summary>

```csv
Name,Edition,Foil,Qty
Lightning Bolt,Magic 2010,,4
```

**Unique aspects:**
- Simple 4-column format designed for buylist submissions
- `Edition` is full set name
- Foil is "Foil" or empty
</details>

<details>
<summary>Decked Builder</summary>

```csv
Name,Edition,Reg Qty,Foil Qty
Lightning Bolt,M10,4,1
```

**Unique aspects:**
- **Separate quantity columns** for regular and foil copies
- Useful when tracking both versions of the same card
- Edition uses set codes
</details>

<details>
<summary>MTG Studio</summary>

```csv
Name,Edition,Qty,Foil
Lightning Bolt,M10,4,Yes
```

**Unique aspects:**
- Simple format with `Yes`/`No` foil values
- Edition uses set codes
- Minimal column set for basic collection tracking
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
