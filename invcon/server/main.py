# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from os import stat
import os
from urllib import response
import urllib.parse as urlparse
import glob

from cv2 import add
MARK_LINE="==========================================================================="
hostName = '0.0.0.0'
serverPort = 8080
DEBUG = True 
cached_folders = "./Experiment"
class HandleContractAddressQuery:
    @classmethod
    def query(cls, contractAddress):
        return cls.__queryContractAddress(contractAddress)
    
    @classmethod
    def __queryContractAddress(cls, contractAddress):
        matches = glob.glob(f"{cached_folders}/*/{contractAddress}")
        if len(matches) == 0:
            return None, None, None, None  
        else:
            matches1 = glob.glob(f"{matches[0]}/*.sol")
            if len(matches1) == 0:
                return None, None, None, None 
            sourceCode =  open(matches1[0]).read()
            matches2 = glob.glob(f"{matches[0]}/*.inv")
            configs = glob.glob(f"{matches[0]}/config.json")
            assert len(configs) == 1 
            config = json.load(open(configs[0]))
            contractName, compilerVersion = config["name"], config["compiler_version"]
            # print(matches2)
            if len(matches2) == 0:
                return sourceCode, None, contractName, compilerVersion
            else:
                inv = open(matches2[0]).read()
                if inv.find(MARK_LINE) != -1:
                    return sourceCode, inv, contractName, compilerVersion
                else:
                    return sourceCode, None, contractName, compilerVersion
    @classmethod
    def __query_for_cachedresul(cls, contractAddress):

        pass     
    @classmethod
    def __query_for_etherscan(cls, contractAddress):
        pass 

class MyServer(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        headers = self.headers
        path = self.path 
        parameters = urlparse.urlparse(path)
        query =  parameters.query
        queryresult = urlparse.parse_qs(query)
        if DEBUG:
            # print(headers)
            print(path)
        print(queryresult)
        self._set_response()
        if "address" in queryresult:
            assert len(queryresult["address"]) == 1, "only accept one contract address per request"
            address = queryresult["address"][0]
            source, inv, contractName, compilerVersion = HandleContractAddressQuery.query(contractAddress=address)
            if source is None:
                # this contract has not been searched
                # so we search the contract and detect its invariant;
                # invariant detection may take some time depending on the number of smart contract transactions 
                # because we need to crawler relevant transaction information from etherscan
                cmd = "invcon --eth_address {contractAddress} --workspace ./Experiment/tmp"
                os.system(cmd)
                source, inv, contractName, compilerVersion = HandleContractAddressQuery.query(contractAddress=address)
            response_data = dict(data="hello from server", source = source, inv=inv, contractName=contractName, compilerVersion=compilerVersion)
        else:
            response_data = dict(data="hello from server")
        self.wfile.write(json.dumps(response_data).encode("utf-8"))

if __name__ == "__main__":
    webServer =  HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")