from wikipedia import WikipediaPage, page
from typing import List
import pandas as pd
import re


def main():
    print_animals()


def get_value(row: List, col: str) -> str:
    """Get the row value without brackets

    Args:
        row (List): the row values
        col (str): the column name

    Returns:
        str: the row value
    """
    value: str = str(row[col][0])
    value = re.sub("[\(\[].*?[\)\]]", "", value).strip()

    return value


def print_animals():
    """Print the animals

    Guidelines:
        Animals with no nouns print animal and adjective
        Animals with multiple nouns print animal and the nouns
    """
    html: WikipediaPage = page("List_of_animal_names").html().encode("UTF-8")
    df: list[pd.DataFrame] = pd.read_html(html, header=None, na_values=["?", "-"])[2]

    for _, row in df.iterrows():
        anim: str = get_value(row, "Animal")
        anim = anim.split()[0]
        nouns: str = get_value(row, "Collective noun")

        if anim == nouns:
            # Got the current row letter, skipping
            continue

        if nouns == "nan" or not nouns.isascii():
            # Got no nouns: print the animal and the adjective
            adj: str = get_value(row, ["Collateral adjective"])

            if adj:
                print(f"{anim} - {adj}")
            else:
                print(f"{anim}")

        else:
            # Got multiple nouns: print the animal and the nouns
            for noun in nouns.split():
                noun = noun.replace(",", "").strip()
                if noun:
                    print(f"{anim} - {noun}")


if __name__ == "__main__":
    main()
