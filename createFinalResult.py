import json
import sys
import os
import re
import glob 

from argon2 import hash_password 

args = sys.argv[1:]
assert len(args) == 2, "workdir outputdir; two input must be provided."
workdir = args[0]
outputdir = args[1]

all_addressdirs = set()

MARK_LINE="==========================================================================="

BOOKSUMREGEX = re.compile('^orig\(this\..*\)\s==\ssum\(this\..*\[\]\.getValue\(\)\)')
BOOKSUMREGEX2 = re.compile('^this\..*\s==\ssum\(this\..*\[\]\.getValue\(\)\)')
TRANSFERREGEX = re.compile("^(\-)?((0\.9|1\.0)[0-9]+\s\*\s)*orig\(.*\)\s[+|-]\s\s*((0\.9|1\.0)[0-9]+\s\*\s)*this.*\[.*\]\.getValue\(\)\s[+|-]\s\s*((0\.9|1\.0)[0-9]+\s\*\s)*orig\(this.*\[.*\]\.getValue\(\)\)\s==\s0")
APPROVEREGEX = re.compile('^orig\(.*\)\s==\sthis\..*\[pair\(.*\)\]\.getSubValue\(\)')
TRANSFERFROMREGEX = re.compile('^-\s.*\s-\ssum\(.*\)\s+.*sum\(.*\).*==.*0')
booksum_set =  set()
transfer_set = set()
approve_set = set()
transferfrom_set = set()

if not os.path.exists(outputdir):
    os.makedirs(outputdir)

if not os.path.exists(f"{outputdir}/total"):
    os.makedirs(f"{outputdir}/total")

if not os.path.exists(f"{outputdir}/booksum"):
    os.makedirs(f"{outputdir}/booksum")

if not os.path.exists(f"{outputdir}/nobooksum"):
    os.makedirs(f"{outputdir}/nobooksum")

if not os.path.exists(f"{outputdir}/transferarithmatic"):
    os.makedirs(f"{outputdir}/transferarithmatic")

if not os.path.exists(f"{outputdir}/notransferarithmatic"):
    os.makedirs(f"{outputdir}/notransferarithmatic")

if not os.path.exists(f"{outputdir}/approveinvariant"):
    os.makedirs(f"{outputdir}/approveinvariant")

if not os.path.exists(f"{outputdir}/notapproveinvariant"):
    os.makedirs(f"{outputdir}/notapproveinvariant")

if not os.path.exists(f"{outputdir}/transferfrominvariant"):
    os.makedirs(f"{outputdir}/transferfrominvariant")

if not os.path.exists(f"{outputdir}/nottransferfrominvariant"):
    os.makedirs(f"{outputdir}/nottransferfrominvariant")


number1 = 0
number2 = 0
number3 = 0

for item in os.listdir(workdir):
    addressdir = os.path.join(workdir, item)
    if os.path.isdir(addressdir):
        hasInv = False
        for item_ in os.listdir(addressdir):
            if item_.endswith(".inv"):
                hasInv = True
                inv_file = os.path.join(addressdir, item_)
                with open(inv_file) as f:
                    lines = f.readlines()
                    all_content = "\n".join(lines)
                    if all_content.find(MARK_LINE)!=-1:
                        all_addressdirs.add(addressdir)
                        cmd = f"cp -rf {addressdir} {outputdir}/total"
                        os.system(cmd)
                        number1 += 1
                        hasBookSum = False
                        hasTransferArith = False
                        hasApprove = False
                        hasTransferFrom = False
                        for line in lines:
                            line = line.strip()
                            m1, m2 = BOOKSUMREGEX.match(line), BOOKSUMREGEX2.match(line)
                            if m1 is not None or m2 is not None:
                                hasBookSum = True 
                                booksum_set.add(addressdir)
                            m = TRANSFERREGEX.match(line)
                            if m:
                                hasTransferArith = True 
                                transfer_set.add(addressdir)
                            m = APPROVEREGEX.match(line)
                            if m:
                                hasApprove = True 
                                approve_set.add(addressdir)
                            m = TRANSFERFROMREGEX.match(line)
                            if m:
                                hasTransferFrom = True
                                transferfrom_set.add(addressdir)
                        if hasBookSum:
                            cmd = f"cp -rf {addressdir} {outputdir}/booksum"
                            os.system(cmd)
                        else:
                            cmd = f"cp -rf {addressdir} {outputdir}/nobooksum"
                            os.system(cmd)
                        if hasTransferArith:
                            cmd = f"cp -rf {addressdir} {outputdir}/transferarithmatic"
                            os.system(cmd)
                        else:
                            cmd = f"cp -rf {addressdir} {outputdir}/notransferarithmatic"
                            os.system(cmd)
                        
                        if hasApprove:
                            cmd = f"cp -rf {addressdir} {outputdir}/approveinvariant"
                            os.system(cmd)
                        else:
                            cmd = f"cp -rf {addressdir} {outputdir}/notapproveinvariant"
                            os.system(cmd)
                        
                          
                        if hasTransferFrom:
                            cmd = f"cp -rf {addressdir} {outputdir}/transferfrominvariant"
                            os.system(cmd)
                        else:
                            cmd = f"cp -rf {addressdir} {outputdir}/nottransferfrominvariant"
                            os.system(cmd)

                    else:
                        print("no such invariant content:", addressdir )
                        number2 += 1
        
        if not hasInv:
                print("no such invaraint file:", addressdir)
                number3 += 1

