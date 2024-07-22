from markdown import markdown
import shlex
import re
from datetime import datetime
from citations import markup_citation
from monthly import monthly_list

page_references = []
ref_map = {}


def markup(content, icons=True, paragraphs=True):
    global page_references

    while "<!--" in content:
        a, b = content.split("<!--", 1)
        content = a
        if "-->" in b:
            content += b.split("-->", 1)[1]

    if "{{monthly_list}}" in content:
        content = content.replace("{{monthly_list}}", monthly_list())

    if "{% no markup %}" in content:
        before, after = content.split("{% no markup %}", 1)
        middle, after = after.split("{% end no markup %}", 1)
        return markup(before, icons) + middle + markup(after, icons)

    while "{{if " in content:
        pre, rest = content.split("{{if ", 1)
        condition, rest = rest.split("}}", 1)
        optional, post = rest.split("{{fi}}", 1)
        condition, options = condition.split(" ", 1)
        content = pre
        if condition in ["before", "after"]:
            options = [int(i) for i in options.split(",")]
            if condition == "before" and datetime.now() < datetime(*options):
                content += optional
            if condition == "after" and datetime.now() > datetime(*options):
                content += optional
        elif condition == "dateis":
            y, m, d = [int(i) for i in options.split(",")]
            y2 = datetime.now().year
            m2 = datetime.now().month
            d2 = datetime.now().day
            if y == y2 and m == m2 and d == d2:
                content += optional
        else:
            raise ValueError(f"Unknown condition: {condition}")
        content += post

    while "<person>" in content:
        a, b = content.split("<person>", 1)
        b, c = b.split("</person>", 1)
        content = a + markup_person(b) + c

    if "```" in content:
        content0, code, content1 = content.split("```", 2)
        if code.startswith("python"):
            code = python_highlight(code)
        else:
            code = code.strip().replace(" ", "&nbsp;")
        return f"{markup(content0)}<p class='pcode'>{code}</p>{markup(content1)}"

    content = content.replace(".md)", ".html)")

    out = markdown(content)
    if not paragraphs:
        out = out.replace("<p>", "").replace("</p>", "")

    page_references = []

    out = re.sub(r"<time ([0-2][0-9]):([0-6][0-9])>", r"<span class='bst-time' data-format='{24 0HOUR}:{MINUTE}' data-day='17' data-month='7' data-year='2024' data-hour='\1' data-minute='\2'>\1:\2</span>", out)
    out = re.sub(r"<time Wednesday ([0-2][0-9]):([0-6][0-9])>", r"<span class='bst-time' data-format='{24 0HOUR}:{MINUTE}' data-day='17' data-month='7' data-year='2024' data-hour='\1' data-minute='\2'>\1:\2</span>", out)
    out = re.sub(r"<time Thursday ([0-2][0-9]):([0-6][0-9])>", r"<span class='bst-time' data-format='{24 0HOUR}:{MINUTE}' data-day='18' data-month='7' data-year='2024' data-hour='\1' data-minute='\2'>\1:\2</span>", out)
    out = re.sub(r"<time Friday ([0-2][0-9]):([0-6][0-9])>", r"<span class='bst-time' data-format='{24 0HOUR}:{MINUTE}' data-day='19' data-month='7' data-year='2024' data-hour='\1' data-minute='\2'>\1:\2</span>", out)
    out = re.sub(r"<tzone>", r"<span class='tzone'> BST</span>", out)
    out = out.replace("<timeselector>", "<select id='tzselect' onchange='change_timezone_dropdown(this.value)'></select>")
    out = re.sub(r"<ref ([^>]+)>", add_citation, out)
    out = re.sub(r"<ghostref ([^>]+)>", add_ghost_citation, out)
    out = insert_links(out)
    if icons:
        out = insert_icons(out)

    out = re.sub(r"{{icon:([^}]+)}}", enter_icon, out)
    out = re.sub(r"`([^`]+)`", r"<span style='font-family:monospace'>\1</span>", out)

    if len(page_references) > 0:
        out += "<h2>References</h2>"
        out += "<ul class='citations'>"
        out += "".join([f"<li><a class='refid' id='ref{i+1}'>[{i+1}]</a> {j}</li>"
                        for i, j in enumerate(page_references)])
        out += "</ul>"

    out = insert_dates(out)
    return out


