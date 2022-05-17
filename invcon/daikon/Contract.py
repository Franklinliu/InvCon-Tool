import os 
import json 
import math 
from web3 import Web3
import traceback
import math 
import invcon.consts.Config as config
import invcon.daikon.Daikon as daikon
from alive_progress import alive_bar
from .Daikon import *
INTERNAL_TRANSACTION="internal_transactions"

Comparability_Enum= 4
Comparability_Int = 5
Comparability_Mapping= 6
Comparability_String = 7
Comparability_Address = 8
Comparability_Boolean = 9
Comparability_Others = 10

Comparability_Indice = 11

def _obj_var_decl_head(objvarname="Dicether.GameChannel",  ref=False):
    if not ref:
        return \
"""ppt {0}:::Object
ppt-type object
variable this
  var-kind variable
  dec-type {0}
  rep-type hashcode
  flags non_null
  comparability 0""".format(objvarname)
    else:
      return \
"""parent parent {0}:::Object 1
ppt-type object
variable this
  var-kind variable
  dec-type {0}
  rep-type hashcode
  flags is_param nomod
  parent {0}:::Object 1""".format(objvarname)

def _obj_field_decl(varname, vartype, reptype, comparability, enclosing_var="this", objvarname="Dicether.GameChannel", ref=False):
    if not ref:
        return \
"""variable {4}.{0}
    var-kind field {0}
    enclosing-var {4}
    dec-type {1}
    rep-type {2}
    flags non_null
    comparability {3}""".format(varname, vartype, reptype, comparability, enclosing_var)
    else:
        return \
"""variable {4}.{0}
    var-kind field {0}
    enclosing-var {4}
    dec-type {1}
    rep-type {2}
    flags non_null
    comparability {3}
    parent {5}:::Object 1""".format(varname, vartype, reptype, comparability, enclosing_var, objvarname)

def _obj_field_array1_decl(varname, vartype, reptype, comparability,  enclosing_var="this", objvarname="Dicether.GameChannel", ref=False):
    if not ref:
        return \
"""variable {5}.{0}[..]
    var-kind array
    enclosing-var {5}.{0}
    array 1
    dec-type {1}[]
    rep-type {2}[]
    flags non_null
    comparability {3}[{4}]""".format(varname, vartype, reptype, comparability, Comparability_Indice, enclosing_var)
    else:
        return \
"""variable {6}.{0}[..]
    var-kind array
    enclosing-var {6}.{0}
    array 1
    dec-type {1}[]
    rep-type {2}[]
    flags non_null
    comparability {3}[{4}]
    parent {5}:::Object 1""".format(varname, vartype, reptype, comparability, Comparability_Indice, objvarname, enclosing_var )

def _obj_field_array2_decl(varname, vartype, reptype, comparability, objvarname="Dicether.GameChannel", ref=False):
    if not ref:
        return \
"""variable this.{0}[..]
    var-kind array
    enclosing-var this.{0}
    array 1
    dec-type {1}[][]
    rep-type {2}[][]
    flags non_null
    comparability {3}[{4}][{4}]""".format(varname, vartype, reptype, comparability, Comparability_Indice)
    else:
        return \
"""variable this.{0}[..]
    var-kind array
    enclosing-var this.{0}
    array 1
    dec-type {1}[][]
    rep-type {2}[][]
    flags non_null
    comparability {3}[{4}][{4}]
    parent {5}:::Object 1""".format(varname, vartype, reptype, comparability, Comparability_Indice, objvarname)


def _obj_field_mapping_value_decl(varname, structfiledname, vartype, reptype, comparability, objvarname="Dicether.GameChannel", ref=False):
    if not ref:
        return \
"""variable this.{0}[..].get{1}()
    var-kind function get{1}()
    enclosing-var this.{0}[..]
    array 1
    dec-type {2}[]
    rep-type {3}[]
    flags non_null
    comparability {4}[{5}]""".format(varname, structfiledname, vartype, reptype, comparability, Comparability_Indice )
    else:
        return \
"""variable this.{0}[..].get{1}()
    var-kind function get{1}()
    enclosing-var this.{0}[..]
    array 1
    dec-type {2}[]
    rep-type {3}[]
    flags non_null
    comparability {4}[{5}]
    parent {6}:::Object 1""".format(varname, structfiledname, vartype, reptype, comparability, Comparability_Indice, objvarname)

def _obj_field_mapping_value_decl2(varname, structfiledname, vartype, reptype, comparability, objvarname="Dicether.GameChannel", ref=False):
    if not ref:
        return \
"""variable this.{0}[..].get{1}()
    var-kind function get{1}()
    enclosing-var this.{0}[..]
    array 1
    dec-type {2}[]
    rep-type {3}[]
    flags non_null
    comparability {4}[{5}]""".format(varname, structfiledname, vartype, reptype, comparability, Comparability_Indice )
    else:
        return \
"""variable this.{0}[..].get{1}()
    var-kind function get{1}()
    enclosing-var this.{0}[..]
    array 1
    dec-type {2}[]
    rep-type {3}[]
    flags non_null
    comparability {4}[{5}]
    parent {6}:::Object 1""".format(varname, structfiledname, vartype, reptype, comparability, Comparability_Indice, objvarname)


def toHex(val, size=8):
    # print(type(val))
    if isinstance(val, str):
        assert val.startswith("0x")
        val = int(val, 16)
    try:    
        assert isinstance(val, int)
    except:
        # print(val)
        traceback.print_exc()
        pass
    return '0x{0:0{1}x}'.format(val, size)

def toInt(hexstr):
    if not isinstance(hexstr, int):
        if not isinstance(hexstr, str):
            hexstr = hexstr.hex()
        if hexstr.startswith("0x"):
                return int(hexstr, 16)
        else:
                return int(hexstr)
            
    else:
        return hexstr 

ClassMapping = dict() 
Constants = set()

# For different types including int, uint, array, mapping, struct, enum and etc., 
# each storage must have a known slot and optional value
def Type_init(self, astId, contract, label, offset, slot, type):
    global Constants
    self.astId, self.contract, self.name, self.offset, self.slot, self.type_identifier = astId, contract, label, offset, slot, type 
    
    self.offset = toInt(self.offset)
    self.slot = toInt(self.slot)
    
    try:
        if self.encoding=="dynamic_array":
            self.firstElementSlot = toInt(Web3.soliditySha3(["uint256"], [self.slot]))
            self.value = 0
            self.elements = list() 
            # the num of elements is stored at memory of 'self.slot'
            self.numOfItems = 0
            Constants.add(self.numOfItems)
            Constants.add(self.numOfItems+1)

        elif self.encoding == "mapping":
            self.value = 0
            self.values = dict()
        elif self.encoding == "inplace":
            """
                uint8, .., uint256
                int8, .. , int256
                byte8, .., byte32
                address
                bytes, or string (note: length <= 32 bytes)
                fixed array
            """
            if self.isStruct():
                self.value = ContractStorageMonitor(self.members, self.slot)
            elif self.getType().find("[")==-1 and (self.getType().find("int")!=-1 or self.isEnum() or self.getType().find("bool")!=-1):
                self.value = 0
            elif self.basecls is not None:
                # this is a static array
                baseNumOfBytes = int(ClassMapping[self.basecls].numOfBytes)
                self.staticarraysize = int(int(self.numOfBytes)/baseNumOfBytes)
                self.elements = []
                for i in range(self.staticarraysize):
                    elementSlot = int(self.slot) + int((i*baseNumOfBytes)/32)
                    self.elements.append(self.getBasecls()(astId=self.astId, contract=self.contract, label="", offset=0, slot=elementSlot, type=self.getBasecls().label))
                self.values = self.elements
            else:
                self.value = toHex(0, size=2*self.numOfBytes)
            # TODO 
            pass 
        elif self.encoding == "bytes":
            # TODO 
            # This default value may be not true
            self.value = "0x0"

        # For context slicing; record the tainted mapping keys w.r.t. each transaction
        self.taintedKeys = []
    except Exception as e:
        print(e)
        print(self.members)
        traceback.print_exc()
        raise Exception("Unknown error")

