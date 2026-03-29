import logging

import typer

from analyze import Fund, Instrument, get_fund

app = typer.Typer(add_completion=False)
logger = logging.getLogger(__name__)
# avoid annoying "Using selector: KqueueSelector" when running in debug:
logging.getLogger("asyncio").setLevel(logging.INFO)


def delta(f1: Fund, f2: Fund) -> list[Instrument]:
    instrdict: dict[str, Instrument] = {}
    for instrument in f1.instruments:
        instrdict[instrument.isin] = instrument

    for instrument in f2.instruments:
        if instrument.isin in instrdict:
            instrdict[instrument.isin].andel -= instrument.andel
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
    d = delta(f1, f2)
    d.sort(key=lambda instrument: abs(instrument.andel), reverse=True)
    for instrument in d:
        if abs(instrument.andel) > 0.5:
            print(f"{instrument.isin} {instrument.instrumentnamn} {instrument.andel:.2f}%")


if __name__ == "__main__":
    app()
