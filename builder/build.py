import os
import typing
import yaml
import argparse
from datetime import datetime
from markup import markup
from monthly import pull_monthly, issues_path, latest_issue, rss

months = ["Nilember", "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def join(*parts: str) -> str:
    """Join two or more parts of a file path."""
    if len(parts) == 1:
        return parts[0]
    return join(os.path.join(*parts[:2]), *parts[2:])


dir_path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description="Build rust-scicomp.github.io")

with open(join(dir_path, "..", "info.yml")) as f:
    info_yaml = yaml.load(f, Loader=yaml.FullLoader)

dates_dict = info_yaml["dates"]
latest_year = max(dates_dict.keys())

parser.add_argument(
    '--destination', metavar='destination', nargs="?",
    default=None,
    help="Destination of HTML files.")
parser.add_argument(
    '--year', metavar='year', nargs="?",
    default=f"{latest_year}", help="Year")

args = parser.parse_args()
year = int(args.year)
archive = year != latest_year
html_path = args.destination

if archive:
    if html_path is None:
        html_path = os.path.join(dir_path, f"../archive/{year}/html")
    talks_path = os.path.join(dir_path, f"../archive/{year}/talks")
    template_path = os.path.join(dir_path, f"../archive/{year}/template")
    pages_path = os.path.join(dir_path, f"../archive/{year}/pages")
else:
    if html_path is None:
        html_path = os.path.join(dir_path, "../_html")
    talks_path = os.path.join(dir_path, "../talks")
    template_path = os.path.join(dir_path, "../template")
    pages_path = os.path.join(dir_path, "../pages")
main_template_path = os.path.join(dir_path, "../template")

if year in dates_dict:
    dates = dates_dict[year]
else:
    dates = f"TBC {year}"

if os.path.isdir(html_path):
    os.system(f"rm -rf {html_path}")
os.mkdir(html_path)
os.mkdir(os.path.join(html_path, f"{year}"))
os.mkdir(os.path.join(html_path, os.path.join(f"{year}", "talks")))
os.mkdir(os.path.join(html_path, "slides"))

if not archive:
    slides_path = os.path.join(dir_path, "../slides")
    files_path = os.path.join(dir_path, "../files")
    os.system(f"cp -r {slides_path}/* {html_path}/slides")
    os.system(f"cp -r {files_path}/* {html_path}")
    for y in range(2023, year):
        archive_path = os.path.join(dir_path, f"../archive/{y}/html")
        os.system(f"cp -r {archive_path}/* {html_path}")

    pull_monthly()


special = {
    "intro": {"title": "Welcome and introduction"},
    "outro": {"title": "Closing remarks"},
}


def load_template(
    file: str, title: str, url: str, workshop: typing.Optional[int] = None,
    monthly: bool = False,
) -> str:
    if os.path.isfile(os.path.join(template_path, file)):
        with open(os.path.join(template_path, file)) as f:
            content = f.read()
    else:
        with open(os.path.join(main_template_path, file)) as f:
            content = f.read()
    content = content.replace("{{pagetitle}}", title)
    content = content.replace("{{latest-workshop}}", f"{latest_year}")
    content = content.replace("{{pagefullurl}}", f"https://scientificcomputing.rs/{url}")
    content = content.replace("{{year}}", f"{year}")
    while "{{if workshop" in content:
        pre, rest = content.split("{{if workshop", 1)
        ifyear, rest = rest.split("}}", 1)
        if ifyear == "":
            ifyear = "all"
        elif ifyear.strip() == "latest":
            ifyear = latest_year
        elif ifyear.strip() == "old":
            ifyear = "old"
        else:
            ifyear = int(ifyear)
        inner, rest = rest.split("{{fi}}", 1)
        if workshop is not None and (ifyear == "all" or ifyear == workshop or (ifyear == "old" and workshop < latest_year)):
            content = pre + inner + rest
        else:
            content = pre + rest
    if workshop is not None:
        content = content.replace("{{workshop-year}}", f"{workshop}")
        content = content.replace("{{workshop-dates}}", dates_dict[workshop])
        content = content.replace("{{latest-year}}", f"{latest_year}")
    while "{{if monthly}}" in content:
        pre, rest = content.split("{{if monthly}}", 1)
        inner, rest = rest.split("{{fi}}", 1)
        if monthly:
            content = pre + inner + rest
        else:
            content = pre + rest
    if monthly:
        content = content.replace("'/monthly/latest'", f"'/monthly/{latest_issue()}'")
        content = content.replace('"/monthly/latest"', f'"/monthly/{latest_issue()}"')
    return content


