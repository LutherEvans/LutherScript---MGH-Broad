"""
Goal of script: Read in a file, extract a column, path extraction manipulation, and then write to new file.
​
This script needs the following package:
- pandas
"""
import argparse
import pandas as pd
import os
from typing import List


# Delimiter
D = "\t"

def get_array_from_string(text: str) -> List[str]:
    """
    Extracts items encode in an array-like text.

    Parameters
    ----------
    text: An string in the following format:
        `["filename1.txt", "filename2.txt"]`
    Returns
    -------
        A list of items extracted from the list-like text encoding.
    """
    text = text.replace("[", "").replace("]", "").replace("\"", "")
    items = text.split(",")
    return items

def extract_columns_from_terra_manifest_file(filename: str):
    output = []
    filename = '/Users/le919/PycharmProjects/pythonProject/sample_set_entity.tsv'
    with open(filename) as f:
        header = f.readline().rstrip().split(D)
        genotyped_vcfs_index = header.index("genotyped_segments_vcfs")
        filtered_intervals_index = header.index("filtered_intervals")
        for line in f:
            columns = line.rstrip().split(D)
            if not(columns[0].endswith("_CASE") or
                   columns[0].endswith("_COHORT")):
                continue

            if len(columns) < genotyped_vcfs_index or len(columns) < filtered_intervals_index:
                continue

            cluster = columns[0]
            vcfs = get_array_from_string(columns[genotyped_vcfs_index])
            filtered_intervals = columns[filtered_intervals_index]

            for vcf in vcfs:
                # TODO: In case I might want to extract sample from the URI. If so, this is the way to do it,
                #  otherwise, correct this to best match your application.
                sample = os.path.basename(vcf).split(".")[0].replace("genotyped-segments-", "")

                output.append([sample, vcf, filtered_intervals, cluster])

    output_df = pd.DataFrame(output, columns=["sample", "genotyped_segments_vcf", "filtered_intervals", "cluster"])
    return output_df

def extract_columns(filename):
    """
    Parameters
    ----------
    filename
    Returns
    -------
    """
    print(filename)
    df = pd.read_csv(filename, sep="\t")
    column_x = df["x"] # where x is the name of the column you want to get

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_filename',
        help="some description of what is this file")
    parser.add_argument(
        'output_filename',
        help="...")
    args = parser.parse_args()
    output_df = extract_columns_from_terra_manifest_file(args.input_filename)
    output_df.to_csv(args.output_filename, sep="\t", index=False)

if __name__ == "__main__":
    main()

#filename = '/Users/le919/PycharmProjects/pythonProject/sample_set_entity.tsv'
#filename = '/Users/le919/gCNV_samples/sample_set/001_PostProcessing/sample_set_entity.tsv'
# /Users/le919/PycharmProjects/pythonProject/sample_set_entity.tsv, /Users/le919/PycharmProjects/pythonProject/sample_set_OUTPUT.tsv