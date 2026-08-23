#!/usr/bin/env python3“””Validate medical extractor outputs against the clinical recommendation JSON schemaand run additional provenance/flag checks.“””import jsonimport sysfrom jsonschema import validate, ValidationErrorfrom pathlib import Path

SCHEMA_PATH = Path(file).resolve().parents[1] / “docs” / “schemas” / “clinical_recommendation.schema.json”

def load_schema():with open(SCHEMA_PATH, “r”, encoding=“utf-8”) as f:return json.load(f)

def validate_recommendation(rec, schema):try:validate(instance=rec, schema=schema)return True, Noneexcept ValidationError as e:return False, str(e)

def validate_file(path):data = json.load(open(path, “r”, encoding=“utf-8”))schema = load_schema()problems = []for rec in data.get(“recommendations”, []):ok, err = validate_recommendation(rec, schema)if not ok:problems.append({“id”: rec.get(“id”), “error”: err})# provenance checksprov = rec.get(“provenance”, {})if “source” not in prov:problems.append({“id”: rec.get(“id”), “error”: “missing provenance.source”})if rec.get(“requires_human_review”) is not True:problems.append({“id”: rec.get(“id”), “error”: “requires_human_review not set true”})return problems

if name == “main”:if len(sys.argv) < 2:print(“Usage: validate_medical_skill.py <extracted_json>”)sys.exit(2)path = sys.argv[1]problems = validate_file(path)if problems:print(“Validation failed:”)for p in problems:print(p)sys.exit(1)print(“Validation passed”)sys.exit(0)