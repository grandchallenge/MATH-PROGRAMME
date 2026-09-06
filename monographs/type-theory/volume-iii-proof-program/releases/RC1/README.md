# Volume III — PROOF / PROGRAM RC1 source admission packet

This directory preserves an exact, content-addressed rebuildable representation of the composition-complete RC1 source archive for **Volume III — PROOF / PROGRAM: Logic Becomes Executable**.

The source archive is transported as ordered Base64 text chunks. `SOURCE_TRANSPORT_MANIFEST.json` fixes the order, character lengths, Git blob identities, decoded size, and expected SHA-256. Run `python RECONSTRUCT_SOURCE.py` from this directory to reconstruct and verify the archive.

Canonical decoded source identity:

`sha256:70c9ffedefa795cf40e2536c45db8a7f3fb0223719d4c6cf24f921e7637d7a62`

This packet is an admission artifact, not a mathematical review or publication-authority record. Until protected merge and protected readback occur, RC1 remains composition-complete but not durably admitted. Independent mathematical review remains pending and publication authority is not granted.
