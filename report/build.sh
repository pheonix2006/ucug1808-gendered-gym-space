#!/usr/bin/env bash
# Compile main.tex -> main.pdf
# Requires: XeLaTeX, biber, ctex, biblatex-apa
# Usage: bash build.sh

set -euo pipefail

cd "$(dirname "$0")"

echo "==> Pass 1: xelatex"
xelatex -interaction=nonstopmode main.tex

echo "==> Pass 2: biber"
biber main

echo "==> Pass 3: xelatex (resolve references)"
xelatex -interaction=nonstopmode main.tex

echo "==> Pass 4: xelatex (finalize cross-refs)"
xelatex -interaction=nonstopmode main.tex

echo "==> Done: main.pdf"
