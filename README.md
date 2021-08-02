# Transmute
CLI tool for converting CSV-based Magic: the Gathering (MtG) collection files

## CSV Formats

#### Helvault
```csv
collector_number,extras,language,name,oracle_id,quantity,scryfall_id,set_code,set_name
"136","foil","en","Goblin Arsonist","c1177f22-a1cf-4da3-a68d-ff954e878403","4","c24751fd-5e9b-4d7d-83ba-e306b439bbe1","m12","Magic 2012"
```

#### Scryfall
```csv
```

#### MTGO
```csv
Card Name,Quantity,ID #,Rarity,Set,Collector #,Premium,
"Banisher Priest",1,51909,Uncommon,PRM,1136/1158,Yes'
"Batterskull",10,51909,Uncommon,PRM,1136/1158,Yes'
Notes: ID #, Rarity, Collector # are optional (leave the column empty). Set is the 3-letter set code, Premium is "Yes" for foils or "No" otherwise.
```

#### MTG Studio
```csv
Name,Edition,Qty,Foil
Aether Vial,MMA,1,No
Anax and Cymede,THS,4,Yes
Notes: Edition is the 3-letter set code, Foil should be "Yes" or "No"
```

#### Deckbox
```csv
Count,Tradelist Count,Name,Edition,Card Number,Condition,Language,Foil,Signed,Artist Proof,Altered Art,Mis,
4,4,Angel of Serenity,Return to Ravnica,1,Near Mint,English,,,,,,,,
1,1,Ashen Rider,Theros,187,Near Mint,English,,,,,,,,
1,0,Anax and Cymede,Theros,186,Near Mint,English,foil,,,,,,,
Notes: Foil should be "foil" for foils. Edition is the name of the set.
```

#### Deck Builder
```csv
Total Qty,Reg Qty,Foil Qty,Card,Set,Mana Cost,Card Type,Color,Rarity,Mvid,Single Price,Single Foil Price,Total Price,Price Source,Notes
3,2,1,Black Sun's Zenith,Mirrodin Besieged,XBB,Sorcery,Black,Rare,214061,1.00,6.25,7.25,cardshark,
1,1,0,Snapcaster Mage,Innistrad,1U,Creature  - Human Wizard,Blue,Rare,227676,26.60,115.00,141.60,cardshark,
Notes: Foils are indicated in the Foil Qty column.
```

#### Pucatrade
```csv
Count,Name,Edition,Rarity,Expansion Symbol,Points,Foil,Condition,Language,Status,Entered Date,Updated Date,Exported Date
1,Breeding Pool,Gatecrash,RARE,GTC,1009,0,"Near Mint","English",NOT FOR TRADE,"11/19/2014","11/29/2014","11/30/2014",19632
8,Rattleclaw Mystic,Khans of Tarkir,RARE,KTK,194,0,"Near Mint","English",HAVE,"11/29/2014","11/29/2014","11/30/2014",25942
1,Opulent Palace,Khans of Tarkir,UNCOMMON,KTK,461,1,"Near Mint","English",HAVE,"11/29/2014","11/29/2014","11/30/2014",25928
1,Tasigur the Golden Fang,Fate Reforged,RARE,FRF,1045,1,"Near Mint","English",HAVE,"1/24/2015","1/24/2015","2/03/2015",270
1,Tasigur the Golden Fang,Fate Reforged,RARE,FRF,1045,1,"Near Mint","English",HAVE,"1/24/2015","1/24/2015","2/03/2015",270
Notes: Foil should be 1 for foils (0 otherwise).
```

#### MTGGoldfish
```csv
Card,Set ID,Set Name,Quantity,Foil,Variation
Aether Vial,MMA,Modern Masters,1,""
Anax and Cymede,THS,Theros,4,FOIL,""
Notes: Foil should be FOIL for foil cards, REGULAR for regular cards, FOIL_ETCHED for foil-etched cards.
```

#### MTGStocks
```csv
"Card","Set","Quantity","Price","Condition","Language","Foil","Signed"
"Abandon Hope","Tempest",2,0.24,M,en,No,No
"Abduction","Classic Sixth Edition",1,0.33,M,en,No,No
"Advent of the Wurm","Modern Masters 2017",1,0.99,M,en,Yes,No
"Advent of the Wurm","Modern Masters 2017",3,0.35,M,en,No,No
```

#### TCGPlayer
```csv
Quantity,Name,Simple Name,Set,Card Number,Set Code,Printing,Condition,Language,Rarity,Product ID,SKU
1,Verdant Catacombs,Verdant Catacombs,Zendikar,229,ZEN,Normal,Near Mint,English,Rare,33470,315319
1,Graven Cairns,Graven Cairns,Zendikar Expeditions,28,EXP,Foil,Near Mint,English,Mythic,110729,3042202
1,Olivia Voldaren,Olivia Voldaren,Innistrad,215,ISD,Foil,Near Mint,English,Mythic,52181,500457
```

#### Deckstats
```csv
amount,card_name,is_foil,is_pinned,set_id,set_code
1,"Abandon Reason",0,0,147,"EMN"
2,"Abandoned Sarcophagus",0,0,187,"HOU"
```

#### MTGManager
```csv
Quantity,Name,Code,PurchasePrice,Foil,Condition,Language,PurchaseDate
1,"Amulet of Vigor",WWK,18.04,0,0,0,5/6/2018
1,"Arcane Lighthouse",C14,3.83,0,0,0,5/6/2018