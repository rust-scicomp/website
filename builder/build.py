import os
import yaml
import argparse
from markup import markup

dir_path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description="Build rust-scicomp.github.io")

parser.add_argument(
    '--destination', metavar='destination', nargs="?",
    default=None,
    help="Destination of HTML files.")
parser.add_argument(
    '--year', metavar='year', nargs="?",
    default="2024", help="Year")

args = parser.parse_args()
year = int(args.year)
archive = year != 2024
html_path = args.destination

if archive:
    webroot = f"/{year}"
    webslides = f"/slides/{year}"
    if html_path is None:
        html_path = os.path.join(dir_path, f"../archive/{year}/html")
    talks_path = os.path.join(dir_path, f"../archive/{year}/talks")
    template_path = os.path.join(dir_path, f"../archive/{year}/template")
    pages_path = os.path.join(dir_path, f"../archive/{year}/pages")
else:
    webroot = ""
    webslides = "/slides"
    if html_path is None:
        html_path = os.path.join(dir_path, "../_html")
    talks_path = os.path.join(dir_path, "../talks")
    template_path = os.path.join(dir_path, "../template")
    pages_path = os.path.join(dir_path, "../pages")
main_template_path = os.path.join(dir_path, "../template")

dates_dict = {
    2023: "13-14 July 2023",
    2024: "17-19 July 2024",
}
if year in dates_dict:
    dates = dates_dict[year]
else:
    dates = f"TBC {year}"

if os.path.isdir(html_path):
    os.system(f"rm -rf {html_path}")
os.mkdir(html_path)
os.mkdir(os.path.join(html_path, "talks"))
os.mkdir(os.path.join(html_path, "slides"))


if not archive:
    slides_path = os.path.join(dir_path, "../slides")
    files_path = os.path.join(dir_path, "../files")
    os.system(f"cp -r {slides_path}/* {html_path}/slides")
    os.system(f"cp -r {files_path}/* {html_path}")
    for y in range(2023, year):
        archive_path = os.path.join(dir_path, f"../archive/{y}/html")
        os.system(f"cp -r {archive_path} {html_path}/{y}")


def load_template(file, title, url):
    if os.path.isfile(os.path.join(template_path, file)):
        with open(os.path.join(template_path, file)) as f:
            content = f.read()
    else:
        with open(os.path.join(main_template_path, file)) as f:
            content = f.read()
    content = content.replace("{{pagetitle}}", title)
    content = content.replace("{{pagefullurl}}", f"https://scientificcomputing.rs/{url}")
    content = content.replace("{{year}}", f"{year}")
    return content


def write_page(url, content, title=None):
    if title is None:
        title = f"Scientific Computing in Rust {year}"
    else:
        title = f"Scientific Computing in Rust {year}: {title}"
    with open(os.path.join(html_path, url), "w") as f:
        f.write(load_template("head.html", title, url))
        f.write(load_template("intro.html", title, url))
        f.write(content)
        f.write(load_template("outro.html", title, url))


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


