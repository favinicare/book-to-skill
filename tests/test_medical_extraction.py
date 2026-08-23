import json from scripts.extractor.medical_extractor import extract_from_textfrom tools.validate_medical_skill import load_schema, validate_recommendation

SAMPLE = “””Recommendations:

1. We recommend that adults with condition X should receive treatment Y (strong recommendation, high quality evidence) (Smith 2020).

2. For pregnant women, do not use treatment Z.“””

def test_extract_and_validate():out = extract_from_text(SAMPLE, source_label=“sample”)assert “recommendations” in outassert len(out[“recommendations”]) >= 1schema = load_schema()for rec in out[“recommendations”]:ok, err = validate_recommendation(rec, schema)assert ok, f”validation error: {err}”


Arquivo 9Caminho: .github/workflows/medical-integration.ymlConteúdo:name: medical-guideline-integration

on:push:branches:- medical-guideline-integrationworkflow_dispatch:

jobs:test:runs-on: ubuntu-lateststeps:- uses: actions/checkout@v4- name: Setup Pythonuses: actions/setup-python@v4with:python-version: “3.10”- name: Install dependenciesrun: |python -m pip install –upgrade pippip install jsonschema pytest- name: Run testsrun: |pytest -q- name: Lint / quick checkrun: |test -f docs/schemas/clinical_recommendation.schema.json && echo “schema ok”