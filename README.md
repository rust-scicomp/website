# Scientific Computing in Rust

This repo runs the [Scientific Computing in Rust website](https://scientificcomputing.rs).

## Building the website

To build the website run:

```bash
python builder/build.py
```

The HTML website will be created in a new folder called `_html`. To locally view the build website,
you can run:

```bash
cd _html
python -m http.server
```

The archive of a previous year's website can be created by running (for example for 2023):

```bash
python builder/build.py --year 2023
```

The HTML files that this creates are included in the repo, so this needs to be run locally and changes to HTML files
need to be pushed to edit an archived year.


## Editing the website

To edit the website, you may need to edit files in a range of locations:

- The `builder` folder contains the Python scripts that convert the input files into a HTML website.
- The `files` folder contains non-HTML files for the website (eg image, CSS style files). These
  will be copied into the `_html` folder when the website is built.
- The `pages` folder contains markdown files for pages on the website. The file `filename.md` will
  become `filename.html` when the website is built.
- The `talks` folder contains yaml files for the talks and the talk timetable.
- The `template` folder contains html files that form the template for each html page.

## License

The code to generate the Scientific Computing in Rust website is released under an
[MIT license](LICENSE).
This project additionally redistributes the following third-party software, which
is licensed under its own license:

- [Font Awesome](https://fontawesome.com/) [Font Awesome Free License](https://fontawesome.com/license/free)

