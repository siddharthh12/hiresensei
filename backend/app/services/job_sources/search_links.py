import urllib.parse

def generate_search_links(query: str, location: str = "") -> dict:
    q = urllib.parse.quote(query)
    l = urllib.parse.quote(location)
    
    return {
        "linkedin": f"https://www.linkedin.com/jobs/search/?keywords={q}&location={l}",
        "indeed": f"https://www.indeed.com/jobs?q={q}&l={l}",
        "google_jobs": f"https://www.google.com/search?q={q}+jobs+in+{l}&ibp=htl;jobs"
    }
