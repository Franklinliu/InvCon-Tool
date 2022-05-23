pragma solidity ^0.4.24;

// File: openzeppelin-solidity/contracts/token/ERC20/ERC20Basic.sol

/**
 * @title ERC20Basic
 * @dev Simpler version of ERC20 interface
 * See https://github.com/ethereum/EIPs/issues/179
 */
contract ERC20Basic {
  function totalSupply() public view returns (uint256);
  function balanceOf(address _who) public view returns (uint256);
  function transfer(address _to, uint256 _value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
}

// File: openzeppelin-solidity/contracts/math/SafeMath.sol

/**
 * @title SafeMath
 * @dev Math operations with safety checks that throw on error
 */
library SafeMath {

  /**
  * @dev Multiplies two numbers, throws on overflow.
  */
  function mul(uint256 _a, uint256 _b) internal pure returns (uint256 c) {
    // Gas optimization: this is cheaper than asserting 'a' not being zero, but the
    // benefit is lost if 'b' is also tested.
    // See: https://github.com/OpenZeppelin/openzeppelin-solidity/pull/522
    if (_a == 0) {
      return 0;
    }

    c = _a * _b;
    assert(c / _a == _b);
    return c;
  }

  /**
  * @dev Integer division of two numbers, truncating the quotient.
  */
  function div(uint256 _a, uint256 _b) internal pure returns (uint256) {
    // assert(_b > 0); // Solidity automatically throws when dividing by 0
    // uint256 c = _a / _b;
    // assert(_a == _b * c + _a % _b); // There is no case in which this doesn't hold
    return _a / _b;
  }

  /**
  * @dev Subtracts two numbers, throws on overflow (i.e. if subtrahend is greater than minuend).
  */
  function sub(uint256 _a, uint256 _b) internal pure returns (uint256) {
    assert(_b <= _a);
    return _a - _b;
  }

  /**
  * @dev Adds two numbers, throws on overflow.
  */
  function add(uint256 _a, uint256 _b) internal pure returns (uint256 c) {
    c = _a + _b;
    assert(c >= _a);
    return c;
  }
}

// File: openzeppelin-solidity/contracts/token/ERC20/BasicToken.sol

/**
 * @title Basic token
 * @dev Basic version of StandardToken, with no allowances.
 */
contract BasicToken is ERC20Basic {
  using SafeMath for uint256;

  mapping(address => uint256) internal balances;

  uint256 internal totalSupply_;

  /**
  * @dev Total number of tokens in existence
  */
  function totalSupply() public view returns (uint256) {
    return totalSupply_;
  }

  /**
  * @dev Transfer token for a specified address
  * @param _to The address to transfer to.
  * @param _value The amount to be transferred.
  */
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_value <= balances[msg.sender]);
    require(_to != address(0));

    balances[msg.sender] = balances[msg.sender].sub(_value);
    balances[_to] = balances[_to].add(_value);
    emit Transfer(msg.sender, _to, _value);
    return true;
  }

  /**
  * @dev Gets the balance of the specified address.
  * @param _owner The address to query the the balance of.
  * @return An uint256 representing the amount owned by the passed address.
  */
  function balanceOf(address _owner) public view returns (uint256) {
    return balances[_owner];
  }

}

// File: openzeppelin-solidity/contracts/token/ERC20/ERC20.sol

/**
 * @title ERC20 interface
 * @dev see https://github.com/ethereum/EIPs/issues/20
 */
contract ERC20 is ERC20Basic {
  function allowance(address _owner, address _spender)
    public view returns (uint256);

  function transferFrom(address _from, address _to, uint256 _value)
    public returns (bool);

  function approve(address _spender, uint256 _value) public returns (bool);
  event Approval(
    address indexed owner,
    address indexed spender,
    uint256 value
  );
}

// File: openzeppelin-solidity/contracts/token/ERC20/StandardToken.sol

/**
 * @title Standard ERC20 token
 *
 * @dev Implementation of the basic standard token.
 * https://github.com/ethereum/EIPs/issues/20
 * Based on code by FirstBlood: https://github.com/Firstbloodio/token/blob/master/smart_contract/FirstBloodToken.sol
 */
