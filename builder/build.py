import os
import re
import yaml
import argparse
from markup import markup

dir_path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description="Build rust-scicomp.github.io")

parser.add_argument(
    'destination', metavar='destination', nargs="?",
    default=os.path.join(dir_path, "../_html"),
    help="Destination of HTML files.")

args = parser.parse_args()
html_path = args.destination
files_path = os.path.join(dir_path, "../files")
talks_path = os.path.join(dir_path, "../talks")
slides_path = os.path.join(dir_path, "../slides")
pages_path = os.path.join(dir_path, "../pages")
template_path = os.path.join(dir_path, "../template")

if os.path.isdir(html_path):
    os.system(f"rm -rf {html_path}")
os.mkdir(html_path)
os.mkdir(os.path.join(html_path, "talks"))
os.mkdir(os.path.join(html_path, "slides"))

os.system(f"cp -r {files_path}/* {html_path}")
#os.system(f"cp -r {slides_path}/* {html_path}/slides")

with open(os.path.join(html_path, "CNAME"), "w") as f:
    f.write("fenics2021.com")

with open(os.path.join(talks_path, "_timetable.yml")) as f:
    timetable = yaml.load(f, Loader=yaml.FullLoader)


def write_page(url, content, title=None):
    if title is None:
        title = "Scientific Computing in Rust 2023"
    else:
        title = "Scientific Computing in Rust 2023: " + title
    with open(os.path.join(html_path, url), "w") as f:
        with open(os.path.join(template_path, "intro.html")) as f2:
            f.write(f2.read().replace("{{pagetitle}}", title))
        f.write(content)
        with open(os.path.join(template_path, "outro.html")) as f2:
            f.write(f2.read())


