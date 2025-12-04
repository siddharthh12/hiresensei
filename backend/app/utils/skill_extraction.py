import re
from typing import List, Set

# Common tech skills mapping for normalization
# Key: Normalized Skill Name, Value: List of synonyms/variations
SKILL_MAPPING = {
    "python": ["python", "py"],
    "javascript": ["javascript", "js", "es6"],
    "typescript": ["typescript", "ts"],
    "react": ["react", "reactjs", "react.js"],
    "node.js": ["node.js", "nodejs", "node"],
    "express": ["express", "expressjs", "express.js"],
    "fastapi": ["fastapi"],
    "flask": ["flask"],
    "django": ["django"],
    "sql": ["sql", "mysql", "postgresql", "postgres", "sqlite"],
    "nosql": ["nosql", "mongodb", "mongo", "cassandra", "dynamodb"],
    "aws": ["aws", "amazon web services", "ec2", "s3", "lambda"],
    "docker": ["docker", "containerization"],
    "kubernetes": ["kubernetes", "k8s"],
    "git": ["git", "github", "gitlab"],
    "ci/cd": ["ci/cd", "cicd", "jenkins", "github actions"],
    "html": ["html", "html5"],
    "css": ["css", "css3", "tailwind", "bootstrap", "sass", "less"],
    "java": ["java"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "csharp"],
    "go": ["go", "golang"],
    "rust": ["rust"],
    "kafka": ["kafka"],
    "redis": ["redis"],
    "graphql": ["graphql"],
    "rest api": ["rest api", "restful api", "rest"],
    "machine learning": ["machine learning", "ml", "tensorflow", "pytorch", "scikit-learn"],
    "data science": ["data science", "pandas", "numpy"],
    "linux": ["linux", "bash", "shell"],
    "agile": ["agile", "scrum", "kanban"]
}

# Flatten the mapping for easy lookup
SKILL_LOOKUP = {}
for normalized, variations in SKILL_MAPPING.items():
    for var in variations:
        SKILL_LOOKUP[var.lower()] = normalized

def normalize_skill(skill: str) -> str:
    """
    Normalizes a skill string to a standard format.
    """
    cleaned = skill.lower().strip()
    return SKILL_LOOKUP.get(cleaned, cleaned)

def extract_skills_from_text(text: str) -> List[str]:
    """
    Extracts known skills from a block of text using keyword scanning.
    """
    if not text:
        return []
    
    found_skills = set()
    text_lower = text.lower()
    
    # Simple word boundary check for each known skill variation
    # This is O(N*M) where N is text length and M is number of skills, but M is small (~100)
    for variation, normalized in SKILL_LOOKUP.items():
        # Regex to match whole words or specific patterns
        # Escape special chars in variation (like c++, node.js)
        pattern = r'\b' + re.escape(variation) + r'\b'
        
        # Special handling for Java to avoid matching "Java Script" or "Java-Script"
        if variation == "java":
            pattern = r'\bjava\b(?!\s*-?script)'
            
        if re.search(pattern, text_lower):
            found_skills.add(normalized)
            
    return list(found_skills)

def normalize_skill_list(skills: List[str]) -> List[str]:
    """
    Normalizes a list of skills.
    """
    normalized_set = set()
    for skill in skills:
        normalized_set.add(normalize_skill(skill))
    return list(normalized_set)
