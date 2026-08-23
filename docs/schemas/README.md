Note on ontology integration

• UMLS and SNOMED mapping requires credentials/licenses. The code includes placeholders and will emit metadata:“ontology_lookup”: {“status”:“skipped”,“warning”:“ontology_lookup_requires_credentials”}

• To enable mapping: obtain UMLS credentials, set environment variables (see docs/medical-guidelines.md), and run an ontology mapping tool.

Policy:

• When ontology credentials are missing, the extractor must NOT call external ontology services.

• The extractor will instead include the warning metadata and continue.
