# Thoth usage

## General

__Thoth__ has a build-in help system.
This help system will tell you how you can use the __Thoth__ commands.

_NOTE_
__Thoth__ may be installed as source code or as a package.
The examples below assume it is installed as a package.
If you use the source code replace `thoth` by `python thoth/main.py` in the commands.


Example:
```commandline
# thoth ‑‑help

Usage: thoth [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  about
  document  Document commands
  model     Document model commands
  profile   Document profile commands
  template  Document template commands
```

### Notation

Almost all __Thoth__ commands have values as arguments, these are shown between angled
brackets (i.e. `<` and `>`) like this
```commandline
# thoth-command <value>
```
Most of the values are files: enter the path to the file instead of `<value>`.

Some __Thoth__ commands have optional command line elements, these are shown between square
brackets (i.e. `[` and `]`) like this
```commandline
# thoth-command [optional part]
```
If you want to provide the optional part, drop the `[` and `]` from the command line.
Otherwise, drop the `[` and `]` and everything between.

## Create a model

Before you can create a document you will need a document model.

```commandline
# thoth model new
```
This will output an example model to get you started.
As document models are plain text files, you can use any text editor to change it.

A model consists of any number of fields.
Each field is defined over a number of lines.

The first line contains the field's name followed by a column (':').
All next lines of the field definition are indented by at least two spaces with respect
to this first line. Those lines define the properties of the field's value.

| property    | value type                        | default | description                                         |
|-------------|-----------------------------------|---------|-----------------------------------------------------|
| default     | any                               | -none-  | a value to use as default for optional simple types |
| description | text                              | -none-  | a text to explain the property                      |
| repeated    | true or false                     | false   | 'true' if this is a list of any number of values    |
| required    | true or false                     | false   | 'true' if a value must be provided                  |
| struct      | see [below](#structured-fields)   |         | definition of the field's value if it is structured |
| type        | see [below](#simple-field-types)  |         | type of the field's value if it is a simple type    |

NOTE #1: A field must define either 'struct' or 'type'.

NOTE #2: Only a field with a type can have a default, which should be of the appropriate type.

### Simple field types

Simple fields are

| type  | description                            |
|-------|----------------------------------------|
| bool  | a boolean, a truth value (true, false) |
| int   | an integer value, i.e. a whole number  |
| float | a floating point number                |
| str   | a string, a text of any length         |

In addition there is

| type         | description                  |
|--------------|------------------------------|
| multilingual | a text in multiple languages |

An example of a multilingual is
```yaml
en: This is an example of a 'multilingual'. The text is preceded by a language indicator.
nl: Dit is een voorbeeld van een 'multilingual'. De tekst wordt vooraf gegaan door een taalindicator.
```
See [below](#language-codes) for language codes.

### Structured fields

Structured fields are fields with the same structure as a model.
An example of a structured field is
```yaml
measurement:
  description: A measurement is made from a measured value and a unit of measurement
  struct:
    value:
      description: The measured value
      type: float
    unit:
      description: The unit of measurement
      type: str
```

### Language codes

For multilingual text use the two-letter language codes from [ISO 639][ISO-639], e.g.:
- `en` English
- `nl` Dutch

[ISO-639]: https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes


## Create and check a document

A document matches its model, i.e. fills the structure defined in the model.
Given a document model you can create a document as a starting point.

```commandline
# thoth document new --model <model-file> [--output <document-file>]
```
This will output a document that matches the model, with example values for you to edit.
As documents are plain text files, you can use any text editor to change it.

When you're done editing you can check if the document still matches its model.

```commandline
# thoth document check --model <model-file> <document-file>
```

Error messages should be reasonably clear to a non-technical audience.

If all is well, __Thoth__ will simply say "OK".


## Create and check a template

A template defines how to print a document as defined by a model.
Given a document model you can create a template as a starting point.

### Create a plain text template

Plain text templates are:
- markdown (md)
- HTML (html)
- text (txt)

As these are plain text files, you can use any text editor to change it.

See the [Jinja2 template language][JINJA2] on how to control the output from the template.

#### Create a markdown template

```commandline
# thoth template new --model <model-file> --format md [--output <template-file>]
```

#### Create an HTML template

```commandline
# thoth template new --model <model-file> --format html [--output <template-file>]
```

#### Create a text template

```commandline
# thoth template new --model <model-file> --format txt [--output <template-file>]
```

### Create a Microsoft Word template

To create a template for Microsoft Word, start with
```commandline
# thoth template new --model <model-file> --format docx --output <template-file>
```
See the [Word template language][DOCXTPL] on how to control the output of the template.

### Test the template

When you're done editing the template you can check the result with.

```commandline
# thoth document render --model <model-file> --template <template-file> <document-file> [<language>]  [--output <rendered-file>]
```
NOTE #1 If your document contains multilingual texts, you will need to include a `<language>`
for the rendering.

NOTE #2 If you render using a Microsoft Word template, you will always need to define an
output file.

[JINJA2]: https://jinja.palletsprojects.com/en/stable/templates/
[DOCXTPL]: https://docxtpl.readthedocs.io/en/latest/


## Create and check a profile

A profile controls which parts of a document are rendered.
If you create a template as described [above](#create-and-check-a-template) it will already
contain the logic necessary to properly render a document using a profile.

When you render a document without providing a profile, __Thoth__ assumes you want to render
all parts of the document. It generates a profile internally, with all parts enabled.

Given a document model you can create a profile as a starting point.

```commandline
# thoth profile new --model <model-file>  [--output <profile-file>]
```
This will output a profile for the model, with all parts enabled.
As profiles are plain text files, you can use any text editor to change it.

The profile thus generated has all parts enabled: the part is set to 'true'.
To disable a part, change it to 'false'.

NOTE If all parts of a [structured field](#structured-fields) are set to 'false',
the structured field itself is also set to 'false'. You may use this fact e.g. to control
labels only required when the structured field is rendered.

When you're done editing you can check if the profile still matches its model.

```commandline
# thoth document check --model <model-file> <document-file>
```

Error messages should be reasonably clear to a non-technical audience.

If all is well, __Thoth__ will simply say "OK".


## Create fragments

Fragments are pieces of static multi-lingual text for your rendered document,
i.e. given a language the same piece a text should be included in each rendered document.
This could be chapter names, a copyright notice, a project name, etc.

Instead of creating a template with static texts for each language, you create a single
fragments file and include it when rendering a document.

You can create fragments as a starting point.

```commandline
# thoth fragments new   [--output <fragments-file>]
```
This will output example fragments.
As fragments are plain text files, you can use any text editor to change it.

The syntax of fragments should be quite familiar if you have created a model and a document.

When you're done editing you can check if the fragments.

```commandline
# thoth fragments check <fragments-file>
```

Error messages should be reasonably clear to a non-technical audience.

If all is well, __Thoth__ will simply say "OK".


### Render a document

Once you have a document model, one or more templates, and optionally one or more profiles,
you render to file them using
```commandline
# thoth document render --model <model-file> --template <template-file> <document-file> [<language>] --output <output-file>
```
or
```commandline
# thoth document render --model <model-file> --template <template-file> [--fragments <fragments-file>] [--profile <profile-file>] <document-file> [<language>] --output <output-file> [--format <fmt>] [--force]
```
__Thoth__ guesses the output format based on the extension of the template and output file.
If it guesses wrong, you can explicitly tell it the format using `--format`.

NOTE If the `output-file` already exists, either choose another file name or add `--force` to
overwrite it.
