from sqlalchemy import String, Integer, Enum as SQLEnum, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
import enum

class MechanicBucket(enum.Enum):
    FAGNE = "Premium_Fagne"
    APOIO = "Standard_Auxiliar"

class Base(DeclarativeBase):
    pass

class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    whatsapp_number: Mapped[str] = mapped_column(String(20), nullable=False)
    client_name: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Dados Técnicos da Moto
    motorcycle_model: Mapped[str] = mapped_column(String(100), nullable=False)
    displacement: Mapped[int] = mapped_column(Integer, nullable=False)
    cylinders: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Classificação e Controle
    assigned_to: Mapped[MechanicBucket] = mapped_column(SQLEnum(MechanicBucket), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Lead(name={self.client_name}, bike={self.motorcycle_model}, bucket={self.assigned_to})>"