def get_title_and_speaker(t_id):
    with open(os.path.join(talks_path, f"{t_id}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)
    return tinfo["title"], tinfo["speaker"]["name"]


def person(p, bold = False):
    info = ""
    if bold:
        info += "<b>"
    info += p["name"]
    if bold:
        info += "</b>"
    if "website" in p:
        info += (f" <a href='{p['website']}' class='falink'>"
                 "<i class='fab fa-internet-explorer'></i></a>")
    if "github" in p:
        info += (f" <a href='https://github.com/{p['github']}' class='falink'>"
                 "<i class='fab fa-github'></i></a>")
    if "twitter" in p:
        info += (f" <a href='https://twitter.com/{p['twitter']}' class='falink'>"
                 "<i class='fab fa-twitter'></i></a>")

    if "affiliation" in p:
        info += f" ({p['affiliation']}"
        info += ")"
    return info


def is_long(t):
    with open(os.path.join(talks_path, f"{t}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)
    return tinfo["duration"] == "long"


def talk(t, day, session_n, prev=None, next=None):
    with open(os.path.join(talks_path, f"{t}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)

    authors = [person(tinfo["speaker"], True)]
    authornames = [tinfo["speaker"]["name"]]
    if "coauthor" in tinfo:
        authors += [person(a) for a in tinfo["coauthor"]]
        authornames += [a["name"] for a in tinfo["coauthor"]]
    authortxt = "".join([f"<div class='authors'>{i}</div>" for i in authors])

    content = ""
    content += f"<h1>{tinfo['title']}</h1>"
    content += f"<div>{authortxt}</div>"
    content += "<div class='abstract'>"
    abstract = []
    if isinstance(tinfo['abstract'], list):
        for parag in tinfo['abstract']:
            abstract.append(parag)
    else:
        abstract.append(tinfo['abstract'])
    content += markup("\n\n".join(abstract))
    content += "</div>"

    if prev is not None or next is not None:
        content += "<div class='prevnext'>"
        if prev is not None:
            content += "<div class='prevlink'>"
            if prev[0] is not None:
                content += f"<a href='/talks/{prev[0]}.html'>&larr; previous talk"
                if prev[1] is not None:
                    content += f" ({prev[1]})"
                content += "</a>"
            else:
                content += "<i>this is the first talk</i>"
            content += "</div>"
        if next is not None:
            content += "<div class='nextlink'>"
            if next[0] is not None:
                content += f"<a href='/talks/{next[0]}.html'>next talk"
                if next[1] is not None:
                    content += f" ({next[1]})"
                content += " &rarr;</a>"
            else:
                content += "<i>this is the final talk</i>"
            content += "</div>"
        content += "</div>"

    write_page(f"talks/{t}.html", content, tinfo['title'])

    short_content = ""
    short_content += "<div class='talktitle'>"
    short_content += f"<a href='/talks/{t}.html'>{tinfo['title']}</a></div>"
    short_content += f"<div class='timetablelistauthor'>{authortxt}</div>"

    return short_content


def minutes_after_one(time):
    h, m = time.split(":")
    return int(m) + 60 * (int(h) - 13)


for file in os.listdir(pages_path):
    if file.endswith(".md"):
        fname = file[:-3]
        with open(os.path.join(pages_path, file)) as f:
            content = markup(f.read(), False)
        write_page(f"{fname}.html", content)

# Make timetable pages
list_content = "<h1>List of talks</h1>"
tt_content = "<h1>Timetable</h1>"

list_content += "<h1 style='color:red'>This is a provisional timetable and may be changed</h1>"
tt_content += "<h1 style='color:red'>This is a provisional timetable and may be changed</h1>"

tt_content += "<div class='timetablegrid'>\n"
for di, day in enumerate(timetable):
    dcontent = ""
    if day == "Thursday":
        date = f"Thursday 13 July"
    elif day == "Friday":
        date = f"Friday 14 July"
    else:
        raise ValueError(f"Unknown day: {day}")

    list_content += f"<h2><a href='/talklist-{day}.html'>{date}</a></h2>{dcontent}"
    tt_content += ("<div class='gridcell timetableheading' style='grid-column: "
                   f"{2 * di + 1} / span 2;grid-row: 1 /span 1'><a href='/talklist-{day}.html'>"
                   f"{date}</a></div>")

    for si, session in enumerate(timetable[day]):
        dcontent += (f"<h3>Session {si + 1} ({session['start']}&ndash;{session['end']} BST"
                     f", {session['platform']})</h3>")
        col = 2 * di + 2
        print(session['start'], minutes_after_one(session['start']))
        row = 2 + minutes_after_one(session['start'])
        rowend = 2 + minutes_after_one(session['end'])
        tt_content += (f"<div class='gridcell timetableheading rotated' style='"
                       f"grid-column: {col - 1} / span 1; "
                       f"grid-row: {row} / "
                       f"span {minutes_after_one(session['end'])};'>"
                       f"Session {si + 1} ({session['start']}&ndash;{session['end']} BST, "
                       f"{session['platform']})</div>")
        if "description" in session:
            dcontent += f"<div class='timetablelisttalk'>{session['description']}</div>"
        if "chair" in session:
            dcontent += (f"<div class='authors' style='margin-top:-10px;margin-bottom:10px'>"
                         f"Chair: {person(session['chair'])}</div>")
        if "talks" in session:
            talklen = (rowend - row) // sum(3 if is_long(t) else 1 for t in session["talks"])
            for ti, t in enumerate(session["talks"]):
                dcontent += talk(t, day, si)
                title = "title"
                speaker = "person"

                tt_content += (f"<a class='gridcell timetabletalk' href='/talks/{t}.html' style='"
                               f"grid-column: {col} / span 1; "
                               f"grid-row: {row + talklen * ti} / span {talklen}'>"
                               f"<div class='timetabletalktitle'>{title}</div>"
                               f"<div class='timetabletalkspeaker'>{speaker}</div>"
                               "</a>")
        if si > 0 and session["start"] != timetable[day][si - 1]["end"]:
            tt_content += ("<div class='gridcell timetableheading' style='"
                           f"grid-column: {col} / span 1; "
                           f"grid-row: {minutes_after_one(timetable[day][si - 1]['end'])} / "
                           f"{minutes_after_one(session['start'])}'>")
            tt_content += " &nbsp; &nbsp; &nbsp; ".join("BREAK")
            tt_content += "</div>"
    list_content += dcontent
    write_page(f"talklist-{day}.html", f"<h1>{date}</h1>{dcontent}")

    #tt_content += ("<div class='gridcell timetableheading rotated' style='grid-column: 1 / span 1"
    #               f";grid-row: {} /span 2'>"
    #               f"{date}</div>")

tt_content += "</div>"

write_page("talklist.html", list_content)
write_page("timetable.html", tt_content)
