from enhancer.processor.iprocessor import IProcessor

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
    def __init__(self, processor: IProcessor, inputFilename: str, outputFilename: str):
        self.processor = processor
        self.inputFilename = inputFilename
        self.outputFilename = outputFilename

    def save(self):
        with open(self.inputFilename, newline="") as inputCSVFile:
            processedRows = self.processor.process(inputCSVFile)
            with open(self.outputFilename, "w", newline="") as outputCSVFile:
                writer = csv.writer(outputCSVFile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
                writer.writerow(ENHANCED_CSV_HEADERS)
                writer.writerows(map(lambda x: x.as_list(), processedRows))
