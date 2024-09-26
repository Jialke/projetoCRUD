#Importar dados do models
from models import (Cliente, Contato, Produto, Categoria, Pedido, itensPedido, session)
import datetime

#Variaveis globais
continuar = True

#Funções
def add():
    print("\nMenu de adição de dados ao BD")
    tabela = int(input("Selecione em qual tabela deseja adicionar dados:\n[1] - Cliente\n[2] - Produto\n[3] - Categoria\n[4] - Pedido\n"))
    while tabela < 1 or tabela > 4:
        tabela = int(input("Valor inválido! Digite novamente: "))

    print()

    match tabela:
        #Cliente add
        case 1:
           novo_nome_cliente = input("Insira o nome do cliente: ")
           novo_email = input("Insira o e-mail (caso não tenha, simplesmente aperte enter): ")
           novo_cpf = input("Insira o cpf (ex: xxx.xxx.xxx.xx): ")
           nova_data_nasc = input("Insira a data de nascimento (dd-mm-yyyy): ")

           nova_data_formatada = datetime.datetime.strptime(nova_data_nasc, "%d-%m-%Y").date()

           novo_end_cidade = input("Insira a cidade: ")
           novo_end_estado = input("Insira a sigla do estado: ")
           novo_end_pais = input("Insira o país: ")
           novo_end_bairro = input("Insira o bairro: ")
           novo_end_logradouro = input("Insira o logradouro: ")

           cliente = Cliente(
               nome = novo_nome_cliente,
               cpf = novo_cpf,
               email = novo_email,
               data_nasc = nova_data_formatada,
               end_cidade = novo_end_cidade,
               end_bairro = novo_end_bairro,
               end_estado = novo_end_estado,
               end_pais = novo_end_pais,
               end_logradouro = novo_end_logradouro
            )
           
           #Adição de informação/informações na tabela de contatos
           selecaoContato = int(input("Quantos contatos deseja adicionar: "))
           while selecaoContato < 1:
               selecaoContato = int(input("Deve ser adicionado ao menos 1 contato: "))

           for i in range(selecaoContato):
               novo_telefone = input("Insira o telefone: ")

               contato = Contato(telefone= novo_telefone)
               cliente.contato.append(contato)
           
           session.add(cliente)
           session.commit()
           print()
        
        #Produto add
        case 2:
            novo_nome_produto = input("Insira o nome do produto: ")
            novo_valor = float(input("Insira o valor (maximo de 5 inteiros e 2 casas decimais): "))
            novo_descricao_produto = input("Insira uma descrição para o produto: ")
            
            #Listar categorias existentes para selecao
            print("Lista de categorias:")
            categorias = session.query(Categoria).all()
            for categoria in categorias:
                print(f"[{categoria.id}] - {categoria.nome}")

            novo_produto_categoria = int(input("Selecione o id da categoria do produto: "))
            novo_estoque = int(input("Insira a quantia do estoque: "))

            produto = Produto(
                nome = novo_nome_produto,
                valor_unit = novo_valor,
                estoque = novo_estoque,
                descricao = novo_descricao_produto,
                idcategoria = novo_produto_categoria
            )

            session.add(produto)
            session.commit()
            print()

        #Categoria add
        case 3:
            novo_nome_categoria = input("Insira o nome da categoria: ")
            nova_descricao_categoria = input("Insira uma descrição para a categoria: ")

            categoria = Categoria(
                nome = novo_nome_categoria,
                descricao = nova_descricao_categoria
            )

            session.add(categoria)
            session.commit()
            print()
        
        #Pedido add
        case 4:

            nova_data_entrega = input("Insira a data de entrega (dd-mm-yyyy): ")
            nova_entrega_formatada = datetime.datetime.strptime(nova_data_entrega, "%d-%m-%Y").date()

            #Lista de cliente
            clientes = session.query(Cliente).all()
            print("\nLista de clientes:")
            for cliente in clientes:
                print(f"[{cliente.id}] - {cliente.nome}")
            novo_pedido_cliente = int(input("Selecione o id do cliente: "))

            pedido = Pedido(
                data_entrega = nova_entrega_formatada,
                idcliente = novo_pedido_cliente
            )

            #itens do pedido
            compra = True #variavel booleana para realização de loop de seleção de produtos
            v_valor = [] #vetor usado para calcular o valor total do pedido
            while compra:
                produtos = session.query(Produto).all()
                print("\nLista de produtos:")
                for produto in produtos:
                    print(f"[{produto.id}] - {produto.nome}")
                novo_pedido_produto = int(input("Selecione um produto para comprar: "))
                nova_quant = int(input("Insira a quantidade: "))

                #Filtrar o produto selecionado por id para coletar seu valor unitário
                valor_por_id = session.query(Produto).filter_by(id=novo_pedido_produto).one_or_none()
                novo_valor_itens = nova_quant * valor_por_id.valor_unit
                v_valor.append(novo_valor_itens) #Acrescenta o vetor de soma para calcular o valor total do pedido

                itempedido = itensPedido(
                    quant = nova_quant,
                    valor_itens = novo_valor_itens,
                    idproduto = novo_pedido_produto,
                )

                pedido.itenspedido.append(itempedido)

                print()

                loop = int(input("Deseja selecionar mais produtos?\n[1] - Sim\n[2] - Não\n"))
                while loop < 1 or loop > 2:
                    loop = int(input("Valor inválido! Selecione novamente: "))
                if loop == 2:
                    compra = False
            
            #Somar vetor soma de valor
            soma_valor = sum(v_valor)
            pedido.valor_total = soma_valor

            session.add(pedido)
            session.commit()
            print()               

