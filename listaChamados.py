from chamado import Chamado

historico = []

class ListaChamados:

    def __init__(self):
        self._chamadoInicial = None
        self._tamanho = 0
    
    def __len__(self):
        return self._tamanho

    def adicionar(self, nomeCliente, descricao, prioridade):
        #Adiciona um novo Chamado no fim da lista
        if self._chamadoInicial:
            ponteiro = self._chamadoInicial
            while(ponteiro.proximoChamado):
                ponteiro = ponteiro.proximoChamado
            ponteiro.proximoChamado = Chamado(nomeCliente, descricao, prioridade)
            ponteiro.proximoChamado.chamadoAnterior = ponteiro
            a = "O chamado: \n" + str(ponteiro) + "\nfoi adicionado no final da lista.\n"
            historico.append(a)
        else:
            self._chamadoInicial = Chamado(nomeCliente, descricao, prioridade)
            a = "O chamado: \n" + str(self._chamadoInicial) + "\nfoi adicionado no final da lista.\n"
            historico.append(a)
        self._tamanho += 1
    
    def inserir(self, indice, nomeCliente, descricao, prioridade):
        novoChamado = Chamado(nomeCliente, descricao, prioridade)
        if indice == 0:
            novoChamado.proximoChamado = self._chamadoInicial
            if novoChamado.proximoChamado:
                self._chamadoInicial.chamadoAnterior = novoChamado
            self._chamadoInicial = novoChamado
        else:
            ponteiro = self.getChamado(indice-1)
            novoChamado.proximoChamado = ponteiro.proximoChamado
            novoChamado.chamadoAnterior = ponteiro
            if ponteiro.proximoChamado:
                ponteiro.proximoChamado.chamadoAnterior = novoChamado
            ponteiro.proximoChamado = novoChamado
        self._tamanho += 1
        a = "O chamado: \n" + str(novoChamado) + "\nfoi adicionado na lista na posição " + str(indice) + ".\n"
        historico.append(a)
    
    def getChamado(self, identificador):
        ponteiro = self._chamadoInicial
        if isinstance(identificador, int):
            for i in range(identificador):
                if ponteiro:
                    ponteiro = ponteiro.proximoChamado
                else:
                    raise IndexError("Índice fora do intervalo da lista")
        elif isinstance(identificador, str):
            while(ponteiro):
                if ponteiro.getId() == identificador:
                    break
                ponteiro = ponteiro.proximoChamado
            if ponteiro == None:
                raise IndexError("ID não encontrado na lista")
        return ponteiro
    
    def getPosicao(self, identificador):
        ponteiro = self._chamadoInicial
        indice = 0
        while(ponteiro):
            if ponteiro.getId() == str(identificador):
                return indice
            ponteiro = ponteiro.proximoChamado
            indice += 1
        raise IndexError("ID não encontrado na lista")
    
    def remover(self, identificador):
        if self._chamadoInicial == None:
            raise ValueError("{} não está na lista".format(identificador))
        if self._chamadoInicial.getId() == identificador or identificador == 0:
            self._chamadoInicial = self._chamadoInicial.proximoChamado
            if  self._chamadoInicial:
                self._chamadoInicial.chamadoAnterior = None
            self._tamanho = self._tamanho - 1
            return True
        ponteiro = self.getChamado(identificador)
        if ponteiro:
            ponteiro.chamadoAnterior.proximoChamado = ponteiro.proximoChamado
            if ponteiro.proximoChamado:
                ponteiro.proximoChamado.chamadoAnterior = ponteiro.chamadoAnterior
            self._tamanho = self._tamanho - 1
            return True
        raise ValueError("{} não está na lista".format(identificador))
    
    def moverEsquerda(self, identificador): # move para cima
        ponteiro = self.getChamado(identificador)
        
        # Só podemos mover se o ponteiro existir e não for o primeiro da lista
        if ponteiro and ponteiro.chamadoAnterior:
            anterior = ponteiro.chamadoAnterior
            proximo = ponteiro.proximoChamado
            avo = anterior.chamadoAnterior

            # Religa o avô (se existir) ao ponteiro
            if avo:
                avo.proximoChamado = ponteiro
            ponteiro.chamadoAnterior = avo

            # Religa o próximo (se existir) ao anterior
            if proximo:
                proximo.chamadoAnterior = anterior
            anterior.proximoChamado = proximo

            # Troca o ponteiro e o anterior de lugar
            ponteiro.proximoChamado = anterior
            anterior.chamadoAnterior = ponteiro

            # Se o 'anterior' era o início da lista, o 'ponteiro' é o novo início
            if self._chamadoInicial == anterior:
                self._chamadoInicial = ponteiro
            
            # Adiciona ao histórico
            a = f"O chamado ID {ponteiro.getId()} foi movido para cima.\n"
            historico.append(a)

    # Substitua a sua função moverDireita por esta:
    def moverDireita(self, identificador): # move para baixo
        ponteiro = self.getChamado(identificador)

        # Só podemos mover se o ponteiro existir e não for o último da lista
        if ponteiro and ponteiro.proximoChamado:
            proximo = ponteiro.proximoChamado
            anterior = ponteiro.chamadoAnterior
            neto = proximo.proximoChamado

            # Religa o anterior (se existir) ao proximo
            if anterior:
                anterior.proximoChamado = proximo
            proximo.chamadoAnterior = anterior

            # Religa o neto (se existir) ao ponteiro
            if neto:
                neto.chamadoAnterior = ponteiro
            ponteiro.proximoChamado = neto

            # Troca o ponteiro e o proximo de lugar
            proximo.proximoChamado = ponteiro
            ponteiro.chamadoAnterior = proximo

            # Se o 'ponteiro' era o início da lista, o 'proximo' é o novo início
            if self._chamadoInicial == ponteiro:
                self._chamadoInicial = proximo
            
            # Adiciona ao histórico
            a = f"O chamado ID {ponteiro.getId()} foi movido para baixo.\n"
            historico.append(a)
    
    # Dentro da classe ListaChamados

    def concluir(self, identificador):
        ponteiro = self.getChamado(identificador)
        if ponteiro:
            a = "O chamado: \n" + str(ponteiro) + "\nfoi concluído.\n"
            historico.append(a)
            self.remover(identificador)
            return ponteiro # Adicionar esta linha

    def cancelar(self, identificador):
        ponteiro = self.getChamado(identificador)
        if ponteiro:
            a = "O chamado: \n" + str(ponteiro) + "\nfoi cancelado.\n"
            historico.append(a)
            self.remover(identificador)
            return ponteiro # Adicionar esta linha
        
    def editarNome(self, novoNome, chamado):
        a = "O nome do chamado de ID " + chamado.getId() + " foi alterado de "
        a = a + chamado.getNome() + " para " + novoNome
        historico.append(a)
        chamado.setNome(novoNome)
        
        # Dentro da classe ListaChamados

    def editarDescricao(self, novaDescricao, chamado):
        a = "A descrição do chamado de ID " + chamado.getId() + " foi alterado de " # Correção: Usei getId() aqui, pois getI() não existe
        a = a + chamado.getDescricao() + " para " + novaDescricao + "."
        historico.append(a)
        chamado.setDescricao(novaDescricao) # CORRIGIDO

    def editarPrioridade(self, novaPrioridade, chamado):
        a = "A prioridade do chamado de ID " + chamado.getId() + " foi alterado de " # Correção: Usei getId() aqui
        a = a + chamado.getPrioridade() + " para " + novaPrioridade + "."
        historico.append(a)
        chamado.setPrioridade(novaPrioridade) # CORRIGIDO

        # Em listaChamados.py
    # Adicione esta nova função na classe

    # Em listaChamados.py

    # Substitua a sua função adicionar_objeto por esta:
    def adicionar_objeto(self, chamado_existente):
        # !!! CORREÇÃO CRÍTICA: Reseta os ponteiros do chamado antes de adicioná-lo !!!
        chamado_existente.proximoChamado = None
        chamado_existente.chamadoAnterior = None

        # Adiciona um objeto Chamado já criado no fim da lista
        if self._chamadoInicial:
            ponteiro = self._chamadoInicial
            while(ponteiro.proximoChamado):
                ponteiro = ponteiro.proximoChamado
            ponteiro.proximoChamado = chamado_existente
            chamado_existente.chamadoAnterior = ponteiro
        else:
            self._chamadoInicial = chamado_existente
        self._tamanho += 1