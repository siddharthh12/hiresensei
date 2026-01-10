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
                # Filter out single words or very long generic text
                if " " in ent.text and len(ent.text) < 30:
                     data["name"] = ent.text
            
            # Location Extraction (First GPE entity)
            if ent.label_ == "GPE" and not data["location"]:
                data["location"] = ent.text
    
    # Fallbacks if NLP failed or missed
    if not data["name"]:
        # Heuristic: First capitalized line that isn't a header
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        for line in lines[:10]: # Check first 10 lines
            if len(line.split()) < 4 and line.istitle() and "@" not in line and "curriculum" not in line.lower():
                 data["name"] = line
                 break
                 
    if not data["location"]:
        # Heuristic: Regex for City, State/Country pattern 
        # e.g. "New York, NY" or "London, UK"
        loc_pattern = r'\b[A-Z][a-z]+(?: [A-Z][a-z]+)*,\s*[A-Z]{2,}\b'
        loc_match = re.search(loc_pattern, text)
        if loc_match:
            data["location"] = loc_match.group(0)

    # Expanded Skills Extraction
    common_skills = [
        # Languages
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "php", "ruby", "swift", "kotlin", "scala", "r", "matlab",
        # Web
        "html", "css", "react", "angular", "vue", "next.js", "node.js", "django", "flask", "fastapi", "spring boot", "asp.net", "laravel",
        # Data & AI
        "sql", "nosql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "machine learning", "deep learning", "nlp", "tensorflow", "pytorch", "pandas", "numpy", "scikit-learn", "keras", "openai", "llm",
        # DevOps & Cloud
        "docker", "kubernetes", "aws", "azure", "gcp", "google cloud", "jenkins", "gitlab ci", "github actions", "terraform", "ansible", "linux", "bash",
        # Tools
        "git", "jira", "confluence", "slack", "figma", "postman"
    ]
    
    text_lower = text.lower()
    found_skills = set()
    
    for skill in common_skills:
        # Use regex with word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        
        # Special handling
        if skill == "c++":
             pattern = r'\bc\+\+\b' # Escape plus
        elif skill == "c#":
             pattern = r'\bc#\b'
        elif skill == "node.js":
             pattern = r'\bnode(\.js)?\b'
        elif skill == "java":
             pattern = r'\bjava\b(?!\s*-?script)'
        
        if re.search(pattern, text_lower):
            found_skills.add(skill.title())
            
    data["skills"] = list(found_skills)

    # Section Extraction (Simple)
    lines = text.split('\n')
    current_section = None
    
    for line in lines:
        line_clean = line.strip()
        line_lower = line_clean.lower()
        
        if not line_clean:
            continue
            
        # Detect headers
        if any(keyword in line_lower for keyword in ["experience", "employment", "work history"]):
             if len(line_clean) < 30: # Ensure it's likely a header
                current_section = "experience"
                continue
        elif any(keyword in line_lower for keyword in ["education", "academic"]):
             if len(line_clean) < 30:
                current_section = "education"
                continue
        elif "certifications" in line_lower:
             if len(line_clean) < 30:
                current_section = "certifications"
                continue
            
        if current_section == "experience":
            data["experience"].append(line_clean)
        elif current_section == "education":
            data["education"].append(line_clean)
        elif current_section == "certifications":
            data["certifications"].append(line_clean)

    # Clean up lists (limit items for preview, but maybe keep more if needed for analysis)
    # Storing more experience text helps the refined recommendation engine!
    data["experience"] = data["experience"][:20] 
    data["education"] = data["education"][:10]   

    return data
