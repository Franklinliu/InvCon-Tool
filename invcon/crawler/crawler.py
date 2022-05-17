import os
import requests 
from bs4 import BeautifulSoup as soup
import pandas as pd 
import json
import time
import cloudscraper
import math
import traceback
from functools import cmp_to_key
import subprocess
import invcon.consts.Config as config
from alive_progress import alive_bar
from invcon.parsing.storageLayout import main_impl as generateStorageLayout
import shutil

scraper = cloudscraper.create_scraper(browser='chrome') # returns a CloudScraper instance
scraper.proxies = {"http": "socks5://127.0.0.1:20170", "https": "socks5://127.0.0.1:20170",
    "socks5": "socks5://127.0.0.1:20170"}
INTERNAL_TRANSACTION="internal_transactions"

TransactionThreshold = 50
def getPage(url):
    return getPage2(url)

def getPage1(url):
    resp = requests.get(url)
    body = resp.content
    return body

def getPage2(url):
    global scraper
    body = scraper.get(url).content
    return body 

def getAPIData(url):
    body = getPage(url)
    return json.loads(body.decode("utf8"))["result"]

def getLastTransaction(lasttxdate):
    days = 0
    if lasttxdate.find("days")!=-1:
        days = int(lasttxdate.split("days")[0].strip())
        # Calculate how many days ago of the last transaction
        return days
    else:
        return days 

# get traces that call contract at @address inside a external transaction
def getContractInternalTransactions(address, txHash):
        weburl = f"https://etherscan.io/vmtrace?txhash={txHash}&type=parity#raw"
        # print(soup(getPage(weburl), "html.parser").find(id="editor").text)
        page = getPage(weburl)
        internals = json.loads("["+soup(page, "html.parser").find(id="editor").text+"]") 
            # all specific function invocation to contract@address
            # notice: here we do not consider contract creaction
        contractinternaltransactions = list(filter(lambda internal: "to" in internal["action"] and internal["action"]["to"].lower() == address.lower() \
                and internal["action"]["callType"] == "call" , internals))
        return contractinternaltransactions


def getBlockTimeStamp(blockNo):
    url = f"https://api.etherscan.io/api?module=block&action=getblockreward&blockno={blockNo}&apikey={APIKEY_BLOCKCHAIN_ETH}"
    # url = f"https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&tag={hex(blockNo)}&boolean=false&apikey={APIKEY_BLOCKCHAIN_ETH}"
    block = getAPIData(url)
    timeStamp = block["timeStamp"]
    return timeStamp

def getExternalTxHasInternalTransactions(address, internal_transaction_hashes):
    global scraper
    transaction_hashes = set()
    count = 1 
    pageLimit = None 
    transactions = []
    try:
        if internal_transaction_hashes is None:
            while pageLimit is None or count <= pageLimit:
                url = "https://etherscan.io/txsInternal?a={0}&m=advanced&p={1}".format(address, count)
                page = getPage(url)
                page_soup = soup(page, "lxml")
                card_bodys = page_soup.find_all("div", class_="card-body")
                for card_body in card_bodys:
                    divs = card_body.find_all("div")
                    if pageLimit is None:
                        try:
                            lessthan10k = divs[0].find_all("span", class_="d-block")[0].text.find("Showing the last 10k records only")==-1
                        except:
                            # traceback.print_exc()
                            lessthan10k = True
                            pass 
                        pageLimit = int(divs[0].find_all("nav")[0].find_all("li")[2].text.split("of")[-1].strip())
                        if not lessthan10k:
                            print("too many internal transactions")
                            # os._exit(os.EX_OK)
                            assert False, ValueError("too many internal transactions (greater than 10k shown by etherscan.io)")
                        
                    records = divs[1].find_all("tbody")[0].find_all("tr")
                    for record in records:
                        # print(record.find_all("td", class_="bg-light")[0])
                        txhash = record.find_all("td", class_="bg-light")[0].find_all("a")[0].text  
                        transaction_hashes.add(txhash)
                count += 1
            transaction_hashes = list(transaction_hashes)
        else:
            transaction_hashes = list(internal_transaction_hashes)
        print(len(transaction_hashes), " internal txs to crawl...")
        # if len(transaction_hashes)>1000:
        #     transaction_hashes = transaction_hashes[:1000]

        try:
            with alive_bar(len(transaction_hashes), force_tty=True) as bar:
                for txhash in transaction_hashes:
                    url = "https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={0}&apikey={1}".format(txhash, APIKEY_BLOCKCHAIN_ETH)
                    count = 0 
                    while True:
                        count += 1
                        if count > 3:
                            raise Exception("timeout")
                        try:
                                tx = getAPIData(url)
                                # time.sleep(0.1)
                                tx["timeStamp"] = tx["blockNumber"]
                                #  getBlockTimeStamp(int(tx["blockNumber"]) if not tx["blockNumber"].startswith("0x") else int(tx["blockNumber"], 16))
                                tx["type"] = INTERNAL_TRANSACTION
                                tx[INTERNAL_TRANSACTION] = getContractInternalTransactions(address, txhash)
                                transactions.append(tx)
                                # time.sleep(0.1)
                                break 
                        except Exception as e:
                                print(e)
                                time.sleep(30*count)
                                scraper = cloudscraper.create_scraper()
                                continue 
                    bar()
        except Exception as e:
            print(e)
        return transactions
    except:
        traceback.print_exc()
        return transactions

