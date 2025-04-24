#!/usr/bin/env python3
"""
convertLatexToPdfDocx.py: Converts a given LaTeX (.tex) file to PDF and DOCX.

This script:
  - Accepts a TeX file via the -o/--output option.
  - Sets the TEXINPUTS environment variable so that xelatex can locate required class files (e.g. resume.cls in the data folder).
  - Compiles the TeX file using xelatex.
  - Converts the resulting PDF to DOCX using pdf2docx.

Usage:
    python3 convertLatexToPdfDocx.py -o <tex_file>
Example:
    python3 convertLatexToPdfDocx.py -o meta.tex
"""

import subprocess
from pdf2docx import Converter
import os
import argparse

def tex_to_pdf(tex_filename):
    print(f"Compiling {tex_filename} to PDF...")
    # Prepare environment so that xelatex will find resume.cls in the data folder.
    env = os.environ.copy()
    # "data//;" ensures recursive searching in the data directory.
    env["TEXINPUTS"] = "data//;" + env.get("TEXINPUTS", "")
    
    # Run xelatex twice to resolve all references.
    for i in range(2):
        print(f" - Pass {i + 1} of xelatex...")
        result = subprocess.run(
            ['xelatex', '-interaction=nonstopmode', tex_filename],
            env=env
        )
        if result.returncode != 0:
            print(f"⚠️ Warning: xelatex exited with code {result.returncode}. Check your .tex file.")
            break

    pdf_file = tex_filename.rsplit('.tex', 1)[0] + '.pdf'
    if os.path.exists(pdf_file):
        print(f"✅ PDF generated: {pdf_file}")
        clean_auxiliary_files(tex_filename)
    else:
        print("❌ PDF not found after compilation.")
    return pdf_file

def clean_auxiliary_files(tex_filename):
    base_name = tex_filename.rsplit('.tex', 1)[0]
    # Removed '.log' from the deletion list so the log file is preserved.
    extensions = ['.aux', '.out', '.toc', '.synctex.gz']
    deleted = []
    for ext in extensions:
        file_path = base_name + ext
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                deleted.append(file_path)
            except Exception as e:
                print(f"⚠️ Could not delete {file_path}: {e}")
    if deleted:
        print(f"🧹 Deleted auxiliary files: {', '.join(deleted)}")


def pdf_to_docx(pdf_file, docx_file):
    print(f"Converting {pdf_file} to {docx_file}...")
    if not os.path.exists(pdf_file):
        print(f"❌ PDF file {pdf_file} not found.")
        return
    try:
        cv = Converter(pdf_file)
        cv.convert(docx_file, start=0, end=None)
        cv.close()
        if os.path.exists(docx_file):
            print(f"✅ DOCX generated: {docx_file}")
        else:
            print("❌ DOCX not created.")
    except Exception as e:
        print(f"❌ Error during DOCX conversion: {e}")

def tex_to_docx(tex_file):
    pdf_file = tex_to_pdf(tex_file)
    docx_file = tex_file.rsplit('.tex', 1)[0] + '.docx'
    pdf_to_docx(pdf_file, docx_file)

def main():
    parser = argparse.ArgumentParser(description="Convert a TeX file to PDF and DOCX.")
    parser.add_argument("-o", "--output", required=True, help="Path to the TeX file to be converted.")
    args = parser.parse_args()

    tex_file = args.output
    if not os.path.exists(tex_file):
        print(f"❌ TeX file not found: {tex_file}")
        return

    tex_to_docx(tex_file)

if __name__ == '__main__':
    main()