class AbstractStorageItem:
    def __init__(self):
        pass

    def getSlot(self):
        return self.slot

    def getLabel(self):
        return self.name
    
    def getValue(self):
        if self.isInplace() and self.getType().find("int")!=-1:
            if self.basecls is not None:
                return self.values 
            # return int(self.value)%(10**15) 
            else:
                return int(self.value) 
        return self.value
    
    @property
    def mappings(self):
        return self.values

    @classmethod 
    def getType(cls):
        return cls.label

    @classmethod
    def isBytes(cls):
        return cls.encoding == "bytes"

    @classmethod
    def isInplace(cls):
        return cls.encoding == "inplace"

    @classmethod
    def isMapping(cls):
        return cls.encoding=="mapping"
    
    @classmethod
    def isDynamicArray(cls):
        return cls.encoding=="dynamic_array"
    
    @classmethod
    def isFixedArray(cls):
        return cls.encoding=="inplace" and cls.getType().find("[")!=-1
    
    @classmethod
    def isStruct(cls):
        return cls.getType().find("struct") != -1

    @classmethod
    def isEnum(cls):
        return cls.getType().find("enum") != -1

    @classmethod
    def hasArrayMappingValue(cls):
        global ClassMapping
        assert cls.isMapping()
        return ClassMapping[cls.valuecls].encoding=="dynamic_array"
    
    @classmethod
    def hasStructMappingValue(cls):
        global ClassMapping
        assert cls.isMapping()
        return ClassMapping[cls.valuecls].members is not None 
    
    @classmethod
    def getMappingStruct(cls):
        global ClassMapping
        assert cls.hasStructMappingValue()
        return ClassMapping[cls.valuecls]
    
    @classmethod
    def getMappingDynArray(cls):
        global ClassMapping
        assert cls.hasArrayMappingValue()
        return ClassMapping[cls.valuecls]
    
    @classmethod
    def getBasecls(cls):
        assert cls.basecls is not None 
        global ClassMapping
        return ClassMapping[cls.basecls]

    @classmethod
    def getValuecls(cls):
        assert cls.valuecls is not None 
        global ClassMapping
        return ClassMapping[cls.valuecls]
    
    @classmethod
    def getKeycls(cls):
        assert cls.keycls is not None 
        global ClassMapping
        return ClassMapping[cls.keycls]
    
    def _setValue(self, slot, value):
        raise NotImplementedError()

    def setValue(self, slot, value, additionalKeys=list()):
        return self._setValue(slot, value, additionalKeys)

    def getVarDecl(self, objvarname, ref=False ):
            def getTyRepComp(_type):
                # else "double" if _type.find("int")!=-1  \
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
            decls = []
            if self.isInplace() and not self.isFixedArray():
                if not self.isStruct():
                    vartype, reptype, comparability = getTyRepComp(self.getType())
                    decls.append(_obj_field_decl(self.getLabel(), vartype, reptype, comparability, objvarname=objvarname, ref=ref))
                else:
                    structname = self.getLabel()
                    vartype, reptype, comparability = getTyRepComp(self.getType())
                    decls.append(_obj_field_decl(structname, vartype, reptype, comparability, objvarname=objvarname, ref=ref))
    
                    structdef = ContractStorageMonitor(self.members, self.slot)
                    for storage in structdef.storages:
                        fieldname = storage.getLabel()
                        if storage.isInplace():
                            if not storage.isStruct():
                                vartype, reptype, comparability = getTyRepComp(storage.getType())
                                decls.append(_obj_field_decl(fieldname, vartype, reptype, comparability, enclosing_var="this.{0}".format(structname), objvarname=objvarname, ref=ref ))
                            else:
                                print(f"unsupported type: {storage.getType()} {self.getType()}")
                        else:
                            print(f"unsupported type: {storage.getType()}  {self.getType()}")
            elif self.isDynamicArray() or self.isFixedArray():
                vartype, reptype, comparability = self.getType().replace(" ", "_"), "hashcode", Comparability_Others
                decls.append(_obj_field_decl(self.getLabel(), vartype, reptype, comparability, objvarname=objvarname, ref=ref))
                basecls =  self.getBasecls()
                if basecls.isInplace():
                    if not basecls.isStruct():
                        vartype, reptype, comparability = getTyRepComp(basecls.getType())
                        decls.append(_obj_field_array1_decl(self.getLabel(), vartype, reptype, comparability, objvarname=objvarname, ref=ref))
                    else:
                        arrayname = self.getLabel()
                        structdef = ContractStorageMonitor(basecls.members,  Web3.soliditySha3(["uint256"], [self.slot]))
                        for storage in structdef.storages:
                            fieldname = storage.getLabel()
                            if storage.isInplace():
                                if not storage.isStruct():
                                    vartype, reptype, comparability = getTyRepComp(storage.getType())
                                    decls.append(_obj_field_array1_decl(fieldname,vartype, reptype, comparability, objvarname=objvarname, ref=ref, enclosing_var="this.{0}".format(arrayname)))
                                else:
                                    print(f"unsupported type: {storage.getType()} {self.getType()}")
                            else:
                                print(f"unsupported type: {storage.getType()}  {self.getType()}")
    
                pass 
            elif self.isMapping():
                mappingvar = self.getLabel()
                vartype, reptype, comparability = self.getType().replace(" ", "_"), "hashcode", Comparability_Others
                decls.append(_obj_field_decl(mappingvar, vartype, reptype, comparability))
                # decls.append(_obj_field_array1_decl(mappingvar, vartype, reptype, comparability, objvarname=objvarname, ref=ref))
        
                keycls, valuecls = self.getKeycls(), self.getValuecls()
                if keycls.isInplace():
                    assert not keycls.isStruct() 
                    vartype, reptype, comparability = getTyRepComp(keycls.getType())
                    # decls.append(_obj_field_mapping_value_decl(mappingvar, "Key", vartype, reptype, comparability,objvarname=objvarname, ref=ref))
                    decls.append(_obj_field_array1_decl(mappingvar, vartype, reptype, comparability, objvarname=objvarname, ref=ref))
                else:
                    print(f"unsupported mapping key type: {keycls.getType()}  {self.getType()}")

                if valuecls.isInplace() and not valuecls.isFixedArray():
                    if not valuecls.isStruct():
                        vartype, reptype, comparability = getTyRepComp(valuecls.getType())
                        decls.append(_obj_field_mapping_value_decl(mappingvar, "Value", vartype, reptype, comparability, objvarname=objvarname, ref=ref))
                    else:
                        structdef = ContractStorageMonitor(valuecls.members,  Web3.soliditySha3(["uint256"], [self.slot]))
                        for storage in structdef.storages:
                            fieldname = storage.getLabel()
                            if storage.isInplace():
                                if not storage.isStruct():
                                    vartype, reptype, comparability = getTyRepComp(storage.getType())
                                    decls.append(_obj_field_mapping_value_decl(mappingvar, fieldname, vartype, reptype, comparability, objvarname=objvarname, ref=ref))
                                else:
                                    print(f"unsupported type: {storage.getType()} {self.getType()}")
                            else:
                                print(f"unsupported type: {storage.getType()}  {self.getType()}")
                elif valuecls.isFixedArray() or valuecls.isDynamicArray():
                    basecls =  valuecls.getBasecls()
                    if basecls.isInplace():
                        if not basecls.isStruct():
                            vartype, reptype, comparability = getTyRepComp(basecls.getType())
                            decls.append(_obj_field_mapping_value_decl2(mappingvar, "Length", "int", "int", Comparability_Int, objvarname=objvarname, ref=ref))
                            decls.append(_obj_field_mapping_value_decl2(mappingvar, "Value", vartype, reptype, comparability, objvarname=objvarname, ref=ref))
                        else:
                            decls.append(_obj_field_mapping_value_decl2(mappingvar, "Length", "int", "int", Comparability_Int, objvarname=objvarname, ref=ref))

                            structdef = ContractStorageMonitor(basecls.members,  Web3.soliditySha3(["uint256"], [self.slot]))
                            for storage in structdef.storages:
                                fieldname = storage.getLabel()
                                if storage.isInplace():
                                    if not storage.isStruct():
                                        vartype, reptype, comparability = getTyRepComp(storage.getType())
                                        decls.append(_obj_field_mapping_value_decl2(mappingvar, fieldname, vartype, reptype, comparability, objvarname=objvarname, ref=ref))
                                    else:
                                        print(f"unsupported type: {storage.getType()} {self.getType()}")
                                else:
                                    print(f"unsupported type: {storage.getType()}  {self.getType()}")
                    pass 
                # mapping(address=>mapping(address=>uint256)) allowance
                elif valuecls.isMapping():
                    subkeycls = valuecls.getKeycls()
                    subvaluecls = valuecls.getValuecls()
                    assert subkeycls.isInplace()
                    vartype, reptype, comparability = getTyRepComp(subkeycls.getType())
                    decls.append(_obj_field_mapping_value_decl2(mappingvar, "SubLength", "int", "int", Comparability_Int, objvarname=objvarname, ref=ref))
                    decls.append(_obj_field_mapping_value_decl2(mappingvar, "SubKey", vartype, reptype, comparability, objvarname=objvarname, ref=ref))
                    if subvaluecls.isInplace():
                        vartype, reptype, comparability = getTyRepComp(subvaluecls.getType())
                        decls.append(_obj_field_mapping_value_decl2(mappingvar, "SubValue", vartype, reptype, comparability, objvarname=objvarname, ref=ref))
    
            return decls

    def getValueTrace(self):
            dtraces = []
            if self.isInplace() and not self.isFixedArray():
                if not self.isStruct():
                    v = """this.{0}
{1}
1""".format(self.getLabel(),"\"{0}\"".format(self.getValue()) if isinstance(self.getValue(), str) else str(self.getValue()))
                    dtraces.append(v)
                else:
                    structname = self.getLabel()
                    v = """this.{0}
{1}
1""".format(structname, self.getSlot())
                    dtraces.append(v)
    
                    structdef = self.getValue()
                    for storage in structdef.storages:
                        fieldname = storage.getLabel()
                        if storage.isInplace():
                            if not storage.isStruct():
                                v = """this.{0}.{1}
{2}
1""".format(structname, fieldname, "\"{0}\"".format(storage.getValue()) if isinstance(storage.getValue(), str) else str(storage.getValue()))
                                dtraces.append(v)
                            else:
                                print(f"unsupported type: {storage.getType()} {self.getType()}")
                        else:
                            print(f"unsupported type: {storage.getType()}  {self.getType()}")
            elif  self.isFixedArray() or self.isDynamicArray():
                arrayname = self.getLabel()
                v = """this.{0}
{1}
1""".format(arrayname, self.getSlot())
                dtraces.append(v)
                
                basecls =  self.getBasecls()
                if basecls.isInplace():
                    if not basecls.isStruct():

                        v = """this.{0}[..]
[{1}]
1""".format(arrayname, " ".join([ f"\"{elem.getValue()}\"" if isinstance(elem.getValue(),str) else str(elem.getValue()) for elem in self.elements ]))
                        dtraces.append(v)
                    else:
                        # print(self.elements)
                        # print(self.getType())
                        structdef = ContractStorageMonitor(basecls.members,  Web3.soliditySha3(["uint256"], [self.slot]))
                        for storage in structdef.storages:
                            fieldname = storage.getLabel()
                            if storage.isInplace():
                                if not storage.isStruct():
                                    values =  []
                                    for elem in self.elements:
                                        # print(elem)
                                        for _storage in elem.getValue().storages:
                                            if _storage.getLabel() == storage.getLabel():
                                                values.append( f"\"{_storage.getValue()}\""  if isinstance(_storage.getValue(),str) else str(_storage.getValue()))
                                    v = """this.{0}.{1}[..]
[{2}]
1""".format(arrayname, fieldname, " ".join(values))
                                    dtraces.append(v)
                                else:
                                    print(f"unsupported type: {storage.getType()} {self.getType()}")
                            else:
                                print(f"unsupported type: {storage.getType()}  {self.getType()}")
                pass 
            elif self.isMapping():
                mappingvar = self.getLabel()
                v = """this.{0}
{1}
1""".format(mappingvar, self.getSlot())
                dtraces.append(v)

                keycls, valuecls = self.getKeycls(), self.getValuecls()
                if keycls.isInplace():
                    assert not keycls.isStruct() 
                    keys = [f"\"{key}\"" if isinstance(key, str) else str(key) for key in self.values.keys()]
                    # v = """this.{0}[..].get{1}()
    # [{2}]
    # 1""".format(mappingvar, "Key", " ".join(keys)) 
                    v = """this.{0}[..]
[{1}]
1""".format(mappingvar," ".join(keys)) 
                    dtraces.append(v)

                else:
                    print(f"unsupported mapping key type: {keycls.getType()}  {self.getType()}")

                if valuecls.isInplace():
                    if not valuecls.isStruct():
                        values = [f"\"{val.getValue()}\"" if isinstance(val.getValue(), str) else str(val.getValue()) for val in self.values.values()]
                        v = """this.{0}[..].get{1}()
[{2}]
1""".format(mappingvar, "Value", " ".join(values))  
                        dtraces.append(v)

                    else:
                        structdef = ContractStorageMonitor(valuecls.members,  Web3.soliditySha3(["uint256"], [self.slot]))
                        for storage in structdef.storages:
                            fieldname = storage.getLabel()
                            if storage.isInplace():
                                if not storage.isStruct():
                                    values =  []
                                    for val in self.values.values():
                                        for _storage in val.getValue().storages:
                                            if _storage.getLabel() == storage.getLabel():
                                                values.append( f"\"{_storage.getValue()}\""  if isinstance(_storage.getValue(),str) else str(_storage.getValue()))
                                    
                                    v = """this.{0}[..].get{1}()
[{2}]
1""".format(mappingvar, fieldname, " ".join(values))
                                    dtraces.append(v)

                                else:
                                    print(f"unsupported type: {storage.getType()} {self.getType()}")
                            else:
                                print(f"unsupported type: {storage.getType()}  {self.getType()}")
                elif valuecls.isDynamicArray():
                    basecls =  valuecls.getBasecls()
                    if basecls.isInplace():
                        if not basecls.isStruct():
                            values = list()
                            length = list()
                            for val in self.values.values():
                                _values = list()
                                for elem in val.elements:
                                    _values.append( f"\"{elem.getValue()}\"" if isinstance(elem.getValue(), str) else str(elem.getValue()))
                                values.extend(_values)
                                length.append(str(len(_values)))
                            # express two-dimensional array using length array and value array
                            v = """this.{0}[..].get{1}()
[{2}]
1""".format(mappingvar, "Length", " ".join(length))  
                            dtraces.append(v)

                            v = """this.{0}[..].get{1}()
[{2}]
1""".format(mappingvar, "Value", " ".join(values))  
                            dtraces.append(v)

                        else:
                            structdef = ContractStorageMonitor(basecls.members,  Web3.soliditySha3(["uint256"], [self.slot]))
                            length = list()
                            LengthSet = False 
                            for storage in structdef.storages:
                                fieldname = storage.getLabel()
                                if storage.isInplace():
                                    if not storage.isStruct():
                                        values = list()
                                        for val in self.values.values():
                                            _values = []
                                            for elem in val.elements:
                                                for _storage in elem.getValue().storages:
                                                    if _storage.getLabel() ==  storage.getLabel():
                                                        _values.append( f"\"{_storage.getValue()}\"" if isinstance(_storage.getValue(), str) else str(_storage.getValue()))
                                            # values.append("[{0}]".format(" ".join(_values)))
                                            values.extend(_values)
                                            if not LengthSet:
                                                length.append(str(len(_values)))
                                        if not LengthSet:
                                            v = """this.{0}[..].get{1}()
[{2}]
1""".format(mappingvar, "Length", " ".join(length))

                                            dtraces.append(v)
                                            LengthSet = True 

                                        v = """this.{0}[..].get{1}()
[{2}]
1""".format(mappingvar, fieldname, " ".join(values))

                                        dtraces.append(v)

                                    else:
                                        print(f"unsupported type: {storage.getType()} {self.getType()}")
                                else:
                                    print(f"unsupported type: {storage.getType()}  {self.getType()}")
                elif valuecls.isMapping():
                    subkeycls = valuecls.getKeycls()
                    subvaluecls = valuecls.getValuecls()
                    assert subkeycls.isInplace()
                    if subvaluecls.isInplace() and not subvaluecls.isStruct():
                        all_subkeys = []
                        all_subvalues = []
                        all_length = []
                        for firstkey in self.values:
                            subkeys = [f"\"{key}\"" if isinstance(key, str) else str(key) for key in self.values[firstkey].values]
                            subvalues = [f"\"{_val.getValue()}\"" if isinstance(_val.getValue(), str) else str(_val.getValue()) for _val in self.values[firstkey].values.values()]
                            all_subkeys.extend(subkeys)
                            all_subvalues.extend(subvalues)
                            all_length.append(len(subkeys))
                        
                        v = """this.{0}[..].get{1}()
[{2}]
1""".format(mappingvar, "SubLength", " ".join(map(lambda i: str(i), all_length)))  
                        dtraces.append(v)
                        
                        v = """this.{0}[..].get{1}()
[{2}]
1""".format(mappingvar, "SubKey", " ".join(all_subkeys))  
                        dtraces.append(v)

                        v = """this.{0}[..].get{1}()
[{2}]
1""".format(mappingvar, "SubValue", " ".join(all_subvalues))  
                        dtraces.append(v)

                    
            return dtraces    