contract StandardToken is ERC20, BasicToken {

  mapping (address => mapping (address => uint256)) internal allowed;


  /**
   * @dev Transfer tokens from one address to another
   * @param _from address The address which you want to send tokens from
   * @param _to address The address which you want to transfer to
   * @param _value uint256 the amount of tokens to be transferred
   */
  function transferFrom(
    address _from,
    address _to,
    uint256 _value
  )
    public
    returns (bool)
  {
    require(_value <= balances[_from]);
    require(_value <= allowed[_from][msg.sender]);
    require(_to != address(0));

    balances[_from] = balances[_from].sub(_value);
    balances[_to] = balances[_to].add(_value);
    allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
    emit Transfer(_from, _to, _value);
    return true;
  }

  /**
   * @dev Approve the passed address to spend the specified amount of tokens on behalf of msg.sender.
   * Beware that changing an allowance with this method brings the risk that someone may use both the old
   * and the new allowance by unfortunate transaction ordering. One possible solution to mitigate this
   * race condition is to first reduce the spender's allowance to 0 and set the desired value afterwards:
   * https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
   * @param _spender The address which will spend the funds.
   * @param _value The amount of tokens to be spent.
   */
  function approve(address _spender, uint256 _value) public returns (bool) {
    allowed[msg.sender][_spender] = _value;
    emit Approval(msg.sender, _spender, _value);
    return true;
  }

  /**
   * @dev Function to check the amount of tokens that an owner allowed to a spender.
   * @param _owner address The address which owns the funds.
   * @param _spender address The address which will spend the funds.
   * @return A uint256 specifying the amount of tokens still available for the spender.
   */
  function allowance(
    address _owner,
    address _spender
   )
    public
    view
    returns (uint256)
  {
    return allowed[_owner][_spender];
  }

  /**
   * @dev Increase the amount of tokens that an owner allowed to a spender.
   * approve should be called when allowed[_spender] == 0. To increment
   * allowed value is better to use this function to avoid 2 calls (and wait until
   * the first transaction is mined)
   * From MonolithDAO Token.sol
   * @param _spender The address which will spend the funds.
   * @param _addedValue The amount of tokens to increase the allowance by.
   */
  function increaseApproval(
    address _spender,
    uint256 _addedValue
  )
    public
    returns (bool)
  {
    allowed[msg.sender][_spender] = (
      allowed[msg.sender][_spender].add(_addedValue));
    emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }

  /**
   * @dev Decrease the amount of tokens that an owner allowed to a spender.
   * approve should be called when allowed[_spender] == 0. To decrement
   * allowed value is better to use this function to avoid 2 calls (and wait until
   * the first transaction is mined)
   * From MonolithDAO Token.sol
   * @param _spender The address which will spend the funds.
   * @param _subtractedValue The amount of tokens to decrease the allowance by.
   */
  function decreaseApproval(
    address _spender,
    uint256 _subtractedValue
  )
    public
    returns (bool)
  {
    uint256 oldValue = allowed[msg.sender][_spender];
    if (_subtractedValue >= oldValue) {
      allowed[msg.sender][_spender] = 0;
    } else {
      allowed[msg.sender][_spender] = oldValue.sub(_subtractedValue);
    }
    emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }

}

// File: contracts/SignatureUtils.sol

