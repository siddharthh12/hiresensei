import httpx
import xml.etree.ElementTree as ET
from typing import List
from app.services.job_sources.normalize import normalize_job_data
from app.models.hybrid_job import HybridJob
from datetime import datetime

async def scrape_remoteok(query: str) -> List[HybridJob]:
    """
    Scrape RemoteOK jobs using RSS feed to avoid blocking.
    """
    # RemoteOK RSS feed
    url = "https://remoteok.com/remote-jobs.rss"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    async with httpx.AsyncClient() as client:
        try:
            print(f"Fetching RemoteOK RSS: {url}")
            response = await client.get(url, headers=headers, timeout=15.0)
            if response.status_code != 200:
                print(f"RemoteOK RSS returned status {response.status_code}")
                return []
            
            # Parse XML
            try:
                root = ET.fromstring(response.text)
            except ET.ParseError:
                print("RemoteOK XML Parse Error")
                return []

            jobs = []
            
            # RSS structure: <rss><channel><item>...</item></channel></rss>
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
                    description = desc_elem.text if desc_elem is not None else ""
                    
                    # Filter by query (simple case-insensitive check)
                    # RemoteOK RSS returns ALL jobs, so we must filter manually
                    # Relaxed: Check if query terms appear in title OR description
                    search_text = (full_title + " " + description).lower()
                    
                    # Split query into words and check if ANY word is present (broader match)
                    # Or keep it strict but ensure we don't miss obvious ones.
                    # Let's stick to the full query string for now but ensure it's robust.
                    if query.lower() not in search_text:
                        # Try checking individual words if the full phrase fails?
                        # For "python", it should be fine.
                        # For "software engineer", "software" AND "engineer" should be present.
                        query_parts = query.lower().split()
                        if not all(part in search_text for part in query_parts):
                            continue

                    # Title format often "Company: Role" or just "Role"
                    if ":" in full_title:
                        parts = full_title.split(":", 1)
                        company = parts[0].strip()
                        title = parts[1].strip()
                    else:
                        title = full_title
                        company = "RemoteOK"
                        
                    # Parse Date
                    published_at = None
                    if pub_date_elem is not None:
                        try:
                            # RFC 822 format
                            published_at = datetime.strptime(pub_date_elem.text, "%a, %d %b %Y %H:%M:%S %z")
                        except:
                            pass
                            
                    job_id = f"remoteok-{apply_link.split('/')[-1]}" if apply_link else f"remoteok-{hash(full_title)}"
                    
                    job = normalize_job_data(
                        job_id=job_id,
                        title=title,
                        company=company,
                        location="Remote",
                        description=description,
                        apply_link=apply_link,
                        source="remoteok",
                        published_at=published_at,
                        skills=[],
                        raw_data={"rss_title": full_title}
                    )
                    jobs.append(job)
                except Exception as e:
                    continue
            
            print(f"RemoteOK: Found {len(jobs)} jobs matching '{query}'")
            return jobs
        except Exception as e:
            print(f"Error fetching RemoteOK RSS: {e}")
            return []
