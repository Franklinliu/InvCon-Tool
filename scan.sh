#!/bin/bash

# bookkeeping sum
# totalcontracts=$(ls ./Experiment/ERC20/ |wc -l)

# find ./Experiment/ERC20/ -type f -name "*.inv" -exec grep -H -E '^orig\(this\..*\)\s==\ssum\(this\..*\[\]\.getValue\(\)\)' {} \;
# echo "found bookkeeping invariants for "
# find ./Experiment/ERC20/ -type f -name "*.inv" -exec grep -l -E '^orig\(this\..*\)\s==\ssum\(this\..*\[\]\.getValue\(\)\)' {} \;|sort|uniq|wc -l
# echo "out of $totalcontracts contracts!!"
# echo "**************************"

# # transfer invariants
# find ./Experiment/ERC20/ -type f -name "*.inv" -exec grep -H -E "^(\-)?((0\.9|1\.0)[0-9]+\s\*\s)*orig\(.*\)\s[+|-]\s\s*((0\.9|1\.0)[0-9]+\s\*\s)*this.*\[.*\]\.getValue\(\)\s[+|-]\s\s*((0\.9|1\.0)[0-9]+\s\*\s)*orig\(this.*\[.*\]\.getValue\(\)\)\s==\s0" {} \;

# echo "found transfer invariants for "
# find ./Experiment/ERC20/ -type f -name "*.inv" -exec grep -l -E "^(\-)?((0\.9|1\.0)[0-9]+\s\*\s)*orig\(.*\)\s[+|-]\s\s*((0\.9|1\.0)[0-9]+\s\*\s)*this.*\[.*\]\.getValue\(\)\s[+|-]\s\s*((0\.9|1\.0)[0-9]+\s\*\s)*orig\(this.*\[.*\]\.getValue\(\)\)\s==\s0" {} \;|sort|uniq|wc -l
# echo "out of $totalcontracts contracts!!"
# echo "**************************"

# # approve invariants
# find ./Experiment/ERC20/ -type f -name "*.inv" -exec grep -H -E '^orig\(.*\)\s==\sthis\..*\[pair\(.*\)\]\.getSubValue\(\)' {} \;

# echo "found approve invariants for "
# find ./Experiment/ERC20/ -type f -name "*.inv" -exec grep -l -E '^orig\(.*\)\s==\sthis\..*\[pair\(.*\)\]\.getSubValue\(\)' {} \;|sort|uniq|wc -l
# echo "out of $totalcontracts contracts!!"
# echo "**************************"

# # transferFrom invariants
# find ./Experiment/ERC20/ -type f -name "*.inv" -exec grep -H -E '^-\s.*\s-\ssum\(.*\)\s+.*sum\(.*\).*==.*0' {} \;

# echo "found transferFrom invariants for "
# find ./Experiment/ERC20/ -type f -name "*.inv" -exec grep -H -E '^-\s.*\s-\ssum\(.*\)\s+.*sum\(.*\).*==.*0' {} \;|sort|uniq|wc -l
# echo "out of $totalcontracts contracts!!"
# echo "**************************"

python3 createFinalResult.py ./Experiment/ERC20/ ./Experiment/FinalReportERC20/