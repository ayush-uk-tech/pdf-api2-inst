from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from pypdf import PdfWriter
import io
import os

app = FastAPI()

@app.post("/merge-pdf")
async def merge_pdf(file: UploadFile = File(...)):
    # 1. n8n se aayi hui PDF ko read karna
    input_pdf_bytes = await file.read()
    
    writer = PdfWriter()
    
    # 2. n8n wali PDF ko add karna
    writer.append(io.BytesIO(input_pdf_bytes))
    
    # 3. Tumhari pehle se rakhi hui 'attachment.pdf' ko end mein merge karna
    # Ensure karo ki 'attachment.pdf' usi directory me ho jahan ye script run ho rahi hai
    attachment_path = os.path.join(os.path.dirname(__file__), "PDF.pdf")
    
    with open(attachment_path, "rb") as static_file:
        writer.append(static_file)
        
        # 4. Naya merged PDF in-memory save karna
        output_pdf_stream = io.BytesIO()
        writer.write(output_pdf_stream)
        writer.close()
        output_pdf_stream.seek(0)
        
    # 5. Merged PDF wapas n8n ko bhejna
    return Response(
        content=output_pdf_stream.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=merged_{file.filename}"
        }
    )