def setValueForInplace(self, slot, value, additionalKeys=list()):
    global Constants
    try:
        assert isinstance(slot, str) and isinstance(value, str)
        assert slot.startswith("0x") and value.startswith("0x")
        slot = "0x"+slot.replace("0x", "")
        value = "0x"+value.replace("0x", "")
            # struct {
            #  uint gameId, 
            #  uint gameStatus
            #  mapping(uint=>address) xxx
            #  mapping(address=>uint) xxx
            # }
        if self.isStruct():
            if self.value.readStateChange(slot, value, additionalKeys):
                return True 
            else:
                return False 
        # print(slot, value, self.label, self.slot)
        if self.slot <= int(slot, 16) and int(slot, 16) <= self.slot + int((int(self.numOfBytes) + int(self.offset) -1) / 32):
            if self.isEnum():
                value = "0x"+value[66-2*(self.offset+self.numOfBytes):66-2*self.offset].replace("0x", "")
                self.value = int(value, 16)
            else:
                if self.basecls is not None:
                    element_slot = int(slot, 16)-self.slot 
                    baseNumOfBytes = self.getBaseCls().numOfBytes
                    element_index_start, element_index_end = element_slot * 32 / baseNumOfBytes, (element_slot+1) * 32 / baseNumOfBytes
                    for index in range(element_index_start, min(element_index_end, self.staticarraysize)):
                        value = "0x"+value[66-2*(self.offset+(index+1)*baseNumOfBytes):66-2*(self.offset+index*baseNumOfBytes)].replace("0x", "")
                        if self.getType().find("int")!=-1:
                            value = int(value, 16)
                        elif self.getType().find("bool") !=-1:
                            value = int(value, 16)
                        self.values[index] = value 
                else:
                    value = "0x"+value[66-2*(self.offset+self.numOfBytes):66-2*self.offset].replace("0x", "")
                    if self.getType().find("int")!=-1:
                        self.value = int(value, 16)
                        Constants.add(self.value)
                    elif self.getType().find("bool") !=-1:
                        self.value = int(value, 16)
                        # Constants.add(self.value)
                    else:
                        self.value = value 
                        if self.getType().find("address")!=-1:
                            Constants.add(self.value)
            return True 
        return False 
    except:
        traceback.print_exc()
    return False