def has_youtube(t):
    if t == "intro":
        return False

    with open(os.path.join(talks_path, f"{t}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)
    return "youtube" in tinfo


def has_slides(t):
    if t == "intro":
        return False

    with open(os.path.join(talks_path, f"{t}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)
    return "slides" in tinfo


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

    content = f"<h1>{tinfo['title']}</h1>"
    if is_long(t):
        content += "<h2 style='margin-top:-15px'>(30 minute invited talk)</h2>"
    content += f"<div>{authortxt}</div>"

    if day is not None:
        content += (f"<div style='margin-top:5px'>"
                    f"<a href='{webroot}/talklist-{day}.html'>{day}</a>"
                    f" session {session_n} (Zoom) (<a href='javascript:show_tz_change()'>{times}</a>)"
                    "</div>")
        content += markup("<div id='tzonechange' style='display:none;margin-top:15px;text-align:center'>Show times in: <timeselector></div>", paragraphs=False)
    if "recorded" in tinfo and not tinfo["recorded"]:
        content += ("<div style='margin-top:15px'><i class='fa-solid fa-video-slash'></i> "
                    "This talk will not be recorded.</div>")
    if "youtube" in tinfo:
        content += (f"<div style='margin-top:15px'><a href='https://youtu.be/{tinfo['youtube']}'>"
                    "<i class='fab fa-youtube'></i> Watch a recording of this talk on YouTube</a></div>")
    if "slides" in tinfo:
        content += (f"<div style='margin-top:15px'><a href='{webslides}/{tinfo['slides']}'>"
                    "<i class='fa-solid fa-file-powerpoint'></i> Download this talk's slides</a></div>")

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
            content += f"<a href='{webroot}/talks/{prev[0]}.html'>&larr; previous talk"
            if prev[1] is not None:
                content += f" ({prev[1]})"
            content += "</a>"
        else:
            content += "<i>this is the first talk</i>"
        content += "</div>"
    if next is not None:
        content += "<div class='nextlink'>"
        if next[0] is not None:
            content += f"<a href='{webroot}/talks/{next[0]}.html'>next talk"
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
    short_content += f"<a href='{webroot}/talks/{t}.html'>{tinfo['title']}</a>"
    if not recorded(t):
        short_content += " <i class='fa-solid fa-video-slash' alt='This talk will not be recorded' title='This talk will not be recorded'></i>"
    if has_youtube(t):
        short_content += (f" <a href='https://youtu.be/{tinfo['youtube']}'>"
                          "<i class='fab fa-youtube' alt='Watch a recording of this talk on YouTube' title='Watch a recording of this talk on YouTube'></i></a>")
    if has_slides(t):
        short_content += " <i class='fa-solid fa-file-powerpoint' alt='Slides for this talk are available' title='Slides for this talk are available'></i>"
    short_content += "</div>"
    if is_long(t):
        short_content += "<div class='talksubtitle'>(30 minute invited talk)</div>"
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
if os.path.isfile(os.path.join(talks_path, "_timetable.yml")):
    with open(os.path.join(talks_path, "_timetable.yml")) as f:
        timetable = yaml.load(f, Loader=yaml.FullLoader)

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

    # tt_content += "<div style='font-weight:bold;font-size:120%;color:red'>The information on this page is not finalised</div>"
    # list_content += "<div style='font-weight:bold;font-size:120%;color:red'>The information on this page is not finalised</div>"

    list_content += markup("Show times in: <timeselector>")
    tt_content += markup("Show times in: <timeselector>")

    rows = [(3, 8), (10, 14), (16, 16)]

    tt_content += "<style type='text/css'>\n"
    tt_content += ".timetablegrid {\n"
    tt_content += "  grid-template-columns: auto"
    for di, _ in enumerate(timetable):
        if di > 0:
            tt_content += " 0.1fr"
        tt_content += " 3fr"
    tt_content += ";\n"
    tt_content += "  grid-template-rows: auto 10px"
    for i, (row, rowend) in enumerate(rows[:-1]):
        if i > 0:
            tt_content += " 2fr"
        tt_content += f" repeat({rowend + 1 - row}, 1fr)"
    tt_content += "10px auto;\n"
    tt_content += "}\n"
    tt_content += "</style>\n"

    tt_content += "<div class='timetablegrid'>\n"
    for di, day in enumerate(timetable):
        dcontent = ""
        if day == "Wednesday":
            date = "Wednesday 17 July"
        elif day == "Thursday":
            date = "Thursday 18 July"
        elif day == "Friday":
            date = "Friday 19 July"
        else:
            raise ValueError(f"Unknown day: {day}")

        list_content += f"<h2 style='margin-top:100px'>{date}</h2>{dcontent}"
        tt_content += ("<div class='gridcell timetableheading' style='grid-column: "
                       f"{2 * di + 2} / span 1;grid-row: 1 /span 1'><a href='{webroot}/talklist-{day}.html'>"
                       f"{date}</a></div>")

        for si, session in enumerate(timetable[day]):
            session_time = markup(f"<time {day} {session['start']}>&ndash;<time {day} {session['end']}><tzone>", paragraphs=False)
            dcontent += "<h3"
            if si != 0:
                dcontent += " style='margin-top:50px'"
            dcontent += f">Session {si + 1} ({session_time}"
            if "platform" in session:
                dcontent += ", "
                if session['platform'] == "Gather Town":
                    dcontent += "<a href='/gather-town.html'>Gather Town</a>"
                else:
                    dcontent += session['platform']
            dcontent += ")</h3>"
            col = 2 * di + 2
            row, rowend = rows[si]
            if di == 0:
                tt_content += "<div class='gridcell timetableheading rotated' style='"
                tt_content += f"grid-column: {col - 1} / span 1; grid-row: {row} / span {rowend - row + 1}"
                tt_content += "'>"
                inner_content = f"Session {si + 1} (<time {day} {session['start']}>&ndash;<time {day} {session['end']}><tzone>"
                if "platform" in session:
                    inner_content += f", {session['platform']}"
                inner_content += ")"
                tt_content += markup(inner_content, paragraphs=False)
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
                    nrows = 3 if is_long(t) else 1
                    if t == "intro":
                        tt_content += "<div"
                    else:
                        tt_content += "<a"
                    tt_content += " class='gridcell timetabletalk"
                    if is_long(t):
                        tt_content += " longtalk"
                    tt_content += "'"
                    if t != "intro":
                        tt_content += f" href='{webroot}/talks/{t}.html'"
                    tt_content += (f" style='grid-column: {col} / span 1; grid-row: {row + start} / span {nrows}'>"
                                   f"<div class='timetabletalktitle'>{title}</div>")
                    icons = []
                    if not recorded(t):
                        icons.append("<i class='fa-solid fa-video-slash' alt='This talk will not be recorded' title='This talk will not be recorded'></i>")
                    if has_youtube(t):
                        icons.append("<i class='fab fa-youtube' alt='A recording of this talk is available on YouTube' title='A recording of this talk is available on YouTube'></i>")
                    if has_slides(t):
                        icons.append("<i class='fa-solid fa-file-powerpoint' alt='Slides for this talk are available' title='Slides for this talk are available'></i>")
                    if len(icons) > 0:
                        tt_content += f"<div class='timetabletalktitle'>{' '.join(icons)}</div>"
                    if speaker is not None:
                        tt_content += f"<div class='timetabletalkspeaker'>{speaker}</div>"
                    if t == "intro":
                        tt_content += "</div>"
                    else:
                        tt_content += "</a>"
                    start += nrows
            else:
                if "link" in session:
                    tt_content += f"<a href='{session['link']}'"
                else:
                    tt_content += "<div"
                tt_content += " class='gridcell timetabletalk'"
                tt_content += " style='"
                tt_content += f"grid-column: {col} / span 1; grid-row: "
                if "rowstart" in session:
                    tt_content += f"{session['rowstart']}"
                else:
                    tt_content += f"{row}"
                tt_content += " / span "
                if "rows" in session:
                    tt_content += f"{session['rows']}"
                else:
                    tt_content += f"{row}"
                tt_content += "'>"


                tt_content += "<div class='timetabletalktitle'>"
                if "title" in session:
                    tt_content += session["title"]
                else:
                    tt_content += "Discussions"
                tt_content += "</div>"
                if "description" in session:
                    tt_content += f"<div class='timetabletalkspeaker'>{session['description']}</div>"
                if "link" in session:
                    tt_content += "</a>"
                else:
                    tt_content += "</div>"
            if di == 0 and si > 0 and session["start"] != timetable[day][si - 1]["end"]:
                row0 = 2 + minutes_after_one(timetable[day][si - 1]['end'])
                row1 = 2 + minutes_after_one(session['start'])
                tt_content += ("<div class='gridcell timetableheading' style='"
                               "grid-column: 2 / span 5; "
                               "grid-row: 9 / span 1; "
                               "display: flex; justify-content: center; align-items: center;'>")
                tt_content += " &nbsp; &nbsp; &nbsp; ".join("BREAK")
                tt_content += "</div>"
        list_content += dcontent
        write_page(f"talklist-{day}.html", f"<h1>{date}</h1>{markup('Show times in: <timeselector>')}{dcontent}")

    tt_content += "</div>"

    write_page("talklist.html", list_content)
    write_page("timetable.html", tt_content)
