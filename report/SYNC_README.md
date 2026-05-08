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
