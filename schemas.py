from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum

class MechanicBucket(str, Enum):
    FAGNE = "Premium_Fagne"
    APOIO = "Standard_Auxiliar"

class LeadCreate(BaseModel):
    whatsapp_number: str = Field(..., example="5567999999999")
    client_name: Optional[str] = "Cliente WhatsApp"
    motorcycle_model: str = Field(..., example="BMW F850GS")
    displacement: int = Field(..., gt=0)
    cylinders: int = Field(..., gt=0)

    # A lógica de triagem é processada na validação do Schema
    def get_assigned_bucket(self) -> MechanicBucket:
        # Bucket B: Monocilíndricas OU (< 250cc e <= 2 cilindros)
        if self.cylinders == 1:
            return MechanicBucket.APOIO
        if self.cylinders <= 2 and self.displacement < 250:
            return MechanicBucket.APOIO
        
        # Bucket A: >= 2 cilindros e >= 300cc
        if self.cylinders >= 2 and self.displacement >= 300:
            return MechanicBucket.FAGNE
            
        # Fallback de segurança para o mecânico de apoio
        return MechanicBucket.APOIO

class LeadResponse(LeadCreate):
    id: int
    assigned_to: MechanicBucket

    class Config:
        from_attributes = True