from fuzzywuzzy import fuzz
import re
from typing import List, Optional

def calculate_similarity(text1: str, text2: str) -> int:
    """
    Calculate similarity score between two strings using fuzzy matching.
    Returns a score between 0 and 100.
    """
    if not text1 or not text2:
        return 0
    
    # Normalize text
    t1 = text1.lower().strip()
    t2 = text2.lower().strip()
    
    # Use partial ratio for better matching of substrings (e.g. "Python" in "Senior Python Developer")
    return fuzz.partial_ratio(t1, t2)

def extract_years_of_experience(text_list: List[str]) -> float:
    """
    Heuristic to extract max years of experience from a list of strings.
    Prioritizes date ranges (Month Year - Month Year) over simple number matching.
    """
    from datetime import datetime
    
    total_months = 0
    max_years_from_text = 0.0
    
    # Regex for "5 years"
    year_pattern = re.compile(r'(\d+)\+?\s*years?', re.IGNORECASE)
    
    # Regex for Date Ranges: "July 2025 - Present", "07/2025 - 12/2025"
    # Matches: (Month/Num) (Year) - (Month/Num/Present) (Year/Empty)
    # This is a bit complex, let's try a few specific patterns
    
    # Pattern 1: MonthName Year - MonthName Year (or Present)
    # e.g. July 2025 - Present, July, 2025 - Present, Jan 2020 - Feb 2022
    date_pattern_str = r'(?P<start_month>[a-zA-Z]+)[,.]?\s*(?P<start_year>\d{4})\s*[-–to]+\s*(?P<end_str>.*)'
    date_pattern = re.compile(date_pattern_str, re.IGNORECASE)
    
    # Helper to parse month
    month_map = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
        'january': 1, 'february': 2, 'march': 3, 'april': 4, 'june': 6,
        'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12
    }
    
    def get_month_num(m_str):
        m_str = m_str.lower()[:3]
        return month_map.get(m_str, 1) # Default to Jan if unknown

    found_ranges = []

    for text in text_list:
        # 1. Try to find date ranges first (Higher Priority)
        matches = date_pattern.finditer(text)
        for match in matches:
            try:
                s_month = get_month_num(match.group('start_month'))
                s_year = int(match.group('start_year'))
                
                end_str = match.group('end_str').strip().lower()
                
                # Parse end date
                e_month = datetime.now().month
                e_year = datetime.now().year
                
                if 'present' in end_str or 'now' in end_str or 'current' in end_str:
                    pass # Keep defaults (now)
                else:
                    # Try to parse end date from end_str
                    # Expecting "Month Year" or just "Year"
                    # Simple regex for end part
                    end_match = re.search(r'(?P<end_month>[a-zA-Z]+)[,.]?\s*(?P<end_year>\d{4})', end_str)
                    if end_match:
                        e_month = get_month_num(end_match.group('end_month'))
                        e_year = int(end_match.group('end_year'))
                    else:
                        # Maybe just year?
                        year_match = re.search(r'(\d{4})', end_str)
                        if year_match:
                            e_year = int(year_match.group(1))
                            e_month = 12 # Assume end of year? or Jan? Let's say Dec to be generous or match start month?
                
                # Calculate diff in months
                start_date = s_year * 12 + s_month
                end_date = e_year * 12 + e_month
                
                diff_months = end_date - start_date
                if diff_months < 0: diff_months = 0
                
                found_ranges.append(diff_months)
                
            except Exception:
                pass

        # 2. Look for explicit "X years" mentions (Lower Priority, fallback)
        # Only if we haven't found good date ranges, OR we want to take the max?
        # Usually "5 years experience" in summary is reliable.
        matches_years = year_pattern.findall(text)
        for match in matches_years:
            try:
                val = float(match)
                if val < 40:
                    max_years_from_text = max(max_years_from_text, val)
            except ValueError:
                pass

    # Calculation Strategy:
    # If we found date ranges, sum them up (assuming no overlap for simplicity, or take max range?)
    # Usually experience is cumulative. But concurrent jobs shouldn't double count.
    # For this MVP, let's sum them up but cap at reasonable number, or just take the max duration found?
    # Better: Sum of durations.
    
    if found_ranges:
        total_years_from_dates = sum(found_ranges) / 12.0
        # If the text explicitly says "5 years" but dates only show 1, maybe the dates are incomplete?
        # But user specifically complained about "5+" being parsed as 5 years when dates showed less.
        # So we should trust dates if present.
        return round(total_years_from_dates, 1)
    
    return max_years_from_text

def normalize_skills(skills: List[str]) -> List[str]:
    """
    Normalize a list of skills to lowercase for comparison.
    """
    return [s.lower().strip() for s in skills if s]