def read():
    print("\nMenu de leitura de dados ao BD")
    tabela = int(input("Selecione qual tabela deseja ler dados:\n[1] - Cliente\n[2] - Produto\n[3] - Categoria\n[4] - Pedido\n"))
    while tabela < 1 or tabela > 4:
        tabela = int(input("Valor inválido! Digite novamente: "))

    print()

    match tabela:
        case 1:
            print("Lista de clientes:")
            clientes = session.query(Cliente).all()
            for cliente in clientes:
                print(f"id: {cliente.id}\nnome: {cliente.nome}\ne-mail: {cliente.email}\nCPF: {cliente.cpf}\ndata_nasc: {cliente.data_nasc}\nend_cidade: {cliente.end_cidade}\nend_bairro: {cliente.end_bairro}\nend_estado: {cliente.end_estado}\nend_pais: {cliente.end_pais}\nend_logradouro: {cliente.end_logradouro}")

                #Listar contatos conectados ao cliente em questão
                contatos = session.query(Contato).filter_by(idcliente=cliente.id).all()
                for contato in contatos:
                    cont = 1
                    print(f"telefone {cont}: {contato.telefone}")
                    cont += 1

                print()

        case 2:
            print("Lista de produtos:")
            produtos = session.query(Produto).all()
            for produto in produtos:
                print(f"id: {produto.id}\nnome: {produto.nome}\nvalor unitário: {produto.valor_unit}\nestoque: {produto.estoque}\ndescrição: {produto.descricao}")

                #Mostra categoria do produto
                cat = session.query(Categoria).filter_by(id=produto.idcategoria).one_or_none()
                print(f"categoria: {cat.nome}")

                print()

        case 3:
            print("Lista de categorias:")
            categorias = session.query(Categoria).all()
            for categoria in categorias:
                print(f"id: {categoria.id}\ncategoria: {categoria.nome}\ndescrição: {categoria.descricao}")
                print()

        case 4:
            print("Lista de pedidos:")
            pedidos = session.query(Pedido).all()
            for pedido in pedidos:
                print(f"id: {pedido.id}\ndata do pedido: {pedido.data_pedido}\ndata de entraga: {pedido.data_entrega}")

                #Carrega itensPedido para listar os produtos conectados ao pedido
                itenspedido = session.query(itensPedido).filter_by(idpedido=pedido.id).all()
                for itempedido in itenspedido:
                    produtos = session.query(Produto).filter_by(id=itempedido.idproduto).all()
                    for produto in produtos:
                        print(f"produto: {produto.nome}, quantidade: {itempedido.quant}, valor unitário: {produto.valor_unit}, valor total: {itempedido.valor_itens}")

                print(f"valor total do pedido: {pedido.valor_total}")

                cliente = session.query(Cliente).filter_by(id=pedido.idcliente).one_or_none()
                print(f"cliente: {cliente.nome}")

                print()

