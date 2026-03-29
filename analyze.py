import glob
from dataclasses import dataclass

from lxml import etree


@dataclass
class Instrument:
    isin: str
    instrumentnamn: str
    andel: float


@dataclass
class Fund:
    name: str
    instruments: list[Instrument]


xml_files = glob.glob("fi_data/**/*.xml")


def get_fund(name: str) -> Fund:
    for xml_file in xml_files:
        with open(xml_file, encoding="utf-8") as file:
            xml_data = file.read()

        root = etree.fromstring(xml_data)
        ns = {"fi": "http://schemas.fi.se/publika/vardepappersfonder/20200331"}

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
