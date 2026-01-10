import httpx
from bs4 import BeautifulSoup
from typing import List
from app.services.job_sources.normalize import normalize_job_data
from app.models.hybrid_job import HybridJob

async def scrape_hn_jobs(query: str) -> List[HybridJob]:
    url = "https://news.ycombinator.com/jobs"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    async with httpx.AsyncClient() as client:
        try:
            print(f"Scraping HackerNews: {url}")
            response = await client.get(url, headers=headers, timeout=15.0)
            if response.status_code != 200:
                print(f"HN returned status {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.text, "html.parser")
            jobs = []
            
            # HN jobs are in <tr class="athing">
            rows = soup.find_all("tr", class_="athing")
            
            for row in rows:
                try:
                    title_elem = row.find("span", class_="titleline")
                    if not title_elem:
                        continue
                        
                    a_tag = title_elem.find("a")
                    if not a_tag:
                        continue
                        
                    full_text = a_tag.get_text(strip=True)
                    link = a_tag['href']
                    
                    # HN links can be relative or absolute
                    if not link.startswith("http"):
                        link = f"https://news.ycombinator.com/{link}"
                        
                    # Filter by query if provided (simple case-insensitive check)
                    if query and query.lower() not in full_text.lower():
                        continue
                        
                    # Extract Company and Title (Heuristic: "Company is hiring..." or "Company: Role")
                    # HN titles are unstructured. We'll use the whole text as title and try to guess company.
                    company = "HackerNews Job"
                    title = full_text
                    
                    # Simple heuristic: Split by " is hiring " or ":"
                    if " is hiring " in full_text:
                        parts = full_text.split(" is hiring ")
                        company = parts[0]
                        title = parts[1] if len(parts) > 1 else full_text
                    elif ":" in full_text:
                         parts = full_text.split(":", 1)
                         company = parts[0]
                         title = parts[1]
                    
                    job_id = f"hn-{row.get('id')}"
                    
                    job = normalize_job_data(
                        job_id=job_id,
                        title=title,
                        company=company,
                        location="Remote", # HN jobs are often remote-friendly, but hard to tell without parsing text deep
                        description=full_text,
                        apply_link=link,
                        source="hn",
                        skills=[],
                        raw_data={"raw_title": full_text}
                    )
                    jobs.append(job)
                except Exception as e:
                    continue
            
            return jobs
        except Exception as e:
            print(f"Error scraping HN: {e}")
            return []