def setValueForDynamicArray(self, slot, value,  additionalKeys=list()):
    global ClassMapping
    global Constants
    assert isinstance(slot, str) and isinstance(value, str)
    assert slot.startswith("0x") and value.startswith("0x")
   
    try:
        if int(slot, 16) - self.firstElementSlot <=10 and int(slot, 16) - self.firstElementSlot >=0:
            if config.DEBUG:
                print("should find an array slot for ", slot,  int(slot, 16) - self.firstElementSlot)
                print("condition: self.firstElementSlot + int(self.getBasecls().numOfBytes*(len(self.elements)+1)/32) - int(slot, 16) = ",self.firstElementSlot + int(self.getBasecls().numOfBytes*(len(self.elements)+1)/32) - int(slot, 16))
            
        if int(slot, 16) == self.slot:
            self.value = int(value, 16)
            self.numOfItems = self.value 
            Constants.add(self.numOfItems)
            Constants.add(self.numOfItems+1)
            return True

        elif self.firstElementSlot <= int(slot, 16) \
        and int(slot, 16) <= (self.firstElementSlot + math.ceil(self.getBasecls().numOfBytes/32)*(len(self.elements)+1)):
            if config.DEBUG:
                print("find array slot...")
            index = int((int(slot, 16) - self.firstElementSlot) /math.ceil(self.getBasecls().numOfBytes/32))
            # TODO
            # Here, we assume every item in an array are stored at a new slot
            # This may be not true. May apply to uint128 ... uint256 only
            # Need to check later
            elementSlot = index * math.ceil(self.getBasecls().numOfBytes/32) + self.firstElementSlot
            assert elementSlot <= int(slot, 16), "elementSlot must be less than or equal to slot"
            if index < len(self.elements):
                if config.DEBUG:
                    print("update item")
                self.elements[index].setValue(slot, value)
            else:
                if config.DEBUG:
                    print("create item")
                self.elements.append(self.getBasecls()(astId=self.astId, contract=self.contract, label="", offset=0, slot=elementSlot, type=self.getBasecls().label))
                self.elements[-1].setValue(slot, value)
                self.numOfItems = len(self.elements)
            return True 
    except:
        traceback.print_exc()
    return False 


