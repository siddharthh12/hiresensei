import re
import httpx
import xml.etree.ElementTree as ET
from typing import List
from app.services.job_sources.normalize import normalize_job_data
from app.models.hybrid_job import HybridJob
from datetime import datetime

async def scrape_wwr(query: str) -> List[HybridJob]:
    # Use RSS feed to avoid Cloudflare 403
    url = "https://weworkremotely.com/remote-jobs.rss"
    params = {"term": query}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    async with httpx.AsyncClient() as client:
        try:
            print(f"Fetching WeWorkRemotely RSS: {url} ? {params}")
            response = await client.get(url, params=params, headers=headers, timeout=15.0)
            if response.status_code != 200:
                print(f"WWR RSS returned status {response.status_code}")
                return []
            
            # Parse XML
            try:
                root = ET.fromstring(response.text)
            except ET.ParseError:
                # Try simple string parsing or BS4 if XML fails (sometimes encoding issues)
                print("XML Parse Error")
                return []

            jobs = []
            
            # RSS structure: <rss><channel><item>...</item></channel></rss>
            # Namespace might be present
            
            for item in root.findall(".//item"):
                try:
                    title_elem = item.find("title")
                    link_elem = item.find("link")
                    desc_elem = item.find("description")
                    pub_date_elem = item.find("pubDate")
                    
                    if title_elem is None or link_elem is None:
                        continue
                        
                    full_title = title_elem.text
                    apply_link = link_elem.text
                    raw_description = desc_elem.text if desc_elem is not None else ""
                    # Clean description HTML using regex
                    description = re.sub(r'<[^>]+>', '', raw_description).strip()
                    
                    # Title usually "Company: Role" or "Role: Company" or just "Role"
                    # WWR RSS title format: "Role: Company"
                    if ":" in full_title:
                        parts = full_title.split(":", 1)
                        title = parts[0].strip()
                        company = parts[1].strip()
                    else:
                        title = full_title
                        company = "WeWorkRemotely"
                        
                    # Parse Date
                    published_at = None
                    if pub_date_elem is not None:
                        try:
                            # RFC 822 format: "Wed, 02 Oct 2002 13:00:00 GMT"
                            published_at = datetime.strptime(pub_date_elem.text, "%a, %d %b %Y %H:%M:%S %z")
                        except:
                            pass
                            
                    job_id = f"wwr-{apply_link.split('/')[-1]}" if apply_link else f"wwr-{hash(full_title)}"
                    
                    if query and query.lower() not in title.lower() and query.lower() not in description.lower():
                        continue

                    job = normalize_job_data(
                        job_id=job_id,
                        title=title,
                        company=company,
                        location="Remote",
                        description=description,
                        apply_link=apply_link,
                        source="wwr",
                        published_at=published_at,
                        skills=[],
                        raw_data={"rss_title": full_title}
                    )
                    jobs.append(job)
                except Exception as e:
                    continue
                    
            return jobs
        except Exception as e:
            print(f"Error fetching WWR RSS: {e}")
            return []
