#!/usr/bin/env python3
"""
generateResumeLatex.py: Updates a LaTeX resume template with data from a resume JSON file.
Usage:
    python3 generateResumeLatex.py --json <path_to_resume_json> --tex <path_to_latex_template> -o <output_tex_file>

Note: Core formatting and update functions remain unchanged.
"""

import json
import argparse
import logging
import os
import re
import sys
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def format_date(iso_date):
    try:
        dt = datetime.datetime.strptime(iso_date, "%Y-%m")
        return dt.strftime("%b %Y")
    except Exception as e:
        logging.warning(f"Date conversion failed for {iso_date}: {e}")
        return iso_date

def read_json(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logging.info(f"Loaded JSON data from {json_file}")
        return data
    except Exception as e:
        logging.error(f"Error reading JSON file {json_file}: {e}")
        sys.exit(1)

def read_tex(tex_file):
    try:
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        logging.info(f"Loaded LaTeX template from {tex_file}")
        return content
    except Exception as e:
        logging.error(f"Error reading TeX file {tex_file}: {e}")
        sys.exit(1)

def update_introduction(tex_content, basics):
    urls = basics.get("urls", {})
    new_intro = (
        "\\introduction[\n"
        "    fullname={" + basics.get("name", "") + "},\n"
        "    email={" + basics.get("email", "") + "},\n"
        "    phone={" + basics.get("phone", "") + "},\n"
        "    linkedin={" + urls.get("linkedin", "") + "},\n"
        "    github={" + urls.get("github", "") + "}\n"
        "]"
    )
    pattern = re.compile(r"\\introduction\s*\[.*?\]", re.DOTALL)
    updated = re.sub(pattern, lambda m: new_intro, tex_content)
    logging.info("Updated introduction section.")
    return updated

def update_summary(tex_content, basics):
    summary_text = basics.get("summary", "").strip().replace('\n', ' ')
    new_summary = "\\summary{" + summary_text + "}"
    pattern = re.compile(r"\\summary\s*\{.*?\}", re.DOTALL)
    updated = re.sub(pattern, lambda m: new_summary, tex_content)
    logging.info("Updated summary section.")
    return updated

def generate_education_items(edu_list):
    items = []
    for idx, edu in enumerate(edu_list):
        university = edu.get("institution", "")
        graduation = format_date(edu.get("end", ""))
        grade = edu.get("gpa", "") + " GPA"
        program = edu.get("degree", "") + ", " + edu.get("field", "")
        block = (
            "\\educationItem[\n"
            "    university={" + university + "},\n"
            "    graduation={" + graduation + "},\n"
            "    grade={" + grade + "},\n"
            "    program={" + program + "}\n"
            "]"
        )
        items.append(block)
    return "".join(items) + "\n\\vspace{-\\baselineskip}"

def update_education_section(tex_content, edu_list):
    new_items = generate_education_items(edu_list)
    pattern = re.compile(r"(\\begin\{educationSection\}\{[^}]+\})(.*?)(\\end\{educationSection\})", re.DOTALL)
    updated = re.sub(pattern, lambda m: m.group(1) + "\n" + new_items + "\n" + m.group(3), tex_content)
    logging.info("Updated education section.")
    return updated

def generate_skill_items(skills_list):
    items = []
    for dict_item in skills_list:
        for key, value in dict_item.items():
            category = key.replace("_", " ").capitalize()
            block = (
                "\\skillItem[\n"
                "    category={" + category + "},\n"
                "    skills={" + value + "}\n"
                "]"
            )
            items.append(block + "\n\\\\")
    if items:
        items[-1] = items[-1].rstrip("\\")
    return "\n".join(items)

def update_skills_section(tex_content, skills_list):
    new_items = generate_skill_items(skills_list)
    pattern = re.compile(r"(\\begin\{skillsSection\}\{[^}]+\})(.*?)(\\end\{skillsSection\})", re.DOTALL)
    updated = re.sub(pattern, lambda m: m.group(1) + "\n" + new_items + "\n" + m.group(3), tex_content)
    logging.info("Updated skills section.")
    return updated

def generate_experience_items(work_list):
    items = []
    for idx, work in enumerate(work_list):
        company = work.get("company", "")
        location = work.get("location", "")
        position = work.get("position", "")
        duration = format_date(work.get("start", "")) + " - " + format_date(work.get("end", ""))
        header = (
            "\\experienceItem[\n"
            "    company={" + company + "},\n"
            "    location={" + location + "},\n"
            "    position={" + position + "},\n"
            "    duration={" + duration + "}\n"
            "]"
        )
        bullets = ""
        highlights = work.get("highlights", [])
        if highlights:
            bullets += "\\begin{itemize}\n    \\itemsep -6pt {}\n"
            for point in highlights:
                bullets += "    \\item " + point + "\n"
            bullets += "\\end{itemize}"
        full_block = header + "\n" + bullets
        items.append(full_block)
    return "\n".join(items)

def update_experience_section(tex_content, work_list):
    new_items = generate_experience_items(work_list)
    pattern = re.compile(r"(\\begin\{experienceSection\}\{\s*Professional Experience\s*\})(.*?)(\\end\{experienceSection\})", re.DOTALL)
    updated = re.sub(pattern, lambda m: m.group(1) + "\n" + new_items + "\n" + m.group(3), tex_content)
    logging.info("Updated professional experience section.")
    return updated

def generate_project_items(proj_list):
    items = []
    for idx, proj in enumerate(proj_list):
        title = proj.get("name", "")
        duration = format_date(proj.get("start", "")) + " - " + format_date(proj.get("end", ""))
        url = proj.get("url", "")
        # key_highlight = f"GitHub - \\href{{{url}}}{{Link}}" if url else ""
        key_highlight = f"GitHub - {url}" if url else ""  # ← new: full plain URL
        header = (
            "\\projectItem[\n"
            f"    title={{{title}}},\n"
            f"    duration={{{duration}}},\n"
            f"    keyHighlight={{{key_highlight}}}\n"
            "]"
        )
        bullets = ""
        highlights = proj.get("highlights", [])
        if highlights:
            bullets += "\\begin{itemize}\n    \\vspace{-0.5em}\n    \\itemsep -6pt {}\n"
            for point in highlights:
                bullets += "    \\item " + point + "\n"
            bullets += "\\end{itemize}"
        full_block = header + "\n" + bullets
        items.append(full_block)
    return "\n".join(items)

def update_academic_projects_section(tex_content, proj_list):
    new_items = generate_project_items(proj_list)
    pattern = re.compile(r"(\\begin\{experienceSection\}\{\s*Academic\s+projects\s*\})(.*?)(\\end\{experienceSection\})",
                         re.IGNORECASE | re.DOTALL)
    updated = re.sub(pattern, lambda m: m.group(1) + "\n" + new_items + "\n" + m.group(3), tex_content)
    logging.info("Updated academic projects section.")
    return updated

def update_tex_file(tex_content, data):
    basics = data.get("basics", {})
    tex_content = update_introduction(tex_content, basics)
    tex_content = update_summary(tex_content, basics)
    if "education" in data:
        tex_content = update_education_section(tex_content, data["education"])
    if "skills" in data:
        tex_content = update_skills_section(tex_content, data["skills"])
    if "work" in data:
        tex_content = update_experience_section(tex_content, data["work"])
    if "projects" in data:
        tex_content = update_academic_projects_section(tex_content, data["projects"])
    return tex_content

def write_output(tex_content, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(tex_content)
        logging.info(f"Final LaTeX file generated: {output_file}")
    except Exception as e:
        logging.error(f"Error writing output file {output_file}: {e}")
        sys.exit(1)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Update a LaTeX resume template with resume.json data.")
    parser.add_argument("--json", default="resume.json", help="Path to resume JSON file (default: resume.json)")
    parser.add_argument("--tex", default="resume.tex", help="Path to LaTeX template file (default: resume.tex)")
    parser.add_argument("-o", "--output", required=True, help="Output LaTeX file name (e.g., meta.tex)")
    return parser.parse_args()

def main():
    args = parse_arguments()
    if not os.path.exists(args.json):
        logging.error(f"JSON file not found: {args.json}")
        sys.exit(1)
    if not os.path.exists(args.tex):
        logging.error(f"LaTeX template file not found: {args.tex}")
        sys.exit(1)
    
    data = read_json(args.json)
    tex_content = read_tex(args.tex)
    updated_tex = update_tex_file(tex_content, data)
    write_output(updated_tex, args.output)

if __name__ == "__main__":
    main()
