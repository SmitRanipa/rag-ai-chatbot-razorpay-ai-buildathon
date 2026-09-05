import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timezone
import re
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from du_scraper.utils.extract import extract_main_html, compute_hash
from w3lib.url import canonicalize_url

urls = [
"https://darshan.ac.in/placement/list/btech-computer/2026",
"https://darshan.ac.in/placement/list/btech-civil/2026",
"https://darshan.ac.in/placement/list/mba/2026",
"https://darshan.ac.in/placement/list/mca/2026",
"https://darshan.ac.in/placement/list/bca/2026",
"https://darshan.ac.in/placement/list/bsc-it/2026",
"https://darshan.ac.in/placement/list/diploma-mechanical/2026",
"https://darshan.ac.in/placement/list/diploma-electrical/2026",

"https://darshan.ac.in/placement/list/btech-computer/2025",
"https://darshan.ac.in/placement/list/btech-civil/2025",
"https://darshan.ac.in/placement/list/btech-mechanical/2025",
"https://darshan.ac.in/placement/list/mba/2025",
"https://darshan.ac.in/placement/list/mca/2025",
"https://darshan.ac.in/placement/list/bba/2025",
"https://darshan.ac.in/placement/list/bca/2025",
"https://darshan.ac.in/placement/list/bsc-it/2025",
"https://darshan.ac.in/placement/list/diploma-computer/2025",
"https://darshan.ac.in/placement/list/diploma-civil/2025",
"https://darshan.ac.in/placement/list/diploma-mechanical/2025",

"https://darshan.ac.in/placement/list/btech-computer/2024",
"https://darshan.ac.in/placement/list/btech-civil/2024",
"https://darshan.ac.in/placement/list/btech-mechanical/2024",
"https://darshan.ac.in/placement/list/mba/2024",
"https://darshan.ac.in/placement/list/mca/2024",
"https://darshan.ac.in/placement/list/bba/2024",
"https://darshan.ac.in/placement/list/bcom/2024",
"https://darshan.ac.in/placement/list/bca/2024",
"https://darshan.ac.in/placement/list/bsc-it/2024",
"https://darshan.ac.in/placement/list/diploma-civil/2024",
"https://darshan.ac.in/placement/list/diploma-mechanical/2024",

"https://darshan.ac.in/placement/list/btech-computer/2023",
"https://darshan.ac.in/placement/list/btech-civil/2023",
"https://darshan.ac.in/placement/list/btech-mechanical/2023",
"https://darshan.ac.in/placement/list/mba/2023",
"https://darshan.ac.in/placement/list/mca/2023",

"https://darshan.ac.in/placement/list/btech-computer/2022",
"https://darshan.ac.in/placement/list/btech-civil/2022",
"https://darshan.ac.in/placement/list/btech-mechanical/2022",

"https://darshan.ac.in/placement/list/btech-computer/2021",
"https://darshan.ac.in/placement/list/btech-civil/2021",
"https://darshan.ac.in/placement/list/btech-mechanical/2021",

"https://darshan.ac.in/placement/list/btech-computer/2020",
"https://darshan.ac.in/placement/list/btech-civil/2020",
"https://darshan.ac.in/placement/list/btech-mechanical/2020",

"https://darshan.ac.in/placement/list/btech-computer/2019",
"https://darshan.ac.in/placement/list/btech-civil/2019",

"https://darshan.ac.in/placement/list/btech-computer/2018",

"https://darshan.ac.in/placement/list/btech-computer/2017",

"https://darshan.ac.in/placement/list/btech-computer/2016"
]

urls = list(set(urls))

headers = {
    "User-Agent": "DU-RAG-Crawler/1.0 ( DU Student 6th Sem )"
}