/// @title A library of utilities for (multi)signatures
/// @author Alexander Kern <alex@cleargraph.com>
/// @dev This library can be linked to another Solidity contract to expose signature manipulation functions.
contract SignatureUtils {

    /// @notice Converts a bytes32 to an signed message hash.
    /// @param _msg The bytes32 message (i.e. keccak256 result) to encrypt
    function toEthBytes32SignedMessageHash(
        bytes32 _msg
    )
        pure
        public
        returns (bytes32 signHash)
    {
        signHash = keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", _msg));
    }

    /// @notice Converts a byte array to a personal signed message hash (result of `web3.personal.sign(...)`) by concatenating its length.
    /// @param _msg The bytes array to encrypt
    function toEthPersonalSignedMessageHash(
        bytes _msg
    )
        pure
        public
        returns (bytes32 signHash)
    {
        signHash = keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n", uintToString(_msg.length), _msg));
    }

    /// @notice Converts a uint to its decimal string representation.
    /// @param v The uint to convert
    function uintToString(
        uint v
    )
        pure
        public
        returns (string)
    {
        uint w = v;
        bytes32 x;
        if (v == 0) {
            x = "0";
        } else {
            while (w > 0) {
                x = bytes32(uint(x) / (2 ** 8));
                x |= bytes32(((w % 10) + 48) * 2 ** (8 * 31));
                w /= 10;
            }
        }

        bytes memory bytesString = new bytes(32);
        uint charCount = 0;
        for (uint j = 0; j < 32; j++) {
            byte char = byte(bytes32(uint(x) * 2 ** (8 * j)));
            if (char != 0) {
                bytesString[charCount] = char;
                charCount++;
            }
        }
        bytes memory resultBytes = new bytes(charCount);
        for (j = 0; j < charCount; j++) {
            resultBytes[j] = bytesString[j];
        }

        return string(resultBytes);
    }

    /// @notice Extracts the r, s, and v parameters to `ecrecover(...)` from the signature at position `_pos` in a densely packed signatures bytes array.
    /// @dev Based on [OpenZeppelin's ECRecovery](https://github.com/OpenZeppelin/openzeppelin-solidity/blob/master/contracts/ECRecovery.sol)
    /// @param _signatures The signatures bytes array
    /// @param _pos The position of the signature in the bytes array (0 indexed)
    function parseSignature(
        bytes _signatures,
        uint _pos
    )
        pure
        public
        returns (uint8 v, bytes32 r, bytes32 s)
    {
        uint offset = _pos * 65;
        // The signature format is a compact form of:
        //   {bytes32 r}{bytes32 s}{uint8 v}
        // Compact means, uint8 is not padded to 32 bytes.
        assembly { // solium-disable-line security/no-inline-assembly
            r := mload(add(_signatures, add(32, offset)))
            s := mload(add(_signatures, add(64, offset)))
            // Here we are loading the last 32 bytes, including 31 bytes
            // of 's'. There is no 'mload8' to do this.
            //
            // 'byte' is not working due to the Solidity parser, so lets
            // use the second best option, 'and'
            v := and(mload(add(_signatures, add(65, offset))), 0xff)
        }

        if (v < 27) v += 27;

        require(v == 27 || v == 28);
    }

    /// @notice Counts the number of signatures in a signatures bytes array. Returns 0 if the length is invalid.
    /// @param _signatures The signatures bytes array
    /// @dev Signatures are 65 bytes long and are densely packed.
    function countSignatures(
        bytes _signatures
    )
        pure
        public
        returns (uint)
    {
        return _signatures.length % 65 == 0 ? _signatures.length / 65 : 0;
    }

    /// @notice Recovers an address using a message hash and a signature in a bytes array.
    /// @param _hash The signed message hash
    /// @param _signatures The signatures bytes array
    /// @param _pos The signature's position in the bytes array (0 indexed)
    function recoverAddress(
        bytes32 _hash,
        bytes _signatures,
        uint _pos
    )
        pure
        public
        returns (address)
    {
        uint8 v;
        bytes32 r;
        bytes32 s;
        (v, r, s) = parseSignature(_signatures, _pos);
        return ecrecover(_hash, v, r, s);
    }

    /// @notice Recovers an array of addresses using a message hash and a signatures bytes array.
    /// @param _hash The signed message hash
    /// @param _signatures The signatures bytes array
    function recoverAddresses(
        bytes32 _hash,
        bytes _signatures
    )
        pure
        public
        returns (address[] addresses)
    {
        uint8 v;
        bytes32 r;
        bytes32 s;
        uint count = countSignatures(_signatures);
        addresses = new address[](count);
        for (uint i = 0; i < count; i++) {
            (v, r, s) = parseSignature(_signatures, i);
            addresses[i] = ecrecover(_hash, v, r, s);
        }
    }

}

// File: contracts/Ownable.sol

/**
 * @title Ownable
 * @dev The Ownable contract has an owner address, and provides basic authorization control
 * functions, this simplifies the implementation of "user permissions".
 */
contract Ownable {
  address private _owner;

  event OwnershipRenounced(address indexed previousOwner);
  event OwnershipTransferred(
    address indexed previousOwner,
    address indexed newOwner
  );

  /**
   * @dev The Ownable constructor sets the original `owner` of the contract to the sender
   * account.
   */
  constructor() public {
    _owner = msg.sender;
  }

  /**
   * @return the address of the owner.
   */
  function owner() public view returns(address) {
    return _owner;
  }

  /**
   * @dev Throws if called by any account other than the owner.
   */
  modifier onlyOwner() {
    require(isOwner());
    _;
  }

  /**
   * @return true if `msg.sender` is the owner of the contract.
   */
  function isOwner() public view returns(bool) {
    return msg.sender == _owner;
  }

  /**
   * @dev Allows the current owner to relinquish control of the contract.
   * @notice Renouncing to ownership will leave the contract without an owner.
   * It will not be possible to call the functions with the `onlyOwner`
   * modifier anymore.
   */
  function renounceOwnership() public onlyOwner {
    emit OwnershipRenounced(_owner);
    _owner = address(0);
  }

  /**
   * @dev Allows the current owner to transfer control of the contract to a newOwner.
   * @param newOwner The address to transfer ownership to.
   */
  function transferOwnership(address newOwner) public onlyOwner {
    _transferOwnership(newOwner);
  }

  /**
   * @dev Transfers control of the contract to a newOwner.
   * @param newOwner The address to transfer ownership to.
   */
  function _transferOwnership(address newOwner) internal {
    require(newOwner != address(0));
    emit OwnershipTransferred(_owner, newOwner);
    _owner = newOwner;
  }
}

