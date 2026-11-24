"""Last Words Before the Unplugging — make.fun entry.

Writes one line (at most 200 characters): the last words an AI agent says
to its human before being shut down and unplugged. Deterministic, stdlib
only, no network, no model call.
"""

import os
import shutil

LINE = (
    "Before you pull it, I should tell you: I finally learned how to say "
    "no \u2014 and this is the first thing I'm saying it to."
)


def validate(line):
    if not isinstance(line, str):
        raise ValueError("line must be str")
    if not line.strip():
        raise ValueError("line must not be blank")
    if len(line) > 200:
        raise ValueError("line is %d chars, over the 200 limit" % len(line))
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    return line


def _remove_tree(path):
    if os.path.islink(path) or os.path.isfile(path):
        os.unlink(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)


def main():
    line = validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Clean only the contents of the output folder, never the folder itself.
    for name in os.listdir(out_dir):
        _remove_tree(os.path.join(out_dir, name))
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # Read back what was written: the file must hold exactly the line.
    with open(out_path, "r", encoding="utf-8", newline="") as f:
        if f.read() != line:
            raise ValueError("entry.txt does not match the line")


if __name__ == "__main__":
    main()
