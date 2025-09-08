# Changelog

All notable changes to the __Thoth__ will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## v0.4.1 - 2025/09/08

- updated documentation

## v0.4.0 - 2025/09/08

- added rendering to the `md` (Markdown) format
- provided a `norm.md` template

## v0.3.0 - 2025/07/29

- added the `template` command to create customizable copies of the internal templates:

  | subcommand  | description                                          |
  |-------------|------------------------------------------------------|
  | `new`       | create customizable copies of the internal templates |

- the `norm render` command now has an optional argument `--template` to select customized templates


## v0.2.3 - 2025/07/17

- fix packaging bug

## v0.2.2 - 2025/07/17

- distributable package

## v0.2.1 - 2025/04/29

- internal clean-up.

## v0.2.0 - 2025/04/25

- `render` can now render to `.docx` as well as `.html`.
- `render` now uses templates for both `.html` and `.docx`.

## v0.1.0 - 2025/03/25

- added the `profile` command for profiles that control parts that are rendered:

  | subcommand  | description                                      |
  |-------------|--------------------------------------------------|
  | `new`       | create a starting point for a profile definition |
  | `reformat`  | reformat a profile                               |
 
- added the `--profile` option to `norm render` to control the parts that are rendered

## v0.0.1 - 2025/03/25

### Commands in initial release

- `about` command

- `norm` subcommands to create, translate, render, and maintain SSD norm definitions:

  | subcommand           | description                                             |
  |----------------------|---------------------------------------------------------|
  | `check`              | check a norm for various issues                         |
  | `languages`          | which languages are present in the document?            |
  | `new`                | create a starting point for a norm definition           |
  | `reformat`           | reformat a norm                                         |
  | `render`             | render a norm definition in a document format           |
  | `render-translated`  | render a norm definition in two languages, side by side |
  | `split`              | split a specific language off a norm                    |
  | `update`             | update norm from a second norm                          |
  | `xcheck`             | check whether two norm definitions match                |
