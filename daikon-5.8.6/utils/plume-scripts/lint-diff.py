#!/usr/bin/env python3
"""Filter warnings output, to only show output for changed lines."""

# Filter warnings output, to only show output for changed lines.
#
# This is useful when you want to enforce some style guideline, but
# making the changes globally in your project would be too burdensome.
# You can make the requirement only for new and changed lines, so your
# codebase will conform to the new standard gradually, as you edit it.

# Usage:  lint-diff.py [options] diff.txt [warnings.txt]
#         If warnings.txt is omitted, use standard input.
# Output: all lines in warnings.txt that are on a changed line.
#         Output status is 1 if it produced any output, 0 if not, 2 if error.
# Options: --guess-strip means guess values for --strip-diff and --strip-lint.
#          --strip-diff=N means to ignore N leading "/" in diff.txt.
#          --strip-warnings=N means to ignore N leading "/" in warnings.txt.
#              Affects matching, but not output, of lines.
#          --context=N is how many lines adjacent to the changed ones
#              are also considered changed; the default is 2.
#          --debug means to print diagnostic output.

# Here is how you could use this in continuous integration (Azure
# Pipelines, CircleCI, and Travis CI are currently supported) to require
# that pull requests satisfy the command `command-that-issues-warnings`:
#
#  if [ -d /tmp/$USER/plume-scripts ] ; then
#    git -C /tmp/$USER/plume-scripts pull -q > /dev/null 2>&1
#  else
#    mkdir -p /tmp/$USER \
#      && git -C /tmp/$USER clone --depth 1 -q https://github.com/plume-lib/plume-scripts.git
#  fi
# (command-that-issues-warnings > /tmp/warnings.txt 2>&1) || true
# /tmp/$USER/plume-scripts/ci-lint-diff /tmp/warnings.txt

# Implementation notes:
# 1. It may be possible to achieve a similar result using diff (but not `git diff`):
# https://unix.stackexchange.com/questions/34874/diff-output-line-numbers .
# 2. The documentation for diffFilter (https://github.com/exussum12/coverageChecker)
# suggests it has this same functionality, but my tests indicate it does not.

from __future__ import print_function

import argparse
import os
import re
import sys

PROGRAM = os.path.basename(__file__)

DEBUG = False

PLUSPLUSPLUS_RE = re.compile(r'\+\+\+ (\S*).*')

FILENAME_LINENO_RE = re.compile('([^:]*):([0-9]+):.*')


def eprint(*args, **kwargs):
    """Print to stderr."""
    print(*args, file=sys.stderr, **kwargs)


def strip_dirs(filename, num_dirs):
    """Strip off `num_dirs` leading "/" characters."""
    if num_dirs == 0:
        return filename
    return os.path.join(*(filename.split(os.path.sep)[num_dirs:]))


## Tests:
"""
import os
assert strip_dirs("/a/b/c/d", 0) == '/a/b/c/d'
assert strip_dirs("/a/b/c/d", 1) == 'a/b/c/d'
assert strip_dirs("/a/b/c/d", 2) == 'b/c/d'
assert strip_dirs("/a/b/c/d", 3) == 'c/d'
assert strip_dirs("/a/b/c/d", 4) == 'd'
assert strip_dirs("/a/b/c/", 0) == '/a/b/c/'
assert strip_dirs("/a/b/c/", 1) == 'a/b/c/'
assert strip_dirs("/a/b/c/", 2) == 'b/c/'
assert strip_dirs("/a/b/c/", 3) == 'c/'
assert strip_dirs("/a/b/c/", 4) == ''
"""


def min_strips(filename1, filename2):
    """Returns a 4-tuple of 2 integers and 2 strings.  The integers
indicate the smallest strip values that make the two filenames equal,
or a maximal pair if the files have different basenames.  The last two
elements of the tuple are the argument strings."""
    components1 = filename1.split(os.path.sep)
    components2 = filename2.split(os.path.sep)
    if components1[-1] != components2[-1]:
        ## TODO: is this special case necessary?
        return (1000, 1000, filename1, filename2)
    while components1 and components2 and components1[-1] == components2[-1]:
        del components1[-1]
        del components2[-1]
    return (len(components1), len(components2), filename1, filename2)


## Tests:
"""
import os
assert min_strips("/a/b/c/d", "/a/b/c/d") == (0, 0, "/a/b/c/d", "/a/b/c/d")
assert min_strips("e1/e2/a/b/c/d", "/a/b/c/d") == (2, 1, "e1/e2/a/b/c/d", "/a/b/c/d")
assert min_strips("/e1/e2/a/b/c/d", "/a/b/c/d") == (3, 1, "/e1/e2/a/b/c/d", "/a/b/c/d")
assert min_strips("e1/e2/a/b/c/d", "a/b/c/d") == (2, 0, "e1/e2/a/b/c/d", "a/b/c/d")
assert min_strips("/e1/e2/a/b/c/d", "a/b/c/d") == (3, 0, "/e1/e2/a/b/c/d", "a/b/c/d")
assert min_strips("/a/b/c/d", "/e/f/g/h") == (1000, 1000, "/a/b/c/d", "/e/f/g/h")
"""


