class Chamado:
    contador = 1
    def __init__(self, nomeCliente, descricao, prioridade):
        self._id = str(Chamado.contador)
        self._nomeCliente = nomeCliente
        self._descricao = descricao
        self._prioridade = prioridade

        self.proximoChamado = None
        self.chamadoAnterior = None
        Chamado.contador += 1

    def __str__(self):
        return f"ID: {self._id} \nCliente: {self._nomeCliente} \nDescrição: {self._descricao} \nPrioridade: {self._prioridade}"
    
    def editarChamado(self, novoNome, novaDesc, novaPrioridade):
        self._nomeCliente = novoNome
        self._descricao = novaDesc
        self._prioridade = novaPrioridade
        print("Chamado Atualizado!!!")
    
    def setNome(self, novoNome):
        self._nomeCliente = novoNome
    
    def getNome(self):
        return self._nomeCliente

    def setDescricao(self, novaDescricao):
        self._descricao = novaDescricao
    
    def getDescricao(self):
        return self._descricao
    
    def setPrioridade(self, novaPrioridade):
        self._prioridade = novaPrioridade
    
    def getPrioridade(self):
        return self._prioridade
    
    def setProximoChamado(self, novaProximoChamado):
        self.proximoChamado = novaProximoChamado
    
    def getProximoChamado(self):
        return self.proximoChamado
    
    def getChamadoAnterior(self):
        return self.chamadoAnterior

    def getId(self):
        return self._id