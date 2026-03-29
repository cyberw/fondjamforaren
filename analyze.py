import glob

from lxml import etree

xml_files = glob.glob("fi_data/**/*.xml")

for xml_file in xml_files:
    with open(xml_file, encoding="utf-8") as file:
        xml_data = file.read()

    root = etree.fromstring(xml_data)
    ns = {"fi": "http://schemas.fi.se/publika/vardepappersfonder/20200331"}

    fondinformation = root.xpath("//fi:Fondinformation/fi:Fond_namn/text()", namespaces=ns)

    print(fondinformation[0])

    instrument_nodes = root.xpath("//fi:FinansiellaInstrument/fi:FinansielltInstrument", namespaces=ns)
    for instrument in instrument_nodes:
        if instrument.xpath("./fi:ISIN-kod_instrument/text()", namespaces=ns):
            isin = instrument.xpath("./fi:ISIN-kod_instrument/text()", namespaces=ns)[0]
            instrumentnamn = instrument.xpath("./fi:Instrumentnamn/text()", namespaces=ns)[0]
            andel = float(instrument.xpath("./fi:Andel_av_fondförmögenhet_instrument/text()", namespaces=ns)[0])

        print(f"{instrumentnamn} ({isin}): {andel}%")
