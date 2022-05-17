 
# print Daikon declaration
import os
import re
import copy 
import invcon.consts.Config as config

def print_head():
    return ['''// Declarations for Smart Contract Runtime Invariant Identification
// Declarations automatically written by Liu Ye 

decl-version 2.0
var-comparability implicit''']

Comparability_Enum= 4
Comparability_Int = 5
Comparability_Mapping= 6
Comparability_String = 7
Comparability_Address = 8
Comparability_Boolean = 9
Comparability_Others = 10

Comparability_Indice = 11

# Comparability_Index = 12

def _get_full_function_name(name, inputs):
    ret = name 
    argtyps = []
    for item in inputs:
        argtyps.append(item["type"])
    return name +"("+",".join(argtyps)+")"
# 
def _var_decl(varname, vartype, reptype, comparability, isArray=False, enclosing_var="None"):
    if isArray:
        return \
"""variable {0}[..]
    var-kind array
    array 1
    dec-type {1}[]
    rep-type {2}[]
    enclosing-var {5}
    flags is_param non_null is_readonly nomod
    comparability {3}[{4}]""".format(varname, vartype, reptype, comparability, Comparability_Indice, varname)
    else:
        return \
"""variable {0}
    var-kind variable
    dec-type {1}
    rep-type {2}
    flags is_param non_null is_readonly nomod
    comparability {3}""".format(varname, vartype, reptype, comparability)
# 
def _func_ENTER_HEAD(fullfuncname, contractName="Dicether.GameChannel"):
    
    return \
"""ppt {0}.{1}:::ENTER
ppt-type enter""".format(contractName, fullfuncname)

# 
def _func_EXIT1_HEAD(fullfuncname, contractName="Dicether.GameChannel"):
    
    return \
"""ppt {0}.{1}:::EXIT1
ppt-type subexit""".format(contractName, fullfuncname)
# 
def _func_EXIT2_HEAD(fullfuncname, contractName="Dicether.GameChannel"):
    
    return \
"""ppt {0}.{1}:::EXIT2
ppt-type subexit""".format(contractName, fullfuncname)

def getTyRepComp(_type):
            return   _type.replace(" ", "_"), \
                     "int" if _type.find("enum")!=-1 \
                else "hashcode" if _type.find("mapping")!=-1 \
                else "java.math.BigInteger" if _type.find("int")!=-1  \
                else "java.lang.String" if ( _type.find("address")!=-1 or _type.find("contract")!=-1 )\
                else "java.lang.String" if _type.find("string")!=-1 or _type.find("bytes")!=-1 \
                else "boolean" if _type.find("bool")!=-1 \
                else "hashcode", \
                Comparability_Enum if _type.find("enum")!=-1 \
                else Comparability_Mapping if _type.find("mapping")!=-1 \
                else Comparability_Int if _type.find("int")!=-1  \
                else Comparability_Address if ( _type.find("address")!=-1 or _type.find("contract")!=-1 )\
                else Comparability_String if _type.find("string")!=-1 or _type.find("bytes")!=-1 \
                else Comparability_Boolean if _type.find("bool")!=-1 \
                else Comparability_Others

