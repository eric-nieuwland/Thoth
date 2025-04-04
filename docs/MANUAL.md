# Thoth manual

## Introduction

The Center for Information Security and Privacy Protection (CIP) is a public-private
collaborative network organization in The Netherlands.
[The CIP website][CIP-website] provides information on CIP and its activities (in Dutch).

The development and maintenance of 'Grip op SSD' is one of CIP's activities.
It is a method with associated norms to support secure software development (SSD).
SSD products can be found on [the SSD page on the CIP website][SSD-page].

Initially, SSD documents where written and maintained in Dutch using common text editors.
With the adoption of SSD by Dutch and Flemish governments software developers were held
to apply SSD. As software developers need not speak Dutch, translations of SSD documents
became a necessity.
Meanwhile, CIP and its SSD workgroup had the strong desire to be able to generate documents
for various audiences (e.g. project managers, developers, testers) in various formats
(e.g. HTML, PDF) from a single source. Ideally, some sort of version control should
be applied to this single source.<br>
Clearly, common text editors no longer fit the requirements.

Ideally, we should be able to:
- Separate content from presentation;
- Render content in various formats;
- Select document parts to render;
- Create and maintain content using common tools, preferably as plain text;
- Create translations of the content to various languages;
- Maintain translations of the content 'in sync', i.e. simultaneously for multiple languages.

__Thoth__ aims to provide the tools to make this possible.
__Thoth__ documents are [YAML files][YAML-page].
Each document has a fixed structured, with space for translations to specific languages.
__Thoth__ provides the commands to create, manage, maintain, and render these documents.


[CIP-website]: https://www.cip-overheid.nl
[SSD-page]: https://www.cip-overheid.nl/producten-en-diensten/?type=Secure%20Software
[YAML-page]: https://en.wikipedia.org/wiki/YAML


### What's in a name?

[Thoth][Thoth-wikipedia] (𓅝, ḏḥwtj; Djehuti) is the god of the Moon,
wisdom, knowledge, writing, hieroglyphs, science, magic, art and
judgement. As such he plays a major role to maintain Ma'at, the
proper order in the world and the universe.

As CIP's SSD aims to create some order in software development it only seems right to name
the software that helps to create, maintain and render SSD documents after this deity.

To avoid a name clash with a Python package already named `thoth` this software's package name
is `Thoth-dhwtj`, which stresses its relation to Ma'at.


[Thoth-wikipedia]: https://en.wikipedia.org/wiki/Thoth


### What is needed?

__Thoth__ is an Python application, build for Python 3.13 and up.
You may wish to run Thoth in a virtual environment, see [the Python documentation][Python-venv].

It requires some third party packages defined in `pyproject.toml`.
Use `pip` to install those packages.


[Python-venv]: https://docs.python.org/3/library/venv.html


## General

__Thoth__ has a build-in help system.
This help system will tell you how you can use the __Thoth__ commands.

Examples:
```commandline
# python thoth.py ‑‑help

 Usage: thoth.py [OPTIONS] COMMAND [ARGS]...
 
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ‑‑install-completion          Install completion for the current shell.                                         │
│ ‑‑show-completion             Show completion for the current shell, to copy it or customize the installation.  │
│ ‑‑help                        Show this message and exit.                                                       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ about                                                                                                           │
│ norm    Norm commands                                                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
```commandline
# python thoth.py norm ‑‑help

 Usage: thoth.py norm [OPTIONS] COMMAND [ARGS]...

 Norm commands

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ‑‑help          Show this message and exit.                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ check               check a norm for various issues                                                             │
│ languages           which languages are in the document and in howmany translations is each language present?   │
│ new                 create a starting point for a norm definition                                               │
│ reformat            reformat a norm                                                                             │
│ render              render a norm definition in a document format                                               │
│ render-translated   render a norm definition in two languages, side by side                                     │
│ split               split a specific language off a norm                                                        │
│ update              update norm from a second norm                                                              │
│ xcheck              check whether two norm definitions match                                                    │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
```commandline
# python thoth.py norm new <language code> ‑‑output

 Usage: thoth.py norm new [OPTIONS] LANGUAGE

 create a starting point for a norm definition

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    language      TEXT  [default: None] [required]                                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ‑‑output                  PATH  [default: None]                                                                 │
│ ‑‑force     ‑‑no-force          [default: no-force]                                                             │
│ ‑‑help                          Show this message and exit.                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```


