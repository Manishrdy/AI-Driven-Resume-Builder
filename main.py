#!/usr/bin/env python3
import subprocess
import os
import yaml
import argparse
import sys
import shutil

def load_config():
    # config.yml is located at the project root.
    config_path = os.path.join(os.getcwd(), "config.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Orchestrate the resume generation pipeline.")
    parser.add_argument("-o", "--output", required=True, help="Base output file name (e.g., meta)")
    args = parser.parse_args()

    config = load_config()

    # File paths from configuration (files are assumed under the data/ folder relative to project root)
    resume_yaml = config.get("resume_yaml", os.path.join("data", "resume.yaml"))
    job_description_file = config.get("job_description_file", os.path.join("data", "job_description.txt"))
    latex_template = config.get("latex_template", os.path.join("data", "resume.tex"))

    # Load resume and template paths from config
    resume_yaml = config.get("resume_yaml", os.path.join("data", "resume.yaml"))
    template_yaml = config.get("template_yaml", os.path.join("data", "template.yaml"))

    # Base name and output filenames (generated in the current working directory)
    base_name = args.output.strip()
    json_file = f"{base_name}_resume.json"
    tex_file = f"{base_name}.tex"
    
    # Build full paths to the helper scripts inside the "scripts" folder.
    scripts_folder = os.path.join(os.getcwd(), "scripts")
    parse_script = os.path.join(scripts_folder, "convertResumeToJson.py")
    api_script   = os.path.join(scripts_folder, "enhanceResumeWithAPI.py")
    gen_script   = os.path.join(scripts_folder, "generateResumeLatex.py")
    conv_script  = os.path.join(scripts_folder, "convertLatexToPdfDocx.py")
    
    # Use the current Python interpreter.
    python_cmd = sys.executable

    # Step 0: Validate YAML structure
    validate_script = os.path.join("scripts", "validateYamlStructure.py")
    print("Step 0: Validating resume YAML structure...")
    subprocess.run([
        sys.executable, validate_script,
        "--resume", resume_yaml,
        "--template", template_yaml
    ], check=True)

    # Step 1: Convert YAML resume to JSON.
    print("Step 1: Converting YAML to JSON...")
    subprocess.run([
        python_cmd, parse_script,
        "--input", resume_yaml,
        "--output", json_file
    ], check=True)

    # Step 2: Update the resume JSON using the job description (via an API call).
    print("Step 2: Updating resume JSON with job description...")
    subprocess.run([
        python_cmd, api_script,
        "--resume", json_file,
        "--jd", job_description_file
    ], check=True)

    # Step 3: Generate the LaTeX file from the updated JSON and template.
    print("Step 3: Generating LaTeX resume...")
    subprocess.run([
        python_cmd, gen_script,
        "--json", json_file,
        "--tex", latex_template,
        "--output", tex_file
    ], check=True)

    # Step 4: Convert the LaTeX file to PDF and DOCX.
    print("Step 4: Converting LaTeX to PDF and DOCX...")
    subprocess.run([
        python_cmd, conv_script,
        "-o", tex_file
    ], check=True)

    # Final Step: Create a folder named after base_name and move generated files into it.
    target_folder = os.path.join(os.getcwd(), base_name)
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
        print(f"Created folder: {target_folder}")
    else:
        print(f"Folder {target_folder} already exists. Files will be moved into it.")

    # List the files to be moved.
    files_to_move = [
        json_file,
        tex_file,
        f"{base_name}.pdf",
        f"{base_name}.docx",
        f"{base_name}.log"
    ]

    for file in files_to_move:
        if os.path.exists(file):
            shutil.move(file, os.path.join(target_folder, file))
            print(f"Moved {file} to {target_folder}")
        else:
            print(f"❌ File {file} not found, cannot move.")

if __name__ == "__main__":
    main()