def print_function_decl(contractStorageObject, function, contractName):
                #_print_function_decl(function)
                decls = contractStorageObject.getObjectRef(contractName)
                for item in function["inputs"]:
                    if not item["type"].find("[")!=-1:
                        vartype, reptype, comparability = getTyRepComp(item["type"])
                        varname = item["name"]
                        decls.append(_var_decl(varname, vartype, reptype, comparability))
                    else:
                        vartype, reptype, comparability = getTyRepComp(item["type"])
                        vartype = vartype.split("[")[0].strip()
                        varname = item["name"]
                        decls.append(_var_decl(varname, "hashcode", "hashcode", Comparability_Indice))
                        decls.append(_var_decl(varname, vartype, reptype, comparability, isArray=True))
                # 
                decls.append(_var_decl(varname="msg.sender", vartype="address", reptype="java.lang.String", comparability=Comparability_Address))
                decls.append(_var_decl(varname="msg.value", vartype="uint", reptype="java.math.BigInteger", comparability=Comparability_Int))
                decls.append(_var_decl(varname="block.timestamp", vartype="uint", reptype="java.math.BigInteger", comparability=Comparability_Int))
                
                fullfuncname = _get_full_function_name(function["name"], function["inputs"])
                enter = [_func_ENTER_HEAD(fullfuncname, contractName=contractName)]
                exit1 = [_func_EXIT1_HEAD(fullfuncname, contractName=contractName)]
                exit2 = [_func_EXIT2_HEAD(fullfuncname, contractName=contractName)]
                
                enter.extend(decls)
                enter.append("\n")
                exit1.extend(decls)
                exit1.append("\n")

                exit2.extend(decls)
                exit2.append("\n")

                # print("\n".join(enter))
                # print("\n".join(exit1))
                return enter, exit1, exit2

def getDecl(contractName, contractStorageObject, contractAbi=list()):

        g_decls = []    
        g_decls.extend(print_head())
        g_decls.extend(contractStorageObject.getObjectDecl(contractName))
        g_decls.append("\n")
        for function in contractAbi:
            if function["type"] == "function" and (function["stateMutability"] != "view"):
                # print(function)
              enter, exit1, exit2 = print_function_decl(contractStorageObject, function, contractName)
              g_decls.extend(enter)
              g_decls.extend(exit1)
              g_decls.extend(exit2)
        return g_decls


def getContractDtraces(contractName, contractStorageObject):
    dtrace = ["""this
{0}
1""".format(int("192794888",10))]
    dtrace.extend(contractStorageObject.getObjectDataTraces())
    # if Debug:
        # print("\n".join(dtrace))
    return dtrace


def inferLikelyInvaraints(data_trace_file, invariant_file):
    cmd = f"""export DAIKONDIR=/home/liuye/Projects/InvCon/daikon-5.8.6
java -cp $DAIKONDIR/daikon.jar daikon.Daikon --config_option daikon.inv.binary.sequenceScalar.SeqBigIntGreaterEqual.enabled=false --config_option daikon.inv.binary.sequenceScalar.SeqBigIntGreaterThan.enabled=false --config_option daikon.inv.binary.sequenceScalar.SeqBigIntLessEqual.enabled=false --config_option daikon.inv.binary.sequenceScalar.SeqBigIntLessThan.enabled=false --config_option daikon.inv.binary.twoScalar.BigIntGreaterEqual.enabled=false --config_option daikon.inv.binary.twoScalar.BigIntGreaterThan.enabled=true --config_option daikon.inv.binary.twoScalar.BigIntLessEqual.enabled=true --config_option daikon.inv.binary.twoScalar.BigIntNonEqual.enabled=false --config_option daikon.inv.binary.twoScalar.BigIntEqual.enabled=true --config_option daikon.inv.binary.twoScalar.BigIntLessThan.enabled=true --config_option daikon.inv.binary.twoScalar.LinearBinaryBigInt.enabled=false --config_option daikon.derive.unary.SequenceSum.enabled=true  --config_option daikon.derive.ternary.InvConUserBookkeeping.enabled=true  --config_option daikon.derive.senary.InvConUserBookkeeping2.enabled=true --config_option daikon.VarInfo.declared_type_comparability=false --config_option daikon.PptRelation.enable_object_user=false --config_option daikon.PptTopLevel.pairwise_implications=false  --config_option  daikon.Debug.logDetail=true  --config_option daikon.Daikon.undo_opts=false --config_option daikon.PptSliceEquality.set_per_var=false --config_option daikon.DynamicConstants.use_dynamic_constant_optimization=true --config_option daikon.inv.filter.ParentFilter.enabled=true --config_option daikon.inv.filter.DerivedParameterFilter.enabled=false --config_option daikon.inv.filter.ObviousFilter.enabled=true --config_option daikon.inv.filter.UnmodifiedVariableEqualityFilter.enabled=true --config_option daikon.inv.filter.UnjustifiedFilter.enabled=true --config_option daikon.inv.filter.ReadonlyPrestateFilter.enabled=false   --config_option daikon.inv.binary.twoString.StringLessEqual.enabled=false  --config_option daikon.inv.binary.twoString.StringGreaterEqual.enabled=false  --config_option daikon.inv.binary.twoString.StringLessThan.enabled=false  --config_option daikon.inv.binary.twoString.StringGreaterThan.enabled=false --config_option daikon.inv.binary.twoScalar.NumericBigInt.Divides.enabled=false --config_option daikon.inv.binary.sequenceScalar.MemberBigInt.enabled=false --config_option daikon.inv.binary.sequenceString.MemberString.enabled=false --config_option daikon.inv.unary.scalar.OneOfBigInt.enabled=true --config_option daikon.inv.unary.sequence.EltOneOfBigInt.enabled=false --config_option daikon.inv.unary.stringsequence.EltOneOfString.enabled=false  --config_option daikon.inv.unary.stringsequence.OneOfStringSequence.enabled=false --config_option daikon.inv.unary.sequence.OneOfSequence.enabled=false  --config_option daikon.inv.unary.sequence.OneOfBigIntSequence.enabled=false    --config_option daikon.inv.unary.string.OneOfString.enabled=false   --config_option daikon.derive.unary.SequenceLength.enabled=false --config_option daikon.derive.unary.StringLength.enabled=false    {data_trace_file} -o  {invariant_file}.gz > {invariant_file} """
    status = os.system(cmd)
    print(status)
    print(f"finished!\n please check invariant file: {invariant_file}")