def pair_min(pair1, pair2):
    """Given two pairs, returns the one that is pointwise lesser in its first two elements.
Fails if neither is lesser."""
    if pair1[0] <= pair2[0] and pair1[1] <= pair2[1]:
        return pair1
    if pair1[0] >= pair2[0] and pair1[1] >= pair2[1]:
        return pair2
    raise Exception("incomparable pairs: {} {}".format(pair1, pair2))


## Tests:
"""
import os
assert pair_min((3,4,"a","b"), (5,6,"c","d")) == (3,4,"a","b")
assert pair_min((4,3,"a","b"), (6,5,"c","d")) == (4,3,"a","b")
assert pair_min((30,40,"a","b"), (5,6,"c","d")) == (5,6,"c","d")
assert pair_min((40,30,"a","b"), (6,5,"c","d")) == (6,5,"c","d")
"""


def diff_filenames(diff_filename):
    """All the filenames in the given diff file."""
    result = set()
    with open(diff_filename, encoding='utf-8') as diff:
        for diff_line in diff:
            match = PLUSPLUSPLUS_RE.match(diff_line)
            if match:
                filename = match.group(1)
                if filename != "/dev/null":
                    result.add(filename)
    return result


def warning_filenames(warning_filename):
    """All the filenames in the given warning file."""
    result = set()
    with open(warning_filename, encoding='utf-8') as warnings:
        for warning_line in warnings:
            match = FILENAME_LINENO_RE.match(warning_line)
            if match:
                result.add(match.group(1))
    return result


def guess_strip_filenames(diff_filenames, warning_filenames):
    """Arguments are two lists of file names.
    Result is a pair of integers."""
    result = (1000, 1000, "no files seen yet", "no files seen yet")
    for diff_filename in diff_filenames:
        for warning_filename in warning_filenames:
            result = pair_min(result, min_strips(diff_filename, warning_filename))
    return result


def guess_strip_files(diff_file, warning_file):
    """Arguments are files produced by diff and a lint tool, respectively.
    Result is a pair of integers."""
    diff_files = diff_filenames(diff_file)
    warning_files = warning_filenames(warning_file)
    result = guess_strip_filenames(diff_files, warning_files)
    diff_prefix = os.path.commonprefix(list(diff_files))
    warnings_prefix = os.path.commonprefix(list(warning_files))
    if result[0] > diff_prefix.count("/") or result[1] > warnings_prefix.count("/"):
        # This is not necessarily a problem.  It is possible that all the
        # diffs, or all the lint output, happens to be in one subdirectory.
        if DEBUG:
            eprint("lint-diff.py: guess_strip_files all in one subdirectory: " +
                   "result={} diff_prefix={} warnings_prefix={}".format(
                       result, diff_prefix, warnings_prefix))
            eprint("diff_files={}".format(diff_files))
            eprint("warning_files={}".format(warning_files))
    return result


### Main routine


def parse_args():
    """Parse and return the command-line arguments."""
    global DEBUG

    parser = argparse.ArgumentParser(
        description="Filter warnings output, to only show output for changed lines")
    parser.add_argument('--guess-strip',
                        dest='guess_strip',
                        action='store_true',
                        default=False,
                        help="guess values for --strip-diff and --strip-warnings")
    parser.add_argument('--strip-diff',
                        metavar="NUM_SLASHES",
                        dest='strip_diff',
                        action='store',
                        type=int,
                        default=0,
                        help="ignore N leading \"/\" in filenames in diff.txt")
    parser.add_argument('--strip-warnings',
                        metavar="NUM_SLASHES",
                        dest='strip_warnings',
                        action='store',
                        type=int,
                        default=0,
                        help="ignore N leading \"/\" in filenames in warnings.txt")
    # Deprecated; exists for backwards compatibility
    parser.add_argument('--strip-lint',
                        metavar="NUM_SLASHES",
                        dest='strip_warnings',
                        action='store',
                        type=int,
                        default=0,
                        help="(DEPRECATED) ignore N leading \"/\" in filenames in warnings.txt")
    parser.add_argument('--context',
                        metavar="NUM_LINES",
                        dest='context_lines',
                        action='store',
                        type=int,
                        default=2,
                        help="how many lines around each changed one are also considered changed")
    parser.add_argument('--debug',
                        dest='DEBUG',
                        action='store_true',
                        help="print diagnostic output")
    parser.add_argument('diff_filename', metavar='diff.txt', default=os.getcwd())
    parser.add_argument('warning_filename', metavar='warnings.txt', default=None)

    args = parser.parse_args()
    DEBUG = args.DEBUG

    if args.guess_strip and args.strip_diff != 0:
        eprint(PROGRAM, ": don't supply both --guess-strip and --strip-diff")
        sys.exit(2)

    if args.guess_strip and args.strip_warnings != 0:
        eprint(PROGRAM, ": don't supply both --guess-strip and --strip-warnings")
        sys.exit(2)

    if args.guess_strip and args.warning_filename is None:
        eprint(PROGRAM, "needs \"warnings.txt\" file argument when --guess-strip is provided")
        sys.exit(2)

    if args.guess_strip:
        guessed_strip = guess_strip_files(args.diff_filename, args.warning_filename)
        if guessed_strip[0] == 1000:
            if DEBUG:
                eprint(
                    "lint-diff.py: --guess-strip failed to guess values (maybe no files in common?)"
                )
        else:
            args.strip_diff = guessed_strip[0]
            args.strip_warnings = guessed_strip[1]
            if DEBUG:
                eprint("lint-diff.py inferred --strip-diff={} --strip-warnings={}".format(
                    args.strip_diff, args.strip_warnings))

    # A filename if the diff filenames start with "a/" and "b/", otherwise None.
    # Is set by changed_lines().
    args.relative_diff = None

    return args


