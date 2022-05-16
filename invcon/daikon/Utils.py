inv_text = """
Daikon version 5.8.6, released December 2, 2020; http://plse.cs.washington.edu/daikon.
Processing trace data; reading 1 dtrace file:                                  
[2022-03-14T12:31:05.446810]:                                                  Warning: Daikon is using a dataflow hierarchy analysis on a data trace that does not appear to be over a program execution, consider running Daikon with the --nohierarchy flag.
[2022-03-14T12:31:06.044068]: Finished reading daikon.full.dtraces.txt         
===========================================================================    
ETF.transfer(address,uint256):::EXIT1
this._balances == orig(this._balances)
this._allowances == orig(this._allowances)
this._allowances[].getSubLength() == orig(this._allowances[].getSubLength())
this._totalSupply == orig(this._totalSupply)
this._totalSupply == sum(this._balances[].getValue())
this._totalSupply == sum(orig(this._balances[].getValue()))
this.owner == orig(this.owner)
this._paused == orig(this._paused)
orig(this._totalSupply) == sum(this._balances[].getValue())
orig(this._totalSupply) == sum(orig(this._balances[].getValue()))
orig(msg.value) == sum(this._allowances[].getSubValue())
sum(this._balances[].getValue()) == sum(orig(this._balances[].getValue()))
sum(this._allowances[].getSubLength()) == sum(orig(this._allowances[].getSubLength()))
this._balances == null
this._balances[].getValue() elements >= 0
this._allowances has only one value
this._allowances[] == []
this._allowances[].getSubLength() == []
this._allowances[].getSubValue() == []
this._totalSupply == 100000000000000000000000000000
this.owner == "0x077242b55e308acb3384e3c8a7481d76cd38bf65"
this._paused == false
orig(this) has only one value
orig(this) != null
orig(this._balances[].getValue()) elements >= 0
orig(this._totalSupply) == 100000000000000000000000000000
orig(msg.value) == 0
sum(this._balances[].getValue()) == 100000000000000000000000000000
sum(this._allowances[].getSubLength()) == 0
sum(this._allowances[].getSubValue()) == 0
sum(orig(this._balances[].getValue())) == 100000000000000000000000000000
this._balances[orig(msg.sender)].getValue() >= 0
this.owner in this._balances[]
orig(msg.sender) in this._balances[]
this._balances[this.owner].getValue() in this._balances[].getValue()
this._balances[orig(to)].getValue() in this._balances[].getValue()
this._balances[orig(msg.sender)].getValue() in this._balances[].getValue()
this.owner in orig(this._balances[])
this.owner != orig(to)
orig(msg.sender) in orig(this._balances[])
orig(this._balances[post(this.owner)].getValue()) in orig(this._balances[].getValue())
orig(this._balances[post(to)].getValue()) in orig(this._balances[].getValue())
orig(this._balances[post(msg.sender)].getValue()) in orig(this._balances[].getValue())
orig(to) != orig(msg.sender)
size(this._balances[]) >= orig(size(this._balances[]))
size(this._balances[])-1 > size(this._allowances[])
size(this._balances[])-1 <= orig(size(this._balances[]))
size(this._balances[])-1 >= orig(size(this._balances[]))-1
size(this._allowances[]) <= orig(size(this._balances[]))-1
- 1.000153005502073 * this._totalSupply + 9.502423117895064E15 * orig(block.timestamp) + this._balances[this.owner].getValue() == 0
- 1.000153005502073 * orig(this._totalSupply) + 9.502423117895064E15 * orig(block.timestamp) + this._balances[this.owner].getValue() == 0
orig(value) - this._balances[orig(to)].getValue() + orig(this._balances[post(to)].getValue()) == 0
orig(value) + this._balances[orig(msg.sender)].getValue() - orig(this._balances[post(msg.sender)].getValue()) == 0
600001999 * this._balances[this.owner].getValue() + 399798001 * this._balances[orig(msg.sender)].getValue() - 1.9995900019999998E12 * orig(this._balances[post(this.owner)].getValue()) + 1.9985902020009997E41 == 0
Exiting Daikon.
"""

def NONEQUAL(a, b):
    return f"{a} != {b}"
def EQUAL(a, b):
    return f"{a} == {b}"
def LESS(a, b):
    return f"{a} < {b}"
def GREATER(a, b):
    return f"{a} > {b}"
def GREATEREQUAL(a, b):
    return f"{a} >= {b}"
def LESSEQUAL(a, b):
    return f"{a} <= {b}"
def MEMBERIN(a, b):
    return f"{a} in {b}"

def invariant_parse(inv_text_line):
    inv =  inv_text_line.replace(".getValue()", "").replace(".getSubValue()", "")
    if inv.find("==")!=-1:
        left, right = tuple(inv.split("=="))
        return (EQUAL, left.strip(), right.strip())
    elif inv.find("!=")!=-1:
        left, right = tuple(inv.split("!="))
        return (NONEQUAL, left.strip(), right.strip())
    elif inv.find("<")!=-1:
        left, right = tuple(inv.split("<"))
        return (LESS, left.strip(), right.strip())
    elif inv.find(">")!=-1:
        left, right = tuple(inv.split(">"))
        return (GREATER, left.strip(), right.strip())
    elif inv.find(">=")!=-1:
        left, right = tuple(inv.split(">="))
        return (GREATEREQUAL, left.strip(), right.strip())
    elif inv.find("<=")!=-1:
        left, right = tuple(inv.split("<="))
        return (LESSEQUAL, left.strip(), right.strip())
    elif inv.find(" in ")!=-1:
        left, right = tuple(inv.split(" in "))
        return (MEMBERIN, left.strip(), right.strip())

def genDaikonDataTrace():
    pass 

def runDaikon(datatrace_file, invariant_parser_func):
    pass 


def workflow():
    datatrace_file = genDaikonDataTrace()
    invariants = runDaikon(datatrace_file=datatrace_file, invariant_parser_func=invariant_parse)

def main():
    lines = inv_text.split("===========================================================================")[1].strip().split("Exiting Daikon.")[0].splitlines()
    # print(lines)
    all_invariants = dict()
    for line in lines:
        if line.find("::EXIT")!=-1:
            func_exitX = line 
        else:
            invariant = invariant_parse(line)
            if func_exitX not in all_invariants.keys():
                all_invariants[func_exitX] = list()
            all_invariants[func_exitX].append(invariant)
    print(all_invariants)

if __name__ == "__main__":
    main()