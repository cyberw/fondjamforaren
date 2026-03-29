import glob
from dataclasses import dataclass

from lxml import etree


@dataclass
class Instrument:
    isin: str
    instrumentnamn: str
    andel: float
    both: bool = False  # in both funds, only used for comparison


@dataclass
class Fund:
    name: str
    instruments: list[Instrument]


xml_files = glob.glob("fi_data/**/*.xml", recursive=True)


def get_fund(name: str) -> Fund:
    for xml_file in xml_files:
        with open(xml_file, encoding="utf-8") as file:
            xml_data = file.read()

        root = etree.fromstring(xml_data)
        ns = {"fi": "http://schemas.fi.se/publika/vardepappersfonder/20200331"}

        # kommer nog behöva implementera ordning så vi prioriterar den senaste rapporten istället för bara första bästa
        # kvartalsslut = root.xpath("//fi:Rapportinformation/fi:Kvartalsslut/text()", namespaces=ns)[0]

        fondnamn = root.xpath("//fi:Fondinformation/fi:Fond_namn/text()", namespaces=ns)[0]
        if fondnamn == name:
            instrument_nodes = root.xpath("//fi:FinansiellaInstrument/fi:FinansielltInstrument", namespaces=ns)
            instruments = []
            for instrument in instrument_nodes:
                if instrument.xpath("./fi:ISIN-kod_instrument/text()", namespaces=ns):
                    isin = instrument.xpath("./fi:ISIN-kod_instrument/text()", namespaces=ns)[0]
                    instrumentnamn = instrument.xpath("./fi:Instrumentnamn/text()", namespaces=ns)[0]
                    andel = float(instrument.xpath("./fi:Andel_av_fondförmögenhet_instrument/text()", namespaces=ns)[0])
                    instruments.append(Instrument(isin, instrumentnamn, andel))

            return Fund(fondnamn, instruments)
    print(f"Fonden '{name}' kunde inte hittas.")
