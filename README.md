# markdown-spellchecker
Utility for spell-checking markdown files, will recursively search a directory for markdown files or search a given file.

### Prerequisites
Non-standard Python packages:
```
pip install beautifulsoup4
pip install pyspellchecker
pip install markdown
```

### Usage

`python markdown_spellchecker.py -p <file_or_directory> -d <optional_custom_dictionary> -d <optional_custom_dictionary2>`

`file_or_directory` can be a relative path to markdown file or a directory. If it is a directory, the script will search for any files that end in `.md` and will spellcheck them.

`optional_custom_dictionary` is optional, for situations with unique words or names. It is a path to a text file that has a single word, <b>in lower case</b> on each line.

The script can be pulled by either cloning the repository or running `wget https://raw.githubusercontent.com/romangrebin/markdown-spellchecker/master/markdown_spellchecker.py`
