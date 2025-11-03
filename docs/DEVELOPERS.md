# Information for developers

The information here assumes you are already familiar with the Python language.

## Set-up

Assure you have the dependencies and developer's tools handy
```
# python -m pip install -e ".[dev]"
```

## Make changes

Do your magic.

## Create a release

```
# python -m build
```

This will create a directory `dist` containing
- a file with extension `.tar.gz` - the distributable source code
- a file with extension `.whl` - the distributable wheel (you need this)

Also, there will now be a directory `Thoth-dhwtj.egg-info`.
It is safe to discard this directory and its content.

## How to install and use a release

Install the wheel created above
```
# python -m pip install <wheel-file.whl>
```

Start using it
```
# thoth --help
```