print(f"Summary for {workdir}:", number1+number2+number3)
print("no such invaraint file:", number3)
print("no such invariant content:", number2 )
print("include such invariant content:", number1 )


Limit  = 10 
# pick the contract with transaction larger than 20 
check_nonbooksum_contracts = set()
for addressdir in all_addressdirs.difference(booksum_set):
    tx_file = os.path.join(addressdir, "txs.json")
    txs = json.load(open(tx_file))
    if len(txs) > Limit:
        check_nonbooksum_contracts.add(addressdir)
check_nontransferarithmatic_contracts = set()
for addressdir in all_addressdirs.difference(transfer_set):
    tx_file = os.path.join(addressdir, "txs.json")
    txs = json.load(open(tx_file))
    inv_file = glob.glob(os.path.join(addressdir, "*.inv"))[0]
    with open(inv_file) as f:
        if "\n".join(f.readlines()).find("transfer") != -1:
            if len(txs) > Limit:
                check_nontransferarithmatic_contracts.add(addressdir)
check_nonapproveinvariant_contracts = set()
for addressdir in all_addressdirs.difference(approve_set):
    tx_file = os.path.join(addressdir, "txs.json")
    txs = json.load(open(tx_file))
    inv_file = glob.glob(os.path.join(addressdir, "*.inv"))[0]
    with open(inv_file) as f:
        if "\n".join(f.readlines()).find("approve") != -1:
            if len(txs) > Limit:
                check_nonapproveinvariant_contracts.add(addressdir)
check_nontransferfrominvariant_contracts = set()
for addressdir in all_addressdirs.difference(transferfrom_set):
    tx_file = os.path.join(addressdir, "txs.json")
    txs = json.load(open(tx_file))
    inv_file = glob.glob(os.path.join(addressdir, "*.inv"))[0]
    with open(inv_file) as f:
        if "\n".join(f.readlines()).find("transferFrom") != -1:
            if len(txs) > Limit:
                check_nontransferfrominvariant_contracts.add(addressdir)

print("Found book sum invariant:", len(booksum_set))
print("Found transfer arithmatic invariant:", len(transfer_set))
print("Found transferfrom invariant:", len(transferfrom_set))
print("Found approve invariant:", len(approve_set))

with open("audit.txt", "w") as f:
    f.write(f"For bookkeeping invariant, please check the following contracts having at least {Limit} transactions:\n")
    f.write("\n".join(check_nonbooksum_contracts))
    f.write("\n")
    f.write(f"For transfer invariant, please check the following contracts having at least {Limit} transactions:\n")
    f.write("\n".join(check_nontransferarithmatic_contracts))
    f.write("\n")
    f.write(f"For approve invariant, please check the following contracts having at least {Limit} transactions:\n")
    f.write("\n".join(check_nonapproveinvariant_contracts))
    f.write("\n")
    f.write(f"For transferfrom invariant, please check the following contracts having at least {Limit} transactions:\n")
    f.write("\n".join(check_nontransferfrominvariant_contracts))

