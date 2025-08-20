from nota import Problema;

notas = []

notas.append(Problema("Ricardao", "problemão cabuloso", "alta"))
notas.append(Problema("Luizao", "probleminha buxa", "baixa"))

notas[0].info(0)
notas.pop(0)

nomeDoCliente = input("Nome do Cliente: ")
descricao = input("Descricao: ")
prioridade = input("Prioridade ")

notas.append(Problema(nomeDoCliente, descricao, prioridade))

for i, nota in enumerate(notas):
    nota.info(i)