def write_page(
    url: str, content: str, title: typing.Optional[str] = None,
    workshop: typing.Optional[int] = None, monthly: bool = False,
):
    pagetitle = "Scientific Computing in Rust"
    if workshop is not None:
        pagetitle += f" {workshop}"
    if title is not None:
        pagetitle += f": {title}"
    with open(os.path.join(html_path, url), "w") as f:
        f.write(load_template("head.html", pagetitle, url, workshop, monthly))
        f.write(load_template("intro.html", pagetitle, url, workshop, monthly))
        f.write(content)
        f.write(load_template("outro.html", pagetitle, url, workshop, monthly))


def person(p: typing.Dict, bold: bool = False) -> str:
    info = ""
    if bold:
        info += "<b>"
    info += p["name"]
    if bold:
        info += "</b>"
    if "website" in p:
        info += (f" <a href='{p['website']}' class='falink'>"
                 "<i class='fa-brands fa-internet-explorer'></i></a>")
    if "email" in p:
        info += (f" <a href='mailto:{p['email']}' class='falink'>"
                 "<i class='fa-solid fa-envelope'></i></a>")
    if "github" in p:
        info += (f" <a href='https://github.com/{p['github']}' class='falink'>"
                 "<i class='fa-brands fa-github'></i></a>")
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
                 "<i class='fa-brands fa-mastodon'></i></a>")
    if "twitter" in p:
        info += (f" <a href='https://twitter.com/{p['twitter']}' class='falink'>"
                 "<i class='fa-brands fa-twitter'></i></a>")
    if "linkedin" in p:
        info += (f" <a href='https://www.linkedin.com/in/{p['linkedin']}' class='falink'>"
                 "<i class='fa-brands fa-linkedin'></i></a>")

    if "affiliation" in p:
        info += f" ({p['affiliation']}"
        info += ")"
    return info


