import os
import csv
import re

# Define paths
directory = os.path.dirname(os.path.abspath(__file__))
source_path = os.path.join(directory, "source.txt")
output_path = os.path.join(directory, "university_contacts.csv")

def generate_default_data():
    """Generates the full default database structure based on the prompt template."""
    universities = [
        "Cairo University",
        "Cairo National University",
        "Helwan University",
        "Helwan National University",
        "Alexandria University",
        "Alexandria National University",
        "Mansoura University",
        "New Mansoura University",
        "Beni-Suef University"
    ]
    
    faculties = [
        {"name": "Faculty of Medicine", "years": 5},
        {"name": "Faculty of Dentistry", "years": 5},
        {"name": "Faculty of Veterinary Medicine", "years": 5},
        {"name": "Faculty of Nursing", "years": 4},
        {"name": "Faculty of Physical Therapy", "years": 4},
        {"name": "Faculty of Pharmacy", "years": 4},
        {"name": "Faculty of Science", "years": 4}
    ]
    
    rows = []
    for uni in universities:
        for fac in faculties:
            fac_name = fac["name"]
            leader_name = "LeaderName"
            leader_contact = "LeaderContact"
            
            for yr in range(1, fac["years"] + 1):
                year_name = f"{yr}st Year" if yr == 1 else f"{yr}nd Year" if yr == 2 else f"{yr}rd Year" if yr == 3 else f"{yr}th Year"
                for p in range(1, 6):
                    rows.append({
                        "University": uni,
                        "Faculty": fac_name,
                        "Faculty Leader Name": leader_name,
                        "Faculty Leader Contact": leader_contact,
                        "Year": year_name,
                        "Person Number": f"Person {p}",
                        "Person Name": "Name",
                        "Person Contact": "Contact"
                    })
    return rows

def parse_source_file(file_path):
    """Parses a text file with hierarchical structure into flat list of rows."""
    rows = []
    
    current_uni = ""
    current_fac = ""
    current_leader_name = ""
    current_leader_contact = ""
    current_year = ""
    
    # Regular expressions to parse quotes
    quotes_re = re.compile(r'"([^"]*)"')
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue
                
            # Level 4: Person (starts with four dashes)
            if stripped.startswith("----"):
                person_text = stripped[4:].strip()
                if ":" in person_text:
                    person_part, details_part = person_text.split(":", 1)
                    person_number = person_part.strip()
                    quotes = quotes_re.findall(details_part)
                    p_name = quotes[0] if len(quotes) > 0 else ""
                    p_contact = quotes[1] if len(quotes) > 1 else ""
                else:
                    person_number = person_text
                    p_name = ""
                    p_contact = ""
                    
                rows.append({
                    "University": current_uni,
                    "Faculty": current_fac,
                    "Faculty Leader Name": current_leader_name,
                    "Faculty Leader Contact": current_leader_contact,
                    "Year": current_year,
                    "Person Number": person_number,
                    "Person Name": p_name,
                    "Person Contact": p_contact
                })
                
            # Level 3: Year (starts with three dashes)
            elif stripped.startswith("---"):
                current_year = stripped[3:].strip()
                
            # Level 2: Faculty (starts with two dashes)
            elif stripped.startswith("--"):
                faculty_text = stripped[2:].strip()
                if ":" in faculty_text:
                    fac_part, leader_part = faculty_text.split(":", 1)
                    current_fac = fac_part.strip()
                    quotes = quotes_re.findall(leader_part)
                    current_leader_name = quotes[0] if len(quotes) > 0 else ""
                    current_leader_contact = quotes[1] if len(quotes) > 1 else ""
                else:
                    current_fac = faculty_text
                    current_leader_name = ""
                    current_leader_contact = ""
                    
            # Level 1: University (starts with one dash)
            elif stripped.startswith("-"):
                current_uni = stripped[1:].strip()
                
    return rows

def main():
    print("Starting conversion to Excel/CSV...")
    
    if os.path.exists(source_path) and os.path.getsize(source_path) > 0:
        print(f"Found source text file at '{source_path}'. Parsing...")
        try:
            rows = parse_source_file(source_path)
            print(f"Successfully parsed {len(rows)} contact entries from '{source_path}'.")
        except Exception as e:
            print(f"Error parsing '{source_path}': {e}")
            print("Falling back to generating default template structure...")
            rows = generate_default_data()
    else:
        print(f"No source text file found or file is empty at '{source_path}'.")
        print("Generating complete default Egyptian universities directory structure...")
        rows = generate_default_data()
        
        # Write a sample source.txt for reference
        try:
            with open(source_path, "w", encoding="utf-8") as sf:
                sf.write("# You can edit this file with your custom directory structure and re-run parser.py to update the CSV.\n")
                sf.write("- Cairo University\n")
                sf.write("-- Faculty of Medicine: \"LeaderName\" \"LeaderContact\"\n")
                sf.write("--- 1st Year\n")
                sf.write("---- Person 1: \"Name\" \"Contact\"\n")
                sf.write("---- Person 2: \"Name\" \"Contact\"\n")
                sf.write("---- Person 3: \"Name\" \"Contact\"\n")
                sf.write("---- Person 4: \"Name\" \"Contact\"\n")
                sf.write("---- Person 5: \"Name\" \"Contact\"\n")
            print(f"Created sample text file at '{source_path}' for future editing.")
        except Exception as e:
            print(f"Warning: Could not create sample source.txt: {e}")
            
    # Write rows to CSV
    columns = [
        "University", "Faculty", "Faculty Leader Name", "Faculty Leader Contact",
        "Year", "Person Number", "Person Name", "Person Contact"
    ]
    
    try:
        with open(output_path, "w", newline="", encoding="utf-8-sig") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Excel-ready CSV file successfully created at:\n{output_path}")
        print(f"Total rows: {len(rows)}")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

if __name__ == "__main__":
    main()
