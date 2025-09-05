import PyPDF2
import os



def pdf_to_text_native(pdf_path):

    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            full_text = f"Arquivo: {os.path.basename(pdf_path)}\n"
            full_text += f"Total de páginas: {total_pages}\n\n"
            
            for page_num in range(total_pages):
                page = reader.pages[page_num]
                text = page.extract_text()
                # variavel text contem todo o texto
                
                if text.strip():
                    full_text += f"--- Página {page_num+1} ---\n{text}\n"
                else:
                    full_text += f"--- Página {page_num+1} (Conteúdo de imagem - OCR não disponível nesta versão) ---\n"
            
            return full_text
    except Exception as e:
        return f"Erro ao processar PDF: {str(e)}"



