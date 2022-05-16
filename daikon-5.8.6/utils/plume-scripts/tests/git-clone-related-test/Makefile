test: test1 test2 test3 test4 test5 test6 test7 test8 test9 test10

# Here are the repositories and branches that exist.
# 
# Upstreams:
# plume-lib/git-clone-related-test-repo1
#  * branch-upstream-all
#  * branch-not-in-downstream-repo2
#  * branch-upstream-repo1
#  * branch-fallback
# plume-lib/git-clone-related-test-repo2
#  * branch-upstream-all
#  * branch-not-in-downstream-repo2
#  * branch-fallback
# plume-lib/git-clone-related-test-repo3
#  * branch-fallback
# 
# Forks:
# mernst/git-clone-related-test-repo1
#  * branch-downstream-all
#  * branch-not-in-downstream-repo2
#  * branch-downstream-repo1
#  * branch-fallback
# mernst/git-clone-related-test-repo2
#  * branch-downstream-all
#  * branch-fallback
# DOES NOT EXIST: mernst/git-clone-related-test-repo3
# 
# The tests run commands from clones of the two repo1 repositories,
# trying to create clones of the repo2 and repo3 repositories.

# Here are the situations that are tested:
#  * branch ${MYBRANCH} of https://github.com/${MYORG}/${REPO_NAME}.git
#    test1: mernst/repo1, branch-downstream-all => mernst/repo2, branch-downstream-all
#    test2: plume-lib/repo1, branch-upstream-all => plume-lib/repo2, branch-upstream-all
# 
#  * branch ${MYBRANCH} of https://github.com/${UPSTREAM_ORG}/${REPO_NAME}.git
#    test3: mernst/repo1, branch-not-in-downstream-repo2 => plume-lib/repo2, branch-not-in-downstream-repo2
#    test4: plume-lib/repo1, branch-not-in-downstream-repo2 => plume-lib/repo2, branch-not-in-downstream-repo2
#    test9: mernst/repo1, master => plume-lib/repo3, master
#    test10: mernst/repo1, branch-fallback => plume-lib/repo3, branch-fallback
# 
#  * branch ${FALLBACK_BRANCH} of https://github.com/${UPSTREAM_ORG}/${REPO_NAME}.git
#    test5: mernst/repo1, branch-downstream-repo1 => plume-lib/repo2, master
#    test6: plume-lib/repo1, branch-upstream-repo1 => plume-lib/repo2, master
# 
#  * branch ${FALLBACK_BRANCH} of https://github.com/${UPSTREAM_ORG}/${REPO_NAME}.git
#    test7: mernst/repo1, branch-downstream-repo1 => plume-lib/repo2, branch-fallback
#    test8: plume-lib/repo1, branch-upstream-repo1 => plume-lib/repo2, branch-fallback


# mernst/repo1, branch-downstream-all => mernst/repo2, branch-downstream-all
test1:
	./test-git-clone-related.sh https://github.com/mernst/git-clone-related-test-repo1 branch-downstream-all "plume-lib git-clone-related-test-repo2" https://github.com/mernst/git-clone-related-test-repo2.git branch-downstream-all

#   plume-lib/repo1, branch-upstream-all => plume-lib/repo2, branch-upstream-all
test2:
	./test-git-clone-related.sh https://github.com/plume-lib/git-clone-related-test-repo1 branch-upstream-all "plume-lib git-clone-related-test-repo2" https://github.com/plume-lib/git-clone-related-test-repo2.git branch-upstream-all

#   mernst/repo1, branch-not-in-downstream-repo2 => plume-lib/repo2, branch-not-in-downstream-repo2
test3:
	./test-git-clone-related.sh https://github.com/mernst/git-clone-related-test-repo1 branch-not-in-downstream-repo2 "plume-lib git-clone-related-test-repo2" https://github.com/plume-lib/git-clone-related-test-repo2.git branch-not-in-downstream-repo2

#   plume-lib/repo1, branch-not-in-downstream-repo2 => plume-lib/repo2, branch-not-in-downstream-repo2
test4:
	./test-git-clone-related.sh https://github.com/plume-lib/git-clone-related-test-repo1 branch-not-in-downstream-repo2 "plume-lib git-clone-related-test-repo2" https://github.com/plume-lib/git-clone-related-test-repo2.git branch-not-in-downstream-repo2

#   mernst/repo1, branch-downstream-repo1 => plume-lib/repo2, master
test5:
	./test-git-clone-related.sh https://github.com/mernst/git-clone-related-test-repo1 branch-downstream-repo1 "plume-lib git-clone-related-test-repo2" https://github.com/plume-lib/git-clone-related-test-repo2.git master

#   plume-lib/repo1, branch-upstream-repo1 => plume-lib/repo2, master
test6:
	./test-git-clone-related.sh https://github.com/plume-lib/git-clone-related-test-repo1 branch-upstream-repo1 "plume-lib git-clone-related-test-repo2" https://github.com/plume-lib/git-clone-related-test-repo2.git master

#   mernst/repo1, branch-downstream-repo1 => plume-lib/repo2, branch-fallback
test7:
	./test-git-clone-related.sh https://github.com/mernst/git-clone-related-test-repo1 branch-downstream-repo1 "--upstream-branch branch-fallback plume-lib git-clone-related-test-repo2" https://github.com/plume-lib/git-clone-related-test-repo2.git branch-fallback

#   plume-lib/repo1, branch-upstream-repo1 => plume-lib/repo2, branch-fallback
test8:
	./test-git-clone-related.sh https://github.com/plume-lib/git-clone-related-test-repo1 branch-upstream-repo1 "--upstream-branch branch-fallback plume-lib git-clone-related-test-repo2" https://github.com/plume-lib/git-clone-related-test-repo2.git branch-fallback

#   mernst/repo1, master => plume-lib/repo3, master
test9:
	./test-git-clone-related.sh https://github.com/mernst/git-clone-related-test-repo1 master "plume-lib git-clone-related-test-repo3" https://github.com/plume-lib/git-clone-related-test-repo3.git master

#  mernst/repo1, branch-fallback => plume-lib/repo3, branch-fallback
test10:
	./test-git-clone-related.sh https://github.com/mernst/git-clone-related-test-repo1 branch-fallback "plume-lib git-clone-related-test-repo3" https://github.com/plume-lib/git-clone-related-test-repo3.git branch-fallback


clean: 
# Nothing to do
