# Thoth manual

## Introduction

Some types of documentation are highly structured, e.g. standaards, norms, etc.
These highly structured documents contain information for different audiences.
However, not all parts are equally relevant to these audiences.
Therefore, it is desirable to be able to create and maintain a single source document,
while also be able to create different documents derived from that source document.
What is more, various types of documents are structured differently.
So we need to be able to specify our document model to begin with.

Ideally, we should be able to:
- Define a document model;
- Create a document according to this document model;
- Create a rendering template for documents of this document model;
- Render a document in various formats;
- Select which document parts to render independent of the actual document;

What is more, we should be able to create and maintain all content using common tools,
preferably as plain text.

And if the nature of a document would require so, we should be able to create translations
of the content to various languages and to keep those translations 'in sync',
i.e. apply changes simultaneously for multiple languages.

__Thoth__ aims to provide the tools to make this possible.
__Thoth__ documents are [YAML files][YAML-page].
Each document has a defined structure.
__Thoth__ provides commands to create document models, documents, profiles, and rendering
templates and commands to render those documents using templates and profiles.


[YAML-page]: https://en.wikipedia.org/wiki/YAML


### What's in a name?

[Thoth][Thoth-wikipedia] (𓅝, ḏḥwtj; Djehuti) is the old Egyptian god of the Moon, wisdom,
knowledge, writing, hieroglyphs, science, magic, art and judgement. As such he plays a major
role to maintain Ma'at, the proper order in the world and the universe.

This software aims to comprehensively capture structured knowledge,
to allow information to be created and maintained with tools,
and bring some order into what would otherwise be a pile of forms on a desk
or in digital storage.
It thus seems quite fitting to name the software after this deity.

To avoid a name clash with a Python package already named `thoth` this software's package name
is `Thoth-dhwtj`, which stresses its relation to Ma'at.


[Thoth-wikipedia]: https://en.wikipedia.org/wiki/Thoth


## Installation

See [the installation manual](./man/INSTALLATION.md).


## Usage

See [the usage manual](./man/USAGE.md).
