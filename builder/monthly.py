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
    return "\n".join(f"* [#{i[1]} ({i[2]})](monthly/{i[0]})" for i in issues)


def pull_monthly():
    if not os.path.isdir(monthly_path):
        os.system("git clone https://github.com/rust-scicomp/"
                  f"scientific-computing-in-rust-monthly.git {monthly_path}")
    os.system(f"cd {monthly_path} && git pull")
