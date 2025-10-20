"""Taller evaluable presencial"""

import pandas as pd  # type: ignore


def load_data(input_file):
    """Lea el archivo usando pandas y devuelva un DataFrame"""

    # Esta función asume que `input_file` apunta al CSV/TSV con a header
    # columna `raw_text` (como en files/input.txt)
    df = pd.read_csv(input_file)
    return df


def create_key(df, n):
    """Cree una nueva columna en el DataFrame que contenga el key de la
    columna 'raw_text'"""

    df = df.copy()
    # The input file uses column `raw_text`
    df["key"] = df["raw_text"]
    df["key"] = df["key"].str.strip()
    df["key"] = df["key"].str.lower()
    df["key"] = df["key"].str.replace("-", "")
    df["key"] = df["key"].str.translate(
        str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
    )
    df["key"] = df["key"].str.split()

    # ------------------------------------------------------
    # Esta es la parte especifica del algoritmo de n-gram:
    # - Una el texto sin espacios en blanco
    df["key"] = df["key"].str.join("")

    # - Convierta el texto a una lista de n-gramas (length n)
    def _ngrams(s: str) -> list:
        if not isinstance(s, str):
            return []
        L = len(s)
        if L < n:
            return [s]
        return [s[i : i + n] for i in range(0, L - n + 1)]

    df["key"] = df["key"].map(_ngrams)

    # - Ordene la lista de n-gramas y remueve duplicados
    df["key"] = df["key"].apply(lambda x: sorted(set(x)))

    # - Convierta la lista de ngramas a una cadena
    df["key"] = df["key"].str.join("")
    # ------------------------------------------------------

    return df


def generate_cleaned_column(df):
    """Crea la columna 'cleaned' en el DataFrame"""

    df = df.copy()
    # Sort by key and original raw_text so the chosen representative is stable
    df = df.sort_values(by=["key", "raw_text"], ascending=[True, True])
    keys = df.drop_duplicates(subset="key", keep="first")
    key_dict = dict(zip(keys["key"], keys["raw_text"]))
    df["cleaned"] = df["key"].map(key_dict)

    return df


def save_data(df, output_file):
    """Guarda el DataFrame en un archivo con columna `cleaned_text`"""

    df = df.copy()
    df = df[["cleaned"]]
    df = df.rename(columns={"cleaned": "cleaned_text"})
    df.to_csv(output_file, index=False)


def main(input_file, output_file, n=2):
    """Ejecuta la limpieza de datos"""

    df = load_data(input_file)
    df = create_key(df, n)
    df = generate_cleaned_column(df)
    # Write an intermediate file for tests to inspect
    df.to_csv("../files/test.csv", index=False)
    save_data(df, output_file)


if __name__ == "__main__":
    main(
        input_file="files/input.txt",
        output_file="files/output.txt",
    )