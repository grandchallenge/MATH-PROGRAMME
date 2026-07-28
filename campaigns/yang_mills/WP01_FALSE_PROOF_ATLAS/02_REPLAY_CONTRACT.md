# YM-WP01 Replay Contract

The replay is a regression audit. It validates the atlas structure and controlled semantics.

It must reject:

- missing or duplicate fixture IDs;
- any fixture count other than twenty;
- missing invalid inference, obligation, witness, remediation, interface, or non-overreach boundary;
- decisions outside `REJECT` and `NARROW`;
- unknown WP02 theorem-interface IDs;
- protected-target drift away from `YM-T-000`;
- any downstream gate not equal to `CLOSED`.

A passing replay does not evaluate a proposed proof and supplies no evidence that the Clay target is true or false.
