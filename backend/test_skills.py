import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
sys.path.append(os.path.dirname(__file__))

from app.utils.skill_extraction import extract_skills_from_text, normalize_skill

def test_extraction():
    text = "We are looking for a Software Engineer with experience in Python, React.js, and AWS. Knowledge of Docker is a plus."
    skills = extract_skills_from_text(text)
    print(f"Text: {text}")
    print(f"Extracted Skills: {list(skills)}")
    
    expected = {"python", "react", "aws", "docker", "javascript"}
    missing = expected - set(skills)
    extra = set(skills) - expected
    if missing or extra:
        print(f"Missing: {missing}")
        print(f"Extra: {extra}")
    
    assert set(skills) == expected, f"Expected {expected}, got {set(skills)}"
    print("Extraction Test Passed!")

def test_normalization():
    assert normalize_skill("React.js") == "react"
    assert normalize_skill("Node.js") == "node.js"
    assert normalize_skill("C++") == "c++"
    print("Normalization Test Passed!")

if __name__ == "__main__":
    test_extraction()
    test_normalization()
