import PyPDF2
import re
import json

def clean_text(text):
    """
    This function cleans and pre-processes the extracted text.

    Args:
        text: String containing the raw text extracted from the PDF.

    Returns:
        String containing the cleaned and pre-processed text.
    """
    # Remove unwanted characters and formatting
    text = text.strip()  # Remove leading/trailing whitespaces
    text = re.sub(r'[^\w\s\.]', '', text)  # Remove non-alphanumeric characters except whitespace and period

    # Lowercase all characters
    text = text.lower()

    # Additional cleaning steps (optional)
    # - Remove stop words (common words like "the", "a", "an")
    # - Apply stemming or lemmatization to normalize words (e.g., "running" -> "run")

    return text

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF.

    Args:
        file_path: String representing the path to the PDF file.

    Returns:
        String containing the cleaned and pre-processed text extracted from the PDF.
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            # Handle encrypted PDFs gracefully
            if reader.is_encrypted:
                print(f"Skipping encrypted PDF: {file_path}")
                return ""
            
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""  # Extract text from each page

            # Clean and pre-process the extracted text
            clean_text_data = clean_text(text)
            return clean_text_data

    except Exception as e:
        print(f"Error processing PDF {file_path}: {e}")
        return ""  # Return empty string on error

# Paths to PDF files
pdf_files = [
    r'C:\Users\The Den\Desktop\New folder (4)\Air condintioner_heater.pdf', 
    r'C:\Users\The Den\Desktop\New folder (4)\Bow Thruster Pursuit 378.pdf', 
    r'C:\Users\The Den\Desktop\New folder (4)\Dometic_VacuFlush Manual.pdf',
    r'C:\Users\The Den\Desktop\New folder (4)\Generator Panda_8-9mini_Digital_2017_PMS_eng.R02.pdf',
    r'C:\Users\The Den\Desktop\New folder (4)\JL Audio Media Master.pdf',
    r'C:\Users\The Den\Desktop\New folder (4)\Pursuit S 378 Sport Center Console.pdf',
    r'C:\Users\The Den\Desktop\New folder (4)\Rule LoPro LP900D manual-handleiding ENG Nautic Gear.pdf',
    r'C:\Users\The Den\Desktop\New folder (4)\Seakeeper 3.pdf',
    r'C:\Users\The Den\Desktop\New folder (4)\Sealand Vacuflush Toilet.pdf',
    r'C:\Users\The Den\Desktop\New folder (4)\XTO 450 Yamaha Fact Sheet.pdf'
]

knowledge_base = {}

for pdf in pdf_files:
    extracted_text = extract_text_from_pdf(pdf)
    if extracted_text:
        knowledge_base[pdf] = extracted_text

# Save extracted data to a JSON file
output_path = r'C:\Users\The Den\Desktop\POC-2\knowledge_base.json'
try:
    with open(output_path, 'w') as json_file:
        json.dump(knowledge_base, json_file)
    print("Text extraction and cleaning completed!")
except FileNotFoundError as e:
    print(f"Error saving JSON file: {e}")
