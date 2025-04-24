#!/usr/bin/env python3
"""
validateYamlStructure.py: Validates the user's resume YAML file against the structure of a template.
- Supports optional fields
- Supports flexible skill sections with arbitrary categories
"""

import yaml
import argparse
import os
import sys

def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def compare_structure(template, actual, path=""):
    if isinstance(template, dict):
        if not isinstance(actual, dict):
            raise ValueError(f"Expected a dictionary at '{path}', but got {type(actual).__name__}")
        for key in template:
            if key not in actual:
                if template[key] in [None, "", [], {}]:
                    continue  # optional field
                else:
                    raise KeyError(f"Missing key '{path + key}' in resume YAML.")
            # Special handling for "skills"
            if key == "skills":
                validate_skills_section(actual[key], path + key)
            else:
                compare_structure(template[key], actual[key], path + key + ".")

    elif isinstance(template, list):
        if not isinstance(actual, list):
            raise ValueError(f"Expected a list at '{path}', but got {type(actual).__name__}")
        if template and isinstance(template[0], dict):
            for i, item in enumerate(actual):
                compare_structure(template[0], item, path + f"[{i}].")

def validate_skills_section(skills_list, path):
    if not isinstance(skills_list, list) or not skills_list:
        raise ValueError(f"The 'skills' section at '{path}' must be a non-empty list.")
    for i, item in enumerate(skills_list):
        if not isinstance(item, dict) or not item:
            raise ValueError(f"Each entry in 'skills[{i}]' must be a dictionary with at least one key-value pair.")

def main():
    parser = argparse.ArgumentParser(description="Validate resume YAML structure.")
    parser.add_argument('--resume', required=True, help="Path to user resume YAML file")
    parser.add_argument('--template', required=True, help="Path to template YAML file")
    args = parser.parse_args()

    if not os.path.exists(args.resume):
        print(f"❌ Resume YAML file not found: {args.resume}")
        sys.exit(1)
    if not os.path.exists(args.template):
        print(f"❌ Template YAML file not found: {args.template}")
        sys.exit(1)

    try:
        template = load_yaml(args.template)
        actual = load_yaml(args.resume)
        compare_structure(template, actual)
        print("✅ Resume YAML structure is valid.")
    except Exception as e:
        print(f"❌ YAML validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
