import yaml
import os
from PIL import Image

if not os.path.isdir("pngs"):
    os.mkdir("pngs")

if not os.path.isdir("output"):
    os.mkdir("output")

def html2tex(a):
    a = a.replace("&aacute;", "\\'a")
    a = a.replace("&eacute;", "\\'e")
    a = a.replace("&atilde;", "\\~a")
    a = a.replace("&uuml;", "\\\"u")
    a = a.replace("&ndash;", "--")
    a = a.replace(" & ", " \\& ")
    return a

with open("output/end.tex", "w") as f:
    f.write("\\documentclass{standalone}\n")
    f.write("\\usepackage{tikz}\n")
    f.write("\\usepackage{xcolor}\n")
    f.write("\\usepackage{fontspec}\n")
    f.write("\\usepackage{graphicx}\n")
    f.write("\\usepackage[none]{hyphenat}\n")
    f.write("\\setmainfont[Scale=3]{Prompt}\n")
    f.write("\\definecolor{rusto}{HTML}{FFBC6F}\n")
    f.write("\\begin{document}\n")
    f.write("\\begin{tikzpicture}[x=0.5pt,y=0.5pt]\n")
    f.write("\\fill[rusto] (0,0) rectangle (1920,1080);")
    f.write("\\node at (960,920) {\scalebox{1.66}{Scientific Computing in Rust 2024}};")
    f.write("\\node at (960,120) {\scalebox{0.866}{scientificcomputing.rs}};")
    f.write("\\node at (960,540) {\includegraphics[width=300pt]{../../files/img/science-ferris-transparent.png}};")
    f.write("\\end{tikzpicture}\n")
    f.write("\\end{document}\n")
assert os.system("cd output && xelatex end.tex") == 0
assert os.system("cd output && pdftoppm end.pdf end -scale-to 1920 -png") == 0


for file in os.listdir("../talks"):
    if file.startswith("_"):
        continue
    with open(f"../talks/{file}") as f:
        t = yaml.load(f)
    with open("output/" + file.split(".")[0] + ".tex", "w") as f:
        f.write("\\documentclass{standalone}\n")
        f.write("\\usepackage{tikz}\n")
        f.write("\\usepackage{xcolor}\n")
        f.write("\\usepackage{fontspec}\n")
        f.write("\\usepackage{graphicx}\n")
        f.write("\\usepackage[none]{hyphenat}\n")
        f.write("\\setmainfont[Scale=3]{Prompt}\n")
        f.write("\\definecolor{rusto}{HTML}{FFBC6F}\n")
        f.write("\\begin{document}\n")
        f.write("\\begin{tikzpicture}[x=0.5pt,y=0.5pt]\n")
        f.write("\\fill[rusto] (0,0) rectangle (1920,1080);")
        f.write("\\node at (960,920) {\scalebox{1.66}{Scientific Computing in Rust 2024}};")
        f.write("\\node at (960,120) {\scalebox{0.866}{scientificcomputing.rs}};")
        f.write("\\node[anchor=east] at (1850,540) {\includegraphics[width=300pt]{../../files/img/science-ferris-transparent.png}};")
        f.write(f"\\node[anchor=west,align=left,text width=450pt, execute at begin node=\\setlength{{\\baselineskip}}{{2.2ex}}] at (250,540) {{{html2tex(t['title'])}")
        f.write("\n\\par\\vspace{30pt}\n")
        f.write(html2tex(t['speaker']['name']))
        if "affiliation" in t["speaker"]:
            f.write("\\\\(" + html2tex(t['speaker']['affiliation']) + ")")
        f.write("};")
        f.write("\\end{tikzpicture}\n")
        f.write("\\end{document}\n")
    assert os.system("cd output && xelatex " + file.split(".")[0] + ".tex") == 0
    assert os.system("cd output && pdftoppm " + file.split(".")[0] + ".pdf " + file.split(".")[0] + " -scale-to 1920 -png") == 0


os.system("mv output/*.png pngs")
