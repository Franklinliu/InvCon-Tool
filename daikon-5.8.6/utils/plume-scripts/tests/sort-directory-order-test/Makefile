test: clean lines1.output
	diff lines1.output-goal lines1.output

lines1.output: ../../sort-directory-order
	../../sort-directory-order lines1.txt > $@

clean:
	rm -f lines1.output