def isPredicate(inv):
    if  not (inv.find(" < ")!=-1 or \
            inv.find(" <= ")!=-1 or \
            inv.find(" > ")!=-1 or \
            inv.find(" >= ")!=-1 or \
            inv.find(" == ")!=-1):
            return False
    symbol = None 
    if inv.find(" < ")!=-1:
        symbol = " < "
    elif inv.find(" <= ")!=-1:
        symbol = " <= "
    elif inv.find(" >= ")!=-1:
        symbol = " >= "
    elif inv.find(" > ")!=-1:
        symbol = " > "
    elif inv.find(" == ")!=-1:
        symbol = " == "
    if symbol is None:
        return False
    try:
        left, right = inv.split(symbol)
        left = left.strip()
        right = right.strip() 
    except:
        print(inv)
        return False
    if symbol!="==" and re.match(r'^orig\(.*\)$', left) is not None and \
        (re.match(r'^orig\(.*\)$', right) is not None ):
        hasParameter = (re.match(r'^orig\(this\..*\)$', left) is None) or (re.match(r'orig\(this\..*\)', right) is None)
        if hasParameter:
            return True
        else:
            return False
    else:
        if re.match(r'^orig\(.*\)$', left) is not None and re.match(r'.*orig\(this\..*\).*', left) is None and (right.isdigit() or re.match(r'^\'.*\'$', right) is not None):
            return True 
        else:
            return False

def isUpdateFunction(inv):
    if inv.find("==") == -1:
        return False 
    if not isPredicate(inv):
        left, right = inv.split("==")
        left = left.strip()
        right = right.strip()
        if not right.isdigit() and not (right == "false" or right == "true") :
            if f"orig({left})" ==  right and left.find("this.")!=-1:
                return True
        else:
            # TODO 
            z = re.match(r'.*orig\((this\.\w+\[.*\]).*', left)
            if z is not None:
                # print(z, z.groups())
                object_var = z.groups()[0]
                # print(object_var)
                if object_var.find("post")!=-1 and left.find(object_var.replace("post", "orig"))!=-1:
                    return True
            else:
                if right.isdigit() or right == "false" or right == "true":
                    if re.match(r'^this\..*', left) is not None:
                        return True 
            return False 
    return False 

