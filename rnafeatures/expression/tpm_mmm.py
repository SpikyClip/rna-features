import pandas as pd
from pathlib import Path


def get_tpm_mmm_matrix(path):
    """
    Given a tpm.tsv file for each dataset, returns a dataframe of tpm mad, max
    and median for each gene.
    """

    df = pd.read_csv(path, sep="\t", index_col="gene_id")
    # Drop 'gene_name' and rename gene_id to match expression matrix index
    # df.drop(columns="gene_name", inplace=True)
    df.index.name = "gene"

    # Create multiindex column to hold results
    midx = pd.MultiIndex.from_product([["tpm"], ["mad", "max", "median"]])
    tpm_df = pd.DataFrame(index=df.index, columns=midx)

    # Calculate mad, max, and median tpm for each gene.
    tpm_df[("tpm", "mad")] = df.mad(axis="columns")
    tpm_df[("tpm", "max")] = df.max(axis="columns")
    tpm_df[("tpm", "median")] = df.median(axis="columns")

    return tpm_df


if __name__ == "__main__":
    path = Path("../../tests/data/input/set_1/tpm.tsv")
    tpm_df = get_tpm_mmm_matrix(path)
    print(tpm_df)
