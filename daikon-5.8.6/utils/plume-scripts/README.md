# Plume-Scripts:  Scripts for programming and system administration #

These scripts automate various programming as sysadmin tasks.

To install, run the following (or put it at the top of a script).
Then, the scripts are available at `/tmp/$USER/plume-scripts`.

```
if [ -d /tmp/$USER/plume-scripts ] ; then
  git -C /tmp/$USER/plume-scripts pull -q > /dev/null 2>&1
else
  mkdir -p /tmp/$USER && git -C /tmp/$USER clone --depth 1 -q https://github.com/plume-lib/plume-scripts.git
fi
```

For versions of git before 1.8.5 that do not support the `-C` command-line argument, use:

```
if [ -d /tmp/$USER/plume-scripts ] ; then
  (cd /tmp/$USER/plume-scripts && git pull -q) > /dev/null 2>&1
else
  mkdir -p /tmp/$USER && (cd /tmp && git clone --depth 1 -q https://github.com/plume-lib/plume-scripts.git)
fi
```

If you want to use a specific version of `plume-scripts` rather than the
bleeding-edge HEAD, you can do `git checkout _SHA_` after the `git clone`
command.


## classfile_check_version

Check that a class file's version is &leq; the specified version.
This ensures that the class will run on a particular version of Java.
Documentation [at top of file](classfile_check_version).


## cronic

A wrapper for cron jobs so that cron only sends
email when an error has occurred.
Documentation [at top of file](cronic) and at http://habilis.net/cronic/.


## Continuous integration utilities

### ci-info

Obtains information about a CI (continuous integration) job, such as the
organization, the branch, the range of commits, and whether it is a pull
request.  Works for Azure Pipelines, CircleCI, and Travis CI.
[Documentation](ci-info) at top of file.

### ci-lint-diff

Given a file of warnings (such as those output by `lint` or other tools),
reports only those that are in the diff for the current pull request.  Works for
Azure Pipelines, CircleCI, and Travis CI.  [Documentation](ci-lint-diff) at top
of file.

### ci-last-success.py

Prints the SHA commit id corresponding to the most recent successful CI job.
[Documentation](ci-last-success.py) at top of file.


## Cygwin utilities

### cygwin-runner

Takes a command with arguments and translates those arguments from
Cygwin-style filenames into Windows-style filenames.  Its real advantage
is the little bit of intelligence it has as far as which things are files
and which are not.
[Documentation](cygwin-runner) at top of file.

### java-cygwin

A wrapper for calling Java from Cygwin, that tries to convert any
arguments that are Unix-style paths into Windows-style paths.
[Documentation](java-cygwin) at top of file.

### javac-cygwin

A wrapper for calling the Java compiler from Cygwin, that tries to convert any
arguments that are Unix-style paths into Windows-style paths.
[Documentation](javac-cygwin) at top of file.

### javadoc-cygwin

A wrapper for calling Javadoc from Cygwin, that tries to convert any
arguments that are Unix-style paths into Windows-style paths.
[Documentation](javadoc-cygwin) at top of file.


## Git utilities

### ediff-merge-script

A script for use as a git mergetool; runs Emacs ediff as the mergetool.
[Documentation](ediff-merge-script) at top of file.

### git-authors

Lists all the authors of commits in a get repository.
[Documentation](git-authors) at top of file.

### git-clone-related

Clones a repository related to the one where this script is called, trying
to match the fork and branch.
[Documentation](git-clone-related) at top of file.

Suppose you have two related Git repositories:\
  *MY-ORG*`/`*MY-REPO*\
  *MY-ORG*`/`*MY-OTHER-REPO*

In a CI job that is testing branch BR in fork F of *MY-REPO*,
you would like to use fork F of *MY-OTHER-REPO* if it exists,
and you would like to use branch BR if it exists.
Here is how to accomplish that:

```
  if [ -d "/tmp/$USER/plume-scripts" ] ; then
    git -C /tmp/$USER/plume-scripts pull -q > /dev/null 2>&1
  else
    mkdir -p /tmp/$USER && git -C /tmp/$USER clone --depth 1 -q https://github.com/plume-lib/plume-scripts.git
  fi
  /tmp/$USER/plume-scripts/git-clone-related codespecs fjalar
```

### git-find-fork

Finds a fork of a GitHub repository, or returns the upstream repository
if the fork does not exist.
[Documentation](git-find-fork) at top of file.

### git-find-branch

Tests whether a branch exists in a Git repository;
prints the branch, or prints "master" if the branch does not exist.
[Documentation](git-find-branch) at top of file.


## latex-process-inputs

Determines all files that are recursively `\input` by a given
LaTeX file.
[Documentation](latex-process-inputs) at top of file.
The program has two modes:

 * Inline mode (the default):  Create a single LaTeX file for the document,
   by inlining `\input` commands and removing comments.
   The result is appropriate to be sent to a publisher.
 * List mode: List all the files that are (transitively) `\input`.
   This can be useful for getting a list of source files in a logical order,
   for example to be used in a Makefile or Ant buildfile.


## lint-diff.py

Filter the ouput of tools such as `lint`, to only show output for changed
lines in a diff or pull request.
[Documentation](lint-diff.py) at top of file.


## mail-e

Reads standard input, and if not empty calls the `mail` program on it.
In other words, acts like `mail -e` and isuseful when your version of `mail` does not support `-e`.
This feature is useful in scripts and cron jobs, but is not supported
in all versions of `mail`.
[Documentation](mail-e)
at top of file.


## path-remove

Cleans up a path environment variable by removing duplicates and
non-existent directories.
Can optionally remove certain path elements.
Works for either space- or colon- delimiated paths.
[Documentation](path-remove) at top of file.


## Search and replace

### preplace

Replace all matching regular expressions in the given files (or all files
under the current directory).  The timestamp on each file is updated only
if the replacement is performed.
[Documentation](preplace) at top of file.


### search

Jeffrey Friedl's search program combines `find` and `grep`
-- more or less do a 'grep' on a whole directory tree, but is more
efficient, uses Perl regular expressions, and is much more powerful.
This version fixes a tiny bug or two.  For full documentation, see its
[manpage](search.manpage).

This program has been largely superseded by
[`rg`](https://github.com/BurntSushi/ripgrep), and before that by
[`pt`](https://github.com/monochromegane/the_platinum_searcher) and
[`ag`](http://geoff.greer.fm/ag/).  However, it is still useful because it
searches more thoroughly:  in git-ignored files, and in compressed
archives.


## sort-directory-order

Sorts the input lines by directory order:  first, every file in a given
directory, in sorted order; then, process subdirectories recursively, in
sorted order. This is useful for users (e.g., when printing) and for making
output deterministic.
[Documentation](sort-directory-order) at top of file.
