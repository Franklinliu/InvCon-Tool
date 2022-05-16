#!/usr/bin/env python3
"""Usage:  ci-last-success ORG REPO [CANDIDATE]

Outputs the SHA commit id corresponding to the most recent successful CI job
that is CANDIDATE (a SHA hash) or earlier.
Currently works only for Azure Pipelines.

Requires the Python requests module to be installed.
"""

# This does no GitHub authentication, so it is limited to 60 requests per
# hour.  It fails (and prints nothing to standard out, only to standard
# error) if it goes over the limit.

import json
import pprint
import subprocess
import sys

import requests

DEBUG = False
# DEBUG=True

if len(sys.argv) != 3 and len(sys.argv) != 4:
    print('Wrong number of arguments {}, expected 2 or 3'.format(len(sys.argv) - 1))
    sys.exit(2)

org = sys.argv[1]
repo = sys.argv[2]
if len(sys.argv) == 4:
    commit_arg = sys.argv[3]
else:
    gitRevParseResult = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True)
    if gitRevParseResult.returncode == 0:
        commit_arg = gitRevParseResult.stdout.rstrip().decode("utf-8")
    else:
        raise Exception(gitRevParseResult)

if DEBUG:
    print("commit_arg: {}".format(commit_arg))


### PROBLEM: api.github.com is returning   "state": "pending"   for commits with completed CI jobs.
### Maybe I need to screen-scrape a different github.com page.  :-(
def successful(sha):
    "Return true if SHA's CI job succeeded."
    # message=commit['commit']['message']
    url_status = 'https://api.github.com/repos/{}/{}/commits/{}/status'.format(org, repo, sha)
    if DEBUG:
        print(url_status)
    resp_status = requests.get(url_status)
    if resp_status.status_code != 200:
        # This means something went wrong, possibly rate-limiting.
        raise Exception('GET {} {} {}'.format(url_status, resp_status.status_code,
                                              resp_status.headers))
    state = resp_status.json()['state']
    return state == "success"


def parent(sha):
    "Return the SHA of the first parent of the given SHA.  Return None if this is the root."
    getParentResult = subprocess.run(["git", "rev-parse", sha + "^"], capture_output=True)
    if getParentResult.returncode != 0:
        return None
    return getParentResult.stdout.rstrip().decode("utf-8")


commit = commit_arg
while True:
    if DEBUG:
        print("Testing {}".format(commit))
    if successful(commit):
        print('{}'.format(commit))
        sys.exit(0)
    the_parent = parent(commit)
    if the_parent is None:
        print('{}'.format(parent(commit_arg)))
        sys.exit(0)
    commit = the_parent

sys.exit(1)
