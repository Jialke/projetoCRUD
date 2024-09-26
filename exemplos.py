from models import (Cliente, Contato, Produto, Categoria, session)
import datetime

#Implementação de dados base na tabela
#cliente exemplo
data_ex_cliente = datetime.datetime.strptime("19-09-2000", "%d-%m-%Y").date()
cliente1 = Cliente(
    nome = "Paulo Machado",
    email = "Paulo@hotmail.com",
    cpf = "123.123.321.11",
    data_nasc = data_ex_cliente,
    end_cidade = "Curitiba",
    end_bairro = "Juveve",
    end_estado = "PR",
    end_pais = "Brasil",
    end_logradouro = "Rua Aleatoria"
)

#contato exemplo
contato1 = Contato(
    telefone = "99876-9450"
)

cliente1.contato.append(contato1)
session.add(cliente1)

#Categoria exemplo
categoria1 = Categoria(
    nome = "Calças",
    descricao = "Variedade de calças de todos os tamanhos"
)
categoria2 = Categoria(
    nome = "Camisas",
    descricao = "Camisetas com ou sem estampas, para crianças ou adultos"
)
categoria3 = Categoria(
    nome = "Vestidos",
    descricao = "Vestidos longos para as mais variadas situações, desde casuais à vestidos de gala"
)

session.add_all([categoria1, categoria2, categoria3])

#Produto exemplo
produto1 = Produto(
    nome = "Camiseta de manga longa preta basica",
    valor_unit = 55.90,
    estoque = 10,
    descricao = "Camiseta preta basica de manga longa, tamanho M, feito com um tecido de alta qualidade.",
    idcategoria = 2
)
produto2 = Produto(
    nome = "Vestido bordado branco",
    valor_unit = 130.99,
    estoque = 50,
    descricao = "Vestido chique bordado branco com estampas floridas. Tamanho P",
    idcategoria = 3
)
session.add_all([produto1, produto2])

session.commit()