iconlist = []

defelementlist = [
    ("Mardal&ndash;Tai&ndash;Winther", "mardal-tai-winther"),
    ("Arnold&ndash;Winther", "arnold-winther"),
    ("seredipity", "serendipity"),
    ("Lagrange", "lagrange"),
    ("N&eacute;d&eacute;lec", "nedelec1"),
    ("Raviart&ndash;Thomas", "raviart-thomas"),
    ("Scott&ndash;Vogelius", "scott-vogelius"),
    ("Bernstein&ndash;B&eacute;zier", "bernstein"),
]


def enter_icon(matches):
    for t, icon, url in iconlist:
        if matches[1] == t:
            if icon is None:
                return f"<a href='{url}' class='icon'>{t}</a>"
            else:
                return f"<a href='{url}' class='icon'><img src='/img/{icon}'>{t}</a>"
    raise ValueError(f"Icon not found: {matches[1]}")


def insert_icons(txt):
    for t, icon, url in iconlist:
        if icon is None:
            txt = re.sub(
                r"(^|[>\s.!?\(\/])" + t + r"([\s.!?\)\/,']|(?:-based))",
                r"\1<a href='" + url + "' class='icon'>" + t + r"</a>\2",
                txt, 1)
        else:
            txt = re.sub(
                r"(^|[>\s.!?\(\/])" + t + r"([\s.!?\)\/,']|(?:-based))",
                r"\1<a href='" + url + "' class='icon'><img src='/img/" + icon + "'>" + t + r"</a>\2",
                txt, 1)
    for e, url in defelementlist:
        txt = txt.replace(e, f"<a class='icon' href='https://defelement.com/elements/{url}.html'>"
                          f"<img src='/img/defelement.png'>{e}</a>", 1)
    return txt


def insert_links(txt):
    txt = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)\{([^\}]+)\}",
                 r"<a class='icon' href='\2'><img src='/img/\3'>\1</a>", txt)
    txt = re.sub(r"\[([^\]]+)\]\(([^\)]+)\.md\)", r"<a href='\2.html'>\1</a>", txt)
    txt = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", r"<a href='\2'>\1</a>", txt)
    txt = re.sub(r"([^'\"])(https?:\/\/)([^\s\)]+)", r"\1<a href='\2\3'>\3</a>", txt)
    return txt


def add_ghost_citation(matches):
    add_citation(matches)
    return ""


def add_citation(matches):
    global page_references
    global ref_map
    if matches[1] not in ref_map:
        ref = {}
        for i in shlex.split(matches[1]):
            a, b = i.split("=")
            ref[a] = b
        page_references.append(markup_citation(ref))
        ref_map[matches[1]] = len(page_references)
    return f"<a href='#ref{ref_map[matches[1]]}'>[{ref_map[matches[1]]}]</a>"


def insert_dates(txt):
    now = datetime.now()
    txt = txt.replace("{{date:Y}}", now.strftime("%Y"))
    txt = txt.replace("{{date:D-M-Y}}", now.strftime("%d-%B-%Y"))

    return txt


def python_highlight(txt):
    txt = txt.replace(" ", "&nbsp;")
    out = []
    for line in txt.split("\n"):
        comment = ""
        if "#" in line:
            lsp = line.split("#", 1)
            line = lsp[0]
            comment = f"<span style='color:#F77237'>#{lsp[1]}</span>"

        lsp = line.split("\"")
        line = lsp[0]

        for i, j in enumerate(lsp[1:]):
            if i % 2 == 0:
                line += f"<span style='color:#DD2299'>\"{j}"
            else:
                line += f"\"</span>{j}"

        out.append(line + comment)
    return "<br />".join(out)


