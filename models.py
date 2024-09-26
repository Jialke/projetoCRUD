#Importar sqlalchemy
from sqlalchemy import Column, Integer, String, Date, DateTime, DECIMAL, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

#Conexão com banco de dados
db_url = "sqlite:///database.db"

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

#Criação de tabelas

class Contato(Base):
    __tablename__ = "contatos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telefone = Column(String(20))
    idcliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="contato")

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key = True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String(30))
    cpf = Column(String(14), nullable=False)
    data_nasc = Column(Date, nullable=False)
    end_cidade = Column(String(50), nullable=False)
    end_bairro = Column(String(50), nullable=False)
    end_estado = Column(String(2), nullable=False)
    end_pais = Column(String(30), nullable=False)
    end_logradouro = Column(String(50), nullable=False)

    contato = relationship("Contato", back_populates="cliente")
    pedido = relationship("Pedido", back_populates="cliente")

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    valor_unit = Column(DECIMAL(5,2), nullable=False)
    estoque = Column(Integer)
    descricao = Column(String(100))
    idcategoria = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    categoria = relationship("Categoria", back_populates="produto")
    itenspedido = relationship("itensPedido", back_populates="produto")

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(100))

    produto = relationship("Produto", back_populates="categoria")

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_pedido = Column(DateTime(timezone=True), default=func.now())
    data_entrega = Column(Date, nullable=False)
    valor_total = Column(DECIMAL(8,2), nullable=False)

    idcliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="pedido")
    itenspedido = relationship("itensPedido", back_populates="pedido")

class itensPedido(Base):
    __tablename__ = "itensPedido"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quant = Column(Integer, nullable=False)
    valor_itens = Column(DECIMAL(8,2), nullable=False)

    idpedido = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    idproduto = Column(Integer, ForeignKey("produtos.id"), nullable=False)

    pedido = relationship("Pedido", back_populates="itenspedido")
    produto = relationship("Produto", back_populates="itenspedido")

#Executar criação do db
Base.metadata.create_all(engine)