def is_long(t: str) -> bool:
    if t in special:
        return False
    with open(os.path.join(talks_path, f"{t}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)
    return tinfo["duration"] == "long"


def get_title_and_speaker(t: str, short=False) -> typing.Tuple[str, typing.Optional[str]]:
    if t in special:
        return special[t]["title"], None

    with open(os.path.join(talks_path, f"{t}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)
    if short and "short-title" in tinfo:
        return tinfo["short-title"], tinfo["speaker"]["name"]
    else:
        return tinfo["title"], tinfo["speaker"]["name"]


def recorded(t: str) -> bool:
    if t in special:
        return True

    with open(os.path.join(talks_path, f"{t}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)
    return "recorded" not in tinfo or tinfo["recorded"]


def has_youtube(t: str) -> bool:
    if t in special:
        return False

    with open(os.path.join(talks_path, f"{t}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)
    return "youtube" in tinfo


def has_slides(t: str) -> bool:
    if t in special:
        return False

    with open(os.path.join(talks_path, f"{t}.yml")) as f:
        tinfo = yaml.load(f, Loader=yaml.FullLoader)
    return "slides" in tinfo


def talk(
    t: str, day: str, session_n: int, times: str,
    prev: typing.Optional[str] = None, next: typing.Optional[str] = None
) -> str:
    if t in special:
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
                    f"<a href='/{year}/talklist-{day}.html'>{day}</a>"
                    f" session {session_n} (Zoom) (<a href='javascript:show_tz_change()'>{times}</a>)"
                    "</div>")
        content += markup("<div id='tzonechange' style='display:none;margin-top:15px;text-align:center'>Show times in: <timeselector></div>", paragraphs=False, year=year)
    if "recorded" in tinfo and not tinfo["recorded"]:
        content += ("<div style='margin-top:15px'><i class='fa-solid fa-video-slash'></i> "
                    "This talk will not be recorded.</div>")
    if "youtube" in tinfo:
        content += (f"<div style='margin-top:15px'><a href='https://youtu.be/{tinfo['youtube']}'>"
                    "<i class='fa-brands fa-youtube'></i> Watch a recording of this talk on YouTube</a></div>")
    if "slides" in tinfo:
        content += (f"<div style='margin-top:15px'><a href='/slides/{tinfo['slides']}'>"
                    "<i class='fa-solid fa-file-powerpoint'></i> Download this talk's slides</a></div>")

    content += "<div class='abstract'>"
    if "abstract" in tinfo:
        abstract = []
        if isinstance(tinfo['abstract'], list):
            for parag in tinfo['abstract']:
                abstract.append(parag)
        else:
            abstract.append(tinfo['abstract'])
        content += markup("\n\n".join(abstract), year=year)
    content += "</div>"

    content += "<div class='prevnext'>"
    if prev is not None:
        content += "<div class='prevlink'>"
        if prev[0] is not None:
            content += f"<a href='/{year}/talks/{prev[0]}.html'>&larr; previous talk"
            if prev[1] is not None:
                content += f" ({prev[1]})"
            content += "</a>"
        else:
            content += "<i>this is the first talk</i>"
        content += "</div>"
    if next is not None:
        content += "<div class='nextlink'>"
        if next[0] is not None:
            content += f"<a href='/{year}/talks/{next[0]}.html'>next talk"
            if next[1] is not None:
                content += f" ({next[1]})"
            content += " &rarr;</a>"
        else:
            content += "<i>this is the final talk</i>"
        content += "</div>"
    content += "</div>"

    write_page(f"{year}/talks/{t}.html", content, tinfo['title'], workshop=year)

    short_content = ""
    short_content += "<div class='talktitle'>"
    short_content += f"<a href='/{year}/talks/{t}.html'>{tinfo['title']}</a>"
    if not recorded(t):
        short_content += " <i class='fa-solid fa-video-slash' alt='This talk will not be recorded' title='This talk will not be recorded'></i>"
    if has_youtube(t):
        short_content += (f" <a href='https://youtu.be/{tinfo['youtube']}'>"
                          "<i class='fa-brands fa-youtube' alt='Watch a recording of this talk on YouTube' title='Watch a recording of this talk on YouTube'></i></a>")
    if has_slides(t):
        short_content += " <i class='fa-solid fa-file-powerpoint' alt='Slides for this talk are available' title='Slides for this talk are available'></i>"
    short_content += "</div>"
    if is_long(t):
        short_content += "<div class='talksubtitle'>(30 minute invited talk)</div>"
    short_content += f"<div class='timetablelistauthor'>{authortxt}</div>"

    return short_content


def minutes_after_one(time: str) -> int:
    h, m = time.split(":")
    return int(m) + 60 * (int(h) - 13)


def find_md_files(path: str, subpath: str = "") -> typing.List[typing.Tuple[str, str]]:
    out = []
    if subpath == "":
        full_path = path
    else:
        full_path = os.path.join(path, subpath)
    for file in os.listdir(full_path):
        file_with_path = os.path.join(full_path, file)
        if file.endswith(".md") and not file.startswith("."):
            out.append((subpath, file))
        if os.path.isdir(file_with_path):
            out += find_md_files(path, file)
    return out


if os.path.isdir(pages_path):
    for subpath, file in find_md_files(pages_path):
        fname = file[:-3]
        if subpath != "":
            if not os.path.isdir(os.path.join(html_path, subpath)):
                os.mkdir(os.path.join(html_path, subpath))
            file = os.path.join(subpath, file)
        with open(os.path.join(pages_path, file)) as f:
            content = markup(f.read(), False, year=year)
            content = content.replace("{{latest-workshop}}", f"{latest_year}")
        if subpath == "":
            write_page(f"{fname}.html", content)
        else:
            try:
                write_page(f"{subpath}/{fname}.html", content, workshop=int(subpath),
                           monthly=(subpath == "monthly"))
            except ValueError:
                write_page(f"{subpath}/{fname}.html", content, monthly=(subpath == "monthly"))

# Monthly pages
if not archive:
    for subpath, file in find_md_files(issues_path):
        fname = file[:-3]
        assert subpath == ""
        with open(os.path.join(issues_path, file)) as f:
            content = f.read()
        if "\n---\n" in content:
            content = content.split("\n---\n", 1)[1]
        content = markup(content, False, year=year)
        write_page(f"monthly/{fname}.html", content, monthly=True)

    # monthly/rss.xml
    with open(os.path.join(html_path, "monthly/rss.xml"), "w") as f:
        f.write(rss())

    # monthly/latest.html
    latest = latest_issue()
    with open(os.path.join(html_path, "monthly/latest.html"), "w") as f:
        f.write("<html>\n")
        f.write("<head>\n")
        f.write(f"<meta http-equiv='refresh' content='0; url=https://scientificcomputing.rs/monthly/{latest}' />\n")
        f.write("</head>\n")
        f.write("<body>\n")
        f.write(f"<a href='https://scientificcomputing.rs/monthly/{latest}'>If this page does not refresh, please click here.</a>\n")
        f.write("</body>\n")
        f.write("</html>")

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
                    if t not in special:
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

    start = 4
    end = None
    rows = []
    for session in zip(*timetable.values()):
        count = 1
        stime = None
        etime = None
        for i in session:
            if "rows" not in i and "rowstart" not in i:
                if stime is None:
                    stime = i["start"]
                    etime = i["end"]
                assert i["start"] == stime
                assert i["end"] == etime
            if "talks" in i:
                count = max(count, sum(info_yaml["long-length"][year] if is_long(j) else 1 for j in i["talks"]))

        if end is not None:
            if prev_etime == stime:
                start = end + 2
            else:
                start = end + 3

        end = start + count - 1
        rows.append((start, end))
        prev_etime = etime
    list_content = "<h1>List of talks</h1>"
    tt_content = "<h1>Timetable</h1>"

    ics = (
        "BEGIN:VCALENDAR\n"
        "PRODID:=//Scientific Computing in Rust//Scientific Computing in Rust//EN\n"
        "VERSION:2.0\n"
        "CALSCALE:GREGORIAN\n"
        "METHOD:REQUEST\n"
        f"X-WR-CALNAME:Scientific Computing in Rust {year}\n"
        "X-WR-TIMEZONE:Europe/London\n"
        f"X-WR-CALDESC:The schedule for Scientific Computing in Rust {year}\n"
    )

    # tt_content += "<div style='font-weight:bold;font-size:120%;color:red'>The information on this page is not finalised</div>"
    # list_content += "<div style='font-weight:bold;font-size:120%;color:red'>The information on this page is not finalised</div>"

    list_content += markup("Show times in: <timeselector>", year=year)
    tt_content += markup("Show times in: <timeselector>", year=year)

    tt_content += "<style type='text/css'>\n"
    tt_content += ".timetablegrid {\n"
    tt_content += "  grid-template-columns: auto"
    for di, _ in enumerate(timetable):
        if di > 0:
            tt_content += " 0.1fr"
        tt_content += " 3fr"
    tt_content += ";\n"
    tt_content += "  grid-template-rows: auto 10px auto"
    after_break = None
    for i, (row, rowend) in enumerate(rows[:-1]):
        if i > 0:
            tt_content += " 2fr auto"
        tt_content += f" repeat({rowend + 1 - row}, 1fr)"
        if after_break is None:
            after_break = rowend + 2
    tt_content += "10px "
    if year < 2025:
        tt_content += "auto"
    else:
        tt_content += "repeat(4, 1fr)"
    tt_content += ";\n"
    tt_content += "}\n"
    tt_content += "</style>\n"

    def chair_row(start):
        if int(start.split(":")[0]) < 15:
            return 3
        return after_break

    tt_content += "<div class='timetablegrid'>\n"
    for di, day in enumerate(timetable):
        dcontent = ""
        date = info_yaml["days"][year][day]
        ics_day = f"{year}"
        ics_day += ('00' + str(months.index(date.split(" ")[-1])))[-2:]
        ics_day += ('00' + date.split(" ")[1])[-2:]

        list_content += f"<h2 style='margin-top:100px'>{date}</h2>{dcontent}"
        tt_content += ("<div class='gridcell timetableheading' style='grid-column: "
                       f"{2 * di + 2} / span 1;grid-row: 1 /span 1'><a href='/{year}/talklist-{day}.html'>"
                       f"{date}</a></div>")

        subtract = 0
        for si, session in enumerate(timetable[day]):
            ics_desc = ""
            session_time = markup(f"<time {day} {session['start']}>&ndash;<time {day} {session['end']}><tzone>", paragraphs=False, year=year)
            dcontent += "<h3"
            if si != 0:
                dcontent += " style='margin-top:50px'"
            dcontent += f">Session {si + 1} ({session_time}"
            if "platform" in session:
                dcontent += ", "
                if session['platform'] == "Gather Town":
                    dcontent += f"<a href='/{year}/gather-town.html'>Gather Town</a>"
                else:
                    dcontent += session['platform']
            dcontent += ")</h3>"
            col = 2 * di + 2
            row, rowend = rows[si - subtract]
            if "extra" in session and session["extra"]:
                subtract += 1
            if di == 0:
                tt_content += "<div class='gridcell timetableheading rotated' style='"
                tt_content += f"grid-column: {col - 1} / span 1; grid-row: {row} / span {rowend - row + 1}"
                tt_content += "'>"
                inner_content = f"Session {si + 1} (<time {day} {session['start']}>&ndash;<time {day} {session['end']}><tzone>"
                if "platform" in session:
                    inner_content += f", {session['platform']}"
                inner_content += ")"
                tt_content += markup(inner_content, paragraphs=False, year=year)
                tt_content += "</div>"
            if "description" in session:
                dcontent += f"<div class='timetablelisttalk'>{session['description']}</div>"
                ics_desc = session["description"]
            if "chair" in session:
                dcontent += (f"<div class='authors' style='margin-top:-10px;margin-bottom:10px'>"
                             f"Chair: {person(session['chair'])}</div>")
                tt_content += (f"<div style='grid-column: {col} / span 1; grid-row: {chair_row(session['start'])} / span 1;margin:10px;font-size:80%;text-align:center'>"
                               f"Chair: {session['chair']['name']}</div>")
            if "talks" in session:
                talklen = (rowend - row) / sum(info_yaml["long-length"][year] if is_long(t) else 1 for t in session["talks"])
                start = 0
                if "rowstart" in session:
                    row = session["rowstart"]
                for ti, t in enumerate(session["talks"]):
                    if t in special:
                        dcontent += talk(t, day, si + 1, session_time)
                    else:
                        dcontent += talk(t, day, si + 1, session_time, next_and_prev[t]["prev"], next_and_prev[t]["next"])
                    title, speaker = get_title_and_speaker(t, True)
                    length = 70 if is_long(t) else 20
                    nrows = info_yaml["long-length"][year] if is_long(t) else 1
                    if "rows" in session:
                        assert session["rows"] % len(session["talks"]) == 0
                        nrows = session["rows"] // len(session["talks"])
                    if t in special:
                        tt_content += "<div"
                    else:
                        tt_content += "<a"
                    tt_content += " class='gridcell timetabletalk"
                    if is_long(t):
                        tt_content += " longtalk"
                    tt_content += "'"
                    if t not in special:
                        tt_content += f" href='/{year}/talks/{t}.html'"
                    tt_content += (f" style='grid-column: {col} / span 1; grid-row: {row + start} / span {nrows}'>"
                                   f"<div class='timetabletalktitle'>{title}</div>")
                    ics_desc += f"{title}\\n"
                    icons = []
                    if not recorded(t):
                        icons.append("<i class='fa-solid fa-video-slash' alt='This talk will not be recorded' title='This talk will not be recorded'></i>")
                    if has_youtube(t):
                        icons.append("<i class='fa-brands fa-youtube' alt='A recording of this talk is available on YouTube' title='A recording of this talk is available on YouTube'></i>")
                    if has_slides(t):
                        icons.append("<i class='fa-solid fa-file-powerpoint' alt='Slides for this talk are available' title='Slides for this talk are available'></i>")
                    if len(icons) > 0:
                        tt_content += f"<div class='timetabletalktitle'>{' '.join(icons)}</div>"
                    if speaker is not None:
                        tt_content += f"<div class='timetabletalkspeaker'>{speaker}</div>"
                        ics_desc += f"{speaker}\\n"
                    ics_desc += "\\n"
                    if t in special:
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
                               f"grid-row: {row - 2} / span 1; "
                               "display: flex; justify-content: center; align-items: center;'>")
                tt_content += " &nbsp; &nbsp; &nbsp; ".join("BREAK")
                tt_content += "</div>"
            if archive:
                final_day = list(info_yaml["days"][year].values())[-1]
                modified = f"{year}"
                modified += ('00' + str(months.index(final_day.split(" ")[-1])))[-2:]
                modified += ('00' + final_day.split(" ")[1])[-2:]
                modified += "T180000"
            else:
                modified = datetime.now().strftime('%Y%m%dT%H%M00')
            ics += (
                "BEGIN:VEVENT\n"
                f"DTSTART:{ics_day}T{session['start'].replace(':', '')}00\n"
                f"DTEND:{ics_day}T{session['end'].replace(':', '')}00\n"
                f"DTSTAMP:{modified}\n"
                f"UID:w{year}-{day}-{si}@scientificcomputing.rs\n"
                f"CREATED:{year}0501T000000\n"
                f"DESCRIPTION:"
            )
            ics += ics_desc.replace(',', '\\,')
            ics += (
                "\n"
                f"LAST-MODIFIED:{modified}\n"
                "SEQUENCE:0\n"
                "STATUS:CONFIRMED\n"
                f"SUMMARY:{session['title'] if 'title' in session else 'Talks'}\n"
                "TRANSP:OPAQUE\n"
                "END:VEVENT\n"
            )
        list_content += dcontent
        write_page(f"{year}/talklist-{day}.html", f"<h1>{date}</h1>{markup('Show times in: <timeselector>', year=year)}{dcontent}", workshop=year)

    tt_content += "</div>"
    ics += "END:VCALENDAR\n"

    write_page(f"{year}/talklist.html", list_content, workshop=year)
    write_page(f"{year}/timetable.html", tt_content, workshop=year)
    with open(os.path.join(html_path, f"{year}/calendar.ics"), "w") as f:
        f.write(ics)