## Create a norm

To create a new norm first decide in which language you'll write it.

Use the two-letter language code from [ISO 639][ISO-639]:
- `en` English
- `nl` Dutch

1. Let __Thoth__ create a starting point for your norm
   (if `norms/my-first-norm.yaml` already exists, add `‑‑force`):
   ```commandline
   # python thoth.py norm new en ‑‑output norms/my-first-norm.yaml
   ```

2. Use any text editor to modify `norms/my-first-norm.yaml`, but make sure to preserve
   the indentation structure. Also, make sure the identifiers are correct.


3. Let __Thoth__ check your result
   ```commandline
   # python thoth.py norm check norms/my-first-norm.yaml
   ```

4. Have __Thoth__ prepare a translation of the norm, i.e. preserve structure and
   put in placeholders for the new language (you need `‑‑force` as the language is not present)
   ```commandline
   # python thoth.py norm split norms/my-first-norm.yaml nl ‑‑force ‑‑output norms/mijn-eerste-norm.yaml
   ```
   
5. Like step 2, use any text editor to modify `norms/mijn-eerste-norm.yaml`.


6. Have __Thoth__ add the translation of the norm
   ```commandline
   # python thoth.py norm update norms/my-first-norm.yaml nl norms/mijn-eerste-norm.yaml ‑‑output norms/my-bilingual-norm.yaml
   ```
   You may also use either `norms/my-first-norm.yaml` or `norms/mijn-eerste-norm.yaml` with `‑‑output`,
   but you'll need to add `‑‑force` to overwrite it.

You can now maintain the file with the multi-lingual norm, add another translation (repeat steps 4-6),
or edit a single language of the norm (repeat steps 4-6, without `‑‑force` in step 4).

As the norms are plain text files, you can use most version control systems to keep track of versions
and changes.


[ISO-639]: https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes


## Render a norm in one of its languages

1. Have __Thoth__ render a norm to HTML
   ```commandline
   # python thoth.py norm render norms/my-bilingual-norm.yaml nl ‑‑output my-bilingual-norm.html
   ```
   Note: __Thoth__ determines the format from `‑‑output`. If no output is given, use `‑‑format html`.


## Render a norm in two of its languages for comparison

1. Have __Thoth__ render a norm to HTML
   ```commandline
   # python thoth.py norm render-translated norms/my-bilingual-norm.yaml nl en ‑‑output my-bilingual-norm-nl-en.html
   ```
   Note: __Thoth__ determines the format from `‑‑output`. If no output is given, use `‑‑format html`.


## Selectively render parts of a norm

You can specify which items of a norm must be rendered. For this you create a profile:

1. Let __Thoth__ create a starting point for your profile
   (if `profile/my-first-profile.yaml` already exists, add `‑‑force`):
   ```commandline
   # python thoth.py profile new ‑‑output profile/my-first-profile.yaml
   ```

2. Use any text editor to modify `profile/my-first-profile.yaml`, but make sure to preserve
   the indentation structure.
   Change `true` to `false` to turn off rendering of a norm item.
   Items with subitems will not be rendered if all subitems are turned off.


3. Have __Thoth__ render a norm to HTML using the profile
   ```commandline
   # python thoth.py norm render norms/my-bilingual-norm.yaml nl --profile profile/my-first-profile.yaml ‑‑output my-bilingual-norm.html
   ```