def mergeTransactions(external_transactions: list, internal_transactions: list):
    def compare(item1, item2):
        if isinstance(item1["blockNumber"], str):
            if item1["blockNumber"].startswith("0x"):
                b1 = int(item1["blockNumber"], 16)
                item1["blockNumber"] = str(b1)
            else:
                b1 = int(item1["blockNumber"], 10)
        else:
            b1 = int(item1["blockNumber"])

        if isinstance(item2["blockNumber"], str):
            if item2["blockNumber"].startswith("0x"):
                b2 = int(item2["blockNumber"], 16)
                item2["blockNumber"] = str(b2)
            else:
                b2 = int(item2["blockNumber"], 10)
        else:
            b2 = int(item2["blockNumber"])
        

        if isinstance(item1["transactionIndex"], str):
            if item1["transactionIndex"].startswith("0x"):
                i1 = int(item1["transactionIndex"], 16)
                item1["transactionIndex"] = i1
            else:
                i1 = int(item1["transactionIndex"], 10)
        else:
            i1 = int(item1["transactionIndex"])

        if isinstance(item2["transactionIndex"], str):
            if item2["transactionIndex"].startswith("0x"):
                i2 = int(item2["transactionIndex"], 16)
                item2["transactionIndex"] = i2
            else:
                i2 = int(item2["transactionIndex"], 10)
        else:
            i2 = int(item2["transactionIndex"])
        
        if b1>b2 or (b1==b2 and i1>i2):
            return 1
        else:
            return -1

    transactions = external_transactions + internal_transactions
    
    transactions.sort(key=cmp_to_key(compare), reverse=False)

    # it's possible that the first internal transaction is the contract creation
    # so we need to deduplicate the transactions
    if len(transactions)>2 and transactions[0]["hash"] ==  transactions[1]["hash"]:
        transactions = transactions[1:]
    
    print(f"Internal message calls (except fallback function): {len(transactions) - len(external_transactions)}")

    return transactions

def checkSelfDestructed(htmlbody):
    hasSelfDestructed = False
    if str(htmlbody).find("Self Destruct")!=-1:
        hasSelfDestructed = True
    
    print("Self Destruct: ", hasSelfDestructed)
    return hasSelfDestructed

