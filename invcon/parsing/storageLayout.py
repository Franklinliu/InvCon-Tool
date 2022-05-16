from base64 import encode
from cProfile import label
import json
import subprocess
from slither import Slither
from slither.core.solidity_types.mapping_type import MappingType
from slither.core.solidity_types.user_defined_type import UserDefinedType
from slither.core.declarations.structure import Structure
from slither.core.declarations.enum_contract import EnumContract
from slither.core.declarations.structure_contract import StructureContract
from slither.core.variables.structure_variable import StructureVariable
import sys
import math 
import re 


def installSolc(solcVersion):
    subprocess.run(["solc-select","install", solcVersion])
    subprocess.run(["solc-select","use", solcVersion])

dynamicArrayRegex = re.compile(r"(\w+)\[\]")
fixedArrayRegex = re.compile(r"(\w+)\[([0-9]+)\]")
def compute_type_info(vartype, _type_info, contract):
    type_ = str(vartype)
    if type_ == "bool":
        _type_info[contract.name][type_]  = dict(encoding="inplace", label="bool", numberOfBytes =str(vartype.storage_size[0])) 
    elif type_ == "uint256":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="uint256", numberOfBytes = str(vartype.storage_size[0]))
    elif type_ == "uint128":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="uint128", numberOfBytes = str(vartype.storage_size[0]))
    elif type_ == "uint64":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="uint64", numberOfBytes = str(vartype.storage_size[0]))
    elif type_ == "uint32":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="uint32", numberOfBytes =str(vartype.storage_size[0]))
    elif type_ == "uint16":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="uint16", numberOfBytes = str(vartype.storage_size[0]))
    elif type_ == "uint8":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="uint8", numberOfBytes = str(vartype.storage_size[0]))
    elif type_ == "int256":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="int256", numberOfBytes = str(vartype.storage_size[0]))
    elif type_ == "int128":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="int128", numberOfBytes = str(vartype.storage_size[0]))
    elif type_ == "int64":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="int64", numberOfBytes = str(vartype.storage_size[0]))
    elif type_ == "int32":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="int32", numberOfBytes = str(vartype.storage_size[0]))
    elif type_ == "int16":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="int16", numberOfBytes = str(vartype.storage_size[0]))
    elif type_ == "int8":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="int8", numberOfBytes =str(vartype.storage_size[0]))
    elif type_ == "address":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="address", numberOfBytes = str(vartype.storage_size[0]))
    elif type_ == "bytes":
        _type_info[contract.name][type_]  =  dict(encoding="bytes", label="bytes", numberOfBytes = str(vartype.storage_size[0]))
    elif type_ == "string":
        _type_info[contract.name][type_]  =  dict(encoding="bytes", label="string", numberOfBytes = str(vartype.storage_size[0]))
    elif type_ == "bytes32":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="bytes32", numberOfBytes = str(vartype.storage_size[0]))
    elif type_ == "bytes16":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="bytes16", numberOfBytes = str(vartype.storage_size[0]))
    elif type_ == "bytes1":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="bytes1", numberOfBytes = str(vartype.storage_size[0]))
    elif type_ == "enum":
        _type_info[contract.name][type_]  =  dict(encoding="inplace", label="enum", numberOfBytes = str(vartype.storage_size[0]))
    elif fixedArrayRegex.match(type_):
        m = fixedArrayRegex.match(type_)
        base = m.groups()[0]
        size = m.groups()[1]
        info = compute_type_info(base)
        if info["encoding"] == "inplace":
            _type_info[contract.name][type_]  =  dict(base = base, encoding= "inplace", label=type_, numberOfBytes=str(vartype.storage_size[0]))
        else:
            _type_info[contract.name][type_]  =  dict(base = base, encoding= "inplace", label=type_, numberOfBytes=str(vartype.storage_size[0]))
    elif dynamicArrayRegex.match(type_):
        m = dynamicArrayRegex.match(type_)
        base = m.groups()[0]
        _type_info[contract.name][type_]  =  dict(base = base, encoding= "dynamic_array", label=type_, numberOfBytes=str(vartype.storage_size[0]))
        compute_type_info(base.type, _type_info, contract)
    elif isinstance(vartype, MappingType):
        type_from = vartype.type_from
        type_to = vartype.type_to
        _type_info[contract.name][type_] =  dict(encoding="mapping", key=str(type_from), label=type_, numberOfBytes="32", value=str(type_to))
        compute_type_info(type_from, _type_info, contract)
        compute_type_info(type_to, _type_info, contract)
    elif isinstance(vartype, UserDefinedType): 
            # and isinstance(var.type.type, EnumContract):
            # print(type(vartype.type))
            if isinstance(vartype.type, EnumContract):
                _type_info[type_] =  dict(encoding="inplace", label="enum_"+type_, numberOfBytes=str(vartype.storage_size[0]))  
            elif isinstance(vartype.type, StructureContract):
                structure = vartype.type
                name = structure.name 
                elems = structure.elems_ordered
                members = []
                _index = 0
                _slot = 0
                _offset = 0
                totalsize = 0
                for elem in elems:
                    _astid = _index
                    _size, _new_slot = vartype.storage_size
                    totalsize += _size
                    if _new_slot:
                        if _offset > 0:
                            _slot += 1
                            _offset = 0
                    elif _size + _offset > 32:
                            _slot += 1
                            _offset = 0
                            
                    _type_ = str(elem.type)

                    members.append(dict(
                                astId = _astid,
                                contract = contract.name,
                                label = elem.name,
                                offset = _offset,
                                slot = _slot,
                                type = _type_))
                    _index += 1
                    if _type_ not in  _type_info:
                        _type_info[contract.name][_type_] = compute_type_info(elem.type, _type_info, contract)
                    else:
                        pass 
                _type_info[contract.name][type_] = dict(encoding = "inplace", label=name, members=members,numberOfBytes = totalsize)
    else:
        assert False, type_ + " is currently not supported"

