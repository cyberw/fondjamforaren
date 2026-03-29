from dataclasses import dataclass

from lxml import etree


@dataclass
class Instrument:
    isin: str
    name: str
    percentage_of_fund: float


# import glob

# # Hämta sökvägen till den första XML-filen i mappen
# # xml_files = glob.glob("fi_data/**/*.xml")
# xml_files = ["fi_data/Prior & Nilsson Fond- och Kapitalförvaltning Aktiebolag_35514_2026-02-09 12.31\PriorNilsson Evolve Global_67188_VPFO_2025Q4_2026-02-09 12.21.xml"]
# if xml_files:
#     # Läs in XML-filen (du kan behöva installera 'lxml' med pip)
#     df = pd.read_xml(xml_files[0])
#     print(df.head())


xml_data = """
<VärdepappersfondInnehav xmlns="http://schemas.fi.se/publika/vardepappersfonder/20200331">
    <FinansiellaInstrument>
      <FinansielltInstrument>
        <Tillgångsslag_enligt_LVF_5_kap>ÖverlåtbartVärdepapper</Tillgångsslag_enligt_LVF_5_kap>
        <Instrumentnamn>KITRON ASA</Instrumentnamn>
        <ISIN-kod_instrument>NO0003079709</ISIN-kod_instrument>
        <Landkod_Emittent>NO</Landkod_Emittent>
        <Valuta>NOK</Valuta>
        <Antal>13000</Antal>
        <Nominellt_belopp />
        <Kurs_som_använts_vid_värdering_av_instrumentet>72.7</Kurs_som_använts_vid_värdering_av_instrumentet>
        <Valutakurs_instrument>0.9134</Valutakurs_instrument>
        <Marknadsvärde_instrument>863254.34</Marknadsvärde_instrument>
        <Andel_av_fondförmögenhet_instrument>2.76</Andel_av_fondförmögenhet_instrument>
        <Bransch>
          <Branschkod_instrument>45</Branschkod_instrument>
          <Bransch_namn_instrument>Informationsteknologi</Bransch_namn_instrument>
        </Bransch>
      </FinansielltInstrument>
      <FinansielltInstrument>
        <Tillgångsslag_enligt_LVF_5_kap>ÖverlåtbartVärdepapper</Tillgångsslag_enligt_LVF_5_kap>
        <Instrumentnamn>KONECRANES OYJ</Instrumentnamn>
        <ISIN-kod_instrument>FI0009005870</ISIN-kod_instrument>
        <Landkod_Emittent>FI</Landkod_Emittent>
        <Valuta>EUR</Valuta>
        <Antal>1483</Antal>
        <Nominellt_belopp />
        <Kurs_som_använts_vid_värdering_av_instrumentet>93.9</Kurs_som_använts_vid_värdering_av_instrumentet>
        <Valutakurs_instrument>10.82</Valutakurs_instrument>
        <Marknadsvärde_instrument>1506725.03</Marknadsvärde_instrument>
        <Andel_av_fondförmögenhet_instrument>4.82</Andel_av_fondförmögenhet_instrument>
        <Bransch>
          <Branschkod_instrument>20</Branschkod_instrument>
          <Bransch_namn_instrument>Industrivaror och tjänster</Bransch_namn_instrument>
        </Bransch>
      </FinansielltInstrument>
    </FinansiellaInstrument>
</VärdepappersfondInnehav>
"""

root = etree.fromstring(xml_data)

# Default namespace in the XML must be mapped to a prefix for XPath
ns = {"fi": "http://schemas.fi.se/publika/vardepappersfonder/20200331"}

instrument_nodes = root.xpath("//fi:FinansiellaInstrument/fi:FinansielltInstrument", namespaces=ns)


instruments = [
    Instrument(
        instrument.xpath("./fi:ISIN-kod_instrument/text()", namespaces=ns)[0],
        instrument.xpath("./fi:Instrumentnamn/text()", namespaces=ns)[0],
        float(instrument.xpath("./fi:Andel_av_fondförmögenhet_instrument/text()", namespaces=ns)[0]),
    )
    for instrument in instrument_nodes
]

for instrument in instruments:
    print(f"{instrument.name} ({instrument.isin}): {instrument.percentage_of_fund}%")