from functools import lru_cache
@lru_cache
def soliditySha3(key, slot):
    if isinstance(key, int):
                key = key
    elif isinstance(key, str):
                if key.startswith("0x"):
                    key = int(key, 16) 
                else:
                    key = int(key)
    else:
                assert False, f"{key} is not supported"
    assert key >= 0
    return Web3.soliditySha3(["uint256", "uint256"], [key, slot])


def setValueForMapping(self, slot, value, additionalKeys=list()):
    global ClassMapping
    global Constants
    assert isinstance(slot, str) and isinstance(value, str)
    assert slot.startswith("0x") and value.startswith("0x")

    @lru_cache
    def calculateKeySlot(key):
        #  mapping(uintXX=>) or mapping(intXXX => )
        if ClassMapping[self.keycls].label.find("int")!=-1 and ClassMapping[self.keycls].label.find("[")==-1:
            ret = soliditySha3(key, self.slot)
            # print(key, ret.hex())
            return toInt(ret.hex())
        # mapping(address=>) or mapping(address => )
        elif ClassMapping[self.keycls].label.find("address")!=-1 and ClassMapping[self.keycls].label.find("[")==-1:
            ret = soliditySha3(key, self.slot)
            # print(key, ret.hex())
            return toInt(ret.hex())
        
        # mapping(bytes32=>) or mapping(bytes32 => )
        elif ClassMapping[self.keycls].label.find("bytes32")!=-1 and ClassMapping[self.keycls].label.find("[")==-1:
          
            ret = soliditySha3(key, self.slot)
            # print(key, ret.hex())
            return toInt(ret.hex())

        elif (isinstance(key, int) or isinstance(key, str)) and \
             ClassMapping[self.keycls].numOfBytes *2 +2 > (len(hex(key)) if isinstance(key, int) else len(key)):
            ret = soliditySha3(key, self.slot)
            # print("key of arbitrary type:", key, ret.hex())
            return toInt(ret.hex())
        else:
            assert False, f"{key} is not supported for {self.__class__}"
            # pass 
    
    keycls = self.getKeycls()
   
    for key in additionalKeys:
            try:
                if keycls.getType().find("int")!=-1:
                    if isinstance(key, str):
                        if key.startswith("0x"):
                            key = int(key, 16)
                        else:
                            key = int(key)
                candiate_slot = calculateKeySlot(key)
             
                if key not in self.values:
                    var = self.getValuecls()(astId=self.astId, contract=self.contract, label="", offset=0, slot=candiate_slot, type=self.getValuecls().label)
                else:
                    var = self.values[key]
                if True == var.setValue(slot, value, additionalKeys=additionalKeys):
                    self.values[key] = var 
                    # self.taintedKeys = []
                    self.taintedKeys.append(key)
                    # incase there is a nested mapping structure
                    if len(var.taintedKeys)>0:
                        self.taintedKeys.append(var.taintedKeys)
                    return True 
            except:
                pass 
    
    # for key in Constants:
    #         try:
    #             if keycls.getType().find("int")!=-1:
    #                 if isinstance(key, str):
    #                     if key.startswith("0x"):
    #                         key = int(key, 16)
    #                     else:
    #                         key = int(key)
    #             candiate_slot = calculateKeySlot(key)
    #             # print(f"try key: {key} of {self.slot}, {candiate_slot} vs {slot}")
    #             if key not in self.values:
    #                 var = self.getValuecls()(astId=self.astId, contract=self.contract, label="", offset=0, slot=candiate_slot, type=self.getValuecls().label)
    #             else:
    #                 var = self.values[key] 
    #             # print("mapping value cls:", type(var))
    #             if True == var.setValue(slot, value, additionalKeys=additionalKeys):
    #                 self.values[key] = var 
    #                 self.taintedKeys.append(key)
    #                 # incase there is a nested mapping structure
    #                 if len(var.taintedKeys)>0:
    #                     self.taintedKeys.append(var.taintedKeys)
    #                 return True  
    #         except:
    #             pass 

    # for key in self.values.keys():
    #     try:
    #         if keycls.getType().find("int")!=-1:
    #                 if isinstance(key, str):
    #                     if key.startswith("0x"):
    #                         key = int(key, 16)
    #                     else:
    #                         key = int(key)

    #         candiate_slot = calculateKeySlot(key)
    #         var = self.values[key]
    #         if True == var.setValue(slot, value, additionalKeys=additionalKeys):
    #             self.taintedKeys.append(key)
    #             # incase there is a nested mapping structure
    #             if len(var.taintedKeys)>0:
    #                 self.taintedKeys.append(var.taintedKeys)
    #             return True 
    #     except:
    #         pass 
    
    return False 

def setValueForStructMappingValue(self, slot, value, additionalKeys=list()):
    return self.setValueForMapping(slot, value, additionalKeys ) 

def setValueForArrayMappingValue(self, slot, value, additionalKeys=list()):
    return self.setValueForMapping(slot, value, additionalKeys)  

def setValueForInplaceStructValue(self, slot, value, additionalKeys=list()):
    return self.setValueForMapping(slot, value, additionalKeys) 

def setValueForBytes(self, slot, value, additionalKeys=list()):
    if self.setValueForInplace(slot, value, additionalKeys):
        return True 
    #  Here, we assume all the bytes string is less than 32 bytes
    # elif self.setValueForDynamicArray(slot, value, additionalKeys):
    #     return True 
    else:
        return False 

def _setValue(self, slot, value, additionalKeys=list()):
    if self.isInplace():
        return self.setValueForInplace(slot, value, additionalKeys) 
    elif self.isDynamicArray():
        return self.setValueForDynamicArray(slot, value, additionalKeys) 
    elif self.isMapping():
        return self.setValueForMapping(slot, value, additionalKeys)  
        # if self.hasStructMappingValue():
        #     return self.setValueForStructMappingValue(slot, value, additionalKeys) 
        # elif self.hasArrayMappingValue():
        #     return self.setValueForStructMappingValue(slot, value, additionalKeys) 
        # else:   
        #     return self.setValueForInplaceStructValue(slot, value, additionalKeys) 
    elif self.isBytes():
        return self.setValueForBytes(slot, value, additionalKeys)
    else:
        raise LookupError(f"unfounded variable type {self}")

