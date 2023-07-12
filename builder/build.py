import os
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
# os.system(f"cp -r {slides_path}/* {html_path}/slides")

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


def person(p, bold=False):
    info = ""
    if bold:
        info += "<b>"
    info += p["name"]
    if bold:
        info += "</b>"
    if "website" in p:
        info += (f" <a href='{p['website']}' class='falink'>"
                 "<i class='fab fa-internet-explorer'></i></a>")
    if "email" in p:
        info += (f" <a href='mailto:{p['email']}' class='falink'>"
                 "<i class='far fa-envelope'></i></a>")
    if "github" in p:
        info += (f" <a href='https://github.com/{p['github']}' class='falink'>"
                 "<i class='fab fa-github'></i></a>")
    if "codeberg" in p:
        info += (f" <a href='https://codeberg.org/{p['codeberg']}' class='falink'>"
                 "<i class='fa-solid fa-icicles'></i></a>")
    if "zulip" in p:
        info += (f" <a href='https://rust-scicomp.zulipchat.com' title='{p['zulip']} on Rust-SciComp Zulip'>"
                 "<svg class='brand-logo' role='img' aria-label='Zulip' xmlns='http://www.w3.org/2000/svg' viewBox='68.96 55.62 450 450.43' height='16'>"
                 "<path class='filled' d='M473.09 122.97c0 22.69-10.19 42.85-25.72 55.08L296.61 312.69c-2.8 2.4-6.44-1.47-4.42-4.7l55.3-110.72c1.55-3.1-.46-6.91-3.64-6.91H129.36c-33.22 0-60.4-30.32-60.4-67.37 0-37.06 27.18-67.37 60.4-67.37h283.33c33.22-.02 60.4 30.3 60.4 67.35zM129.36 506.05h283.33c33.22 0 60.4-30.32 60.4-67.37 0-37.06-27.18-67.37-60.4-67.37H198.2c-3.18 0-5.19-3.81-3.64-6.91l55.3-110.72c2.02-3.23-1.62-7.1-4.42-4.7L94.68 383.6c-15.53 12.22-25.72 32.39-25.72 55.08 0 37.05 27.18 67.37 60.4 67.37zm522.5-124.15l124.78-179.6v-1.56H663.52v-48.98h190.09v34.21L731.55 363.24v1.56h124.01v48.98h-203.7V381.9zm338.98-230.14V302.6c0 45.09 17.1 68.03 47.43 68.03 31.1 0 48.2-21.77 48.2-68.03V151.76h59.09V298.7c0 80.86-40.82 119.34-109.24 119.34-66.09 0-104.96-36.54-104.96-120.12V151.76h59.48zm244.91 0h59.48v212.25h104.18v49.76h-163.66V151.76zm297 0v262.01h-59.48V151.76h59.48zm90.18 3.5c18.27-3.11 43.93-5.44 80.08-5.44 36.54 0 62.59 7 80.08 20.99 16.72 13.22 27.99 34.99 27.99 60.64 0 25.66-8.55 47.43-24.1 62.2-20.21 19.05-50.15 27.6-85.13 27.6-7.77 0-14.77-.39-20.21-1.17v93.69h-58.7V155.26zm58.7 118.96c5.05 1.17 11.27 1.55 19.83 1.55 31.49 0 50.92-15.94 50.92-42.76 0-24.1-16.72-38.49-46.26-38.49-12.05 0-20.21 1.17-24.49 2.33v77.37z'></path>"
                 "</svg></a>")
    if "mastodon" in p:
        username, domain = p['mastodon'].split('@')
        info += (f" <a href='https://{domain}/@{username}'>"
                 "<i class='fab fa-mastodon'></i></a>")
    if "twitter" in p:
        info += (f" <a href='https://twitter.com/{p['twitter']}' class='falink'>"
                 "<i class='fab fa-twitter'></i></a>")
    if "linkedin" in p:
        info += (f" <a href='https://www.linkedin.com/in/{p['linkedin']}' class='falink'>"
                 "<i class='fab fa-linkedin'></i></a>")

    if "affiliation" in p:
        info += f" ({p['affiliation']}"
        info += ")"
    return info


