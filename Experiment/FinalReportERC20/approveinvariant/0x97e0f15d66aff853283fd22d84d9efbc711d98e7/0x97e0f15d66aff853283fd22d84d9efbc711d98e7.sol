pragma solidity ^0.4.17;

contract Token{
    uint256 public totalSupply;

    function balanceOf(address _owner) public constant returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns   
    (bool success);

    function approve(address _spender, uint256 _value) public returns (bool success);

    function allowance(address _owner, address _spender) public constant returns 
    (uint256 remaining);

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 
    _value);
}

contract Nnbtoken is Token {

    string public name;                 
    uint8 public decimals;              
    string public symbol;             
 
	mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
	
	function Nnbtoken() public {
        balances[msg.sender] = 50000000000000000; // Give the creator all initial tokens
        totalSupply = 50000000000000000;                        // Update total supply
        name = "Niuniubtc";                                   // Set the name for display purposes
        symbol = "Nnb";                             // Set the symbol for display purposes
        decimals = 8;                            // Amount of decimals for display purposes
    }

    function transfer(address _to, uint256 _value) public returns (bool success) { 
        require(balances[msg.sender] >= _value && balances[_to] + _value > balances[_to]);
        require(_to != 0x0);
        balances[msg.sender] -= _value;// 
        balances[_to] += _value;//token_value0 
        Transfer(msg.sender, _to, _value);//
        return true;
    }


    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(balances[_from] >= _value && allowed[_from][msg.sender] >= _value);
        balances[_to] += _value;//token_value
        balances[_from] -= _value; //_fromtoken_value
        allowed[_from][msg.sender] -= _value;//_from_value
        Transfer(_from, _to, _value);//
        return true;
    }
    function balanceOf(address _owner) public constant returns (uint256 balance) {
        return balances[_owner];
    }


    function approve(address _spender, uint256 _value) public returns (bool success)   
    { 
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }

    function allowance(address _owner, address _spender) public constant returns (uint256 remaining) {
        return allowed[_owner][_spender];//_spender_ownertoken
    }

}