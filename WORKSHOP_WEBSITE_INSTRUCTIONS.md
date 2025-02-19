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

## Adding workshop timetable
This should be done around 4 weeks before the workshop

TODO: Write this while updating website for 2025

### Adding chairs

TODO: Write this while updating website for 2025

## Changing to post-event website

TODO: Write this while updating website for 2025
