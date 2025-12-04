import spacy
import pdfplumber
import docx
import re
import os

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback if model isn't found immediately (e.g. during build)
    # In production, ensure model is downloaded
    print("Warning: en_core_web_sm not found. Parsing will be limited.")
    nlp = None

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

def parse_resume_text(text: str) -> dict:
    data = {
        "name": "",
        "email": "",
        "phone": "",
        "location": "",
        "skills": [],
        "experience": [],
        "education": [],
        "certifications": []
    }

    # Basic Regex Extraction
    email_pattern = r"[\w\.-]+@[\w\.-]+"
    phone_pattern = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"

    email_match = re.search(email_pattern, text)
    if email_match:
        data["email"] = email_match.group(0)

    phone_match = re.search(phone_pattern, text)
    if phone_match:
        data["phone"] = phone_match.group(0)

    # NLP Extraction
    if nlp:
        doc = nlp(text)
        
        # Name Extraction (Simple Heuristic: First PERSON entity)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and not data["name"]:
                data["name"] = ent.text
            
            # Location Extraction (First GPE entity)
            if ent.label_ == "GPE" and not data["location"]:
                data["location"] = ent.text
        
        # Fallback for name: First line if short
        if not data["name"]:
            lines = text.split('\n')
            if lines and len(lines[0]) < 50:
                data["name"] = lines[0].strip()

        # Skills Extraction (Keyword matching against a predefined list)
        # In a real app, use a larger database or trained NER model
        common_skills = [
            "python", "java", "javascript", "react", "node.js", "fastapi", "sql", "nosql",
            "docker", "kubernetes", "aws", "azure", "git", "machine learning", "ai",
            "html", "css", "typescript", "c++", "c#", "go", "rust"
        ]
        
        text_lower = text.lower()
        for skill in common_skills:
            # Use regex with word boundaries to avoid partial matches (e.g. "java" in "javascript")
            pattern = r'\b' + re.escape(skill) + r'\b'
            
            # Special handling for Java to avoid matching "Java Script" or "Java-Script"
            if skill == "java":
                pattern = r'\bjava\b(?!\s*-?script)'
            
            if re.search(pattern, text_lower):
                data["skills"].append(skill.title())

    # Simple keyword-based section extraction (Experience, Education)
    # This is rudimentary. A real parser would use layout analysis or ML.
    lines = text.split('\n')
    current_section = None
    
    for line in lines:
        line_lower = line.lower().strip()
        if "experience" in line_lower or "work history" in line_lower:
            current_section = "experience"
            continue
        elif "education" in line_lower:
            current_section = "education"
            continue
        elif "skills" in line_lower:
            current_section = "skills_section" # Already handled by keywords, but could extract more
            continue
        elif "certifications" in line_lower:
            current_section = "certifications"
            continue
            
        if current_section == "experience" and line.strip():
            data["experience"].append(line.strip())
        elif current_section == "education" and line.strip():
            data["education"].append(line.strip())
        elif current_section == "certifications" and line.strip():
            data["certifications"].append(line.strip())

    # Clean up lists (limit items for preview)
    data["experience"] = data["experience"][:5] # First 5 lines of experience
    data["education"] = data["education"][:3]   # First 3 lines of education

    return data
