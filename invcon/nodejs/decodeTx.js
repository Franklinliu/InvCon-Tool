const fs = require("fs");
const web3 = require("web3-eth-abi");
const { program } = require("commander");
const { count } = require("console");
program.version("0.0.1");

var HashMethodMap = new Map();

function loadABI(abi_file){
    let count = 0;
    let ABIs = JSON.parse(fs.readFileSync(abi_file));
    for (let abi of ABIs){
        if((false == abi.constant|| "view"!=abi.stateMutability) && abi.type == "function"){
            
            let hash = web3.encodeFunctionSignature(abi);
            HashMethodMap[hash] = abi;

        }else if (abi.type=="constructor"){

            HashMethodMap["constructor"] = abi;
        }

        else if (abi.type == "event" && abi.name == "DigitalMediaCreateEvent")
        {
            createDigitalEvent = abi;
            createDigitalTopic = web3.encodeEventSignature(createDigitalEvent);
        }
    }
    HashMethodMap["0x"] = {name: "fallback", inputs: null };
    // console.log(HashMethodMap)
    // console.log(ABIs)
}
var INTERNAL_TRANSACTION="internal_transactions"
function filter(tx_file, tx_o_file){
    // if (fs.existsSync(tx_o_file))
    //     return;
    let json = JSON.parse(fs.readFileSync(tx_file));
    
    if (json.result)
        json = json.result; 
    json = {result: json};
    var count = 0 
    for(let tx of json.result.slice(0)){
        if (count==0 &&  tx.type==INTERNAL_TRANSACTION){
            // count++;
            continue
        }
        // console.log(HashMethodMap,  HashMethodMap[tx.input.substring(0,10)])
        if (count==0){
            try{
            tx.decoded = {function: "constructor",  args:  web3.decodeParameters(HashMethodMap["constructor"].inputs, tx.input)}
            }catch(error){
                tx.decoded = {function: "constructor",  args: tx.input}
            }
            // console.log(tx)
        }
        else{
            // console.log(tx.input.substring(0,10))
            if (tx.input == "0x"){
                tx.decoded = {function: HashMethodMap[tx.input].name,  args: []}
            }else{
                try {
                    tx.decoded = {function: HashMethodMap[tx.input.substring(0,10)].name,  args: web3.decodeParameters(HashMethodMap[tx.input.substring(0,10)].inputs, "0x"+tx.input.slice(10))}    
                } catch (error) {
                    tx.decoded = {function: tx.input.substring(0,10),  args: "0x"+tx.input.slice(10)}
                }
                
            }
        }

        if (tx.type == INTERNAL_TRANSACTION){
            for (let interntx of tx.internal_transactions){
                if (interntx.input == "0x"){
                    interntx.decoded = {function: HashMethodMap[interntx.action.input].name,  args: []}
                }else{
                    try {
                        interntx.decoded = {function: HashMethodMap[interntx.action.input.substring(0,10)].name,  args: web3.decodeParameters(HashMethodMap[interntx.action.input.substring(0,10)].inputs, "0x"+interntx.action.input.slice(10))}    
                    } catch (error) {
                        interntx.decoded = {function: interntx.action.input.substring(0,10),  args: "0x"+interntx.action.input.slice(10)}
                    }
                }
            }
        }


        count ++
    }

    fs.writeFileSync(tx_o_file, JSON.stringify(json))
}

program
    .option("-a, --abi <type>", "contract abi file")
    .option("-t, --tx <type>", "contract tx file")
    .option("-o, --output <type>", "output file containing decoded txs")
    .parse(process.argv)

// console.log(program)
const options = program.opts()
console.log(options)

if (options.abi && options.tx && options.output){
    // loadABI("./demo/GameChannel.abi")
    // filter("./demo/tx.json", "./demo/tx_decode.json");
    loadABI(options.abi);
    filter(options.tx, options.output);
}

