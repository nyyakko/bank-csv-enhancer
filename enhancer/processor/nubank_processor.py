from .core.iprocessor import IProcessor
from .core.transaction import Transaction

import csv, re, os, uuid

_DEFAULT_HEADERS = ["Data", "Valor", "Identificador", "Descrição"]

class NubankProcessor(IProcessor):
    def process(self, csvFile):
        reader = csv.reader(csvFile, delimiter=",", quotechar="|")

        headers = next(reader)
        if headers != _DEFAULT_HEADERS:
            raise RuntimeError(f"O arquivo recebido \"{csvFile.name}\" não parece ser um extrato válido do Nubank")

        transactions = []

        for row in reader:
            transaction = {}

            if re.search(r"Estorno", row[-1], re.IGNORECASE):
                transaction = process_refund(row)
                transaction.descricao = f"Estorno {"de" if float(transaction.valor) > 0 else "para"} {transaction.nome_pessoa}"
            elif re.search(r"Transferência", row[-1], re.IGNORECASE):
                transaction = process_transfer(row)
                transaction.descricao = f"Transferência {"de" if float(transaction.valor) > 0 else "para"} {transaction.nome_pessoa}"
            elif re.search(r"Pagamento", row[-1], re.IGNORECASE):
                transaction = process_payment(row)
                transaction.descricao = f"{transaction.tipo_movimentacao.replace("_", " ").title()}"
            elif re.search(r"Compra", row[-1], re.IGNORECASE):
                transaction = process_purchase(row)
                transaction.descricao = f"Compra em {transaction.tipo_movimentacao.title()}"
            elif re.search(r"(Resgate|Aplicação)\s+RDB", row[-1], re.IGNORECASE):
                transaction = process_rdb(row)
                transaction.descricao = f"{transaction.tipo_movimentacao.title()} RDB"
            else:
                print(f"[AVISO] Pulando transação: {row[2]}")
                continue

            transactions.append(transaction)

        return transactions

def process_transfer(row):
    result = Transaction(identificador=row[2], data=row[0], valor=row[1], tipo_operacao="TRANSFERENCIA")
    description = row[-1]

    tipo_match = re.search(r"Transferência (\w+)", description, re.IGNORECASE)
    result.tipo_movimentacao = tipo_match.group(1).upper() if tipo_match else "__TIPO_MOVIMENTACAO__"

    inst_match = re.search(r"([^-]+\.\d{3}\.\d{3}-[^-]+|[^-]+\d{2}\.\d{3}\.\d{3}\/\d{4}-[^-]+)-([^-]*.*)(\(\d+\)|Agência)", description)
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

def process_refund(row):
    result = Transaction(identificador=str(uuid.uuid5(uuid.NAMESPACE_DNS, " ".join(row))), data=row[0], valor=row[1], tipo_operacao="ESTORNO")
    description = row[-1]

    tipo_match = re.search(r"Transferência (\w+)", description, re.IGNORECASE)
    result.tipo_movimentacao = tipo_match.group(1).upper() if tipo_match else "__TIPO_MOVIMENTACAO__"

    inst_match = re.search(r"([^-]+\.\d{3}\.\d{3}-[^-]+|[^-]+\d{2}\.\d{3}\.\d{3}\/\d{4}-[^-]+)-([^-]*.*)\(\d+\)", description)
    result.instituicao = inst_match.group(2).strip() if inst_match else "__INSTITUICAO__"

    codigo_match = re.search(r"\((\d+)\)", description)
    result.codigo_instituicao = codigo_match.group(1) if codigo_match else "__CODIGO_INSTITUICAO__"

    nome_match = re.search(r"-\s*(.+?)\s*-\s*(.+?)\s*-([^-]+\.\d{3}\.\d{3}-[^-]+|[^-]+\d{2}\.\d{3}\.\d{3}\/\d{4}-[^-]+)", description)
    result.nome_pessoa = f"{nome_match.group(2).strip().title()} ({result.codigo_instituicao})" if nome_match else "__NOME_PESSOA__"

    agencia_match = re.search(r"Agência:\s*(\d+)", description)
    result.agencia = agencia_match.group(1) if agencia_match else "__AGENCIA__"

    conta_match = re.search(r"Conta:\s*([\d\-]+)", description)
    result.conta = conta_match.group(1) if conta_match else "__CONTA__"

    return result

def process_payment(row):
    result = Transaction(identificador=row[2], data=row[0], valor=row[1], tipo_operacao="TRANSFERENCIA")
    description = row[-1]

    if re.search(r"([^,]*crédito)", description, re.IGNORECASE):
        tipo_match = re.search(r"([^,]*crédito)", description, re.IGNORECASE)
    elif re.search(r"([^,]*boleto)", description, re.IGNORECASE):
        tipo_match = re.search(r"([^,]*boleto)", description, re.IGNORECASE)
    else:
        pass

    result.tipo_movimentacao = (tipo_match.group(1).upper() if tipo_match else "__TIPO_MOVIMENTACAO__").replace(" ", "_")

    return result

def process_rdb(row):
    result = Transaction(identificador=row[2], data=row[0], valor=row[1], tipo_operacao="RDB")
    description = row[-1]

    tipo_match = re.search(r"(Resgate|Aplicação)\s+RDB", description, re.IGNORECASE)
    result.tipo_movimentacao = tipo_match.group(1).upper() if tipo_match else "__TIPO_MOVIMENTACAO__"

    return result

def process_purchase(row):
    result = Transaction(identificador=row[2], data=row[0], valor=row[1], tipo_operacao="COMPRA")
    description = row[-1]

    if re.search(r"débito", description, re.IGNORECASE):
        result.tipo_movimentacao = "DÉBITO"
    else:
        pass

    nome_match = re.search(r"([^,]*débito)\s-\s(.+)", description)
    result.nome_pessoa = f"{nome_match.group(2).strip().title()}" if nome_match else "__NOME_PESSOA__"

    return result
