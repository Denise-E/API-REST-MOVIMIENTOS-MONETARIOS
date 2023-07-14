from config.database import Base
from sqlalchemy import Column, ForeignKey, Integer


class Categoria_Cliente(Base):
    __tablename__ = "categoria_cliente"

    id_categoria = Column(Integer, ForeignKey("categorias.id"), primary_key=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), primary_key=True)