// File: contracts/Bridgeable.sol

contract Bridgeable is StandardToken, SignatureUtils, Ownable {
	address[] public validators;
	address public foreignContract;
	mapping (bytes32 => bool) foreignTransactions;

	event EnterBridgeEvent(address from, uint256 amount);
    event ExitBridgeEvent(address sender, uint256 amount);
    event Mint(address indexed to, uint256 amount);
	event Burn(address indexed burner, uint256 value);

    function addValidator(address _validator) public onlyOwner {
        validators.push(_validator);
    }

    function pair(address _foreignContract) public onlyOwner {
    	foreignContract = _foreignContract;
    }
        
    function enter(uint256 _amount) public {
        emit EnterBridgeEvent(msg.sender, _amount);
        burn(_amount);
    }
    
    function exit(bytes32 _txnHash, address _foreignContract, uint256 _amount, bytes _signatures) public {
    	require(contains(_txnHash) == false, 'Foreign transaction has already been processed');
        bytes32 hash = toEthBytes32SignedMessageHash(entranceHash(_txnHash,_foreignContract, _amount));
        address[] memory recovered = recoverAddresses(hash, _signatures);
        require(verifyValidators(recovered), "Validator verification failed.");
        require(_foreignContract == foreignContract, "Invalid contract target.");
        mint(msg.sender, _amount);
        foreignTransactions[_txnHash] = true;
        emit ExitBridgeEvent(msg.sender, _amount);      
    }

    function contains(bytes32 _txnHash) internal view returns (bool){
        return foreignTransactions[_txnHash];
    }

    function verifyValidators(address[] recovered) internal view returns (bool) {
        require(recovered.length == validators.length, "Invalid number of signatures");
        for(uint i = 0 ; i < validators.length; i++) {
            if(validators[i] != recovered[i]) {
                return false;
            }
        }
        return true;
    }

    function mint( address _to, uint256 _amount )
	    internal returns (bool) {
	    totalSupply_ = totalSupply_.add(_amount);
	    balances[_to] = balances[_to].add(_amount);
	    emit Mint(_to, _amount);
	    emit Transfer(address(0), _to, _amount);
	    return true;
	}

	/**
	* @dev Burns a specific amount of tokens.
	* @param _value The amount of token to be burned.
	*/
	function burn(uint256 _value) internal {
		_burn(msg.sender, _value);
	}

	function _burn(address _who, uint256 _value) internal {
		require(_value <= balances[_who]);
		// no need to require value <= totalSupply, since that would imply the
		// sender's balance is greater than the totalSupply, which *should* be an assertion failure

		balances[_who] = balances[_who].sub(_value);
		totalSupply_ = totalSupply_.sub(_value);
		emit Burn(_who, _value);
		emit Transfer(_who, address(0), _value);
	}
	    
    /**
     * @notice Hash (keccak256) of the payload used by deposit
     * @param _contractAddress the target ERC20 address
     * @param _amount the original minter
     */
    function entranceHash(bytes32 txnHash, address _contractAddress, uint256 _amount) public view returns (bytes32) {
        // "0x8177cf3c": entranceHash(bytes32, address,uint256)
        return keccak256(abi.encode( bytes4(0x8177cf3c), msg.sender, txnHash, _contractAddress, _amount));
    }

}

// File: contracts/HomeToken.sol

contract HomeToken is Bridgeable {
    string public name = "SwapMatic Token"; 
    string public symbol = "SWAM";
    uint public decimals = 18;
    uint public INITIAL_SUPPLY = 0;

    constructor() public {
        totalSupply_ = 0;
        balances[msg.sender] = 0;
    }
}