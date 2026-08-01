"""Compatibility import for the governed OTP-UMBRELLA-SYNC-001 validator.

The authoritative implementation lives under governance/validators and is
exercised by the repository unit-test suite. This module intentionally contains
no executable entrypoint.
"""

from governance.validators.openai_ten_proofs_umbrella_sync import (  # noqa: F401
    DOCUMENT_PATH,
    EXPECTED_FORGE_ARTIFACTS,
    RECORD_PATH,
    SCHEMA_PATH,
    load_json,
    validation_errors,
)
