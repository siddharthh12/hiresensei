import re
from datetime import datetime

def extract_years_of_experience(text_list):
    max_years = 0.0
    
    # Regex to find patterns like "5 years", "5+ years", "2018-2022"
    year_pattern = re.compile(r'(\d+)\+?\s*years?', re.IGNORECASE)
    date_range_pattern = re.compile(r'(\d{4})\s*-\s*(present|now|\d{4})', re.IGNORECASE)
    
    print(f"Analyzing text list: {text_list}")
    
    for text in text_list:
        # Check for explicit mentions like "5 years"
        matches = year_pattern.findall(text)
        for match in matches:
            print(f"Matched year pattern in '{text}': {match}")
            try:
                years = float(match)
                if years < 40: # Sanity check
                    max_years = max(max_years, years)
            except ValueError:
                pass
                
        # Check for date ranges
        date_matches = date_range_pattern.findall(text)
        for start, end in date_matches:
            print(f"Matched date pattern in '{text}': {start} - {end}")
            try:
                start_year = int(start)
                if end.lower() in ['present', 'now']:
                    end_year = datetime.now().year
                else:
                    end_year = int(end)
                
                diff = end_year - start_year
                print(f"Calculated diff: {diff}")
                if 0 <= diff < 40:
                    max_years = max(max_years, float(diff))
            except ValueError:
                pass
                
    return max_years

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

if __name__ == "__main__":
    test()
