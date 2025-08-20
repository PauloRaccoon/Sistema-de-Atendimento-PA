class Problema:
    def __init__(self, nomeCliente, descricao, prioridade):
        self.nomeCliente = nomeCliente
        self.descricao = descricao
        self.prioridade = prioridade

    def info(self, indice):
        print(f"{indice} - {self.nomeCliente} - {self.descricao} - {self.prioridade}", flush=True)



