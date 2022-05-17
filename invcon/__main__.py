import argparse
from invcon.crawler.crawler import Crawler
from invcon.crawler.crawler import BLOCKCHAIN_ETH
from invcon.daikon.main import main as daikon_main
import invcon.consts.Config as config
import os 

def execute_command(args):
    # config env
    config.DEBUG = args.debug
    config.CACHED = args.cached
    config.ParserReadTransactionLimit = args.parserReadLimit
    
    if not os.path.exists(args.workspace):
        os.makedirs(args.workspace)

    crawler = Crawler(address = args.eth_address, blockchain=args.blockchain, workdir=args.workspace)
    results = crawler.crawl()
    
   

    if not args.crawl_only:
        daikon_main(address = args.eth_address,  workdir=args.workspace,  contractName = results["name"], storageLayoutJson = results["storageLayout_file"],  input_abi = results["abi_file"],  input_state_change = results["allstatechanges_file"] ,  input_tx_receipt = results["tx_decode_file"])


def main():
    parser = argparse.ArgumentParser(description='InvCon: A Dynamic Invariant Detector for Ethereum Smart Contracts!')
    
    parser.add_argument('--eth_address', type=str, required=True, 
                        help='address of Ethereum smart contract')
    parser.add_argument('--blockchain', type=str, default = BLOCKCHAIN_ETH, 
                        help='blockchain (currently support ETH and BSC)') 
    parser.add_argument('--crawl_only', dest="crawl_only", action="store_true",
                        help='crawl only data, default is false')
    parser.add_argument('--debug', dest="debug", action="store_true",
                        help='debug mode, default is false')
    parser.add_argument('--cached', dest="cached", action="store_false",
                        help='whethere using previous result, default is true')
    parser.add_argument('--workspace', type=str, default = "./tmp", 
                        help='workspace including contract source code, invariants (default is "./tmp")')  
    parser.add_argument('--parserReadLimit', type=int, default=config.ParserReadTransactionLimit, 
                        help=f'how many method invocations are used to infer likely invariants (default is {config.ParserReadTransactionLimit})')
    args = parser.parse_args()
    execute_command(args)

if __name__ ==  "__main__":
    main()