def getETHHtmlBody(address):
    body = ""
    url = "https://etherscan.io/address/{0}".format(address)
    body = getPage(url)
    page_soup = soup(body, "html.parser")  
    body = page_soup
    title = page_soup.title.text
    print(title)
    for link in page_soup.find_all('a'):
        if link.get("title")=="Click to view full list":
            # print(link)
            # print(link.text)
            transactionNo = int(link.text.replace(",",""))
    body = page_soup.prettify()
    Transfers_info_table_1 = page_soup.find("div", {"class": "table-responsive"})
    df = pd.read_html(str(Transfers_info_table_1))[0]

    name, compiler_version, optimization, othersetting = tuple([div.text.strip() for div in page_soup.find_all("div", {"class": "col-7 col-lg-8"})])
    print(name, compiler_version, optimization, othersetting)
    divs = page_soup.select(".mb-4 ")
    # print(divs)
    arguments = "" 
    for div in divs:
        h4s = div.select("div h4")
        if len(h4s)>0:
            h4 = h4s[0]
            if h4 is not None and h4.text.find("Constructor Arguments")!=-1:
                arguments = div.select("div pre")[0].text.split("-----Decoded View---------------")[0]
                print(arguments)
                break    
    last_tx_date = df.iloc[0, 4]    
    is_killed = checkSelfDestructed(body)
    return is_killed, title, transactionNo, last_tx_date, name, compiler_version, optimization, othersetting, arguments

def getBSCHtmlBody(address):
    body = ""
    url = "https://bscscan.com/address/{0}".format(address)
    body = getPage(url)
    page_soup = soup(body, "html.parser")  
    body = page_soup
    title = page_soup.title.text
    print(title)
    for link in page_soup.find_all('a'):
        if link.get("title")=="Click to view full list":
            # print(link)
            # print(link.text)
            transactionNo = int(link.text.replace(",",""))
    body = page_soup.prettify()
    Transfers_info_table_1 = page_soup.find("div", {"class": "table-responsive"})
    df = pd.read_html(str(Transfers_info_table_1))[0]

    name, compiler_version, optimization, othersetting = tuple([div.text.strip() for div in page_soup.find_all("div", {"class": "col-7 col-lg-8"})])
    print(name, compiler_version, optimization, othersetting)
    divs = page_soup.select(".mb-4 ")
    # print(divs)
    arguments = "" 
    for div in divs:
        h4s = div.select("div h4")
        if len(h4s)>0:
            h4 = h4s[0]
            if h4 is not None and h4.text.find("Constructor Arguments")!=-1:
                arguments = div.select("div pre")[0].text.split("-----Decoded View---------------")[0]
                print(arguments)
                break    
    last_tx_date = df.iloc[0, 4]    
    is_killed = checkSelfDestructed(body)
    return is_killed, title, transactionNo, last_tx_date, name, compiler_version, optimization, othersetting, arguments


BLOCKCHAIN_ETH = "ETH"
BLOCKCHAIN_BSC = "BSC"

APIKEY_BLOCKCHAIN_ETH = "URF6R5PGNZ7CT6TTBU7M8NH5V8WRISHIZZ"
APIKEY_BLOCKCHAIN_BSC = "A4YZESUAIA4IGXSBK8D4NYQMUBMWTVAXN9"

WEBPAGE_FUNC_BLOCKCAHIN_ETH = getETHHtmlBody
WEBPAGE_FUNC_BLOCKCHAIN_BSC = getBSCHtmlBody

APIENDPOINT_BLOCKCHAIN_ETH = "https://api.etherscan.io/api"
APIENDPOINT_BLOCKCHAIN_BSC = "https://api.bscscan.com/api"

SOURCECODE_API_BLOCKCHAIN_ETH = "module=contract&action=getsourcecode&address={0}&apikey={1}"
SOURCECODE_API_BLOCKCHAIN_BSC = "module=contract&action=getsourcecode&address={0}&apikey={1}"

TXS_API_BLOCKCHAIN_ETH = "module=account&action=txlist&address={0}&startblock={1}&endblock=99999999&sort=asc&apikey={2}"
TXS_API_BLOCKCHAIN_BSC =  "module=account&action=txlist&address={0}&startblock={1}&endblock=99999999&sort=asc&apikey={2}"

ABI_API_BLOCKCHAIN_ETH = "module=contract&action=getabi&address={0}&apikey={1}"
ABI_API_BLOCKCHAIN_BSC = "module=contract&action=getabi&address={0}&apikey={1}"

ETH_GETTRANSACTION_ETH="module=proxy&action=eth_getTransactionByHash&txhash={0}&apikey={1}"

Benchmark_csv_file = "./benchmark.csv"

