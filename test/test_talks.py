import pytest
import yaml
import os


def join(*args):
    if len(args) == 1:
        return args[0]
    return os.path.join(args[0], join(*args[1:]))


root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

files = [
    join(root, "talks", file)
    for file in os.listdir(os.path.join(root, "talks"))
    if file.endswith(".yml") and not file.startswith("_")
]
year = 2023
while os.path.isdir(join(root, "archive", f"{year}", "talks")):
    files += [
        join(root, "archive", f"{year}", "talks", file)
        for file in os.listdir(os.path.join(root, "archive", f"{year}", "talks"))
        if file.endswith(".yml") and not file.startswith("_")
    ]
    year += 1

person_template = {
    "name": "STRING",
    "website": "STRING",
    "email": "STRING",
    "github": "STRING",
    "codeberg": "STRING",
    "zulip": "STRING",
    "mastodon": "STRING",
    "bluesky": "STRING",
    "twitter": "STRING",
    "linkedin": "STRING",
    "matrix": "STRING",
    "custom": (
        "LIST",
        {
            "url": "STRING",
            "icon": "STRING",
            "caption": "STRING",
            "*REQUIRED": ["url", "icon"],
        },
    ),
    "affiliation": "STRING",
    "*REQUIRED": ["name"],
}
yaml_talk_template = {
    "title": "STRING",
    "short-title": "STRING",
    "abstract": ("OR", [("LIST", "STRING"), "STRING"]),
    "speaker": person_template,
    "coauthor": ("LIST", person_template),
    "duration": ("VALUES", ["short", "long"]),
    "recorded": ("VALUES", [False]),
    "slides": "STRING",
    "slides_link": "STRING",
    "youtube": "STRING",
    "*REQUIRED": ["title", "abstract", "duration"],
}


def validate_yaml(data, template):
    if isinstance(template, dict):
        if not isinstance(data, dict):
            raise TypeError(f"Incorrect type (expected dict): {data}")
        for r in template.get("*REQUIRED", []):
            if r not in data:
                raise ValueError(f"Missing required field: {r}")
        for key, value in data.items():
            if key not in template:
                raise KeyError(f"Unexpected key: {key}")
            validate_yaml(value, template[key])
    elif isinstance(template, tuple):
        if template[0] == "LIST":
            if not isinstance(data, list):
                raise TypeError(f"Incorrect type (expected list): {data}")
            for i in data:
                validate_yaml(i, template[1])
        elif template[0] == "VALUES":
            if data not in template[1]:
                raise ValueError(f"Invalid value: {data} not in {template[i]}")
        elif template[0] == "OR":
            for option in template[1]:
                try:
                    validate_yaml(data, option)
                    break
                except BaseException:
                    pass
            else:
                raise TypeError(
                    f"Incorrect type (expected one of {template[1]}): {data}"
                )
        else:
            raise ValueError(f"Unexpected type: {template[0]}")
    elif template == "STRING":
        assert isinstance(data, str)
    else:
        raise ValueError(f"Unexpected template: {template}")


@pytest.mark.parametrize("file", files)
def test_file(file):
    with open(file) as f:
        data = yaml.load(f, yaml.FullLoader)
    validate_yaml(data, yaml_talk_template)
