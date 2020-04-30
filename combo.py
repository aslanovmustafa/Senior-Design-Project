# combines all txt files in folder into one txt file

import glob

read_files = glob.glob("*.txt")

with open("combined_corpus.txt", "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())