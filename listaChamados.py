from chamado import Chamado

historico = []

class ListaChamados:

    def __init__(self): #Cria uma lista encadeada
        self._chamadoInicial = None
        self._tamanho = 0
    
    def __len__(self): #Retorna o tamanho da lista
        return self._tamanho

    def adicionar(self, nomeCliente, descricao, prioridade):
        #Adiciona um novo Chamado no fim da lista
        if self._chamadoInicial: #Verdadeiro se houver um chamado na lista
            ponteiro = self._chamadoInicial
            while(ponteiro.proximoChamado):
                ponteiro = ponteiro.proximoChamado
            ponteiro.proximoChamado = Chamado(nomeCliente, descricao, prioridade)
            ponteiro.proximoChamado.chamadoAnterior = ponteiro
            a = "\nO chamado: \n" + str(ponteiro) + "\nfoi adicionado no final da lista.\n"
        else: #Se não houver nenhum chamado na lista
            self._chamadoInicial = Chamado(nomeCliente, descricao, prioridade)
            a = "\nO chamado: \n" + str(self._chamadoInicial) + "\nfoi adicionado na lista.\n"
        historico.append(a) #Registra ação no histórico
        #print(historico)
        self._tamanho += 1 #Aumenta o tamanho da lista
    
    def inserir(self, indice, nomeCliente, descricao, prioridade):
        #Adiciona um novo chamado em uma posição específica da lista
        novoChamado = Chamado(nomeCliente, descricao, prioridade)
        if indice == 0: #Se for no inserido no início da lista
            novoChamado.proximoChamado = self._chamadoInicial
            if novoChamado.proximoChamado:
                self._chamadoInicial.chamadoAnterior = novoChamado
            self._chamadoInicial = novoChamado
        else:
            ponteiro = self.getChamado(indice-1) #Pega o chamado na posição anterior aonde o novo chamado serpa inserido 
            novoChamado.proximoChamado = ponteiro.proximoChamado
            novoChamado.chamadoAnterior = ponteiro
            if ponteiro.proximoChamado:
                ponteiro.proximoChamado.chamadoAnterior = novoChamado
            ponteiro.proximoChamado = novoChamado
        self._tamanho += 1 #Aumenta o tamanho da lista
        a = "\nO chamado: \n" + str(novoChamado) + "\nfoi adicionado na lista na posição " + str(indice) + ".\n"
        historico.append(a) #Registra ação no histórico
    
    def getChamado(self, identificador): #Busca um chamado específico a partir da posição ou ID
        ponteiro = self._chamadoInicial
        if isinstance(identificador, int): #Se o identificadoe for tipo inteiro, tradado como indice de posição
            for i in range(identificador):
                if ponteiro:
                    ponteiro = ponteiro.proximoChamado
                else:
                    raise IndexError("Índice fora do intervalo da lista")
        elif isinstance(identificador, str): #Se for tipo string, tradado como ID do chamado
            while(ponteiro):
                if ponteiro.getId() == identificador:
                    break
                ponteiro = ponteiro.proximoChamado
            if ponteiro == None:
                raise IndexError("ID não encontrado na lista")
        return ponteiro #Retorna o chamado buscado
    
    def getPosicao(self, identificador): #Retorna a posição (indice) de um chamado a partir do seu ID
        ponteiro = self._chamadoInicial
        indice = 0
        while(ponteiro):
            if ponteiro.getId() == str(identificador):
                return indice #retorna posição
            ponteiro = ponteiro.proximoChamado
            indice += 1
        raise IndexError("ID não encontrado na lista")
    
    def remover(self, identificador): #Remove um chamado da lista
        if self._chamadoInicial == None:
            raise ValueError("{} não está na lista".format(identificador))
        if self._chamadoInicial.getId() == identificador or identificador == 0: #Se o chamado a ser removido estiver no início da lista
            self._chamadoInicial = self._chamadoInicial.proximoChamado
            if  self._chamadoInicial:
                self._chamadoInicial.chamadoAnterior = None
            self._tamanho = self._tamanho - 1 #Diminui o tamanho da lista
            return True #Retorna verdadeiro 
        ponteiro = self.getChamado(identificador) #Pega o chamado
        if ponteiro: #Se o chamado estiver na lista
            ponteiro.chamadoAnterior.proximoChamado = ponteiro.proximoChamado
            if ponteiro.proximoChamado:
                ponteiro.proximoChamado.chamadoAnterior = ponteiro.chamadoAnterior
            self._tamanho = self._tamanho - 1 #Diminui o tamanho da lista
            return True #Retorna verdadeiro
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
            a = f"O chamado de ID {ponteiro.getId()} foi movido para cima.\n"
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
            a = f"O chamado de ID {ponteiro.getId()} foi movido para baixo.\n"
            historico.append(a)
    
    # Dentro da classe ListaChamados

    def concluir(self, identificador): #Conclui um chamado
        ponteiro = self.getChamado(identificador) #Pega o chamado
        if ponteiro:
            a = "\nO seguinte chamado foi concluído.: \n" + str(ponteiro) + "\n\n"
            historico.append(a) #Registra ação no histórico
            self.remover(identificador) #Remove o chamado da lista
            return ponteiro # Adicionar esta linha

    def cancelar(self, identificador): #Cancela um chamado
        ponteiro = self.getChamado(identificador) #Pega o chamado
        if ponteiro:
            a = "\nO seguinte chamado foi cancelado.: \n" + str(ponteiro) + "\n\n"
            historico.append(a) #Registra ação no histórico
            self.remover(identificador) #Remove o chamado da lista
            return ponteiro # Adicionar esta linha
        
    def editarNome(self, novoNome, chamado): #Edita o nome do chamado
        a = "O nome do chamado de ID " + chamado.getId() + " foi alterado de "
        a = a + chamado.getNome() + " para " + novoNome + ". \n"
        historico.append(a) #Registra ação no histórico
        chamado.setNome(novoNome)
        
        # Dentro da classe ListaChamados

    def editarDescricao(self, novaDescricao, chamado): #Edita a descrição do chamado
        a = "A descrição do chamado de ID " + chamado.getId() + " foi alterado de " # Correção: Usei getId() aqui, pois getI() não existe
        a = a + chamado.getDescricao() + " para " + novaDescricao + ". \n"
        historico.append(a) #Registra ação no histórico
        chamado.setDescricao(novaDescricao) # CORRIGIDO

    def editarPrioridade(self, novaPrioridade, chamado): #Edita prioridade do chamado
        a = "A prioridade do chamado de ID " + chamado.getId() + " foi alterado de " # Correção: Usei getId() aqui
        a = a + chamado.getPrioridade() + " para " + novaPrioridade + ". \n"
        historico.append(a) #Registra ação no histórico
        chamado.setPrioridade(novaPrioridade) # CORRIGIDO

        # Em listaChamados.py
    # Adicione esta nova função na classe

    # Em listaChamados.py

    # Substitua a sua função adicionar_objeto por esta:
    def adicionar_objeto(self, chamado_existente):# Usado para adicionar um chamado removido de uma lista para outra
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
