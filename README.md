# shopen

shopen is a proper implementation of os.startfile to launch a target file/URL. Use it to launch the
preferred system viewer for the user to view or edit a target file or URL.

[![PyPI - Version](https://img.shields.io/pypi/v/shopen.svg)](https://pypi.org/project/shopen)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/shopen.svg)](https://pypi.org/project/shopen)

-----

## Usage

Simply install as a dependency of your project and then use it to launch an opener for a file or
URL:

```python
import pathlib
import shopen
shopen.open("https://zombo.com/")  # Opens web browser
shopen.open(pathlib.Path("~/somefile.txt").expanduser())  # Opens file viewer
```

## Why?

Python's standard library provides nice cross-platform utilites for lots of different purposes, but
so far no simple file/URL opener that would work on all platforms.

On Windows there's [os.startfile], but strangely that doesn't support any other platform.

There was a proposal [python/cpython#47427](https://github.com/python/cpython/issues/47427) to
implement it as `shutil.open`, but it was rejected for now. Python users keep [asking](
https://stackoverflow.com/questions/434597/open-document-with-default-os-application-in-python-both-in-windows-and-mac-os)
for a decent way to do it, but the only answer had been brittle copypasta… until now!

Ideally this can be added into stdlib after proving its usefulness and then only be needed as a
polyfill for older versions of python.

[os.startfile]: https://docs.python.org/3/library/os.html#os.startfile
