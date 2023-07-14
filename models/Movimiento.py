from config.database import Base
from sqlalchemy import Column, ForeignKey, Integer,Float, DateTime


class Movimiento(Base):
    __tablename__ = "movimientos"  

    id = Column(Integer, primary_key=True, index=True)
    id_cuenta = Column(Integer, ForeignKey("cuentas.id"), nullable=False)
    tipo = Column(Integer, ForeignKey("tipo_movimiento.id"), nullable=False)
    importe = Column(Float, nullable=False)
    fecha = Column(DateTime, nullable=False)
