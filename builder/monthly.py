import os

dir_path = os.path.dirname(os.path.realpath(__file__))
monthly_path = os.path.join(dir_path, "../monthly")
issues_path = os.path.join(monthly_path, "issues")


def monthly_list():
    issues = []
    for file in os.listdir(issues_path):
        if file.endswith(".md") and not file.startswith("."):
            date = None
            number = None
            with open(os.path.join(issues_path, file)) as f:
                first = True
                for line in f:
                    line = line.strip()
                    if first:
                        assert line == "---"
                        first = False
                    elif line.startswith("number:"):
                        number = int(line[7:])
                    elif line.startswith("date:"):
                        date = line[5:].strip()
                    elif line == "---":
                        break
            issues.append((file[:-3], number, date))
    issues.sort(key=lambda i: -i[1])
    return "\n".join(f"* [Scientific Computing in Rust Monthly #{i[1]} ({i[2]})](/monthly/{i[0]})" for i in issues)


def pull_monthly():
    if not os.path.isdir(monthly_path):
        os.system("git clone https://github.com/rust-scicomp/"
                  f"scientific-computing-in-rust-monthly.git {monthly_path}")
    os.system(f"cd {monthly_path} && git pull")


def latest_issue():
    issues = []
    for file in os.listdir(issues_path):
        if file.endswith(".md") and not file.startswith("."):
            date = None
            number = None
            with open(os.path.join(issues_path, file)) as f:
                first = True
                for line in f:
                    line = line.strip()
                    if first:
                        assert line == "---"
                        first = False
                    elif line.startswith("number:"):
                        number = int(line[7:])
                    elif line.startswith("date:"):
                        date = line[5:].strip()
                    elif line == "---":
                        break
            issues.append((file[:-3], number, date))
    issues.sort(key=lambda i: -i[1])
    return issues[0][0]


def rss():
    from markup import markup
    out = (
        "<?xml version='1.0'?>\n"
        "<rss version='2.0' xmlns:atom='http://www.w3.org/2005/Atom'>\n"
        "<channel>\n"
        "<atom:link href='https://www.scientificcomputing.rs/monthly/rss.xml' rel='self' type='application/rss+xml' />\n"
        "<title>Scientific Compting in Rust Monthly</title>\n"
        "<description>A monthly newsletter containing the latest information about scientific computing in the Rust programming language.</description>\n"
        "<link>https://www.scientificcomputing.rs/monthly/</link>\n")

    issues = []
    for file in os.listdir(issues_path):
        if file.endswith(".md") and not file.startswith("."):
            date = None
            day = None
            number = None
            with open(os.path.join(issues_path, file)) as f:
                first = True
                for line in f:
                    line = line.strip()
                    if first:
                        assert line == "---"
                        first = False
                    elif line.startswith("number:"):
                        number = int(line[7:])
                    elif line.startswith("date:"):
                        date = line[5:].strip()
                    elif line.startswith("day:"):
                        day = line[5:].strip()
                    elif line == "---":
                        break
            issues.append((file[:-3], number, date, day))
    issues.sort(key=lambda i: -i[1])

    for i in issues[:12]:
        with open(os.path.join(issues_path, f"{i[0]}.md")) as f:
            content = markup(f.read().split("---", 2)[-1])
        content = content.replace("<", "&lt;")
        content = content.replace(">", "&gt;")
        out += (
            "<item>\n"
            f"<title>Scientific Computing in Rust #{i[1]}</title>\n"
            f"<description>{content}</description>\n"
            f"<link>https://www.scientificcomputing.rs/monthly/{i[0]}</link>\n"
            f"<guid>https://www.scientificcomputing.rs/monthly/{i[0]}</guid>\n"
            f"<pubDate>{i[3]} {i[2][:3]} {i[2][-4:]} 12:00:00 GMT</pubDate>\n"
            "</item>\n")
    out += "</channel>\n</rss>\n"
    return out
