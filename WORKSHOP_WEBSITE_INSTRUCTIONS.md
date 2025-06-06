# Scientific Computing in Rust workshop website updating instructions

This guide details how the website for the annual workshop can be updated when adding
details about the next workshop.

## Adding a new workshop
This should be done in ~January every year.

- [ ] Add dates to [info.yml](info.yml)
- [ ] Make a directory pages/{YEAR} containing:
    - [ ] index.md
    - [ ] register.md
    - [ ] submit-talk.md
    - [ ] team.md
- [ ] Update pages/index.md to link to latest year
- [ ] Update archive by running `python builder/build.py --year {YEAR - 1}`. You
      May also need to update the years before this.
- [ ] Update tamplate/intro.html to make the latest workshop have links:
    - {{workshop-year}} home
    - Register
    - Propose talk
    - Organisers

## Adding workshop timetable
This should be done around 4 weeks before the workshop.

- [ ] Make a directory talks containing:
    - [ ] a .yml file for every talk, containing the fields:
        - [ ] title
        - [ ] abstract
        - [ ] speaker (with name, affiliation, github, email, website, etc)
        - [ ] coauthor (optional)
        - [ ] duration (short or long)
    - [ ] _timetable.yml
- [ ] Update tamplate/intro.html to make the latest workshop have links:
    - {{workshop-year}} home
    - Register
    - Timetable
    - List of talks
    - Propose tutorial
    - Organisers
- [ ] Update index.html to link to workshop schedule

### Adding chairs
This should be done 1-2 weeks before the workshop.

- [ ] Add `chair` field to each session in the timetable (with name, github, email, website, etc)

## Changing to post-event website
This should be done 0-1 weeks after the workshop.

- [ ] Add `youtube` field to the .yml file for each talk that was recorded with the YouTube id of the recording.
- [ ] Remove registration link.
- [ ] Change text on all pages to past tense.

TODO: Write this while updating website for 2025