def compute_storage_layout(self):
        if not hasattr(self, "_type_info") or self._type_info is None:
            self._type_info = dict()
            self._storage = dict() 
        for contract in self.contracts:
            if contract.name not in self._type_info:
                self._type_info[contract.name] = dict()
            if contract.name not in self._storage:
                self._storage[contract.name] = []
            slot = 0
            offset = 0
            index = 0
            for var in contract.state_variables_ordered:
                if var.is_constant or var.is_immutable:
                    continue    
                astnode_id = index
                size, new_slot = var.type.storage_size
                if new_slot:
                    if offset > 0:
                        slot += 1
                        offset = 0
                elif size + offset > 32:
                    slot += 1
                    offset = 0
                type_ = str(var.type)
                self._storage[contract.name].append(dict(
                    astId = astnode_id,
                    contract = contract.name,
                    label = var.name,
                    offset = offset,
                    slot = str(slot),
                    type = type_
                ))
                compute_type_info(var.type, self._type_info, contract)
                if new_slot:
                    slot += math.ceil(size / 32)
                else:
                    offset += size
                index += 1

# print(ss)
def main_impl(sol_file, contractName, compilerVersion, outStorageFile=None):
    ss = Slither(sol_file)
    compilation_units = ss.compilation_units
    installSolc(compilerVersion)
    for compilation_unit in compilation_units:
        compute_storage_layout(compilation_unit)
        # for contract in compilation_unit.contracts:
        #     storage = compilation_unit._storage[contract.name]
        #     type_info = compilation_unit._type_info[contract.name]
        #     layout =  dict(storage = storage, types = type_info)
            # print(contract.name)
            # print(layout)
    result =  dict(storage = compilation_unit._storage[contractName], types = compilation_unit._type_info[contractName])
    if outStorageFile is not None:
        json.dump(result, open(outStorageFile, "w"))
    return result

def main():
    assert len(sys.argv[1:])==3, "file contractName compilerVersion. A three tuple on source code file (.sol), target contract name and compiler version"
    sol_file = sys.argv[1]
    contractName = sys.argv[2]
    compilerVersion = sys.argv[3]
    contractStorageLayout = main_impl(sol_file=sol_file, contractName=contractName, compilerVersion=compilerVersion)
    print(contractName, contractStorageLayout)

if __name__ == "__main__":
    main()

    