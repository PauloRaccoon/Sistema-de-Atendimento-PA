import customtkinter as ctk
from listaChamados import ListaChamados, historico
from chamado import Chamado
from tkinter import messagebox, filedialog
import datetime

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 1. Configuração da Janela Principal ---
        self.title("Sistema de Atendimento ao Cliente")
        self.geometry("850x500")
        ctk.set_appearance_mode("dark")
        self.resizable(False, False)

        # --- 1.5. Variáveis de Controle e Listas do Back-end ---
        self.lista_ativos = ListaChamados()
        self.lista_concluidos = ListaChamados()
        self.lista_cancelados = ListaChamados()
        self.chamado_selecionado = None

        # Adicionando dados de teste
        self.lista_ativos.adicionar("Ana Silva", "Impressora não funciona", "Alta")
        self.lista_ativos.adicionar("Beto Costa", "PC muito lento", "Média")
        self.lista_ativos.adicionar("Carlos Dias", "Email não envia", "Baixa")
        self.lista_ativos.adicionar("Daniela Faria", "Monitor com listras", "Alta")

        # --- 2. Configuração do Grid (Layout) ---
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- 3. Criação dos Frames Principais ---
        self.frame_esquerda = ctk.CTkFrame(self)
        self.frame_esquerda.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_esquerda.grid_rowconfigure(0, weight=1) 
        self.frame_esquerda.grid_rowconfigure(1, weight=2) 
        self.frame_esquerda.grid_columnconfigure(0, weight=1)

        self.frame_direita = ctk.CTkFrame(self)
        self.frame_direita.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")

        # --- 3.5 Widgets do Frame da Esquerda ---
        self.painel_ativo = ctk.CTkFrame(self.frame_esquerda)
        self.painel_ativo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.scrollable_frame_chamados = ctk.CTkScrollableFrame(self.frame_esquerda, label_text="Próximos na Fila")
        self.scrollable_frame_chamados.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # --- 4. Adicionando os Botões no Frame da Direita ---
        self.btn_criar = ctk.CTkButton(self.frame_direita, text="Criar Chamado", command=self.abrir_janela_criar)
        self.btn_criar.pack(pady=23, padx=15, fill="x")
        self.btn_editar = ctk.CTkButton(self.frame_direita, text="Editar Chamado", command=self.abrir_janela_editar)
        self.btn_editar.pack(pady=23, padx=15, fill="x")
        # ... (resto dos botões)
        self.btn_cancelar = ctk.CTkButton(self.frame_direita, text="Cancelar Chamado", command=self.cancelar_chamado)
        self.btn_cancelar.pack(pady=23, padx=15, fill="x")
        self.btn_finalizar = ctk.CTkButton(self.frame_direita, text="Finalizar Atendimento", command=self.finalizar_atendimento)
        self.btn_finalizar.pack(pady=23, padx=15, fill="x")
        self.btn_relatorio = ctk.CTkButton(self.frame_direita, text="Gerar Relatório", command=self.gerar_relatorio)
        self.btn_relatorio.pack(pady=(23, 20), padx=15, fill="x")
        self.frame_botoes_mover = ctk.CTkFrame(self.frame_direita)
        self.frame_botoes_mover.pack(pady=23, padx=15, fill="x")
        self.frame_botoes_mover.grid_columnconfigure((0, 1), weight=1)
        self.btn_mover_cima = ctk.CTkButton(self.frame_botoes_mover, text="↑", command=self.mover_chamado_cima)
        self.btn_mover_cima.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        self.btn_mover_baixo = ctk.CTkButton(self.frame_botoes_mover, text="↓", command=self.mover_chamado_baixo)
        self.btn_mover_baixo.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        # --- 5. Inicialização da Interface (CORREÇÃO DO BUG 1) ---
        self.atualizar_lista_chamados()
        self.atualizar_painel_ativo()

    def gerar_relatorio(self):
        # 1. Abre a janela "Salvar Como..."
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                  filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        
        # Se o usuário cancelar, o filepath será vazio, então paramos a função
        if not filepath:
            return

        try:
            # 2. Abre o arquivo no modo de escrita ('w')
            with open(filepath, "w", encoding="utf-8") as file:
                # -- Cabeçalho --
                now = datetime.datetime.now()
                file.write("="*50 + "\n")
                file.write("RELATÓRIO DE ATENDIMENTO\n")
                file.write(f"Gerado em: {now.strftime('%d/%m/%Y %H:%M:%S')}\n")
                file.write("="*50 + "\n\n")

                # -- Histórico de Eventos --
                file.write("--- HISTÓRICO DE EVENTOS ---\n\n")
                if not historico:
                    file.write("Nenhum evento registrado nesta sessão.\n\n")
                else:
                    # Acessa a variável global 'historico' importada
                    for evento in historico:
                        file.write(evento) # Os eventos no histórico já têm "\n"
                
                file.write("\n")

                # -- Função auxiliar para escrever as listas --
                def escrever_lista(titulo, lista_de_chamados):
                    file.write(f"--- {titulo} ({len(lista_de_chamados)}) ---\n\n")
                    if len(lista_de_chamados) == 0:
                        file.write("Nenhum chamado nesta categoria.\n\n")
                    else:
                        ponteiro = lista_de_chamados._chamadoInicial
                        while ponteiro:
                            file.write(str(ponteiro) + "\n")
                            file.write("-" * 20 + "\n")
                            ponteiro = ponteiro.proximoChamado
                        file.write("\n")
                
                # -- Escreve cada lista de resumo --
                escrever_lista("RESUMO: CHAMADOS PENDENTES", self.lista_ativos)
                escrever_lista("RESUMO: CHAMADOS CONCLUÍDOS", self.lista_concluidos)
                escrever_lista("RESUMO: CHAMADOS CANCELADOS", self.lista_cancelados)
            
            # 3. Mostra mensagem de sucesso
            messagebox.showinfo("Sucesso", f"Relatório salvo com sucesso em:\n{filepath}")

        except Exception as e:
            # 4. Mostra mensagem de erro se algo der errado
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o arquivo:\n{e}")
    

    # --- FUNÇÕES DA INTERFACE ---
    def cancelar_chamado(self):
        # 1. Verificação Inicial: só funciona se um chamado estiver selecionado
        if not self.chamado_selecionado:
            messagebox.showinfo("Aviso", "Por favor, selecione um chamado para cancelar.")
            return

        # 2. A Caixa de Confirmação
        id_para_cancelar = self.chamado_selecionado.getId()
        nome_para_cancelar = self.chamado_selecionado.getNome()
        resposta = messagebox.askyesno("Confirmar Cancelamento",
                                       f"Tem certeza que deseja cancelar o chamado {id_para_cancelar} ({nome_para_cancelar})?")

        # 3. Executando a Lógica (se o usuário clicou "Sim")
        if resposta:
            # Remove da lista de ativos e o objeto é retornado
            chamado_removido = self.lista_ativos.cancelar(id_para_cancelar)
            # Adiciona o objeto retornado à lista de cancelados
            self.lista_cancelados.adicionar_objeto(chamado_removido)

            print(f"Chamado {chamado_removido.getId()} movido para a lista de cancelados.")
            print(f"Tamanho da lista de cancelados agora: {len(self.lista_cancelados)}")

            # Limpa a seleção e atualiza a tela
            self.chamado_selecionado = None
            self.atualizar_lista_chamados()
            self.atualizar_painel_ativo()

    def abrir_janela_criar(self):
        janela_criar = ctk.CTkToplevel(self)
        janela_criar.title("Criar Novo Chamado")
        janela_criar.geometry("400x450")
        janela_criar.transient(self)
        janela_criar.resizable(False, False)

        ctk.CTkLabel(janela_criar, text="Nome do Cliente:").pack(padx=20, pady=(10, 0), anchor="w")
        entry_nome = ctk.CTkEntry(janela_criar, placeholder_text="Digite o nome")
        entry_nome.pack(padx=20, pady=5, fill="x")
        ctk.CTkLabel(janela_criar, text="Descrição do Problema:").pack(padx=20, pady=(10, 0), anchor="w")
        entry_desc = ctk.CTkEntry(janela_criar, placeholder_text="Descreva o problema")
        entry_desc.pack(padx=20, pady=5, fill="x")
        ctk.CTkLabel(janela_criar, text="Prioridade:").pack(padx=20, pady=(10, 0), anchor="w")
        
        # --- CORREÇÃO DO BUG 2 ---
        combo_pri = ctk.CTkComboBox(janela_criar, values=["Baixa", "Média", "Alta"], state="readonly")
        combo_pri.pack(padx=20, pady=5, fill="x")
        combo_pri.set("Média")

        ctk.CTkLabel(janela_criar, text="Posição na Fila:").pack(padx=20, pady=(10, 0), anchor="w")
        tamanho = len(self.lista_ativos)
        opcoes_posicao = [str(i) for i in range(tamanho + 1)]
        
        # --- CORREÇÃO DO BUG 2 ---
        combo_pos = ctk.CTkComboBox(janela_criar, values=opcoes_posicao, state="readonly")
        combo_pos.pack(padx=20, pady=5, fill="x")
        combo_pos.set(str(tamanho))

        def salvar_novo_chamado():
            nome = entry_nome.get()
            descricao = entry_desc.get()
            prioridade = combo_pri.get()
            posicao = int(combo_pos.get())
            if not nome or not descricao:
                print("Erro: Nome e descrição são obrigatórios!")
                return
            if posicao == len(self.lista_ativos):
                self.lista_ativos.adicionar(nome, descricao, prioridade)
            else:
                self.lista_ativos.inserir(posicao, nome, descricao, prioridade)
            self.atualizar_lista_chamados()
            self.atualizar_painel_ativo() # Adicionado para limpar o painel de seleção
            janela_criar.destroy()

        btn_salvar = ctk.CTkButton(janela_criar, text="Salvar Chamado", command=salvar_novo_chamado)
        btn_salvar.pack(pady=20, padx=20)

    def atualizar_lista_chamados(self):
        for widget in self.scrollable_frame_chamados.winfo_children():
            widget.destroy()

        ponteiro = self.lista_ativos._chamadoInicial
        while ponteiro:
            texto = f"ID: {ponteiro.getId()} | {ponteiro.getNome()}"
            
            # --- CORREÇÃO DO BUG 3 ---
            # Lógica alterada para corrigir o erro da cor "default"
            command = lambda id=ponteiro.getId(): self.selecionar_chamado(id)
            if self.chamado_selecionado and self.chamado_selecionado.getId() == ponteiro.getId():
                # Botão SELECIONADO
                chamado_widget = ctk.CTkButton(self.scrollable_frame_chamados, text=texto,
                                               fg_color="blue", command=command)
            else:
                # Botão NÃO SELECIONADO (deixa a cor padrão do tema)
                chamado_widget = ctk.CTkButton(self.scrollable_frame_chamados, text=texto,
                                               command=command)
                                               
            chamado_widget.pack(pady=5, padx=10, fill="x")
            ponteiro = ponteiro.proximoChamado

    def selecionar_chamado(self, chamado_id):
        self.chamado_selecionado = self.lista_ativos.getChamado(chamado_id)
        print(f"Chamado ID {chamado_id} selecionado.")
        self.atualizar_painel_ativo()
        self.atualizar_lista_chamados()

    def atualizar_painel_ativo(self):
        for widget in self.painel_ativo.winfo_children():
            widget.destroy()
        if self.chamado_selecionado:
            ctk.CTkLabel(self.painel_ativo, text=f"ID: {self.chamado_selecionado.getId()}", font=("Arial", 14)).pack(anchor="w", padx=10)
            ctk.CTkLabel(self.painel_ativo, text=f"Nome: {self.chamado_selecionado.getNome()}", font=("Arial", 20, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(self.painel_ativo, text=f"Descrição: {self.chamado_selecionado.getDescricao()}", font=("Arial", 14)).pack(anchor="w", padx=10)
            ctk.CTkLabel(self.painel_ativo, text=f"Prioridade: {self.chamado_selecionado.getPrioridade()}", font=("Arial", 14)).pack(anchor="w", padx=10)
        else:
            ctk.CTkLabel(self.painel_ativo, text="Nenhum chamado selecionado", font=("Arial", 16)).pack(expand=True)

    def finalizar_atendimento(self):
        # 1. Verificação: agora checa se um chamado está SELECIONADO
        if not self.chamado_selecionado:
            messagebox.showinfo("Aviso", "Por favor, selecione um chamado para finalizar.")
            return

        # 2. Pega os dados do chamado selecionado e pede confirmação
        chamado_para_finalizar = self.chamado_selecionado
        resposta = messagebox.askyesno("Confirmar Finalização",
                                       f"Tem certeza que deseja finalizar o chamado {chamado_para_finalizar.getId()} ({chamado_para_finalizar.getNome()})?")

        # 3. Executando a Lógica (se o usuário clicou "Sim")
        if resposta:
            id_para_finalizar = chamado_para_finalizar.getId()

            # Remove da lista de ativos e o objeto é retornado
            chamado_finalizado = self.lista_ativos.concluir(id_para_finalizar)
            # Adiciona o objeto retornado à lista de concluídos
            self.lista_concluidos.adicionar_objeto(chamado_finalizado)

            print(f"Chamado {chamado_finalizado.getId()} movido para a lista de concluídos.")
            print(f"Tamanho da lista de concluídos agora: {len(self.lista_concluidos)}")

            # Limpa a seleção e atualiza a tela
            self.chamado_selecionado = None
            self.atualizar_lista_chamados()
            self.atualizar_painel_ativo()

    def abrir_janela_editar(self):
        # 1. Verificação Inicial
        if not self.chamado_selecionado:
            messagebox.showinfo("Aviso", "Por favor, selecione um chamado para editar.")
            return

        # 2. Criação da Janela Pop-up
        janela_editar = ctk.CTkToplevel(self)
        janela_editar.title("Editar Chamado")
        janela_editar.geometry("400x300")
        janela_editar.transient(self)
        janela_editar.resizable(False, False)

        # 3. Criação e Preenchimento dos Campos
        ctk.CTkLabel(janela_editar, text="Nome do Cliente:").pack(padx=20, pady=(10, 0), anchor="w")
        entry_nome = ctk.CTkEntry(janela_editar)
        entry_nome.insert(0, self.chamado_selecionado.getNome()) # Preenche com o nome atual
        entry_nome.pack(padx=20, pady=5, fill="x")

        ctk.CTkLabel(janela_editar, text="Descrição do Problema:").pack(padx=20, pady=(10, 0), anchor="w")
        entry_desc = ctk.CTkEntry(janela_editar)
        entry_desc.insert(0, self.chamado_selecionado.getDescricao()) # Preenche com a descrição atual
        entry_desc.pack(padx=20, pady=5, fill="x")

        ctk.CTkLabel(janela_editar, text="Prioridade:").pack(padx=20, pady=(10, 0), anchor="w")
        combo_pri = ctk.CTkComboBox(janela_editar, values=["Baixa", "Média", "Alta"], state="readonly")
        combo_pri.set(self.chamado_selecionado.getPrioridade()) # Seleciona a prioridade atual
        combo_pri.pack(padx=20, pady=5, fill="x")

        # 4. Lógica para Salvar as Alterações
        def salvar_alteracoes():
            novo_nome = entry_nome.get()
            nova_desc = entry_desc.get()
            nova_pri = combo_pri.get()

            # Chama os métodos de edição do back-end no objeto original
            self.lista_ativos.editarNome(novo_nome, self.chamado_selecionado)
            self.lista_ativos.editarDescricao(nova_desc, self.chamado_selecionado)
            self.lista_ativos.editarPrioridade(nova_pri, self.chamado_selecionado)

            # Atualiza a tela e fecha a janela de edição
            self.atualizar_lista_chamados()
            self.atualizar_painel_ativo()
            janela_editar.destroy()

        # 5. Botão de Salvar
        btn_salvar = ctk.CTkButton(janela_editar, text="Salvar Alterações", command=salvar_alteracoes)
        btn_salvar.pack(pady=20, padx=20)
    
    def mover_chamado_cima(self):
        if not self.chamado_selecionado:
            messagebox.showinfo("Aviso", "Por favor, selecione um chamado para mover.")
            return

        id_para_mover = self.chamado_selecionado.getId()
        self.lista_ativos.moverEsquerda(id_para_mover)
        
        # Apenas redesenha a lista na nova ordem
        self.atualizar_lista_chamados()

    def mover_chamado_baixo(self):
        if not self.chamado_selecionado:
            messagebox.showinfo("Aviso", "Por favor, selecione um chamado para mover.")
            return

        id_para_mover = self.chamado_selecionado.getId()
        self.lista_ativos.moverDireita(id_para_mover)
        
        # Apenas redesenha a lista na nova ordem
        self.atualizar_lista_chamados()
if __name__ == "__main__":
    app = App()
    app.mainloop()