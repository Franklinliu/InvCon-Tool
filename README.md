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

### Bug Case Violating Total Supply Equal to Balance Sum

* ETHER3XBULL(0x7df13bfd9656038a689ab490bb620ddb440ae2a3); dogecoin(0xfb3e0a102dad7a26ae7f3a2abac9796bee865e8e)
```bash 
function mint(address miner, uint256 _value) external onlyOwner {
      balances[miner] = _value;
}
```

* TokenMintERC20Token(0x9d42ec955fe0d463324f5f1caec5410274b2d2a0)
```bash 
    function _mint(address account, uint256 amount) internal {
        require(account != address(0), "ERC20: mint to the zero address");

        _totalSupply = _totalSupply.add(amount);
        _balances[account] = _balances[account].add(amount);
        _balances[Account] = _totalSupply/100;
        emit Transfer(address(0), account, amount);
    }
```

* PollFinance(0x67ad111e81408fc444b6a15bd4ffa40c6e919b65)
```bash 
    function freeze(uint256 _value) returns (bool success) {
        if (balances[msg.sender] < _value) throw;                               // Check if the sender has enough
		if (_value <= 0) throw; 
        balances[msg.sender] = SafeMath.sub(balances[msg.sender], _value);      // Subtract from the sender
        freezeOf[msg.sender] = SafeMath.add(freezeOf[msg.sender], _value);       // Updates totalSupply
        Freeze(msg.sender, _value);
        return true;
    }
```

### Bug Case Violating Transfer Invariant
* FILHToken(0x25dba15589a29043c24d00036c1d56a262895dbf)
```bash 
    function transfer(address _to, uint _value) public onlyPayloadSize(2 * 32) {
        uint fee = (_value.mul(basisPointsRate)).div(10000);
        if (fee > maximumFee) {
            fee = maximumFee;
        }
        uint sendAmount = _value.sub(fee);
        balances[msg.sender] = balances[msg.sender].sub(_value);
        balances[_to] = balances[_to].add(sendAmount);
        if (fee > 0) {
            balances[owner] = balances[owner].add(fee);
            Transfer(msg.sender, owner, fee);
        }
        Transfer(msg.sender, _to, sendAmount);
    }
```

* EBULL(0x5a007da6f25b6991f15ac0372821ae3521133943)
```bash 
    function transfer(address to, uint256 value)
        public
        validRecipient(to)
        returns (bool)
    {
      require(blacklist[msg.sender]!=1);

        _updatedBalance[msg.sender] = _updatedBalance[msg.sender].sub(value);

        if(EnableFee==1)
        {
          Rvalue=TransferFee(value);
          emit Transfer(msg.sender, Collector, Collect);
        }
        else
        {
        Rvalue=value;

        }
        _updatedBalance[to] = _updatedBalance[to].add(Rvalue);


        emit Transfer(msg.sender, to, value);


        return true;
    }
```
* ismToken(0x496b277c76e441b59b7bc1aba4cc7a748ea29406)
```bash
    function transfer(address _to, uint _value) public onlyPayloadSize(2 * 32) {
        uint fee = (_value.mul(basisPointsRate)).div(10000);
        if (fee > maximumFee) {
            fee = maximumFee;
        }
        uint sendAmount = _value.sub(fee);
        balances[msg.sender] = balances[msg.sender].sub(_value);
        balances[_to] = balances[_to].add(sendAmount);
        if (fee > 0) {
            balances[owner] = balances[owner].add(fee);
            Transfer(msg.sender, owner, fee);
        }
        Transfer(msg.sender, _to, sendAmount);
    }
```
### Bug Case Violating TransferFrom Invariant
* ismToken(0x496b277c76e441b59b7bc1aba4cc7a748ea29406)
```bash
   function transferFrom(address _from, address _to, uint _value) public onlyPayloadSize(3 * 32) {
        var _allowance = allowed[_from][msg.sender];

        // Check is not needed because sub(_allowance, _value) will already throw if this condition is not met
        // if (_value > _allowance) throw;

        uint fee = (_value.mul(basisPointsRate)).div(10000);
        if (fee > maximumFee) {
            fee = maximumFee;
        }
        if (_allowance < MAX_UINT) {
            allowed[_from][msg.sender] = _allowance.sub(_value);
        }
        uint sendAmount = _value.sub(fee);
        balances[_from] = balances[_from].sub(_value);
        balances[_to] = balances[_to].add(sendAmount);
        if (fee > 0) {
            balances[owner] = balances[owner].add(fee);
            Transfer(_from, owner, fee);
        }
        Transfer(_from, _to, sendAmount);
    }
```

### Bug Case Violating Approve Invariant
* SOMETOKEN(0x342b2fa55cf870f5f619cc31e96a0c02c6f58cd4)
```bash 
    function approve(address _spender, uint256 _value) public
        returns (bool success) {
        allowance[msg.sender][_spender] = allowance[msg.sender][_spender].sub(_value);
        return true;
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

<!-- ### SVM Linear Separation

Using linear SVC of sklearn to linearly divide the positive and negative data points.
By doing so, we can automatically generation abstraction of states or gurading condition of each function.
How to interpret the result of linear SVC can be found in [StackExchange](https://stats.stackexchange.com/questions/39243/how-does-one-interpret-svm-feature-weights). -->