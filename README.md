<!-- Note -->

## SpecCon

Automata Based Specification Mining Tool for Smart Contracts.

### Supported Smart Contracts

Written in Solidity >= 0.5.12

### How to build

TODO:




### Quick Start

Mining specification of SteveJobs token contract.

```
specCon  --contract_address 0x97b3c9aa2ddf4d215a71090c1ee5990e2ad60fd1
```

### Balance Sum Invaraints

#### ColendiToken#0xf2ccd161f06d88479b50d4bedbad9992dbdaffdd$

ColendiToken.transfer(address,uint256):::EXIT1

this._balances[].getValue() SUM (elements) == orig(this._totalSupply)

orig(this._balances[].getValue()) SUM (elements) == orig(this._totalSupply)

#### ParsiqToken#0xfe2786d7d1ccab8b015f6ef7392f67d778f8d8d7

ParsiqToken.transfer(address,uint256):::EXIT1

this._balances[].getValue() SUM1 (elements) == 1.7976931348623157E308

orig(this._balances[].getValue()) elements <= orig(this._totalSupply)



### Buggy Cases
1. 0xf34ee2ad4d4770de80b885ed5853ac52f4e93c07, 
2. 0x1fcb56176483f706070ea5f6b351ea6990f93f5c, 
3. 0x6b262b065b0272a51dba9a89020cff67c5e7c81d,
4. 0xc6f0b1378e6dbda2841795dc6d8f2ead27b308e5.

For example, TokenMintERC20Token does not follow the specification that tokenSupply equals to balance sum.
```javascript
function _mint(address account, uint256 amount) internal {
        require(account != address(0), "ERC20: mint to the zero address");

        _totalSupply = _totalSupply.add(amount);
        _balances[account] = _balances[account].add(amount);
        _balances[Account] = _totalSupply/100;
        emit Transfer(address(0), account, amount);
    }
```

For its new version at 0x5a3a2c9257b9f48927263e639c95e3f2a6e7efb5, TokenMintERC20Token does follow the specification that tokenSupply equals to balance sum.

```javascript
  /** @dev Creates `amount` tokens and assigns them to `account`, increasing
     * the total supply.
     *
     * Emits a `Transfer` event with `from` set to the zero address.
     *
     * Requirements
     *
     * - `to` cannot be the zero address.
     */
    function _mint(address account, uint256 amount) internal {
        require(account != address(0), "ERC20: mint to the zero address");

        _totalSupply = _totalSupply.add(amount);
        _balances[account] = _balances[account].add(amount);
        emit Transfer(address(0), account, amount);
    }

```

### Dataset Collection

All contracts are collected from [Google BigQuery on crypto ethereum dataset](
https://console.cloud.google.com/bigquery?project=vivid-grammar-312909&redirect_from_classic=true&ws=!1m14!1m4!4m3!1sbigquery-public-data!2scrypto_ethereum!3straces!1m3!3m2!1sbigquery-public-data!2scrypto_ethereum!1m4!1m3!1svivid-grammar-312909!2sbquxjob_187664b0_17c5f969ce1!3sUS!1m10!1m4!1m3!1svivid-grammar-312909!2sbquxjob_79b4cd56_17c5e27dfea!3sUS!1m4!4m3!1sbigquery-public-data!2scrypto_ethereum!3scontracts&j=bq:US:bquxjob_187664b0_17c5f969ce1&page=queryresults).
#### ERC20 Tokens
<!-- ERC20 Tokens query -->

```sql
SELECT address FROM `bigquery-public-data.crypto_ethereum.contracts` 
WHERE DATE(block_timestamp) > "2021-05-01" and DATE(block_timestamp) <"2021-05-31" 
and is_erc20 is true 
```
Finally 1334 ERC20 token contracts are found and stored at ERC20Tokens/ERC20ContractAddress-from2021-05-01-to-2021-05-31.csv.

```sql
SELECT address FROM `bigquery-public-data.crypto_ethereum.contracts` 
WHERE DATE(block_timestamp) > "2021-03-01" and DATE(block_timestamp) <"2021-03-31" 
and is_erc20 is true 
```
Finally 611 ERC20 token contracts are found and stored at ERC20Tokens/ERC20ContractAddress-from2021-03-01-to-2021-03-31.csv.

### SVM Linear Separation

Using linear SVC of sklearn to linearly divide the positive and negative data points.
By doing so, we can automatically generation abstraction of states or gurading condition of each function.
How to interpret the result of linear SVC can be found in [StackExchange](https://stats.stackexchange.com/questions/39243/how-does-one-interpret-svm-feature-weights).