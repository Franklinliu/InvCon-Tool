#!/usr/local/bin/node

const fs = require("fs");
const spath = require('path');
const { exit } = require("process");
const shell = require("shelljs");
const { isRegExp } = require("util");

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

function write2File(dir, file_name, content) {
	if (!fs.existsSync(dir)) {
		shell.mkdir("-p", dir);
	}
	if (content)
		fs.writeFileSync(dir + "/" + file_name, content);
	else if (!fs.existsSync(dir + "/" + file_name)) {
		shell.mkdir("-p", dir + "/" + file_name);
	}
}

function compile(contractFolder, contract, out) {
	let output = {};
	let input = {};
	let version = "0.4.25";
	
	input[contract] = fs.readFileSync(spath.join(contractFolder, contract), 'utf8');
	let match =  input[contract].match(/solidity\s+(>=|>|\^)(.*);/);
	if(match){
		console.log(match[2]);
		console.log(spath.join(contractFolder, contract));
		version = match[2];
	}
	
	console.log("solidity version: ", version);
	let compiledContract ;
	if (version.indexOf("0.4")!=-1){
		// install specific solc version
		if(false == checkSolcInstalled(version))
			shell.exec("npm install solc-"+version+"@npm:solc@"+version + " --save");
			let solc = require("solc-"+version);
			compiledContract = solc.compile({
				sources: input
			}, 1);
			console.log("keys:", Object.keys(compiledContract.sources));
	}else {
		    // try new version
		    if(false == checkSolcInstalled(version))
				shell.exec("npm install solc-"+version+"@npm:solc@"+version + " --save");
			let solc = require("solc-"+version);

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
			compiledContract =JSON.parse(solc.compile(JSON.stringify(standardInput)));
			console.log(compiledContract);
			for (let source  of Object.keys(compiledContract.contracts)){
				// console.log(source, compiledContract.contracts[source]);
				let file_name = source.split(".")[0];
				console.log(source, " compiled");
				for(let contract_name of Object.keys(compiledContract.contracts[source])){
					        let dir = spath.join(__dirname, out, contract_name);
							let content = compiledContract.contracts[source][contract_name];
							content.sourcePath = spath.join(__dirname, "./" + contractFolder, file_name + ".sol");
							// console.log(content.sourcePath);
							console.log(dir);
							write2File(dir, contract_name + ".abi", JSON.stringify(content.abi));
							// console.log(content.evm.bytecode);
							write2File(dir, contract_name + ".bin", JSON.stringify(content.evm.bytecode));
							write2File(dir, contract_name + ".artifact", JSON.stringify(content));
							write2File(dir, "storage.json", JSON.stringify( content.storageLayout));
							shell.cp("-f",content.sourcePath, dir);
							output[contract_name] = content.abi;
				}
			}
			return output;
		
	}
	// console.log(compiledContract);
	for (let contract of Object.keys(compiledContract.contracts)) {
		let name = contract;
		let file_name = name.split(":")[0].split(".")[0];
		let contract_name = name.split(":")[1];
		let dir = spath.join(__dirname, out, contract_name);
		// console.log(file_name, contract_name);
		console.log(dir);
		console.log(file_name, " to compile");
		let content = compiledContract.contracts[name];
		content.sourcePath = spath.join(__dirname, contractFolder, file_name + ".sol");
		console.log(content.sourcePath);
		write2File(dir, contract_name + ".abi", JSON.stringify(JSON.parse(content.interface)));
		write2File(dir, contract_name + ".bin", content.bytecode);
		write2File(dir, contract_name + ".artifact", JSON.stringify(content));
		shell.cp("-f",content.sourcePath, dir);
		
		output[contract_name] = JSON.parse(content.interface);
	
	}
	
	console.log(output);
	return output;
}


const help = `Smart Contract Integrated Compiler by Liu Ye
		--directory	 contract directory (default "./")
		--contract smart contract file name
		--output  output directory
`;
const print = console.log;
args = process.argv.slice(2);
if (args.length==0){
	print(help);
	exit(-1);
}
// print(args);
let options = {};
options.directory = "./"
options.output = "./compiled"
for(let i=0; i<args.length;){
	try {
		switch(args[i]){
			case "--directory":{
				options.directory = args[i+1];
				i += 2;
				break;
			}
			case "--contract":{
				options.contract = args[i+1];
				i += 2;
				break;
			}
			case "--output":{
				options.output = args[i+1];
				i += 2;
				break;
			}
			default:{
				print(help);
				exit(-1);		
			}
		}
		
	} catch (error) {
		print(help);
		exit(-1);
	}
}
print(options);

compile(options.directory, options.contract, options.output)