def isProperty(inv):
    if inv.find("==") == -1:
        return False 
    if not isUpdateFunction(inv) and not isPredicate(inv):
        left, right = inv.split("==")
        left = left.strip()
        right = right.strip()
        if not right.isdigit():
            if f"orig({left})" ==  right:
                return False 
        return True 
    return False

def filterOutInterestingInvariants(invariant_files, contractInvariants):
    all_file_invariants = dict()
    for inv_file in invariant_files:
        lines = open(inv_file).read().split("===========================================================================")[1].strip().split("Exiting Daikon.")[0].splitlines()
        func_head = lines[0].strip()
        if func_head not in all_file_invariants:
            all_file_invariants[func_head] = dict()
        # lines = filter(lambda line:  line.find("block.timestamp")==-1 and line.find("msg.value")==-1 and line.find("null")==-1 and isPredicate(line), lines[1:])
        # lines = lines[1:]
        lines = list(filter(lambda line:  line.find("block.timestamp")==-1 and line.find("null")==-1, lines[1:]))
        invs =set(lines).difference(contractInvariants[func_head])
        all_file_invariants[func_head][inv_file] = invs 

    file_intersting_invariants = dict()
    for func_head in all_file_invariants.keys():
        file_invariants = all_file_invariants[func_head]
        file_intersting_invariants[func_head] = list()
        invariant_files = list(file_invariants.keys())
        for i in range(len(invariant_files)):
            invs  = set(copy.deepcopy(file_invariants[invariant_files[i]]))
            common_invs = invs
            for j in range(len(invariant_files)):
                if i!=j:
                    # common_invs = common_invs.intersection(file_invariants[invariant_files[j]])
                    invs.difference_update(file_invariants[invariant_files[j]])
            # file_intersting_invariants[invariant_files[i]] =  invs 
            eq_inv = None 
            if config.DEBUG:
                print(invariant_files[i])
            if invariant_files[i].find("eq_") != -1:
                eq_inv = ""+invariant_files[i].split("eq_")[1].split(".inv")[0].strip()+" == user"
            updateInvs = list(filter(lambda line: isUpdateFunction(line), invs))
            predicateInvs = list(filter(lambda line: isPredicate(line), invs))
            propertyInvs = list(filter(lambda line: isProperty(line), invs))
            if eq_inv:
                predicateInvs.append(eq_inv)
            if config.DEBUG:
                print(func_head)
                print("")
                print(updateInvs)
                print("")
                print(predicateInvs)
                print("")
                print(propertyInvs)
                print("")
            file_intersting_invariants[func_head].append([updateInvs, predicateInvs, propertyInvs])
    # print(file_intersting_invariants)
    return file_intersting_invariants


def filterOutERC20Invariants(invariant_files):
    file_invariants = dict()
    for inv_file in invariant_files:
        file_invariants[inv_file] = dict()
        func_invs = open(inv_file).read().split("Exiting Daikon.")[0].split("===========================================================================")[1:]
        for func_inv in func_invs:
            func_inv = func_inv.strip()
            func_head = func_inv.splitlines()[0].strip()
            lines = list(filter(lambda line: line.find("block.timestamp")==-1 and line.find("null")==-1, func_inv.splitlines()[1:]))
            updateInvs = list(filter(lambda line: isUpdateFunction(line), lines))
            predicateInvs = list(filter(lambda line: isPredicate(line), lines))
            propertyInvs = list(filter(lambda line: isProperty(line), lines))
            file_invariants[inv_file][func_head] = list(lines)
            if True or config.DEBUG:
                print(func_head)
                print("")
                print(updateInvs)
                print("")
                print(predicateInvs)
                print("")
                print(propertyInvs)
                print("")

    return file_invariants