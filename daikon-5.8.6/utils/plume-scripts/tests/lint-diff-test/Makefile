test: clean test-words test-reldir test-guessstrip


# "words" test

test-words: words2-lint-pruned.txt-goal-nofilename words2-lint-pruned.txt-nofilename
	diff $^

# words1.txt and words2.txt are subsets of words.txt.
words1.txt: words.txt
	grep -v 'a.*e.*t' $< > $@

words2.txt: words.txt
	grep -v 'a.*a.*e' $< > $@

# Suppose that the edit goes from words1.txt to words2.txt.
words12-diff.txt: words1.txt words2.txt
	diff -u $^ > $@ || true

words-lint.txt: words.txt
	grep -Hn 'a.*i' $< > $@ || true

# Suppose that there are warnings on files with "a.*i".
words2-lint.txt: words2.txt
	grep -Hn 'a.*i' $< > $@ || true

words2-lint-pruned.txt: words12-diff.txt words2-lint.txt
	../../lint-diff.py --context=0 $^ > $@ || true

# The goal is lines from words-lint.txt that are in words2.txt but not words1.txt.
# perl command removes lines that match both a.*e.*t and a.*a.*e .
words2-lint-pruned.txt-goal: words-lint.txt
	grep ':.*a.*e.*t' $< | perl -ni -e 'print unless /a.*e.*t/ && /a.*a.*e/' > $@ || true

%-nofilename: %
	sed 's/^[-A-Za-z0-9.]\{1,\}:[0-9]\{1,\}://' $< > $@


# "reldir" test

test-reldir: reldir-lint-pruned.txt-goal reldir-lint-pruned.txt
	diff $^

reldir-lint-pruned.txt: reldir-diff.txt reldir-lint.txt
	../../lint-diff.py --strip-diff=1 --strip-lint=2 --context=0 $^ > $@ || true


# "guessstrip" test

test-guessstrip: guessstrip-lint-pruned.txt-goal guessstrip-lint-pruned.txt
	diff $^

guessstrip-lint-pruned.txt: guessstrip-diff.txt guessstrip-lint.txt
	../../lint-diff.py  --guess-strip $^ > $@ || true


# Miscellaneous targets

# It would be nicer to put all generated files in a subdirectory.
clean:
	rm -f words1.txt words2.txt words12-diff.txt words-lint.txt words2-lint.txt words2-lint-pruned.txt words2-lint-pruned.txt-goal words2-lint.txt-goal-pruned words2-lint.txt-pruned words2-lint-pruned.txt-goal-nofilename words2-lint-pruned.txt-nofilename reldir-lint-pruned.txt guessstrip-lint-pruned.txt