def changed_lines(args):
    """Returns a dictionary from file names to a set of ints (line numbers for changed lines)."""

    changed = {}

    with open(args.diff_filename, encoding='utf-8') as diff:
        atat_re = re.compile('@@ -([0-9]+)(,[0-9]+)? \+([0-9]+)(,[0-9]+)? @@.*')
        content_re = re.compile('[ +-].*')

        filename = ''
        lineno = -1000000
        for diff_line in diff:
            if diff_line.startswith("---"):
                continue
            match = PLUSPLUSPLUS_RE.match(diff_line)
            if match:
                if match.group(1).startswith("b/"):  # heuristic
                    args.relative_diff = diff_line
                try:
                    filename = strip_dirs(match.group(1), args.strip_diff)
                except TypeError:
                    filename = "diff filename above common directory"
                    ## It's not an error; it just means this file doesn't appear in warnings output.
                    # eprint('Bad --strip-diff={0} ; line has fewer "/": {1}'.format(
                    #   strip_diff, match.group(1)))
                    # sys.exit(2)
                if filename not in changed:
                    changed[filename] = set()
                continue
            match = atat_re.match(diff_line)
            if match:
                lineno = int(match.group(3))
                continue
            if diff_line.startswith("+"):
                # Not just the changed line: changed[filename].add(lineno)
                for changed_lineno in range(lineno - args.context_lines,
                                            lineno + args.context_lines + 1):
                    changed[filename].add(changed_lineno)
                lineno += 1
            if diff_line.startswith(" "):
                lineno += 1
            if diff_line.startswith("-"):
                for changed_lineno in range(lineno - args.context_lines,
                                            lineno + args.context_lines):
                    changed[filename].add(changed_lineno)
                continue

    return changed


def warn_relative_diff(args):
    """Possibly warn about relative directories."""

    result = False
    if args.relative_diff is not None and args.strip_diff == 0:
        # This is usually not an error, so don't warn.
        if DEBUG:
            eprint("warning:", args.diff_filename, "may use relative paths (e.g.,",
                   args.relative_diff.strip(), ") but --strip-diff=0",
                   ("(guessed)" if args.guess_strip else ""))
            eprint("warning: (Maybe there were no files in common.)")
        result = True
        if DEBUG:
            eprint("lint-diff.py: diff file {}:".format(args.diff_filename))
            with open(args.diff_filename, 'r', encoding='utf-8') as fin:
                eprint("{}", fin.read())
            eprint("lint-diff.py: lint file {}:".format(args.warning_filename))
            with open(args.warning_filename, 'r', encoding='utf-8') as fin:
                eprint("{}", fin.read())
            eprint("lint-diff.py: end of input files.")

    return result


def main():
    """The main routine"""

    global DEBUG

    args = parse_args()

    # A dictionary from file names to a set of ints (line numbers for changed lines)
    changed = changed_lines(args)

    if DEBUG:
        for filename in sorted(changed):
            print(filename, sorted(changed[filename]))

    # True if a warning has been issued about relative directories.
    relative_diff_warned = warn_relative_diff(args)

    if args.warning_filename is None:
        args.warning_filename = "stdin"
        warnings = sys.stdin
    else:
        warnings = open(args.warning_filename, encoding='utf-8')

    # 1 if this produced any output, 0 if not
    status = 0

    for warning_line in warnings:
        match = FILENAME_LINENO_RE.match(warning_line)
        if match:
            try:
                filename = strip_dirs(match.group(1), args.strip_warnings)
            except TypeError:
                filename = "warnings filename above common directory"
                ## It's not an error; it just means this file doesn't appear in warnings output.
                # eprint('Bad --strip-warnings={0} ; line has fewer "/": {1}'.format(
                #   strip_warnings, match.group(1)))
                # sys.exit(2)
            if filename.startswith(
                    "/") and args.relative_diff is not None and args.strip_warnings == 0:
                if not relative_diff_warned:
                    eprint("warning:", args.diff_filename, "uses relative paths but",
                           args.warning_filename, "uses absolute paths")
                    relative_diff_warned = True
            lineno = int(match.group(2))
            if (filename in changed and lineno in changed[filename]):
                print(warning_line, end='')
                status = 1

    if warnings is not sys.stdin:
        warnings.close

    sys.exit(status)


if __name__ == '__main__':
    main()
