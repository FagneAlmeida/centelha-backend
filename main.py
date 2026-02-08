from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, engine
from models import Base, Lead
from schemas import LeadCreate, LeadResponse
from crm_integration import send_lead_to_crm

app = FastAPI(title="Centelha - Oficina FG Motos API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/webhook/lead", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead_in: LeadCreate, 
    background_tasks: BackgroundTasks, 
    db: AsyncSession = Depends(get_db)
):
    try:
        bucket = lead_in.get_assigned_bucket()
        
        new_lead = Lead(
            whatsapp_number=lead_in.whatsapp_number,
            client_name=lead_in.client_name,
            motorcycle_model=lead_in.motorcycle_model,
            displacement=lead_in.displacement,
            cylinders=lead_in.cylinders,
            assigned_to=bucket
        )
        
        db.add(new_lead)
        await db.commit()
        await db.refresh(new_lead)

        # Preparamos os dados para o CRM
        lead_payload = {
            "client_name": new_lead.client_name,
            "whatsapp_number": new_lead.whatsapp_number,
            "motorcycle_model": new_lead.motorcycle_model,
            "displacement": new_lead.displacement,
            "cylinders": new_lead.cylinders,
            "assigned_to": new_lead.assigned_to.value # Pega a string do Enum
        }

        # BackgroundTask: Envia ao CRM sem fazer o cliente esperar a resposta do WhatsApp
        background_tasks.add_task(send_lead_to_crm, lead_payload)
        
        return new_lead

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))