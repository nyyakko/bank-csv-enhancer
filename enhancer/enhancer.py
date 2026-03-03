from enhancer.processor.core.iprocessor import IProcessor

import csv

ENHANCED_CSV_HEADERS = [
    "Identificador",
    "Data",
    "Valor",
    "Tipo_Operacao",
    "Tipo_Movimentacao",
    "Nome_Pessoa",
    "Instituicao",
    "Codigo_Instituicao",
    "Agencia",
    "Conta",
    "Descricao"
]

class Enhancer:
    def __init__(self):
        self.processor = None

    def set_processor(self, processor: IProcessor):
        self.processor = processor

    def enhance(self, inputFilename: str, outputFilename: str):
        with open(inputFilename, newline="") as inputCSVFile:
            transactions = self.processor.process(inputCSVFile)
            with open(outputFilename, "w", newline="") as outputCSVFile:
                writer = csv.writer(outputCSVFile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
                writer.writerow(ENHANCED_CSV_HEADERS)
                writer.writerows(map(lambda x: x.as_list(), transactions))
