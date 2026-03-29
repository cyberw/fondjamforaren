import logging

import typer
from rich.table import Table

from analyze import Fund, Instrument, get_fund

app = typer.Typer(add_completion=False)
logger = logging.getLogger(__name__)
# avoid annoying "Using selector: KqueueSelector" when running in debug:
logging.getLogger("asyncio").setLevel(logging.INFO)
from rich.console import Console


def delta(f1: Fund, f2: Fund) -> list[Instrument]:
    instrdict: dict[str, Instrument] = {}
    for instrument in f1.instruments:
        instrdict[instrument.isin] = instrument

    for instrument in f2.instruments:
        if instrument.isin in instrdict:
            instrdict[instrument.isin].andel -= instrument.andel
            instrdict[instrument.isin].both = True
        else:
            instrdict[instrument.isin] = instrument
            instrdict[instrument.isin].andel = -instrument.andel

    return list(instrdict.values())


@app.command()
def main(
    fund1: str,
    fund2: str,
):
    """
    Compare two funds and print the differences.
    """
    logger.info(f"Comparing {fund1} and {fund2}...")
    f1 = get_fund(fund1)
    f2 = get_fund(fund2)
    if not f1 or not f2:
        return
    d = delta(f1, f2)
    d.sort(key=lambda instrument: abs(instrument.andel), reverse=True)
    table = Table(show_edge=False)
    table.add_column("Namn", max_width=40)
    table.add_column("Skillnad", justify="right")

    for instrument in d[:30]:
        table.add_row(instrument.instrumentnamn, f"{instrument.andel:.2f}%")

    if len(d) > 30:
        table.add_row("...", "", "")

    Console().print(table)


if __name__ == "__main__":
    app()
