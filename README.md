# Ett verktyg för att räkna ut skillnaden mellan olika fonders innehav

Fondjämföraren kan användas för att jämföra hur breda/smala två indexfonder är, men också ge en uppfattning om hur mycket en aktivt förvaltad fond verkligen avviker från sitt index.

Den använder sig av informationen som fondbolagen rapporterar in till [Finansinspektionen](https://www.fi.se/sv/vara-register/fondinnehav-per-kvartal/).

Jag rekommenderar att du använder [uv](https://docs.astral.sh/uv/getting-started/installation/) för installation.

```text
❯ uv run download.py
Letar efter senaste filen på https://www.fi.se/sv/vara-register/fondinnehav-per-kvartal/...
Laddar ner: https://www.fi.se/FondInnehavLista/download?filnamn=Fondinnehav_2025Q4_2026-03-17 17.09.zip
Klart! 706 XML-filer har sparats i mappen 'fi_data'.
```

För att göra analysen skriver du bara in två fonder som parametrar:

```text
❯ uv run main.py "Avanza Global" "Swedbank Robur Access Global"
 Namn                        ┃ Skillnad ┃
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━
 MICROSOFT CORP              │    0.77% │
 AMAZON.COM INC              │    0.65% │
 APPLE INC                   │    0.59% │
 General Electric            │   -0.53% │
 ALPHABET INC-CL A           │    0.51% │
 JPMORGAN CHASE & CO         │   -0.50% │
 AbbVie                      │   -0.50% │
 TESLA INC                   │    0.49% │
 PALANTIR TECHNOLOGIES INC-A │   -0.46% │
 ELI LILLY & CO              │   -0.41% │
 COSTCO WHOLESALE CORP       │   -0.41% │
 JOHNSON & JOHNSON           │    0.36% │
 Caterpillar                 │   -0.36% │
 WALMART INC                 │    0.34% │
 HSBC HOLDINGS PLC           │   -0.32% │
 Loews                       │   -0.32% │
 HOME DEPOT INC              │    0.32% │
 BROADCOM INC                │   -0.30% │
 PROCTER & GAMBLE CO/THE     │    0.30% │
 McDonald's                  │   -0.30% │
 ASTRAZENECA PLC LN          │    0.29% │
 Parker Hannifin             │   -0.27% │
 ADVANCED MICRO DEVICES      │    0.26% │
 YARA INTERNATIONAL ASA      │   -0.26% │
 META PLATFORMS INC-CLASS A  │    0.25% │
 WELLS FARGO & CO            │   -0.24% │
 NEXTERA ENERGY INC          │   -0.23% │
 Howmet Aerospace            │   -0.23% │
 Shopify                     │   -0.23% │
 VISA INC-CLASS A SHARES     │    0.22% │
 ...                         │          │
```

Ovanstående visar t ex se att Avanza Global är betydligt tyngre i Microsoft och Amazon (kanske pga färre aktier i indexet man följer?), men har ett betydligt mindre innehav i GE än Swedbank Access Global (kanske har den uteslutits pga ESG?).

Du kan även jämföra en aktivt förvaltad med en passiv, vilket ger en viss indikation av hur "aktiv" fonden verkligen är. Allra träffsäkrast är det förstås om du hittar en passiv fond som följer den aktiva fondens jämförelseindex.

Här kan man t ex se att AMF Aktiefond Global's största avvikelse från Avanza Global är deras innehav i Tencent och TSMC:

```text
❯ uv run main.py "AMF Aktiefond Global" "Avanza Global"
 Namn                                  ┃ Skillnad ┃
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━
 Tencent Holdings                      │    2.74% │
 Taiwan Semiconductor Manufacturing US │    2.71% │
 Alphabet C                            │    2.53% │
 ALPHABET INC-CL A                     │   -2.39% │
 Sumitomo Mitsui Financial             │    2.22% │
 ING Group                             │    2.18% │
 Parker Hannifin Corp                  │    2.15% │
 Prologis                              │    2.08% │
 TESLA INC                             │   -1.98% │
 AstraZeneca SEK                       │    1.96% │
 Bank of America                       │    1.91% │
 Anheuser-Busch Inbev                  │    1.74% │
 Deutsche Post                         │    1.74% │
 Siemens                               │    1.72% │
 Eli Lilly & Company                   │    1.69% │
 Alibaba Group Holding US              │    1.69% │
 Intercontinetal Exchange              │    1.50% │
 Apple                                 │   -1.44% │
 Nvidia                                │    1.39% │
 Reliance Industries                   │    1.31% │
 Visa                                  │    1.31% │
 Linde                                 │    1.27% │
 Western Digital                       │    1.26% │
 Microsoft                             │    1.20% │
 MercadoLibre                          │    1.09% │
 Comfort Systems USA                   │    1.08% │
 JOHNSON & JOHNSON                     │   -1.04% │
 Taiwan Semiconductor Manufacturing    │    0.98% │
 TotalEnergies                         │    0.96% │
 Rollins                               │    0.95% │
 ...                                   │          │
 ```

 Stjärnan indikerar att värdepappret finns i bägge fonder.