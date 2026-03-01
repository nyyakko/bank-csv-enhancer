from dataclasses import dataclass, astuple

@dataclass
class Transaction:
    identificador: str | None = None
    data: str | None = None
    valor: str | None = None
    tipo_operacao: str | None = None
    tipo_movimentacao: str | None = None
    nome_pessoa: str | None = None
    instituicao: str | None = None
    codigo_instituicao: str | None = None
    agencia: str | None = None
    conta: str | None = None
    descricao: str | None = None

    def as_list(self): return list(astuple(self))
