import sys
import os

# Add the current directory to sys.path so we can import app
sys.path.append(os.getcwd())

from app.utils.text_similarity import extract_years_of_experience

def test():
    # Text from the user's image
    texts = [
        "Aartick Technologies",
        "Full Stack Developer Intern July, 2025 - Present",
        "Developed 5+ full-stack web apps with Next.js, React.js reducing page load by 40% via code splitting and lazy loading",
        "Built RESTful APIs (Node.js, Express.js) handling 100+ concurrent requests with MongoDB optimization",
        "Implemented real-time features (WebSockets, Firebase) improving user engagement by 25%",
        "Deployed on Vercel and Azure with CI/CD pipelines, reducing deployment time by 60%"
    ]
    
    years = extract_years_of_experience(texts)
    print(f"Total Years Extracted: {years}")
    
    # Test case 2: 2 years experience
    texts2 = [
        "Software Engineer Jan 2020 - Jan 2022",
        "Worked on stuff."
    ]
    years2 = extract_years_of_experience(texts2)
    print(f"Test Case 2 (2 years): {years2}")

if __name__ == "__main__":
    test()
