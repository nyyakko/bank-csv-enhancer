from .iprocessor import IProcessor
from .core.row import Row

import csv, re

class NubankProcessor(IProcessor):
    def process(self, csvFile):
        reader = csv.reader(csvFile, delimiter=",", quotechar="|")
        next(reader)

        processedRows = []

        for row in reader:
            processedRow = {}

            if re.search(r"Transferência", row[-1], re.IGNORECASE):
                processedRow = process_transfer(row)
                processedRow.descricao = f"Transferência {"de" if float(processedRow.valor) > 0 else "para"} {processedRow.nome_pessoa}"
            elif re.search(r"Pagamento", row[-1], re.IGNORECASE):
                processedRow = process_payment(row)
                processedRow.descricao = f"{processedRow.tipo_movimentacao.title()}"
            elif re.search(r"(Resgate|Aplicação)\s+RDB", row[-1], re.IGNORECASE):
                processedRow = process_rdb(row)
                processedRow.descricao = f"{processedRow.tipo_movimentacao.title()} RDB"
            else:
                print(f"[WARN] Skipping transaction: {row[2]}")
                continue

            processedRows.append(processedRow)

        return processedRows

def process_transfer(row):
    result = Row(identificador=row[2], data=row[0], valor=row[1], tipo_operacao="TRANSFERENCIA")
    description = row[-1]

    tipo_match = re.search(r"Transferência (\w+)", description, re.IGNORECASE)
    result.tipo_movimentacao = tipo_match.group(1).upper() if tipo_match else "__TIPO_MOVIMENTACAO__"

    inst_match = re.search(r"([^-]+\.\d{3}\.\d{3}-[^-]+)-([^-]*.*)\(\d+\)", description)
    result.instituicao = inst_match.group(2).strip() if inst_match else "__INSTITUICAO__"

    codigo_match = re.search(r"\((\d+)\)", description)
    result.codigo_instituicao = codigo_match.group(1) if codigo_match else "__CODIGO_INSTITUICAO__"

    nome_match = re.search(r"-\s*(.+?)\s*-", description)
    result.nome_pessoa = f"{nome_match.group(1).strip().title()} ({result.codigo_instituicao})" if nome_match else "__NOME_PESSOA__"

    agencia_match = re.search(r"Agência:\s*(\d+)", description)
    result.agencia = agencia_match.group(1) if agencia_match else "__AGENCIA__"

    conta_match = re.search(r"Conta:\s*([\d\-]+)", description)
    result.conta = conta_match.group(1) if conta_match else "__CONTA__"

    return result

def process_payment(row):
    result = Row(identificador=row[2], data=row[0], valor=row[1], tipo_operacao="TRANSFERENCIA")
    description = row[-1]

    if re.search(r"([^,]*fatura[^,]*)", description, re.IGNORECASE):
        tipo_match = re.search(r"([^,]*fatura[^,]*)", description, re.IGNORECASE)
        result.tipo_movimentacao = tipo_match.group(1).upper() if tipo_match else "__TIPO_MOVIMENTACAO__"
    else:
        pass

    return result

def process_rdb(row):
    result = Row(identificador=row[2], data=row[0], valor=row[1], tipo_operacao="RDB")
    description = row[-1]

    tipo_match = re.search(r"(Resgate|Aplicação)\s+RDB", description, re.IGNORECASE)
    result.tipo_movimentacao = tipo_match.group(1).upper() if tipo_match else "__TIPO_MOVIMENTACAO__"

    return result
