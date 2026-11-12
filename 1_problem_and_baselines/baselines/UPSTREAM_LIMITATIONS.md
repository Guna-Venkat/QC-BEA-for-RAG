# Reference-source limitations

Official snapshots are pinned, licensed subsets, not bundled datasets/weights or proof of a working installed environment. Full upstream examples/images/data may not be included; use the original repository links for those reference-only assets.

The pinned SARA snapshot contains a pre-existing syntax error in src/visual/plot_generalization_base_model.py around line94. It is an ancillary plotting file, not a tested project allocator or the SARA CLI. Its source was preserved exactly and the finding recorded in baseline_upstream_checks.json. It was not silently repaired or presented as a successful reproduction. RECOMP and selected LLMLingua source parse statically; no dependency imports/models/evaluations were run.

Three distinct identities must remain separate: published paper version, pinned current official reference source, and project execution adaptation/checkpoint. Equal source-file bytes do not establish equal evaluated systems. Original code licenses apply to code; paper copyrights and model/dataset terms remain their own.