def markup_person(details):
    out = "<div class='person'>"
    info = {}
    for line in details.strip().split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            info[key.strip()] = value.strip()

    if "img" in info:
        out += f"<div class='imgwrap'><img src='{info['img']}'></div>\n"
    else:
        out += "<div class='imgwrap'><img src='/img/faceholder.png'></div>\n"
    out += "<div class='innertext'>\n"
    out += f"<h3>{info['name']}</h3>\n{info['about']}"
    if "rust-about" in info:
        out += f" {info['rust-about']}"
    out += "<ul class='sociallist'>"
    if "email" in info:
        out += f"<li><a href='mailto:{info['email']}'><i class='fa-solid fa-envelope'></i>&nbsp;"
        out += info["email"]
        out += "</a></li>"
    if "website" in info:
        out += f"<li><a href='{info['website']}'><i class='fa-brands fa-internet-explorer'></i>&nbsp;"
        out += info["website"].split("://")[1]
        out += "</a></li>"
    if "github" in info:
        out += f"<li><a href='https://github.com/{info['github']}'>"
        out += "<i class='fa-brands fa-github'></i>&nbsp;"
        out += info["github"]
        out += "</a></li>"
    if "zulip" in info:
        out += "<li><a href='https://rust-scicomp.zulipchat.com'>"
        out += "<svg class='brand-logo' role='img' aria-label='Zulip' xmlns='http://www.w3.org/2000/svg' viewBox='68.96 55.62 450 450.43' height='15.5'>"
        out += "<path class='filled' d='M473.09 122.97c0 22.69-10.19 42.85-25.72 55.08L296.61 312.69c-2.8 2.4-6.44-1.47-4.42-4.7l55.3-110.72c1.55-3.1-.46-6.91-3.64-6.91H129.36c-33.22 0-60.4-30.32-60.4-67.37 0-37.06 27.18-67.37 60.4-67.37h283.33c33.22-.02 60.4 30.3 60.4 67.35zM129.36 506.05h283.33c33.22 0 60.4-30.32 60.4-67.37 0-37.06-27.18-67.37-60.4-67.37H198.2c-3.18 0-5.19-3.81-3.64-6.91l55.3-110.72c2.02-3.23-1.62-7.1-4.42-4.7L94.68 383.6c-15.53 12.22-25.72 32.39-25.72 55.08 0 37.05 27.18 67.37 60.4 67.37zm522.5-124.15l124.78-179.6v-1.56H663.52v-48.98h190.09v34.21L731.55 363.24v1.56h124.01v48.98h-203.7V381.9zm338.98-230.14V302.6c0 45.09 17.1 68.03 47.43 68.03 31.1 0 48.2-21.77 48.2-68.03V151.76h59.09V298.7c0 80.86-40.82 119.34-109.24 119.34-66.09 0-104.96-36.54-104.96-120.12V151.76h59.48zm244.91 0h59.48v212.25h104.18v49.76h-163.66V151.76zm297 0v262.01h-59.48V151.76h59.48zm90.18 3.5c18.27-3.11 43.93-5.44 80.08-5.44 36.54 0 62.59 7 80.08 20.99 16.72 13.22 27.99 34.99 27.99 60.64 0 25.66-8.55 47.43-24.1 62.2-20.21 19.05-50.15 27.6-85.13 27.6-7.77 0-14.77-.39-20.21-1.17v93.69h-58.7V155.26zm58.7 118.96c5.05 1.17 11.27 1.55 19.83 1.55 31.49 0 50.92-15.94 50.92-42.76 0-24.1-16.72-38.49-46.26-38.49-12.05 0-20.21 1.17-24.49 2.33v77.37z'></path>"
        out += "</svg>&nbsp;"
        out += info["zulip"]
        out += "</a></li>"
    if "mastodon" in info:
        username, domain = info['mastodon'].split('@')
        out += f"<li><a href='https://{domain}/@{username}'>"
        out += "<i class='fa-brands fa-mastodon'></i>&nbsp;"
        out += "@" + info["mastodon"]
        out += "</a></li>"
    if "twitter" in info:
        out += f"<li><a href='https://twitter.com/{info['twitter']}'>"
        out += "<i class='fa-brands fa-twitter'></i>&nbsp;"
        out += "@" + info["twitter"]
        out += "</a></li>"

    out += "</ul></div></div>"
    return out
