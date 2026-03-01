#!/usr/bin/env python

from enhancer.enhancer import Enhancer
from enhancer.processor.nubank_processor import NubankProcessor

import argparse

parser = argparse.ArgumentParser(prog="bank-csv-enhancer")

parser.add_argument("-b", "--bank", default="Nubank")

parser.add_argument("filename")
parser.add_argument("-o", "--output", default="output")

try:
    args = parser.parse_args()

    enhancer = Enhancer()

    if args.bank == "Nubank":
        enhancer.set_processor(NubankProcessor())
    else:
        raise RuntimeError(f"An unknown bank was given: \"{args.bank}\"")

    inputFilename, outputFilename = (args.filename, f"{args.output}.enhanced.csv")
    enhancer.enhance(inputFilename, outputFilename)

    print(f"O arquivo \"{inputFilename}\" foi tratado com sucesso!")
except RuntimeError as e:
    print(e)
except SystemExit:
    pass
