# AI-Driven Resume Builder 🚀

Transform a structured YAML resume into tailored, professional-grade PDF and DOCX formats—fully customized for any job description using Large Language Models.

---

## 📌 Features

- 🧩 **YAML to JSON**: Converts structured resume data into normalized JSON format with default fallbacks.
- 🎨 **LaTeX Integration**: Dynamically fills out a LaTeX template with resume content.
- 🧠 **LLM Personalization**: Tailors summary, experience, projects, and skills to match a job description (via Perplexity API).
- 📄 **Multi-format Output**: Outputs resume in both PDF and DOCX formats.
- 🧹 **Clean Compilation**: Handles LaTeX auxiliary files post-compilation.

---

## 🛠️ Tech Stack

- Python 3
- PyYAML
- LaTeX (xelatex)
- pdf2docx
- Perplexity API (LLM via `sonar-pro`)

---

## 📁 Project Structure

    ai-resume-builder/
    ├── data/
    │   ├── resume.yaml              # ✅ Your YAML resume file (based on template.yaml)
    │   ├── template.yaml            # 📋 YAML structure template for reference
    │   ├── job_description.txt      # 📝 Paste the job description here
    │   └── resume.tex               # 🎨 Base LaTeX template
    ├── config.yml                   # ⚙️ Edit this for your Perplexity API key and paths
    ├── 1_parse_resume_yaml.py       # 🔁 Convert YAML to JSON (with field normalization)
    ├── 3_resume_generator_tex.py    # 🛠️ Injects resume data into LaTeX template
    ├── 4_tex_to_pdf.py              # 📄 Compiles LaTeX to PDF and converts to DOCX
    ├── requirements.txt             # 📦 Dependencies list
    └── README.md                    # 📘 You’re here!

---

## 🚀 How to Use This Project

Follow these steps to generate a tailored PDF/DOCX resume using your own data and job description:

---

### 🧩 Step 1: Create Your Resume

1. Go to `data/template.yaml` to view the structure of the resume YAML.
2. Create your own resume file following that structure.
3. Save it as `data/resume.yaml`.  
   ✅ A sample `resume.yaml` is already provided for reference.

---

### 🛠️ Step 2: Configure the Project

1. Open the `config.yml` file.
2. Update the following fields:
   ```yaml
   api_key: "your-perplexity-api-key-here"  # 🔑 Required
   model: "sonar-pro"                        # 🧠 Model name
   resume_yaml: "data/resume.yaml"          # 📄 Your actual resume file
   job_description_file: "data/job_description.txt"  # 📋 Paste your JD here
3. ⚠️ Do not change the rest of the keys in the config file.

---

### 📋 Step 3: Paste Your Job Application Description

1. Open data/job_description.txt and paste the complete job description of the position you want to apply for. Save and close the file.

---

### 📦 Step 4: Install Requirements

1. Run the following command to install all necessary dependencies:
    ```python
    pip install -r requirements.txt

---

### 🏗️ Step 5: Generate Your Resume

1. Run the following command
    ```python
    python main.py -o filename

---

### ✅ Done! Your Final Resume Is Ready
