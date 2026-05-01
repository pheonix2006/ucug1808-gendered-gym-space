@echo off
REM Compile main.tex -> main.pdf
REM Requires: XeLaTeX, biber, ctex, biblatex-apa
REM Usage: double-click build.bat or run from report\ directory

cd /d "%~dp0"

echo === Pass 1: xelatex ===
xelatex -interaction=nonstopmode main.tex
if errorlevel 1 goto :error

echo === Pass 2: biber ===
biber main
if errorlevel 1 goto :error

echo === Pass 3: xelatex (resolve references) ===
xelatex -interaction=nonstopmode main.tex
if errorlevel 1 goto :error

echo === Pass 4: xelatex (finalize cross-refs) ===
xelatex -interaction=nonstopmode main.tex
if errorlevel 1 goto :error

echo === Done: main.pdf ===
goto :eof

:error
echo === BUILD FAILED ===
pause
exit /b 1
