# Overleaf 同步说明

本地 Overleaf 仓库位于 `E:\Project\overleaf-1808\`

## 本地修改 → 推送到 Overleaf

```bash
cd /e/Project/overleaf-1808
cp "E:/Project/1808论文/report/main.tex" .
cp "E:/Project/1808论文/report/references.bib" .
cp -r "E:/Project/1808论文/report/sections" .
cp -r "E:/Project/1808论文/report/figures" .
git add . && git commit -m "update" && git push origin master
```

## Overleaf 修改 → 拉到本地

```bash
cd /e/Project/overleaf-1808
git pull origin master
cp main.tex "E:/Project/1808论文/report/"
cp references.bib "E:/Project/1808论文/report/"
cp -r sections "E:/Project/1808论文/report/"
cp -r figures "E:/Project/1808论文/report/"
```

## Overleaf 编译设置

- Compiler: **XeLaTeX**
- Main document: `main.tex`

## Overleaf 已知问题

`main.tex` 中的 `\setCJKmainfont{SimSun}[BoldFont=SimHei, ItalicFont=KaiTi]` 在 Overleaf 上会报错，因为 Overleaf（Linux）没有 SimSun/SimHei/KaiTi 这些 Windows 字体。

推送到 Overleaf 前需将这行临时注释掉，或替换为 Overleaf 支持的字体，例如：

```latex
\setCJKmainfont{Noto Serif CJK SC}[BoldFont=Noto Sans CJK SC Bold, ItalicFont=Noto Serif CJK SC Bold]
```