def semantically_extract_placements(html, url):
    soup = BeautifulSoup(html, "lxml")
    
    parts = url.strip('/').split('/')
    year = parts[-1] if len(parts) >= 1 else ""
    branch_slug = parts[-2] if len(parts) >= 2 else ""
    
    branch = branch_slug.replace('-', ' ').title()
    if branch.startswith('Btech'): branch = branch.replace('Btech', 'B.Tech')
    if branch.startswith('Mca'): branch = 'MCA'
    if branch.startswith('Mba'): branch = 'MBA'
    if branch.startswith('Bca'): branch = 'BCA'
    if branch.startswith('Bsc'): branch = branch.replace('Bsc', 'B.Sc')
    if branch.startswith('Bba'): branch = 'BBA'
    
    # 1. EXTRACT OVERALL STATS (Registered, Placed, Ratio, Highest Package, Median, Companies Visited)
    labels = ['Registered Students', 'Placed Students', 'Placement Rate', 'Highest Package', 'Median Package', 'Companies Visited']
    stats_sentences = []
    
    # Aggressively build repetitive phrasing so semantic dot-product grabs the exact year/branch 
    summary_header = f"Placement Overview for {branch} in the year {year}. These statistics represent the {year} placement drive for the {branch} batch at Darshan University: \n"
    for label in labels:
        elem = soup.find(string=re.compile(label, re.I))
        if elem:
            parent = elem.parent
            for _ in range(3):
                if parent.name == 'div' and any(char.isdigit() for char in parent.get_text()):
                    break
                if parent.parent:
                   parent = parent.parent
            
            # Text will be "290 Registered Students" or "10.00 Lakh Highest Package".
            # We rewrite it cleanly.
            stat_text = parent.get_text(' ', strip=True).replace(label, '').strip()
            
            structured_str = f"The {label} for {branch} in the {year} batch is precisely {stat_text} {label}."
            if stat_text:  # Check if we successfully grabbed a number
                if label == 'Highest Package':
                    structured_str = f"The {label} for students of {branch} in {year} is {stat_text}."
                elif label == 'Median Package':
                    structured_str = f"The {label} for students of {branch} in {year} is {stat_text}."
                elif label == 'Placement Rate':
                    structured_str = f"The {label} (or Placement Ratio) for {branch} in the year {year} is {stat_text}."
            
            stats_sentences.append(structured_str)

    # 2. EXTRACT INDIVIDUAL STUDENT CARDS
    student_sentences = []
    seen = set()
    
    enroll_nodes = soup.find_all(string=re.compile(r'^\s*\d{10,12}\s*$'))
    for node in enroll_nodes:
        enroll = node.strip()
        
        container = node.parent
        for _ in range(5):
            if container.name in ['div', 'li', 'article']:
                strs = list(container.stripped_strings)
                if 4 <= len(strs) <= 25 and enroll in strs:
                    break
            if container.parent:
                container = container.parent
                
        strs = list(container.stripped_strings)
        try:
            idx_e = strs.index(enroll)
            name = " ".join(strs[:idx_e])
            if "Total Students" in name or "Placed Students" in name: 
                name = name.split(" Students")[-1].strip()
            if "Admission" in name:
                name = name.split("Admission")[-1].strip()
            
            package = "N/A"
            for i, s in enumerate(strs):
                if s in ['CTC per Annum', 'Package'] and i+1 < len(strs):
                    package = strs[i+1]
                    
            # Company: first try text labels, then fall back to img alt
            company = "N/A"
            for i, s in enumerate(strs):
                if s in ['Placed at'] and i+1 < len(strs):
                    company = strs[i+1]
            
            if company == "N/A":
                # Company logo is an <img> with alt = company name
                imgs = container.find_all('img')
                # The recruiter logo has 'Recruiter' in its src URL
                for img in imgs:
                    src = img.get('src', '')
                    alt = (img.get('alt') or '').strip()
                    if alt and ('Recruiter' in src or 'recruiter' in src or 'company' in src.lower()):
                        company = alt
                        break
                # If still N/A, take any non-student-photo img alt
                if company == "N/A":
                    for img in imgs:
                        alt = (img.get('alt') or '').strip()
                        src = img.get('src', '')
                        # Skip student photos and university logos
                        if alt and alt.lower() not in ('confidential', '', 'darshan university') \
                                and 'student' not in src.lower() \
                                and 'profile' not in src.lower():
                            company = alt
                            break
            
            # Location: separate from company
            location = "N/A"
            for i, s in enumerate(strs):
                if s in ['Self Placed in', 'Placed in'] and i+1 < len(strs):
                    location = strs[i+1]
                    break
            
            # Build explicit sentence with both company and location
            loc_part = f" in {location}" if location != "N/A" else ""
            sentence = f"In the {year} placement drive for {branch}, student {name} (Enrollment Number: {enroll}) was placed at {company}{loc_part} with a package of {package}."
            if sentence not in seen:
                seen.add(sentence)
                student_sentences.append(sentence)
                
        except Exception:
            continue
            
    final_text = summary_header + "\n".join(stats_sentences) + "\n\n"
    if student_sentences:
        final_text += "Specific Student Placement Records:\n" + "\n".join(student_sentences)
        
    return final_text

os.makedirs("data/raw", exist_ok=True)

print(f"Starting to fetch {len(urls)} URLs for Structural Semantic Extraction V2...")
with open("data/raw/placements.jsonl", "w", encoding="utf-8") as f:
    for url in urls:
        print(f"Fetching {url}...")
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code != 200:
                print(f"Skipping {url}, status code: {resp.status_code}")
                continue
            
            raw_html = resp.text
            soup = BeautifulSoup(raw_html, "lxml")
            
            title = (soup.title.string or "").strip() if soup.title else ""
            meta_desc_tag = soup.find("meta", attrs={"name": "description"})
            meta_desc = (meta_desc_tag["content"] or "").strip() if meta_desc_tag and meta_desc_tag.has_attr("content") else ""
            headings = [h.text.strip() for h in soup.find_all(["h1", "h2", "h3"]) if h.text.strip()]
            
            main_html = extract_main_html(raw_html)
            text = semantically_extract_placements(raw_html, url)
            
            item = {
                "url": url,
                "canonical_url": canonicalize_url(url, keep_fragments=False),
                "title": title,
                "meta_description": meta_desc,
                "headings": headings,
                "raw_html": raw_html,
                "main_html": main_html,
                "text": text,
                "text_length": len(text or ""),
                "content_hash": compute_hash(text or ""),
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            }
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            time.sleep(0.5)
        except Exception as e:
            print(f"Error fetching {url}: {e}")

# Clean master file and append
master_file = "data/raw/pages_full_20260304_1333.jsonl"
print("Cleaning old placement objects from master file...")
cleaned_rows = []
try:
    with open(master_file, "r", encoding="utf-8") as rf:
        for line in rf:
            if not line.strip(): continue
            try:
                row = json.loads(line)
                url_field = row.get("url", "")
                if "/placement/list/" not in url_field:
                    cleaned_rows.append(line)
            except Exception:
                cleaned_rows.append(line)
                
    with open(master_file, "w", encoding="utf-8") as wf:
        wf.writelines(cleaned_rows)
        
    print("Cleaned. Now merging the newly extracted semantic records...")
    with open("data/raw/placements.jsonl", "r", encoding="utf-8") as rf:
        with open(master_file, "a", encoding="utf-8") as af:
            af.write("\n")
            af.write(rf.read())
            
    print("Successfully merged into", master_file)
except Exception as e:
    print(f"Error during merge: {e}")
