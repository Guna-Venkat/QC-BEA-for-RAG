# Publication readiness report

Prepared: 12 November 2026. Scope: `FINAL_PROJECT_MAIN/` only. No actual publication, remote, commit, training or reader run was performed.

## Added / updated

- Root `requirements.txt`: pinned saved-view/numerical dependencies.
- `requirements-live.txt`: optional Torch/Transformers/SFR/tokenizer software.
- `requirements-dev.txt`: copied-demo regression/browser tools.
- `.python-version`, `setup_demo.sh`, `INSTALLATION.md`: Python 3.11, local-venv install and platform/model-access scope.
- `demo/launch.sh`: prefer a standalone repository `.venv` before the old server fallback; `DEMO_PYTHON` still overrides.
- `.gitattributes`: preserve exact bytes with `* -text`; exact-path LFS for both 108 MiB split JSON copies and the 97 MiB saved demo bundle. No artifact compression/rewriting occurred.
- `.gitignore`: keep credentials/environments/private runtime data out; a nested override keeps the required saved replay index visible.
- Root README: project purpose, conservative findings, numbered map, launch, tests, reproduction limits and publishing route. Earlier README preserved as `publication/README_BEFORE_PUBLICATION.md`.
- MIT `LICENSE` as requested, `THIRD_PARTY_NOTICES.md`, `CITATION.cff`; original baseline license/source-lock bytes unchanged.
- `PUBLICATION.md`: separate-copy instructions, new `gagan` repository, LFS setup before the first add/commit, manual push commands only.
- `publication/check_readiness.py`, packaging/saved-profile tests and machine-readable check receipts.

## Two publication-only test/UI adjustments

1. The copied ignore-policy test distinguishes the historical ignored working demo from the independent publishable demo. It still requires runtime/environments to be ignored, while required source, bundle and replay index must be visible.
2. The final copied UI's GPU-status import tolerates an absent optional Torch installation. Saved views can open without the model stack. This changes no allocator, reader prompt, parser, score, threshold or scientific definition.

Original `demo/` outside this final folder was not modified by this publication pass. These two changes are reflected in the copied payload hash inventory rather than silently bypassing integrity checks.

## Verification

- Pre-existing scientific/code files checked: **6384**. Differences limited to the two packaging-only paths above; all other protected files unchanged.
- Copied-payload identities: **324 files** verified.
- Internal relative links: **6,927**, none broken or outside the folder.
- Part-I final-method SHA: `d0188a3582d6aead0a3a31f9f15bad9b51a88a6b475b05ac79ae38e58f05366b`.
- Both frozen split copies match. Demo source manifest and published 1,620-condition bundle verified.
- Common credential-pattern scan: **0 matches**; this does not replace human privacy/redistribution review.
- Pinned dev-profile dependency closure: **76 installed distributions**, no missing/incompatible declared dependencies.
- Standalone-copy Git checks: all three exact LFS filters apply; required files are not ignored; representative credential/runtime paths are ignored. `git add --dry-run` succeeds. No staged commit or remote was created.
- Packaging unit checks: **6 passed**.
- Saved-only UI: all four workspaces passed with optional ML modules intentionally blocked; **no optional model package loaded**.
- Standalone browser check: all four workspaces passed without inference.
- Full independent-copy demo regression suite: **193 passed in 28.98 seconds** after the final packaging adjustments.

## Installation qualification limit

The test used a separate filesystem copy and temporary local Git repository with the existing compatible interpreter. A fresh network installation of all packages into an empty machine/venv was **not** performed, and no model weights were downloaded. Requirements are direct pins, not a universal transitive/platform lock. The declared dependency closure was checked against installed metadata and exercised through tests. An unrelated pre-existing `llama-index-core`/`setuptools` mismatch in the broad server environment is not in these profiles and was not altered.

Research notebook execution still requires phase-specific datasets/checkpoints and the documented historical missing-shard limits. These requirements primarily qualify the saved/custom-input demo, not universal reproduction of every archived baseline environment. Scientific identities, cohorts, historical outputs and the frozen final policy remain unchanged.

## Next

Copy the folder with `cp -a` to a new independent location. Follow `PUBLICATION.md` and run `publication/check_readiness.py` there. The original ignored final folder is not initialized or pushed by these preparation commands. Fetch LFS files before opening saved results in a future clone.
