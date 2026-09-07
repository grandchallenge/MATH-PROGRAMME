# Volume IV — PROTOCOL RC1 source admission packet

This directory preserves an exact, content-addressed rebuildable representation of the composition-complete RC1 source archive for **Volume IV — PROTOCOL: Computation as Communication**.

The source archive is the exact built source at `9e7d817daf388e020ceb2b4d83bb7543d8c57f12` used by Gate-7 run `34170916991`. It is transported as ordered Base64 text chunks. `SOURCE_TRANSPORT_MANIFEST.json` fixes the order, character lengths, Git blob identities, decoded size, and expected SHA-256. Run `python RECONSTRUCT_SOURCE.py` from this directory to reconstruct and verify the archive.

Canonical decoded source identity:

`sha256:48e2d1f32b1cbf8349ddd3a0f5a807781c6e75b50a411fba8a8f8f038302508e`

This packet is an admission artifact, not a mathematical review or publication-authority record. Until protected merge and protected readback occur, RC1 is composition-complete but not durably admitted. Independent mathematical review remains pending and publication authority is not granted.