def printData(self, globalTaintedKeysRecorderSet=dict()):
        # print(self)
        if self.encoding=="dynamic_array":
            print("***********************")
            print(self.elements)
            print("***********************")
        
        elif self.encoding == "mapping":
            print("***********************")
            print(
            "Slot: {0}\n Offset: {1}\n BytesSize: {2}\n VarName: {3}\n Label: {4}".
            format(toHex(self.slot), toHex(self.offset), self.numOfBytes, self.name, self.label)
            )
            if self.name:
                globalTaintedKeysRecorderSet[self.name] = self
            print("Tainted Keys: {0}".format(self.taintedKeys))
            # print(toHex(self.slot), toHex(self.offset), self.numOfBytes, self.name, self.label)
            for key in self.values:
                print(">>>key:", key)
                print("   value: ")
                if self.values[key].isStruct():
                    # print("{0}:".format(key))
                    self.values[key].value.printStorageVariables()
                else:
                    self.values[key].printData()
            print("***********************")
        else:
            if self.isStruct():
                self.value.printStorageVariables()
            else:
                if self.name:
                    print(
                    "Slot: {0}\n Offset: {1}\n BytesSize: {2}\n VarName: {3}\n Label: {4}\n Value: {5}".
                    format(toHex(self.slot), toHex(self.offset), self.numOfBytes, self.name, self.label, toHex(self.value, size=self.numOfBytes*2))
                    )
                else:
                    print(
                    "Slot: {0}\n Offset: {1}\n BytesSize: {2}\n Label: {3}\n Value: {4}".
                    format(toHex(self.slot), toHex(self.offset), self.numOfBytes,  self.label, toHex(self.value, size=self.numOfBytes*2))
                    )
            

def createTypeClasses(types):
    global ClassMapping
    for type_identifier in types:
        try:
            if isinstance(type_identifier, dict):
                type_identifier = type_identifier["type"]
            
            ClassMapping[type_identifier] = type(type_identifier, (AbstractStorageItem, ), \
                {
                    "encoding": types[type_identifier]["encoding"],
                    "label": types[type_identifier]["label"],
                    "basecls": types[type_identifier]["base"] if "base" in types[type_identifier] else None,
                    "numOfBytes": toInt(types[type_identifier]["numberOfBytes"]) if "numberOfBytes" in types[type_identifier] else None,
                    "keycls": types[type_identifier]["key"] if "key" in types[type_identifier] else None,
                    "valuecls": types[type_identifier]["value"] if "value" in types[type_identifier] else None,
                    "members": types[type_identifier]["members"] if "members" in types[type_identifier] else None,
                    "__init__": Type_init,
                    "_setValue": _setValue,
                    "setValueForInplace": setValueForInplace, 
                    "setValueForDynamicArray": setValueForDynamicArray,
                    "setValueForMapping": setValueForMapping, 
                    "setValueForStructMappingValue": setValueForStructMappingValue, 
                    "setValueForArrayMappingValue": setValueForArrayMappingValue,
                    "setValueForInplaceStructValue": setValueForInplaceStructValue,
                    "setValueForBytes": setValueForBytes,
                    "printData": printData
                }
            )
        except:
            # traceback.print_exc()
            # print(type_identifier, types)
            pass 
            # raise Exception("Unsupported type")
    pass 


class ContractStorageMonitor:
    
    def __init__(self, storageJson, slot=0, typeJson = None):
        global ClassMapping
        
        if typeJson is not None:
            try:
                if type(storageJson) == int:
                    print(storageJson)
                assert not isinstance(storageJson, int)

                if type(typeJson) == int:
                    print(typeJson)
                assert not isinstance(typeJson, int)
            except:
                print(storageJson)
                print(typeJson)
                raise Exception("unknown error")
            createTypeClasses(types=typeJson)
        
        self.slot = toInt(slot) 
        self.storages = list()

        self.storageJson = storageJson
        
        self.availableslots = dict()
        self.grid_storages = dict()
        grid_storages = self.grid_storages 

        self.fields = list()
        for storageItem in storageJson:
            try:
                astId, contract, label, offset, slot, type_identifier = storageItem["astId"], storageItem["contract"], storageItem["label"],storageItem["offset"],storageItem["slot"],storageItem["type"]
                if isinstance(slot, str):
                    if slot.startswith("0x"):
                        slot = int(slot, 16) + self.slot  
                    else:
                        try:
                            slot = int(slot) + self.slot 
                        except:
                            print(slot, type(slot), self.slot, type(self.slot))
                            raise Exception()

                if isinstance(offset, str):
                    if offset.startswith("0x"):
                        offset = int(offset, 16)
                    else:
                        offset = int(offset)
                if slot not in grid_storages:
                    grid_storages[slot] = dict()
                
                # print(astId, contract, label, offset, slot, type_identifier)
                assert type_identifier in ClassMapping
                # print("test0")
                grid_storages[slot][offset] = ClassMapping[type_identifier](astId, contract, label, offset, slot, type_identifier)
                # print("test1")
                self.storages.append(grid_storages[slot][offset])
                # print("test2")
                setattr(self, label, grid_storages[slot][offset])
                # print("test3")
                self.fields.append((label, grid_storages[slot][offset]))
            except:
                traceback.print_exc()
                print(storageItem) 
                print(ClassMapping[type_identifier])
                raise Exception("Unknown Error")     
    
    def getFields(self):
        return self.fields


    def getAllInplaceValues(self):
        inplace_values = set() 
        for storageItem in self.storages:
            if storageItem.isInplace() and not storageItem.isStruct() and storageItem.basecls is None:
               inplace_values.add(storageItem.getValue())
        return inplace_values

    def readStateChange(self, slot, value, additionalKeys):
        assert isinstance(value, str), "value should be hex string"
        assert value.startswith("0x")==True, "value should be hex string"
        assert isinstance(slot, str), "slot should be hex string"
        assert slot.startswith("0x")==True, "slot should be hex string"
        if config.DEBUG:
            print(">>>Update storage.\n Slot: {0}\n Value: {1}".format(slot, value))
        isRoot = False
        if value.find("-")!=-1:
            # this is a root entry for state change read 
            oldval, value = value.split("-")
            isRoot = True 
            if slot in self.availableslots:
                if self.availableslots[slot] != oldval.strip():
                    assert False, f"the recorded value of {slot} is inconsistent. recorded: {self.availableslots[slot]} vs actual: {oldval}"
            else:
                assert int(oldval, base=16) == 0, f"the recorded value of {slot} is inconsistent. recorded: {0} vs actual: {oldval}"
        hit = False
        for storageItem in self.storages:
            if storageItem.setValue(slot, value, additionalKeys):
                hit = True 
                if storageItem.numOfBytes>=32:
                    break 
                # return True 
        if hit:
            # print(f"{slot} is hit")
            self.availableslots[slot] = value 
            return True 
        else:
            if isRoot:
                print(f"{slot} not found")
            return False 

    def _before(self, funcName, msg_sender, msg_value,  args, failedFlag, txHash):
        if config.DEBUG:
            print("before:")
    
    def _after(self, funcName, msg_sender, msg_value, args, failedFlag, txHash):
        if config.DEBUG:
            print("after:")
        
    def txStateTransition(self, slot_statechanges, funcName, additionalKeys, msg_sender, msg_value, args, showflag=False, txHash=None):
        failedFlag = len(slot_statechanges) == 0
        if showflag:
            self._before(funcName=funcName, msg_sender=msg_sender, msg_value=msg_value, args = args, failedFlag=failedFlag, txHash=txHash)
        for slot_statechange in slot_statechanges:
                slot, state = tuple(slot_statechange.split(":"))
                self.readStateChange(slot, state, additionalKeys=additionalKeys)
        if showflag:
            self._after(funcName=funcName, msg_sender=msg_sender,  msg_value=msg_value, args = args, failedFlag=failedFlag, txHash=txHash)

    def getObjectDecl(self, contractName):
        decls = [_obj_var_decl_head(objvarname=contractName)]
        for storageItem in self.storages:
            decls.extend(storageItem.getVarDecl(objvarname=contractName))
        return decls

    def getObjectRef(self, contractName):
        refdecls = [_obj_var_decl_head(objvarname=contractName, ref=True)]
        for storageItem in self.storages:
            refdecls.extend(storageItem.getVarDecl(objvarname=contractName, ref=True))
        return refdecls

    def getObjectDataTraces(self):
        dtraces = []
        for storageItem in self.storages:
            dtraces.extend(storageItem.getValueTrace())
        return dtraces

    def printStorageVariables(self):
        if config.DEBUG:
            globalTaintedKeysRecorderSet = dict()
            print("Contract Storage>>>>")
            # print(list(self.grid_storages.keys()))
            for _slot in self.grid_storages.keys():
                # print(_slot)
                for _offset in self.grid_storages[_slot].keys():
                    self.grid_storages[_slot][_offset].printData(globalTaintedKeysRecorderSet=globalTaintedKeysRecorderSet)
        
            def clearEmpyList(taintedKeys):
                newTaintedKeys = list()
                hasNestedTaintedKeys = False
                for ele in taintedKeys:
                    if isinstance(ele, list) and len(ele) == 0:
                        continue
                    elif isinstance(ele, list) and len(ele) > 0:
                        ele, _ = clearEmpyList(ele)
                        hasNestedTaintedKeys = True 
                        newTaintedKeys.append(ele)
                    else:
                        newTaintedKeys.append(ele)
                return newTaintedKeys, hasNestedTaintedKeys


            def ERC20TokenContextSlicing(balancesKeys, allowanceKeys):
                slicingKeysPairSet = set()
                secondKey = ""
                for primaryKey in balancesKeys:
                    for sender in allowanceKeys.keys():
                        if primaryKey in allowanceKeys[sender]:
                            secondKey = sender
                    
                    slicingKeysPairSet.add((primaryKey, secondKey))
                
                for sender in allowanceKeys.keys():
                        for primaryKey in allowanceKeys[sender]:
                            slicingKeysPairSet.add((primaryKey, sender))
                print(slicingKeysPairSet)
                return slicingKeysPairSet

            isERC20 = True 
            if isERC20:
                balancesKeys = list()
                allowanceKeys = dict()
            for taintedMappingVar in globalTaintedKeysRecorderSet.keys():
                taintedKeys = globalTaintedKeysRecorderSet[taintedMappingVar].taintedKeys
                newTaintedKeys, hasNestedTaintedKeys = clearEmpyList(taintedKeys)
                if not hasNestedTaintedKeys:
                    newTaintedKeys = list(set(newTaintedKeys))
                    if isERC20:
                        balancesKeys = newTaintedKeys
                else:
                    # maping(xxx=>mapping(xxx=> xxx))
                    taintedKeys = dict()
                    for i in range(0, len(newTaintedKeys), 2):
                        if newTaintedKeys[i] not in taintedKeys.keys():
                            taintedKeys[newTaintedKeys[i]] = list(set(newTaintedKeys[i+1]))
                        else:
                            taintedKeys[newTaintedKeys[i]] = list(set(newTaintedKeys[i+1]).union(taintedKeys[newTaintedKeys[i]]))
                    newTaintedKeys = taintedKeys
                    if isERC20:
                        allowanceKeys = newTaintedKeys
                print("MappingVar: {0}\n hasNestedTaintedKeys: {1}\n TaintedKeys: {2}\n".
                format(taintedMappingVar, hasNestedTaintedKeys,  newTaintedKeys)
                )

            ERC20TokenContextSlicing(balancesKeys=balancesKeys, allowanceKeys=allowanceKeys)
           

