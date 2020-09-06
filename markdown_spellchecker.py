
from bs4 import BeautifulSoup
import markdown
from pathlib import Path
from spellchecker import SpellChecker
import string

def spellcheck_file(filepath, dictionary):
    file_errors = {}
    with open(filepath) as f:
        line_num = 1

        while True:
            md_line = f.readline()
            if not md_line:
                break
            new_errors = spellcheck_line(md_line, dictionary)

            for word in new_errors:
                if word not in file_errors:
                    file_errors[word] = []
                for word_num in new_errors[word]:
                    file_errors[word].append("Line {}, word {}".format(line_num, word_num))

            line_num += 1

    return file_errors


def spellcheck_line(line, dictionary):
    """
    Returns python dictionary, keys are words that are  not in the SpellChecker and not in the custom dictionary
        Return dictionary values are list of the word locations on the line
    """

    sc = SpellChecker()

    # Convert the markdown to html
    html = markdown.markdown(line)

    # text = "".join(BeautifulSoup(html, "lxml").findAll(text=True))
    text = "".join(BeautifulSoup(html).findAll(text=True))

    # Remove punctuation symbols
    text = "".join(c if c not in string.punctuation else " " for c in text)

    # Split string into list of words
    words = text.split()

    errors = {}

    word_num = 1

    for word in words:
        if sc.unknown([word]) and word.lower() not in dictionary and word.isalpha():
            if word not in errors:
                errors[word] = []
            
            errors[word].append(word_num)
        word_num += 1

    return errors


def spellcheck_path(path, dictionary):

    if os.path.isdir(path):
        print("Parsing directory...")
        file_paths = Path(path).rglob('*.md')
            
    else:
        print("Spellchecking single file...")
        file_paths = [path]

    for file_path in file_paths:
        print("\n\nIn file {}:".format(file_path))
        spellcheck_errors = spellcheck_file(file_path, dictionary)
        if not spellcheck_errors:
            print("No errors!")
        for word in spellcheck_errors:
            print("'{}' locations:".format(word))
            for location in spellcheck_errors[word]:
                print("   {}".format(location))



if __name__ == "__main__":

    import argparse
    import os

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--path",
        "-p",
        help="Path to the markdown file or directory with markdown files that should be spellchecked",
        type=str
    )

    parser.add_argument(
        "--dictionary",
        "-d",
        action="append",
        default=[],
        help="Path to custom dictionary. Flag can be used multiple times for multiple dictionary paths"
    )

    args = parser.parse_args()

    # if args.dictionary:
    # Combine the dictionaries
    dictionary = []
    for dict_path in args.dictionary:
        try:
            with open(dict_path) as f:
                dictionary += f.readlines()
        except Exception as e:
            print("Failed to open dictionary path '{}' skipping it. Exception:".format(dict_path))
            print(e)
    dictionary = [word.replace("\n", "") for word in dictionary]
    
    spellcheck_errors = spellcheck_path(args.path, dictionary)

    if spellcheck_errors:
        import sys
        sys.exit(-1)
