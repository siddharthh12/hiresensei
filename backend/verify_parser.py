import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.resume_parser import parse_resume_text

mock_resume = """
John Doe
123 Main St, New York, NY
john.doe@example.com
(555) 123-4567

Summary
Experienced Software Engineer with 5 years of experience in Python and React.

Skills
Python, JavaScript, React, FastAPI, Docker, AWS, SQL, Git

Experience
Senior Developer
Tech Corp - San Francisco, CA
Jan 2020 - Present
- Built scalable APIs using FastAPI and PostgreSQL.
- Deployed applications on AWS using Docker.

Education
B.S. Computer Science
University of Technology
2015 - 2019
"""

def test_parser():
    print("Testing Parser...")
    data = parse_resume_text(mock_resume)
    
    print(f"Name: {data['name']}")
    print(f"Location: {data['location']}")
    print(f"Skills: {data['skills']}")
    print(f"Experience Lines: {len(data['experience'])}")
    
    if data['name'] == "John Doe" and "New York" in data['location']:
        print("SUCCESS: Name and Location extracted.")
    else:
        print("FAILURE: Name or Location missing.")
        
    if "Python" in data['skills'] and "FastAPI" in data['skills']:
        print("SUCCESS: Skills extracted.")
    else:
        print("FAILURE: Skills missing.")

if __name__ == "__main__":
    test_parser()
