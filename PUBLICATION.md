# Copy and publish as a separate repository

The working `FINAL_PROJECT_MAIN` remains ignored by its outer repository. Publish a separate copy; do not unignore or merge it into the original `main`.

## 1. Copy to a new location

On Linux, choose a **new empty destination outside the existing repository** and preserve links/permissions:

```bash
cp -a /absolute/path/to/FINAL_PROJECT_MAIN /absolute/path/to/CS787-final-publication
cd /absolute/path/to/CS787-final-publication
```

Substitute real paths. Do not use symlink-dereferencing copy flags: the internal links intentionally share canonical files. Copying this folder does not move or remove the source. All links must still resolve inside the copied folder.

## 2. Check/install and verify

```bash
bash setup_demo.sh --dev
.venv/bin/python publication/check_readiness.py
.venv/bin/python demo/verify_copy.py
bash demo/launch.sh
```

For a saved-only installation use `--saved`; `--dev` installs the software needed by the full copied-demo tests. No checkpoint downloads or inference occur automatically. Use the README test command for the regression suite. Stop the preview when finished.

## 3. Initialize the new repository and enable LFS before adding files

```bash
git init -b gagan
git lfs install --local
git add .gitattributes
git add .
git status --short
git lfs ls-files
```

The byte-preserving `* -text` rule prevents Git line-ending conversion from changing frozen checksums. The three paths in `.gitattributes` must appear in LFS: the two frozen split JSON copies and the saved `bundle.json`. These rules do not blanket-ignore scientific results. Raw files remain available locally with their original checksums.

Inspect the staged list before committing. Do not add virtual environments, raw model weights, credentials, temporary sessions or unrelated data. Preserve upstream licenses and source locks. A credential-pattern scan reduces obvious mistakes but is not a guarantee that no sensitive content exists; review any private notes or dataset redistribution obligations yourself.

## 4. Commit and push only when you are ready

```bash
git commit -m "Publish curated CS787 research and Evidence Lab demo"
git remote add origin YOUR_NEW_REPOSITORY_URL
git push -u origin gagan
```

Replace the URL with your own newly created repository. No actual remote URL is invented here. After pushing, verify `git lfs pull` and startup in a clean clone before sharing it. Add the eventual repository URL to `CITATION.cff` if desired.

None of the preparation scripts initializes, commits, configures an actual remote or pushes this working folder. Git commands above are manual instructions for the independent copy only.