def update():
    print("\nMenu de atualização de dados ao BD")
    tabela = int(input("Selecione em qual tabela deseja atualizar dados:\n[1] - Cliente\n[2] - Produto\n[3] - Categoria\n[4] - Pedido\n"))
    while tabela < 1 or tabela > 4:
        tabela = int(input("Valor inválido! Digite novamente: "))

    print()

    match tabela:
        case 1:
            #Cliente update
            clientes = session.query(Cliente).all()
            for cliente in clientes:
                print(f"[{cliente.id}] - {cliente.nome}")
            
            #Seleciona id
            att_id = int(input("Selecione o id do cliente: "))

            #Seleciona o campo da tabela
            campo = int(input("Selecione o que deseja alterar:\n[1] - nome\n[2] - e-mail\n[3] - cpf\n[4] - data_nasc\n[5] - cidade\n[6] - estado\n[7] - pais\n[8] - bairro\n[9] - logradouro\n[10] - contato\n"))
            while campo < 1 or campo > 10:
                campo = int(input("Valor inválido! Tente novamente: "))
            
            #Filtra a instância correta por id e faz o update de acordo com a seleção prévia
            cliente = session.query(Cliente).filter_by(id=att_id).one_or_none()
            match campo:
                case 1:
                    cliente.nome = input("Digite o nome: ")
                case 2:
                    cliente.email = input("Digite o e-mail: ")
                case 3:
                    cliente.cpf = input("Digite o CPF (ex: xxx.xxx.xxx.xx): ")
                case 4:
                    nova_data = input("Digite a data de nascimento (dd-mm-yyyy): ")
                    cliente.data_nasc = datetime.datetime.strptime(nova_data, "%d-%m-%Y").date()
                case 5:
                    cliente.end_cidade = input("Digite a cidade: ")
                case 6:
                    cliente.end_estado = input("Digite a sigla do Estado: ")
                case 7:
                    cliente.end_pais = input("Digite o país: ")
                case 8:
                    cliente.end_bairro = input("Digite o bairro: ")
                case 9:
                    cliente.end_logradouro = input("Digite o logradouro: ")
                case 10:
                    contatos = session.query(Contato).filter_by(idcliente=cliente.id).all()
                    print("Lista de contatos:")
                    for contato in contatos:
                        print(f"id: {contato.id}, telefone: {contato.telefone}")
                    id_contato = int(input("Selecione o id do telefone: "))

                    #query novamente para att o telefone correto
                    contato = session.query(Contato).filter_by(id=id_contato).one_or_none()
                    contato.telefone = input("Digite o telefone: ")
            
            session.commit
            print()

        case 2:
            #Produto update
            produtos = session.query(Produto).all()
            print("Lista de produtos")
            for produto in produtos:
                print(f"[{produto.id}] - {produto.nome}")

            #Seleciona id
            att_id = int(input("Selecione o id do produto para atualizar: "))

            #Seleciona o campo da tabela
            campo = int(input("Selecione o que deseja alterar:\n[1] - nome\n[2] - valor unitário\n[3] - estoque\n[4] - descrição\n[5] - categoria\n"))
            while campo < 1 or campo > 5:
                campo = int(input("Valor inválido! Tente novamente: "))

            #Filtra a instância correta por id e faz o update de acordo com a seleção prévia
            produto = session.query(Produto).filter_by(id=att_id).one_or_none()
            match campo:
                case 1:
                    produto.nome = input("Digite o nome: ")
                case 2:
                    produto.valor_unit = float(input("Digite o valor unitário: "))
                case 3:
                    produto.estoque = int(input("Digite a quantia em estoque: "))
                case 4:
                    produto.descricao = input("Digite a descrição: ")
                case 5:
                    categorias = session.query(Categoria).all()
                    print("Lista de categorias:")
                    for categoria in categorias:
                        print(f"[{categoria.id}] - {categoria.nome}")
                    produto.idcategoria = int(input("Digite o id da categoria: "))
            
            session.commit()
            print()

        case 3:
            #Categoria update
            categorias = session.query(Categoria).all()
            print("Lista de categorias:")
            for categoria in categorias:
                print(f"[{categoria.id}] - {categoria.nome}")

            #Seleciona id
            att_id = int(input("Digite o id da categoria para alterar: "))

            #Seleciona o campo da tabela
            campo = int(input("Selecione o que deseja alterar:\n[1] - nome\n[2] - descrição\n"))

            #Filtra a instância correta por id e faz o update de acordo com a seleção prévia
            categoria = session.query(Categoria).filter_by(id=att_id).one_or_none()
            match campo:
                case 1:
                    categoria.nome = input("Digite o nome: ")
                case 2:
                    categoria.descricao = input("Digite a descrição: ")

            session.commit()
            print()
        
        case 4:
            #Pedido update:
            pedidos = session.query(Pedido).all()
            for pedido in pedidos:
                print(f"[{pedido.id}] - data do pedido: {pedido.data_pedido}, idcliente: {pedido.idcliente}")

            #Seleciona id
            att_id = int(input("Selecione o id do pedido para alterar: "))

            #Seleciona o campo da tabela
            campo = (int(input("Selecione o que deseja alterar:\n[1] - data de entrega\n[2] - valor total\n[3] - itens do pedido\n")))

            #Filtra a instância correta por id e faz o update de acordo com a seleção prévia
            pedido = session.query(Pedido).filter_by(id=att_id).one_or_none()
            match campo:
                case 1:
                    nova_data = input("Digite a data de entrega (dd-mm-yyyy): ")
                    pedido.data_entrega = datetime.datetime.strptime(nova_data, "%d-%m-%Y").date()
                case 2:
                    pedido.valor_total = float(input("Digite o valor total: "))
                case 3:
                    itenspedido = session.query(itensPedido).filter_by(idpedido=att_id).all()
                    for itempedido in itenspedido:
                        print(f"[{itempedido.id}] - produto: {itempedido.idproduto}, quantidade: {itempedido.quant}")
                    
                    id_item = int(input("Selecione o id do item do pedido a ser alterado: "))

                    itempedido = session.query(itensPedido).filter_by(id=id_item).one_or_none()
                    
                    campo2 = int(input("Selecione o que deseja alterar:\n[1] - idproduto\n[2] - quantidade\n"))
                    match campo2:
                        case 1:
                            produtos = session.query(Produto).all()
                            for produto in produtos:
                                print(f"[{produto.id}] - {produto.nome}")
                            itempedido.idproduto = int(input("Selecione o id do produto"))

                        case 2:
                            itempedido.quant = int(input("Digite a quantidade: "))
                            
                    #Alterar valor total dos itens
                    produto = session.query(Produto).filter_by(id=itempedido.idproduto).one_or_none()
                    itempedido.valor_itens = itempedido.quant * produto.valor_unit

                    #Alterar valor total do pedido
                    v_valor = []
                    itenspedido = session.query(itensPedido).filter_by(idpedido=att_id).all()
                    for itempedido in itenspedido:
                        v_valor.append(itempedido.valor_itens)
                    total = sum(v_valor)
                    pedido.valor_total = total
                
            session.commit()
            print()