class Crawler:
    def __init__(self, address, blockchain, workdir="./"):
        self.address = address
        workdir = os.path.abspath(workdir)
        # self.workdir = os.path.join(workdir, "./crawler")
        self.workdir = workdir
        if not os.path.exists(self.workdir):
            os.mkdir(self.workdir)
        if blockchain == BLOCKCHAIN_ETH:
            self.api_key = APIKEY_BLOCKCHAIN_ETH
            self.apiendpoint = APIENDPOINT_BLOCKCHAIN_ETH
            self.source_api = SOURCECODE_API_BLOCKCHAIN_ETH
            self.txs_api = TXS_API_BLOCKCHAIN_ETH
            self.abi_api = ABI_API_BLOCKCHAIN_ETH
            self.webpage_func = WEBPAGE_FUNC_BLOCKCAHIN_ETH
            self.tx_api = ETH_GETTRANSACTION_ETH
        elif blockchain == BLOCKCHAIN_BSC:
            self.api_key = APIKEY_BLOCKCHAIN_BSC
            self.apiendpoint = APIENDPOINT_BLOCKCHAIN_BSC
            self.source_api = SOURCECODE_API_BLOCKCHAIN_BSC
            self.txs_api = TXS_API_BLOCKCHAIN_BSC
            self.abi_api = ABI_API_BLOCKCHAIN_BSC
            self.webpage_func = WEBPAGE_FUNC_BLOCKCAHIN_ETH
        self.addressdir = f"{self.workdir}/{self.address}"
    
    
    def readLocalSource(self):
        if config.CACHED and os.path.exists(f"{self.addressdir}/config.json"):
            return True, json.load(open(f"{self.addressdir}/config.json"))
        else:
            return False, None
           
    def saveLocal(self, dictobj):
        json.dump(dictobj, open(f"{self.addressdir}/config.json", "w"), indent=6)
          

    def getSourceCode(self):
        url = self.apiendpoint+"?"+self.source_api.format(self.address, self.api_key)
        sourcecode = getAPIData(url)
        # There is some case that a lot of source code files are provided
        # TODO 
        contractName = sourcecode[0]["ContractName"]
        compilerVersion = sourcecode[0]["CompilerVersion"]
        constructorArguments = sourcecode[0]["ConstructorArguments"]

        sourcecode = "\n".join([ contract["SourceCode"] for contract in sourcecode ])
        assert isinstance(sourcecode, str), "Error in source code; either network error or source code is unavailable!"
        with open(f"{self.addressdir}/{self.address}.sol", "w") as f:
            f.write(sourcecode.encode("charmap", "ignore").decode("utf8", "ignore"))
        return contractName, compilerVersion, constructorArguments, f"{self.addressdir}/{self.address}.sol"

    def getABI(self):
        url = self.apiendpoint+"?"+self.abi_api.format(self.address, self.api_key)
        abi = getAPIData(url)
        assert isinstance(abi, str), "Error in abi; either network error or abi is unavailable!"
        with open(f"{self.addressdir}/{self.address}.abi", "w") as f:
            f.write(str(abi))
        return f"{self.addressdir}/{self.address}.abi"

    def getTxsFromBitQueryResult(self, transactionsByBigQuery_file):
        transactionsByBigQuery = json.load(open(transactionsByBigQuery_file))
        all_transactions = []
        for transaction in transactionsByBigQuery:
            txhash = transaction["hash"]
            external = transaction["external"]
            url = self.apiendpoint+"?"+self.tx_api.format(txhash, self.api_key)
            transaction = getAPIData(url)
            transaction["isExternalContractCall"] = external
            all_transactions.append(transaction)
        
        with open(f"{self.addressdir}/txs.json", "w") as f:
                f.write(json.dumps(all_transactions))
        return f"{self.addressdir}/txs.json"
        
    # only use at most 10,000 txs for specification mining
    # we target the transactions in the earliest 180 days of deployed smart contracts
    def getTxs(self, transactionNo, arguments=""):
        if config.CACHED and os.path.exists(f"{self.addressdir}/txs.json"):
            return f"{self.addressdir}/txs.json"
        all_transaction_hashes =  None
        LIMIT = config.TransactionMaxCrawl
        if os.path.exists(f"{self.addressdir}/180dtxs.csv"):
            all_transaction_hashes =  list() 
            _all_transaction_hashes = open(f"{self.addressdir}/180dtxs.csv").readlines()[1:]
            if len(_all_transaction_hashes)>LIMIT:
                _all_transaction_hashes = _all_transaction_hashes[:LIMIT]
            for  tx_hash in _all_transaction_hashes:
                if tx_hash.strip() not in all_transaction_hashes:
                    all_transaction_hashes.append(tx_hash.strip())
        if transactionNo > LIMIT:
            transactionNo = LIMIT
        startblock = 0
        url = self.apiendpoint+"?"+self.txs_api.format(self.address, startblock, self.api_key)
        transactions = []
        cnt = 0
        while cnt < math.ceil(transactionNo/10000):
            ttransactions = getAPIData(url)
            if len(ttransactions) >0:
                startblock = str(int(ttransactions[-1]["blockNumber"])+1)
                cnt = cnt+1
                transactions.extend(ttransactions)
                for transaction in ttransactions:
                    tx_hash = transaction["hash"]
                    if all_transaction_hashes is not None and tx_hash.strip().lower() in all_transaction_hashes:
                        all_transaction_hashes.remove(tx_hash.strip().lower())
                url = self.apiendpoint+"?"+self.txs_api.format(self.address, startblock, self.api_key)
            else:
                break
        transactions[0]["input"]=arguments
        if len(transactions) > transactionNo:
            transactions = transactions[:transactionNo]
        internal_transactions = getExternalTxHasInternalTransactions(self.address, internal_transaction_hashes=all_transaction_hashes)
        transactions = mergeTransactions(transactions, internal_transactions=internal_transactions)
        if len(transactions)>LIMIT:
            transactions = transactions[:LIMIT]
        # print(transactions)
        with open(f"{self.addressdir}/txs.json", "w") as f:
                f.write(json.dumps(transactions))
        return f"{self.addressdir}/txs.json"
  
    def crawl(self):
        if os.path.exists(self.addressdir):
            boolflag, results = self.readLocalSource()
            if boolflag:
                nodejs_dir = "/home/liuye/Projects/InvCon/invcon/nodejs"
                cmd = f'cd {nodejs_dir} && node decodeTx.js --abi {results["abi_file"]} --tx {results["transactions_file"]} --output {os.path.join(os.path.dirname(results["transactions_file"]), "tx_decode.json")}'
                os.system(cmd)
                assert os.path.exists(os.path.join(os.path.dirname(results["transactions_file"]), "tx_decode.json")), "Decoding error: failed to decode transactions"
                results["tx_decode_file"] = os.path.join(os.path.dirname(results["transactions_file"]), "tx_decode.json") 
                return results 
        if not os.path.exists(self.addressdir):
            os.mkdir(self.addressdir)
        try:
            results = dict()
            contractName, compilerVersion, constructorArguments, sourcecode = self.getSourceCode()
            if contractName is None or compilerVersion is None or contractName == "" or compilerVersion == "":
                shutil.rmtree(self.addressdir)
                with open(os.path.dirname(self.addressdir)+"/sourceCodeNotAvailable.txt", "a") as f:
                    f.write(self.address)
                    f.write("\n")
                exit(-1)
            results["sourcecode_file"] = sourcecode
            results["name"] = contractName
            results["compiler_version"] = compilerVersion
            results["arguments"] = constructorArguments
            abi = self.getABI()
            results["abi_file"] = abi
            txs = self.getTxs(transactionNo=config.TransactionMaxCrawl, arguments="0x"+results["arguments"])
            results["transactions_file"] = txs 
            
            # decode txs
            nodejs_dir ="/home/liuye/Projects/InvCon/invcon/nodejs"
            tx_decode_file = os.path.join(os.path.dirname(results["transactions_file"]), "tx_decode.json")
            cmd = f'cd {nodejs_dir} && node decodeTx.js --abi {results["abi_file"]} --tx {results["transactions_file"]} --output {tx_decode_file}'
            os.system(cmd)
            if not os.path.exists(tx_decode_file):
                shutil.rmtree(self.addressdir)
                with open(os.path.dirname(self.addressdir)+"/sourceCodeNotAvailable.txt", "a") as f:
                    f.write(self.address)
                    f.write("\n")
                exit(-1)
            assert os.path.exists(tx_decode_file), "Decoding error: failed to decode transactions"
            results["tx_decode_file"] = tx_decode_file
            
            # get state changes
            allstatechanges_file = self.crawlStateChange4AllTxs(results["transactions_file"])
            results["allstatechanges_file"] = allstatechanges_file 
            results["storageLayout_file"] = os.path.join(os.path.dirname(results["sourcecode_file"]), "storage.json")
            # compile sourcecode to get storage file
            generateStorageLayout(sol_file= results["sourcecode_file"], contractName=results["name"], compilerVersion=results["compiler_version"], outStorageFile=results["storageLayout_file"])
            assert os.path.exists(results["storageLayout_file"]), "Compiling error: failed to create storage.json"
            self.saveLocal(results)
            return results
        except:
            traceback.print_exc()
            exit(-1)

    def crawlStateChange4Tx(self, txhash):
        global scraper
        url = f"https://etherscan.io/accountstatediff?m=normal&a={txhash}" 
        count = 0
        while True: 
            count +=  1
            if count > 3:
                raise Exception("timeout")
            try:
                html = getPage(url)
                page_soup = soup(html, features="lxml")
                break 
            except:
                print(url)
                scraper = cloudscraper.create_scraper() # returns a CloudScraper instance
                time.sleep(30*count)
                continue
        # print(page_soup)
        statechanges = list([f"txhash:{txhash}"])
        targetdivs = page_soup.find_all("tr", id = f"tr_{self.address.lower()}")

        for targetdiv in targetdivs:
            divs = targetdiv.find_all("div", class_ = "dl-space bg-light rounded border p-3 mb-2")
            for div in divs:
                dds = div.find_all("dd", class_="col-md-10 mb-0")
                storage, before, afer = tuple(dds)
                slot = storage.string 
                oldval = before.find_all("span", class_="text-monospace text-break")[0].string
                newval = afer.find_all("span", class_="text-monospace text-break")[0].string
                # print(slot, newval)
                statechanges.append(":".join([slot, oldval+"-"+newval]))
        # add separation space
        return statechanges 

    def crawlStateChange4AllTxs(self, transaction_file):
        assert os.path.exists(transaction_file), "txs is not downloaded"
        if config.CACHED and os.path.exists(f"{self.addressdir}/statechanges.txt"):
            return f"{self.addressdir}/statechanges.txt"
        with open(transaction_file) as f:
            allstatechanges4alltxs = list()
            txJsonObject = json.load(f)
            if "result" in txJsonObject:
                txJsonObject = txJsonObject["result"]
            LIMIT = config.StateChangeMaxCrawl
            print("crawl contract state changes along transactions...")
            try:
                count = 0 
                with alive_bar(min(LIMIT, len(txJsonObject)), force_tty=True) as bar:
                    for tx in txJsonObject:
                        txhash = tx["hash"]
                        allstatechanges4alltxs.extend(self.crawlStateChange4Tx(txhash))
                        count += 1
                        time.sleep(0.2)
                        bar()
                        if count>=LIMIT:
                            break
            except Exception as e:
                print(e)

            with open(f"{self.addressdir}/statechanges.txt", "w") as fo:
                fo.write("\n".join(allstatechanges4alltxs))
            return f"{self.addressdir}/statechanges.txt"

def main():
    # contract_address = "0x00b113a5570a046c60ac8cfa4983b1dc1c780629"
    contract_address =  "0xF34eE2AD4d4770dE80b885ED5853AC52f4E93c07"
    crawler = Crawler(address=contract_address, blockchain=BLOCKCHAIN_ETH)
    results = crawler.crawl()
    print(results)

def testInternalTransactions():
    contract_address = "0xF34eE2AD4d4770dE80b885ED5853AC52f4E93c07"
    txhashes = getExternalTxHasInternalTransactions(contract_address)
    print(txhashes)

if __name__ == "__main__":
    print("Hello world.")
    main()
    # testInternalTransactions()
