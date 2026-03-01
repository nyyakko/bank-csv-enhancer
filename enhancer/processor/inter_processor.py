from .core.iprocessor import IProcessor
from .core.transaction import Transaction

import csv, re, uuid

_DEFAULT_HEADERS = ["Data Lançamento", "Histórico", "Descrição", "Valor", "Saldo"]

class InterProcessor(IProcessor):
    def process(self, csvFile):
        reader = csv.reader(csvFile, delimiter=";", quotechar="|")

        [next(reader) for x in range(5)] # skip the first junk lines

        headers = next(reader)
        if headers != _DEFAULT_HEADERS:
            raise RuntimeError("The given file does not seem to be a valid Inter statement csv")

        transactions = []

        for row in reader:
            transaction = {}

            if re.search(r"Pix (\w+)", row[1], re.IGNORECASE):
                transaction = process_transfer(row)
                transaction.descricao = f"Transferência {"de" if float(transaction.valor) > 0 else "para"} {transaction.nome_pessoa}"
            else:
                print(f"[WARN] Skipping transaction: {row[2]}")
                continue

            transactions.append(transaction)

        return transactions

def process_transfer(row):
    result = Transaction(identificador=str(uuid.uuid4()), data=row[0], valor=row[3].replace(",", "."), tipo_operacao="TRANSFERENCIA")

    tipo_match = re.search(r"Pix (\w+)", row[1], re.IGNORECASE)
    result.tipo_movimentacao = ((tipo_match.group(1)[:-1] + "a").upper() if tipo_match else "__TIPO_MOVIMENTACAO__")

    result.nome_pessoa = row[2]

    return result
