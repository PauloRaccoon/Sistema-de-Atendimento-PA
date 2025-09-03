class Chamado:
    contador = 1
    def __init__(self, nomeCliente, descricao, prioridade):#Cria um objeto de Chamado
        self._id = str(Chamado.contador)
        self._nomeCliente = nomeCliente
        self._descricao = descricao
        self._prioridade = prioridade

        self.proximoChamado = None
        self.chamadoAnterior = None
        Chamado.contador += 1

    def __str__(self): #Permite que o objeto de Chamado seja usada em print e/ou transformada em string
        return f"ID: {self._id} \nCliente: {self._nomeCliente} \nDescrição: {self._descricao} \nPrioridade: {self._prioridade} \n"
    
    def editarChamado(self, novoNome, novaDesc, novaPrioridade):
        #Atualiza todas as informações básicas do objeto
        self._nomeCliente = novoNome
        self._descricao = novaDesc
        self._prioridade = novaPrioridade
    
    def setNome(self, novoNome):
        #Atualiza o nome do objeto
        self._nomeCliente = novoNome
    
    def getNome(self):
        #Retorna o nome do objeto
        return self._nomeCliente

    def setDescricao(self, novaDescricao):
        #Atualiza a descrição do objeto
        self._descricao = novaDescricao
    
    def getDescricao(self):
        #Retorna a descrição do objeto
        return self._descricao
    
    def setPrioridade(self, novaPrioridade):
        #Atualiza a prioridade do objeto
        self._prioridade = novaPrioridade
    
    def getPrioridade(self):
        #Retorna a prioridade do objeto
        return self._prioridade
    
    def setProximoChamado(self, novaProximoChamado):
        #Atualiza a referência ao próximo objeto da lista nesse objeto
        self.proximoChamado = novaProximoChamado
    
    def getProximoChamado(self):
        #Retorna a referência ao próximo objeto da lista nesse objeto
        return self.proximoChamado
    
    def getChamadoAnterior(self):
        #Atualiza a referência ao objeto anterior da lista nesse objeto
        return self.chamadoAnterior

    def getId(self):
        #Retorna o ID do objeto
        return self._id