def delete():
    print("\nMenu de exclusão de dados ao BD")
    tabela = int(input("Selecione em qual tabela deseja deletar dados:\n[1] - Cliente\n[2] - Produto\n[3] - Categoria\n[4] - Pedido\n"))
    while tabela < 1 or tabela > 4:
        tabela = int(input("Valor inválido! Digite novamente: "))

    print()

    match tabela:
        case 1:
            #Cliente delete
            print("Lista de clientes:")
            clientes = session.query(Cliente).all()
            for cliente in clientes:
                print(f"[{cliente.id}] - {cliente.nome}")

            #Seleciona id
            del_id = int(input("Selecione o id do cliente: "))

            apagar = int(input("Certeza que deseja apagar essa instância?\n[1] - sim\n[2] - não\n"))
            while apagar < 1 or apagar > 2:
                apagar = int(input("Digite um valor valido: "))

            if apagar == 1:
                #Filtra a instância correta por id
                #apagar contato
                session.query(Contato).filter_by(idcliente=del_id).delete(synchronize_session=False)

                cliente = session.query(Cliente).filter_by(id=del_id).one_or_none()
                session.delete(cliente)
            
        case 2:
            #Produto delete
            print("Lista de produtos:")
            produtos = session.query(Produto).all()
            for produto in produtos:
                print(f"[{produto.id}] - {produto.nome}")
            
            #Seleciona id
            del_id = int(input("Selecione o id do produto: "))

            apagar = int(input("Certeza que deseja apagar essa instância?\n[1] - sim\n[2] - não\n"))
            while apagar < 1 or apagar > 2:
                apagar = int(input("Digite um valor valido: "))

            if apagar == 1:
                #Filtra a instância correta por id
                produto = session.query(Produto).filter_by(id=del_id).one_or_none()
                session.delete(produto)
        
        case 3:
            #Categoria delete
            print("Lista de categorias:")
            categorias = session.query(Categoria).all()
            for categoria in categorias:
                print(f"[{categoria.id}] - {categoria.nome}")
            
            #Seleciona id
            del_id = int(input("Selecione o id da categoria: "))

            apagar = int(input("Certeza que deseja apagar essa instância?\n[1] - sim\n[2] - não\n"))
            while apagar < 1 or apagar > 2:
                apagar = int(input("Digite um valor valido: "))

            if apagar == 1:
                #Filtra a instância correta por id
                categoria = session.query(Categoria).filter_by(id=del_id).one_or_none()
                session.delete(categoria)
        
        case 4:
            #Pedido delete
            pedidos = session.query(Pedido).all()
            for pedido in pedidos:
                print(f"[{pedido.id}] - data do pedido: {pedido.data_pedido}, idcliente: {pedido.idcliente}")
            
            #Seleciona id
            del_id = int(input("Selecione o id do pedido: "))

            apagar = int(input("Certeza que deseja apagar essa instância?\n[1] - sim\n[2] - não\n"))
            while apagar < 1 or apagar > 2:
                apagar = int(input("Digite um valor valido: "))

            if apagar == 1:
                #Filtra a instância correta por id
                #deletar itenspedidos
                session.query(itensPedido).filter_by(idpedido=del_id).delete(synchronize_session=False)

                pedido = session.query(Pedido).filter_by(id=del_id). one_or_none()
                session.delete(pedido)
        
    session.commit()
    print()

def selecionarAtividade():
    print("####################################")
    print("## CRUD do Banco de Dados de Loja ##")
    print("####################################")
    
    selecionar = int(input("\nSelecione qual operação deseja realizar:\n[1] - Adicionar\n[2] - Leitura\n[3] - Atualizar\n[4] - Deletar\n[5] - Sair\n"))
    while selecionar < 1 or selecionar > 5:
        selecionar = int(input("\nValor inválido! Digite novamente: "))

    match selecionar:
        case 1:
            return add()
        case 2:
            return read()
        case 3:
            return update()
        case 4:
            return delete()
        case 5:
            global continuar
            continuar = False

while continuar:
    selecionarAtividade()