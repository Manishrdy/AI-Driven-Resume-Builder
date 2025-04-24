#!/usr/bin/env python3
"""
convertResumeToJson.py: Converts a structured YAML resume file into a JSON formatted resume.
If expected fields are missing, they are added with a null or empty value.
Also normalizes phone numbers by replacing uncommon Unicode dashes with a standard hyphen.

Usage:
    python3 convertResumeToJson.py --input <path_to_yaml_file> --output <path_to_json_file>

Note: Core functions remain unaltered.
"""

import os
import json
import logging
import argparse
import yaml
from copy import deepcopy

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

DEFAULT_RESUME_STRUCTURE = {
    "basics": {
        "name": None,
        "headline": None,
        "email": None,
        "phone": None,
        "location": {
            "city": None,
            "region": None,
            "country": None,
        },
        "urls": {
            "linkedin": None,
            "github": None,
        },
        "summary": None,
    },
    "education": [],
    "work": [],
    "projects": [],
    "certifications": [],
    "skills": []
}

def merge_defaults(data, defaults):
    if isinstance(defaults, dict):
        if not isinstance(data, dict):
            data = {}
        merged = {}
        for key, default_value in defaults.items():
            if key in data:
                merged[key] = merge_defaults(data.get(key), default_value)
            else:
                merged[key] = deepcopy(default_value)
        for key, value in data.items():
            if key not in merged:
                merged[key] = value
        return merged
    elif isinstance(defaults, list):
        if isinstance(data, list):
            return data
        else:
            return []
    else:
        return data if data is not None else defaults

def normalize_phone_number(phone: str) -> str:
    if phone:
        replacements = {
            "\u2010": "-",
            "\u2011": "-",
            "\u2012": "-",
            "\u2013": "-",
            "\u2014": "-",
            "\u2015": "-"
        }
        for uni_dash, ascii_dash in replacements.items():
            phone = phone.replace(uni_dash, ascii_dash)
    return phone

def load_yaml_file(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            logger.info("YAML file loaded successfully: %s", file_path)
            return data
    except Exception as e:
        logger.error("Error loading YAML file '%s': %s", file_path, e)
        raise

def convert_to_json(data) -> str:
    try:
        json_data = json.dumps(data, indent=4)
        logger.info("Data successfully converted to JSON format.")
        return json_data
    except Exception as e:
        logger.error("Error converting data to JSON: %s", e)
        raise

def main():
    parser = argparse.ArgumentParser(
        description="Convert a structured YAML resume file into a JSON formatted resume."
    )
    parser.add_argument('--input', type=str, required=True, help="Path to the structured YAML resume file.")
    parser.add_argument('--output', type=str, required=True, help="Output file path for the JSON resume.")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        logger.error("The input YAML file does not exist: %s", args.input)
        return

    try:
        yaml_data = load_yaml_file(args.input)
        complete_data = merge_defaults(yaml_data, DEFAULT_RESUME_STRUCTURE)
        
        if complete_data.get("basics", {}).get("phone"):
            complete_data["basics"]["phone"] = normalize_phone_number(complete_data["basics"]["phone"])
            
        json_output = convert_to_json(complete_data)
        with open(args.output, 'w', encoding='utf-8') as out_file:
            out_file.write(json_output)
        logger.info("JSON data has been written to: %s", args.output)
    except Exception as e:
        logger.exception("An error occurred during the conversion process: %s", e)

if __name__ == "__main__":
    main()
