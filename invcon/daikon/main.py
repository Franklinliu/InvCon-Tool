#!/bin/python3
import os 
import json 
import invcon.daikon.Daikon as daikon
from invcon.daikon import Contract

def main(address, workdir, contractName, storageLayoutJson, input_abi, input_state_change, input_tx_receipt):
    decls_file = os.path.join(os.path.dirname(input_tx_receipt),"daikon_decls.txt") 
    dtraces_file = os.path.join (os.path.dirname(input_tx_receipt),"daikon_dtraces.txt") 
    daikon_full_file = os.path.join(os.path.dirname(input_tx_receipt),"daikon.full.dtraces.txt") 
    
    contract =Contract.Contract(workdir, contractName, storageLayoutJson, input_abi,  input_state_change, input_tx_receipt)

    # generate daikon declarations
    g_decls = daikon.getDecl(contractName, contract, contractAbi=json.load(open(input_abi),encoding="utf8") )
    
    with open(decls_file, "w") as f:
        f.write("\n".join(g_decls))

    with open(daikon_full_file, "w") as f:
        f.write("\n".join(g_decls))


    dtraces = contract.readAllTxs()

    with open(dtraces_file, "w") as f:
        f.write("\n".join(dtraces))

    with open(daikon_full_file, "a+") as f:
        f.write("\n".join(dtraces))

    contract.printStorageVariables()
   
    contract.Daikon(address=address, workdir=workdir, full_data_trace=daikon_full_file)

    return daikon_full_file

if __name__ == "__main__":
    main()
    
    