def is_long(t):
    if t == "intro":
        return False
    with open(os.path.join(talks_path, f"{t}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)
    return tinfo["duration"] == "long"


def get_title_and_speaker(t):
    if t == "intro":
        return "Welcome and introduction", None

    with open(os.path.join(talks_path, f"{t}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)
    return tinfo["title"], tinfo["speaker"]["name"]


def recorded(t):
    if t == "intro":
        return True

    with open(os.path.join(talks_path, f"{t}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)
    return "recorded" not in tinfo or tinfo["recorded"]


def talk(t, day, session_n, times, prev=None, next=None):
    if t == "intro":
        title, _ = get_title_and_speaker(t)
        return f"<div class='talktitle'>{title}</div><br />"

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

    if day is not None:
        content += (f"<div style='margin-top:5px'>"
                    f"<a href='/talklist-{day}.html'>{day}</a>"
                    f" session {session_n} (Zoom) (<a href='javascript:show_tz_change()'>{times}</a>)"
                    "</div>")
        content += markup("<div id='tzonechange' style='display:none;margin-top:15px;text-align:center'>Show times in: <timeselector></div>", paragraphs=False)
    if "recorded" in tinfo and not tinfo["recorded"]:
        content += ("<div style='margin-top:15px'><i class='fa-solid fa-video-slash'></i> "
                    "This talk will not be recorded.</div>")

    content += "<div class='abstract'>"
    if "abstract" in tinfo:
        abstract = []
        if isinstance(tinfo['abstract'], list):
            for parag in tinfo['abstract']:
                abstract.append(parag)
        else:
            abstract.append(tinfo['abstract'])
        content += markup("\n\n".join(abstract))
    content += "</div>"

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
    short_content += f"<a href='/talks/{t}.html'>{tinfo['title']}</a>"
    short_content += f"</div><div class='timetablelistauthor'>{authortxt}</div>"

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
next_and_prev = {}
prev = None
for day in timetable.values():
    first_day = True
    for session in day:
        first_session = True
        if "talks" in session:
            for t in session["talks"]:
                if t != "intro":
                    next_and_prev[t] = {"prev": (None, None), "next": (None, None)}
                    if prev is not None:
                        if first_day:
                            next_and_prev[t]["prev"] = (prev, "on the previous day")
                            next_and_prev[prev]["next"] = (t, "on the next day")
                        elif first_session:
                            next_and_prev[t]["prev"] = (prev, "before a break")
                            next_and_prev[prev]["next"] = (t, "after a break")
                        else:
                            next_and_prev[t]["prev"] = (prev, None)
                            next_and_prev[prev]["next"] = (t, None)
                    first_session = False
                    first_day = False
                    prev = t

list_content = "<h1>List of talks</h1>"
tt_content = "<h1>Timetable</h1>"

list_content += markup("Show times in: <timeselector>")
tt_content += markup("Show times in: <timeselector>")


tt_content += "<div class='timetablegrid'>\n"
for di, day in enumerate(timetable):
    dcontent = ""
    if day == "Thursday":
        date = "Thursday 13 July"
    elif day == "Friday":
        date = "Friday 14 July"
    else:
        raise ValueError(f"Unknown day: {day}")

    list_content += f"<h2 style='margin-top:100px'>{date}</h2>{dcontent}"
    tt_content += ("<div class='gridcell timetableheading' style='grid-column: "
                   f"{2 * di + 2} / span 1;grid-row: 1 /span 1'><a href='/talklist-{day}.html'>"
                   f"{date}</a></div>")

    for si, session in enumerate(timetable[day]):
        session_time = markup(f"<time {day} {session['start']}>&ndash;<time {day} {session['end']}><tzone>", paragraphs=False)
        dcontent += "<h3"
        if si != 0:
            dcontent += " style='margin-top:50px'"
        dcontent += f">Session {si + 1} ({session_time}, "
        if session['platform'] == "Gather Town":
            dcontent += "<a href='/gather-town.html'>Gather Town</a>"
        else:
            dcontent += session['platform']
        dcontent += ")</h3>"
        col = 2 * di + 2
        row = [3, 15, 23][si]
        rowend = [13, 21, 23][si]
        if di == 0:
            tt_content += "<div class='gridcell timetableheading rotated' style='"
            if session["platform"] == "Gather Town":
                tt_content += f"grid-column: {col - 1} / span 1; grid-row: {row} / span 1"
            else:
                tt_content += f"grid-column: {col - 1} / span 1; grid-row: {row - 1} / span {rowend - row + 1}"
            tt_content += "'>"
            tt_content += markup(f"Session {si + 1} (<time {day} {session['start']}>&ndash;<time {day} {session['end']}><tzone>, "
                                 f"{session['platform']})", paragraphs=False)
            tt_content += "</div>"
        if "description" in session:
            dcontent += f"<div class='timetablelisttalk'>{session['description']}</div>"
        if "chair" in session:
            dcontent += (f"<div class='authors' style='margin-top:-10px;margin-bottom:10px'>"
                         f"Chair: {person(session['chair'])}</div>")
            tt_content += (f"<div style='grid-column: {col} / span 1; grid-row: {row - 1} / span 1;margin:10px;font-size:80%;text-align:center'>"
                           f"Chair: {session['chair']['name']}</div>")
        if "talks" in session:
            talklen = (rowend - row) / sum(3 if is_long(t) else 1 for t in session["talks"])
            start = 0
            for ti, t in enumerate(session["talks"]):
                if t == "intro":
                    dcontent += talk(t, day, si + 1, session_time)
                else:
                    dcontent += talk(t, day, si + 1, session_time, next_and_prev[t]["prev"], next_and_prev[t]["next"])
                title, speaker = get_title_and_speaker(t)
                length = 70 if is_long(t) else 20
                rows = 3 if is_long(t) else 1
                if t == "intro":
                    tt_content += "<div"
                else:
                    tt_content += "<a"
                tt_content += " class='gridcell timetabletalk"
                if is_long(t):
                    tt_content += " longtalk"
                tt_content += "'"
                if t != "intro":
                    tt_content += f" href='/talks/{t}.html'"
                tt_content += (f" style='grid-column: {col} / span 1; grid-row: {row + start} / span {rows}'>"
                               f"<div class='timetabletalktitle'>{title}</div>")
                if not recorded(t):
                    tt_content += "<div class='timetabletalktitle'><i class='fa-solid fa-video-slash' alt='This talk will not be recorded'></i></div>"
                if speaker is not None:
                    tt_content += f"<div class='timetabletalkspeaker'>{speaker}</div>"
                if t == "intro":
                    tt_content += "</div>"
                else:
                    tt_content += "</a>"
                start += rows
        else:
            tt_content += (f"<a class='gridcell timetabletalk' href='/gather-town.html' style='"
                           f"grid-column: {col} / span 1; grid-row: {row} / span 1'>"
                           "<div class='timetabletalktitle'>Discussions</div>")
            if "description" in session:
                tt_content += f"<div class='timetabletalkspeaker'>{session['description']}</div>"
            tt_content += "</a>"
        if di == 0 and si > 0 and session["start"] != timetable[day][si - 1]["end"]:
            row0 = 2 + minutes_after_one(timetable[day][si - 1]['end'])
            row1 = 2 + minutes_after_one(session['start'])
            tt_content += ("<div class='gridcell timetableheading' style='"
                           "grid-column: 2 / span 3; "
                           "grid-row: 13 / span 1; "
                           "display: flex; justify-content: center; align-items: center;'>")
            tt_content += " &nbsp; &nbsp; &nbsp; ".join("BREAK")
            tt_content += "</div>"
    list_content += dcontent
    write_page(f"talklist-{day}.html", f"<h1>{date}</h1>{markup('Show times in: <timeselector>')}{dcontent}")

tt_content += "</div>"

write_page("talklist.html", list_content)
write_page("timetable.html", tt_content)
