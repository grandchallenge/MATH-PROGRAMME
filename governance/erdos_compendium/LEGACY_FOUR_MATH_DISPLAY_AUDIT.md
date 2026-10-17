# Erdős Compendium — four admitted display-math corrections

Issue: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2698

Confirmed affected problem IDs: #665, #669, #776 and #777. The main
manuscripts are already editorially admitted in EC-BULK-005-R7/R8. Existing
admission SHA-256 values, source issue evidence, mathematical status, and
review documents are immutable.

A source-only mathematical-typography amendment is required for their
unrendered display blocks. Reposition empty Markdown lines from *inside*
the existing $$ delimiters to outside, without modifying any nonwhitespace
text or mathematical characters. Record old and new raw and normalized
SHA-256 and the unchanged nonwhitespace fingerprint in a separate protected
amendment; retain the original admission ledger. Scope is typography only,
not mathematical certification.

Acceptance: exactly four records bound to issue #2698, approved protected PR,
successful strict MkDocs build, passing source QA and browser verification for
both GitHub Markdown and the deployed GitHub Pages output.
