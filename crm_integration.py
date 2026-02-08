import httpx
import logging

# Configurações do seu CRM (Exemplo genérico)
CRM_API_URL = "https://seu-crm.api.com/v1/leads"
CRM_API_TOKEN = "seu_token_aqui"

logger = logging.getLogger(__name__)

async def send_lead_to_crm(lead_data: dict):
    """
    Envia os dados do lead classificado para o CRM.
    """
    headers = {
        "Authorization": f"Bearer {CRM_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Mapeamento para o formato que seu CRM exige
    payload = {
        "title": f"Revisão: {lead_data['motorcycle_model']} - {lead_data['client_name']}",
        "phone": lead_data["whatsapp_number"],
        "description": f"Cilindrada: {lead_data['displacement']}cc | Cilindros: {lead_data['cylinders']}",
        "assigned_to": lead_data["assigned_to"], # 'Premium_Fagne' ou 'Standard_Auxiliar'
        "status": "Novo Lead"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(CRM_API_URL, json=payload, headers=headers, timeout=10.0)
            response.raise_for_status()
            logger.info(f"Lead enviado ao CRM com sucesso: {lead_data['client_name']}")
            return True
        except Exception as e:
            logger.error(f"Falha ao enviar lead ao CRM: {str(e)}")
            return False