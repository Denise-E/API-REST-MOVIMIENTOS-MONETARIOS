from config.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    clientes = relationship('Cliente', secondary='categoria_cliente', overlaps="cuentas")