def isString(v_type):
    return  v_type.find("address")!=-1 or v_type.find("bytes")!=-1 or  v_type.find("contract")!=-1
def isBool(v_type):
    return  v_type.find("bool")!=-1 

def isArray(v_type):
    return  v_type.find("[")!=-1

class Contract(ContractStorageMonitor):
    def __init__(self, workdir, contractName, storageLayoutJson, input_abi, input_state_change, input_tx_receipt):
        assert os.path.exists(storageLayoutJson)
        assert os.path.exists(input_abi)
        assert os.path.exists(input_tx_receipt)
        assert os.path.exists(input_state_change)
        self.workdir = workdir
        layoutjson = json.load(open(storageLayoutJson))
        types = layoutjson["types"]
        storage = layoutjson["storage"]

        super().__init__(typeJson=types, storageJson = storage)

        self.tx_abi = json.load(open(input_abi),encoding="utf8") 
        self.tx_receipts = json.load(open(input_tx_receipt), encoding="utf8")
        if "result" in self.tx_receipts:
                self.tx_receipts = self.tx_receipts["result"]
        
        self.contractName = contractName
        self.input_state_change = input_state_change

        self.tx_hash_before_after_contractStatesDataTraces = dict()

    def readTransactionFunctionInputVariables(self, tx_hash, nonce):
        def _get_full_function_name(name, inputs):
                    ret = name 
                    argtyps = []
                    for item in inputs:
                        argtyps.append(item["type"])
                    return name +"("+",".join(argtyps)+")"
       
        tx = list(filter(lambda tx: tx["hash"] == tx_hash, self.tx_receipts))[0]
        
        if "decoded" not in tx:
            return [], [], [], [], [], None 

        assert "decoded" in tx, "no decoded parameters" 
        if "type" in tx and tx["type"] == INTERNAL_TRANSACTION:
            decoded =  tx[INTERNAL_TRANSACTION][0]["decoded"]
        else:
            decoded = tx["decoded"]
        args = decoded["args"]
        if isinstance(args, dict):
            for _var in args.keys():
                if isinstance(args[_var], str):
                    args[_var] = args[_var].lower()
                    self.envs.add(args[_var])
                elif isinstance(args[_var], list):
                    self.envs.update(args[_var])
                elif isinstance(args[_var], int):
                    self.envs.add(args[_var])
                else:
                    assert False, f"Unsupported parameter type of {_var} of values {args[_var]}" 
        
        # print(decoded["function"], args)
        if decoded["function"] == "constructor":
            return [], [], [], [], args, None 

        dtrace = []

        try:
            functionABI = list(filter(lambda function: function["type"] == "function"  and function["name"]==decoded["function"], self.tx_abi))[0]
            
            enter = ["""{0}.{1}:::ENTER
this_invocation_nonce
{2}""".format(self.contractName, _get_full_function_name(decoded["function"], functionABI["inputs"]), nonce)]
        
            exit1 = ["""{0}.{1}:::EXIT1
this_invocation_nonce
{2}""".format(self.contractName, _get_full_function_name(decoded["function"], functionABI["inputs"]), nonce)]
        
            exit2 = ["""{0}.{1}:::EXIT2
this_invocation_nonce
{2}""".format(self.contractName, _get_full_function_name(decoded["function"], functionABI["inputs"]), nonce)]
        
            length = int(args["__length__"])

            if length>0:
                ignore = set([ "{0}".format(i) for i in range(length)])
                ignore.add("__length__")
            
                variables = list(filter(lambda key: key not in ignore, args))
                
                for var in variables:
                    
                    var_type = list(filter(lambda input: input["name"]==var, functionABI["inputs"]))[0]["type"]
                    
                    if not isArray(var_type):
                        # %(10**27)
                        v = """{0}  
{1}
1""".format(var, "\"{0}\"".format(args[var]) if isString(var_type) else str(int(args[var])) if not isBool(var_type) else 1 if args[var] else 0) 
                        dtrace.append(v)
                    else:
                        _vars = args[var]
                        _vars = ["\"{0}\"".format(str(_var)) if isString(var_type) else  str(int(_var))  if not isBool(var_type) else 1 if _var else 0 for _var in _vars]
                        v = """{0}  
{1}
1""".format(var, 123456) 
                        dtrace.append(v)
                        v = """{0}[..]  
[{1}]
1""".format(var, " ".join(_vars)) 
                        dtrace.append(v)
        
            return enter, exit1, exit2, dtrace, args, decoded["function"]
        except:
            # fallback function
            traceback.print_exc()
            print("tx:", tx_hash, "decoded function:", decoded)
            return [], [], [], [], args, None 

    def readTransactionEnvironmentVariables(self, tx_hash):
        try:
            tx = list(filter(lambda tx: tx["hash"] == tx_hash, self.tx_receipts))[0]
        except:
            traceback.print_exc()
       
        if "type" in tx and tx["type"] == INTERNAL_TRANSACTION:
            if len(tx[INTERNAL_TRANSACTION])==0:
                self.envs.add(tx["from"].lower())
                return tx["from"].lower(), None,  None
            elif len(tx[INTERNAL_TRANSACTION])!=1:
                for interntx in tx[INTERNAL_TRANSACTION]:
                    self.envs.add(interntx["action"]["from"].lower()) 
                    decoded = interntx["decoded"]
                    args = decoded["args"]
                    if isinstance(args, dict):
                        for _var in args.keys():
                            if isinstance(args[_var], str):
                                args[_var] = args[_var].lower()
                                self.envs.add(args[_var])
                            elif isinstance(args[_var], list):
                                self.envs.update(args[_var])
                            elif isinstance(args[_var], int):
                                self.envs.add(args[_var])
                            else:
                                assert False, f"Unsupported parameter type of {_var} of values {args[_var]}" 
                users = [ interntx["action"]["from"].lower() for interntx in tx[INTERNAL_TRANSACTION]]
                return users, None,  None
            else:
                interntx = tx[INTERNAL_TRANSACTION][0]["action"]
                dtrace = []
                v = """msg.sender
"{0}"
1""".format(interntx["from"].lower()) 
                dtrace.append(v)
                v = """msg.value
{0}
1""".format(interntx["value"] if not interntx["value"].startswith("0x") else str(int(interntx["value"],16))) 
                dtrace.append(v)
                v = """block.timestamp
{0}
1""".format(tx["timeStamp"] if not tx["timeStamp"].startswith("0x") else str(int(tx["timeStamp"],16))) 
                dtrace.append(v)
                self.envs.add(interntx["from"].lower())
                return interntx["from"].lower(), interntx["value"], dtrace
        else:
            dtrace = []
            v = """msg.sender
"{0}"
1""".format(tx["from"].lower()) 
            dtrace.append(v)
            v = """msg.value
{0}
1""".format(tx["value"]) 
            dtrace.append(v)
            v = """block.timestamp
{0}
1""".format(tx["timeStamp"]) 
            dtrace.append(v)
            self.envs.add(tx["from"].lower())
            return tx["from"].lower(), tx["value"], dtrace

    def readAllTxs(self):
        # generate daikon traces
        statechanges = open(self.input_state_change).read().strip().split("txhash:")[1:]
        self.envs = set() 
        LIMIT = config.ParserReadTransactionLimit
        nounce = 0
        count = 0
        dtraces = []
        handled_tx_hash_set = set()
        with alive_bar(min(LIMIT, len(statechanges)), force_tty=True) as bar:
            for tx_statechange in statechanges[:min(LIMIT, len(statechanges))]:
                self.envs = set() 
                tx_hash = tx_statechange.strip().split("\n")[0]
                if tx_hash in handled_tx_hash_set:
                    bar()
                    continue
                handled_tx_hash_set.add(tx_hash)
                # print("\ntx:", tx_hash, count)
                msg_sender, msg_value, dtraceEnvs = self.readTransactionEnvironmentVariables(tx_hash)
            
                enter,exit1, exit2 = [], [], []          

                if msg_sender is not None and dtraceEnvs is not None:
                    enter, exit1, exit2, dtraceParameters, args, funcName = self.readTransactionFunctionInputVariables(tx_hash, nounce)

                if count>0:
                    nounce += 1
                
                showflag = False 
                if count>0 and len(enter)>0 and len(exit1)>0 and len(exit2)>0:
                    dtraceObjBefore = daikon.getContractDtraces(self.contractName, self)
                    showflag = True 
                
                self.envs.update(self.getAllInplaceValues())
                
                slot_statechanges = tx_statechange.strip().split("\n")[1:]
                self.txStateTransition(slot_statechanges = slot_statechanges, funcName = funcName, additionalKeys=self.envs, msg_sender=msg_sender, msg_value = msg_value, args = args, showflag=showflag, txHash= tx_hash)
        
                # Note: do not consider constructor invariant or fallback invariant
                if count>0 and len(enter)>0 and len(exit1)>0 and len(exit2)>0:
                    dtraceObjAfter = daikon.getContractDtraces(self.contractName, self)  
                    enter.extend(dtraceObjBefore)
                    enter.extend(dtraceParameters)
                    enter.extend(dtraceEnvs)
                    enter.append("\n")
                    self.tx_hash_before_after_contractStatesDataTraces[tx_hash] = [None, None, None]
                    if len(slot_statechanges)>0:
                        exit1.extend(dtraceObjAfter)
                        exit1.extend(dtraceParameters)
                        exit1.extend(dtraceEnvs)              
                        exit1.append("\n")
                        dtraces.extend(enter)
                        dtraces.extend(exit1)    
                        self.tx_hash_before_after_contractStatesDataTraces[tx_hash][0] = enter
                        self.tx_hash_before_after_contractStatesDataTraces[tx_hash][1] = exit1
                    else:
                        exit2.extend(dtraceObjAfter)
                        exit2.extend(dtraceParameters)
                        exit2.extend(dtraceEnvs)              
                        exit2.append("\n")
                        dtraces.extend(enter)
                        dtraces.extend(exit2)    
                        self.tx_hash_before_after_contractStatesDataTraces[tx_hash][0] = enter
                        self.tx_hash_before_after_contractStatesDataTraces[tx_hash][2] = exit2
                count += 1
                bar()
                if count > LIMIT:
                    break
        return dtraces

    def Daikon(self, address, workdir, full_data_trace):
        self.address = address 
        contract_invariant_file = os.path.join(os.path.dirname(full_data_trace), self.contractName+".inv")
        inferLikelyInvaraints(data_trace_file=full_data_trace, invariant_file=contract_invariant_file)
        return contract_invariant_file