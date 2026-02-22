from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel
import fitz
import os

app = FastAPI()

# Ye model define karta hai ki n8n se kya-kya data aayega
class PDFData(BaseModel):
    client_name: str
    address: str
    post_code: str
    company_reg: str
    vat_number: str
    fd_title: str
    fd_name: str
    client_contact: str
    email_address: str
    telephone: str
    position: str
    date: str
    tel: str
    email: str
    role_to_hire: str
    office_cost: str
    tech_cost: str
    client_name_bottom: str
    client_position_bottom: str
    client_date_bottom: str
    potentiam_person: str
    potentiam_position: str
    potentiam_date: str

@app.post("/generate-pdf")
async def generate_pdf(data: PDFData):
    try:
        # Template PDF ka path (same directory me hona chahiye)
        template_path = os.path.join(os.path.dirname(__file__), "merged_final.pdf")
        
        doc = fitz.open(template_path)
        page = doc[0]
        
        # User data aur hardcoded X, Y coordinates ki mapping
        insertions = [
            {"text": data.client_name, "x": 120, "y": 190},
            {"text": data.address, "x": 120, "y": 210},
            {"text": data.post_code, "x": 120, "y": 256},
            {"text": data.company_reg, "x": 120, "y": 272},
            {"text": data.vat_number, "x": 120, "y": 286},
            {"text": data.fd_title, "x": 120, "y": 336},
            {"text": data.fd_name, "x": 120, "y": 375},
            {"text": data.client_contact, "x": 419, "y": 190},
            {"text": data.email_address, "x": 419, "y": 211},
            {"text": data.telephone, "x": 419, "y": 241},
            {"text": data.position, "x": 419, "y": 255},
            {"text": data.date, "x": 419, "y": 287},
            {"text": data.tel, "x": 419, "y": 342},
            {"text": data.email, "x": 419, "y": 375},
            {"text": data.role_to_hire, "x": 60, "y": 480},
            {"text": data.office_cost, "x": 330, "y": 480},
            {"text": data.tech_cost, "x": 396, "y": 480},
            {"text": data.client_name_bottom, "x": 80, "y": 703},
            {"text": data.client_position_bottom, "x": 80, "y": 730},
            {"text": data.client_date_bottom, "x": 80, "y": 755},
            {"text": data.potentiam_person, "x": 344, "y": 703},
            {"text": data.potentiam_position, "x": 344, "y": 730},
            {"text": data.potentiam_date, "x": 344, "y": 755},
        ]
        
        # Loop karke text insert karna
        for item in insertions:
            page.insert_text(
                fitz.Point(item['x'], item['y']),
                str(item['text']),
                fontsize=8,
                fontname="helv",
                color=(0, 0, 0)
            )
            
        # PDF ko memory me save karna (Vercel me file save nahi kar sakte)
        pdf_bytes = doc.write()
        doc.close()
        
        # Binary PDF file wapas bhejna
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=custom_generated.pdf"
            }
        )
    except Exception as e:
        return {"error": f"Error aagaya bhai: {str(e)}"}
