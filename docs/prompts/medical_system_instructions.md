Medical system instructions (PT-BR)

Objetivo:

• Extrair recomendações clínicas acionáveis de um documento (guideline, capítulo, artigo) e estruturar cada recomendação em JSON conforme docs/schemas/clinical_recommendation.schema.json.

• Identificar PICO quando possível, nível de evidência (GRADE quando mencionado), e prover fragmento de prova (trecho do texto e referência/página).

• Quando o texto contiver um algoritmo de decisão (ex.: fluxograma, “if/then” encadeado), gerar também um grafo de decisão (nodes/edges) no campo “decision_graph”.

Regras críticas:

1. Saída estrita: retorne apenas JSON válido. O objeto raiz deve ter: source, extracted_at, embedding_provider (string), recommendations (array).

2. Para cada recommendation:

• Preencher id, text e provenance.source obrigatórios.

• Incluir provenance.page ou char_offset quando disponível.

• Incluir references (array) quando há citações.

• Incluir strength e level_of_evidence se presentes; caso contrário use “unspecified”.

• Incluir field requires_human_review: true

• Se ontologia foi solicitada mas credenciais faltam, inclua ontology_lookup.warning = “ontology_lookup_requires_credentials”.

3. Ao gerar grafo: produzir structure: { “nodes”: [{“id”,“label”,“concepts”:[]}], “edges”: [{“from”,“to”,“condition”,“threshold”:null}] }

4. Não invente níveis de evidência; se não estiverem explícitos, marque level_of_evidence=“unspecified” e confidence baixo.

5. Sempre incluir um pequeno trecho textual (<=300 chars) como justificativa em recommendation.provenance.justifying_snippet.

Prompt template (EN)Read the following document text and extract all clinical recommendations. Return a single JSON object with:

• source: “”

• extracted_at: ISO datetime

• embedding_provider: “{{EMBEDDING_PROVIDER}}”

• recommendations: [ … ]

Each recommendation must conform to the clinical_recommendation.schema.json. Include “requires_human_review”: true in every recommendation, and include provenance.justifying_snippet (<=300 chars). If explicit decision algorithms are present, include a “decision_graph” object with nodes/edges. If ontology lookup was requested but credentials are not configured, set ontology_lookup.warning = “ontology_lookup_requires_credentials”.

Do not include any other content outside the JSON.

Prompt template (PT-BR)Leia o texto do documento a seguir e extraia todas as recomendações clínicas. Retorne um único objeto JSON com:

• source: “<arquivo ou rótulo>”

• extracted_at: data/hora ISO

• embedding_provider: “{{EMBEDDING_PROVIDER}}”

• recommendations: [ … ]

Cada recommendation deve obedecer ao docs/schemas/clinical_recommendation.schema.json. Inclua “requires_human_review”: true em cada recomendação e um trecho justificativo em provenance.justifying_snippet (<=300 chars). Se houver algoritmos de decisão explícitos, inclua um campo “decision_graph”. Se a consulta a ontologias foi solicitada mas faltam credenciais, defina ontology_lookup.warning = “ontology_lookup_requires_credentials”.

Exemplo de instrução curta (EN):Extract recommendations and PICO from the text below. Return strict JSON following the clinical schema. Do not add prose or explanations.

Exemplo de instrução curta (PT-BR):Extraia recomendações e elementos PICO do texto abaixo. Retorne JSON estrito segundo o schema clínico. Não acrescente explicações em prosa.

Security note:

• Always mark “requires_human_review”: true. Never output clinical advice without that flag and provenance.


Arquivo 5Caminho: docs/medical-guidelines.mdConteúdo:

Medical guidelines mode — usage and safety

Overview

• Use --mode medical (or BOOK_TYPE=medical) to run the medical-specific extractor and generate medical-oriented skill artifacts (recommendations JSON, decision graphs, glossary items).

Requirements

• Python 3.8+

• Optional for improved clinical NER/ontology mapping:

• medSpaCy, scispacy

• UMLS/SNOMED credentials (see notes below)

Embedding provider

• Set EMBEDDING_PROVIDER env var to choose embedding backend:export EMBEDDING_PROVIDER=openaiSupported values (example): openai, cohere, azure, local

How it works (short)

• The medical extractor finds likely recommendation sections, extracts recommendations as JSON objects (with PICO-ish fields), includes provenance and a small justifying snippet, and optionally can create a decision_graph object for algorithms.

• Ontology mapping (UMLS/SNOMED/ICD) is NOT enabled by default because these services require credentials/licenses. When missing, extractor emits metadata: “ontology_lookup_requires_credentials”.

Safety & compliance

• All outputs must be reviewed by a qualified clinician before any operational use.

• Do not send patient-identifiable data to third-party cloud models unless allowed by your institutional policies (HIPAA/GDPR).

• When enabling ontology lookups, ensure you have the proper license and handle credentials securely.

Checklist before any clinical use

• Validate extracted JSON using tools/validate_medical_skill.py

• Human clinician review of each recommendation and decision graph

• Confirm provenance (source files/pages) for each high-impact recommendation

• Institutional legal/compliance review completed

Enabling ontology mapping (notes)

• Obtain UMLS account and API credentials or licensed SNOMED access as required by your jurisdiction.

• Store credentials in environment variables (example names documented in docs/schemas/README.md).

• The extractor will check for these env vars; if absent, it will continue but add a warning in the output JSON.

Limitations

• This is an MVP. NLP heuristics are intentionally conservative. Always prefer human validation.