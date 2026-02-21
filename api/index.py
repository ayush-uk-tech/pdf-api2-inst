from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from pypdf import PdfReader, PdfWriter
import io

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "PDF API is running! Use POST /add-blank-page to merge a blank page."}

@app.post("/add-blank-page")
async def add_blank_page(file: UploadFile = File(...)):
    # 1. Incoming PDF ko read karna
    input_pdf_bytes = await file.read()
    
    reader = PdfReader(io.BytesIO(input_pdf_bytes))
    writer = PdfWriter()
    
    # 2. Saare purane pages naye PDF me add karna
    for page in reader.pages:
        writer.add_page(page)
        
    # 3. Last page ka size (width/height) nikalna taaki blank page bhi same size ka ho
    if len(reader.pages) > 0:
        last_page = reader.pages[-1]
        width = last_page.mediabox.width
        height = last_page.mediabox.height
    else:
        width, height = 595.276, 841.890 # Standard A4 size
        
    # 4. Blank page add karna
    writer.add_blank_page(width=width, height=height)
    
    # 5. Naya PDF in-memory save karna
    output_pdf_stream = io.BytesIO()
    writer.write(output_pdf_stream)
    output_pdf_stream.seek(0)
    
    # 6. Modified PDF n8n ko wapas bhejna
    return Response(
        content=output_pdf_stream.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=modified_{file.filename}"
        }
    )
