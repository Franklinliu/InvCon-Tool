#!/usr/local/bin/node

const fs = require("fs");
const path = require('path');
const shell = require("shelljs");
const { program } = require("commander");
program.version("0.0.1");

function write2File(dir, file_name, content) {
	fs.writeFileSync(dir + "/" + file_name, content);
}

function checkSolcInstalled(version){
	const fs = require('fs');
	let installed = false;
	try {
		fs.accessSync('./node_modules/solc-'+version);
		installed = true;
	} catch (err) {
		installed = false;
	}
	return installed;
}

function installSolc(version){
		version3ids = version.split(".")
		subversion = parseInt(version3ids[1])
		smallversion = parseInt(version3ids[2])
		if (subversion<5 || (subversion==5 && smallversion <=14)){
			if (!checkSolcInstalled("0.5.14")){
				shell.exec("npm install solc-"+"0.5.14"+"@npm:solc@"+"0.5.14" + " --save");
			}
			version = "0.5.14"
			return version;
		}
		else if (subversion==5 && smallversion=="0.5.16"){
			if (!checkSolcInstalled("0.5.17")){
				shell.exec("npm install solc-"+"0.5.17"+"@npm:solc@"+"0.5.17" + " --save");
			}
			version = "0.5.17"
			return version;
		}
		else{
		    if (!checkSolcInstalled(version)){
			 	shell.exec("npm install solc-"+version+"@npm:solc@"+version + " --save");
		    }
			return version;
		}
}


function compileContract(sourcecodefile, contractname, version){
	version = installSolc(version);
	if (version.indexOf("0.4.")!=-1 || version.indexOf("0.3.")!=-1){
		let solc = require("solc-"+version);
		let input = {};
		input[contractname] = fs.readFileSync(sourcecodefile, 'utf8');
		
		compiledContract = solc.compile({
				sources: input
		}, 1);
		
		for (let key of Object.keys(compiledContract.contracts)) {
			if (key.indexOf(contractname)!=-1)
			{
				let content = compiledContract.contracts[key];
				content.sourcePath = sourcecodefile ;
				console.log(Object.keys(content))
				write2File(path.dirname(sourcecodefile), contractname + ".abi", JSON.stringify(JSON.parse(content.interface)));
				write2File(path.dirname(sourcecodefile), contractname + ".bin", content.bytecode);
				write2File(path.dirname(sourcecodefile), contractname + ".artifact", JSON.stringify(content));
				// write2File(path.dirname(sourcecodefile), "storage.json", JSON.stringify( content.storageLayout));
				break;
			}
		}
	}else{
		version3ids = version.split(".")
		subversion = parseInt(version3ids[1])
		smallversion = parseInt(version3ids[2])
		
		let input = {};
		input[contractname] = fs.readFileSync(sourcecodefile, 'utf8');
		
		console.log(version, version3ids);

		let solc;
		if (subversion==5 &&  smallversion <=14){
			solc = require("solc-"+"0.5.14");
			input[contractname] = input[contractname].replace(version, "0.5.14");
		}else if (subversion==5 &&  smallversion == 16){
			solc = require("solc-"+"0.5.17");
			input[contractname] = input[contractname].replace(version, "0.5.17");
		}
		else{
			solc = require("solc-"+version);
		}
		// let solc = require("solc-"+version);
		
		
		let standardInput = { language: "Solidity"};
		standardInput.sources = {};
		standardInput.settings = {
				optimizer:{
					enabled: true
				},
				outputSelection: {
				'*': {
				    '*': ['*'],
					"": [
						"ast" ,// Enable the AST output of every single file.
						"storageLayout"
					]
				}
				}
		};
		for (let contract of Object.keys(input)){
			standardInput.sources[contract]={
				content: input[contract]
			}
		}
		// console.log(standardInput);
		compiledContract =JSON.parse(solc.compile(JSON.stringify(standardInput)));
		// console.log(compiledContract)
		for (let source  of Object.keys(compiledContract.contracts)){

				for(let contract_name of Object.keys(compiledContract.contracts[source])){
					if (contract_name ==  contractname){
					        
							let content = compiledContract.contracts[source][contract_name];
							// console.log(Object.keys(content))
							// console.log(Object.keys(content.abi))
							// console.log(Object.keys(content.evm))
							content.sourcePath = sourcecodefile;
						
							write2File(path.dirname(sourcecodefile), contractname + ".abi", JSON.stringify(content.abi));
							// console.log(content.evm.bytecode);
							write2File(path.dirname(sourcecodefile), contractname + ".bin", JSON.stringify(content.evm.bytecode));
							write2File(path.dirname(sourcecodefile), contractname + ".artifact", JSON.stringify(content));
							write2File(path.dirname(sourcecodefile), "storage.json", JSON.stringify(content.storageLayout));
							
							break;
					}
				}
		}


	}
}

program
    .option("-s, --sourcecodefile <type>", "contract source code file")
    .option("-c, --contractname <type>", "contract name")
    .option("-n, --compilerversion <type>", "solidity compiler version")
    .parse(process.argv)
// console.log(program)

const options = program.opts()
// console.log(options)

if (options.sourcecodefile && options.contractname && options.compilerversion){
	try{
		compileContract(options.sourcecodefile, options.contractname, options.compilerversion);
	}catch{
		// TODO
	}
}

