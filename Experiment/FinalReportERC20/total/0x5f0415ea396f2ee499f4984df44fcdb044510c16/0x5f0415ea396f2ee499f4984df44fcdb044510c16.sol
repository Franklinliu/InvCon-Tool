/**
 *Submitted for verification at Etherscan.io on 2020-06-02
*/

pragma solidity ^0.4.18;

/**
 * @title ERC20Basic
 * @dev Simpler version of ERC20 interface
 * @dev see https://github.com/ethereum/EIPs/issues/179
 */
contract ERC20Basic {
  uint256 public totalSupply;
  function balanceOf(address who) public view returns (uint256);
  function transfer(address to, uint256 value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
}


/**
 * @title SafeMath
 * @dev Math operations with safety checks that throw on error
 */
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    assert(c / a == b);
    return c;
  }

  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    // assert(b > 0); // Solidity automatically throws when dividing by 0
    uint256 c = a / b;
    // assert(a == b * c + a % b); // There is no case in which this doesn't hold
    return c;
  }

  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }

  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}


/**
 * @title Basic token
 * @dev Basic version of StandardToken, with no allowances.
 */
contract BasicToken is ERC20Basic {
  using SafeMath for uint256;

  mapping(address => uint256) balances;

  /**
  * @dev transfer token for a specified address
  * @param _to The address to transfer to.
  * @param _value The amount to be transferred.
  */
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= balances[msg.sender]);

    // SafeMath.sub will throw if there is not enough balance.
    balances[msg.sender] = balances[msg.sender].sub(_value);
    balances[_to] = balances[_to].add(_value);
    Transfer(msg.sender, _to, _value);
    return true;
  }

  /**
  * @dev Gets the balance of the specified address.
  * @param _owner The address to query the the balance of.
  * @return An uint256 representing the amount owned by the passed address.
  */
  function balanceOf(address _owner) public view returns (uint256 balance) {
    return balances[_owner];
  }

}


/**
 * @title ERC20 interface
 * @dev see https://github.com/ethereum/EIPs/issues/20
 */
contract ERC20 is ERC20Basic {
  function allowance(address owner, address spender) public view returns (uint256);
  function transferFrom(address from, address to, uint256 value) public returns (bool);
  function approve(address spender, uint256 value) public returns (bool);
  event Approval(address indexed owner, address indexed spender, uint256 value);
}


/**
 * @title Standard ERC20 token
 *
 * @dev Implementation of the basic standard token.
 * @dev https://github.com/ethereum/EIPs/issues/20
 * @dev Based on code by FirstBlood: https://github.com/Firstbloodio/token/blob/master/smart_contract/FirstBloodToken.sol
 */
contract StandardToken is ERC20, BasicToken {

  mapping (address => mapping (address => uint256)) internal allowed;


  /**
   * @dev Transfer tokens from one address to another
   * @param _from address The address which you want to send tokens from
   * @param _to address The address which you want to transfer to
   * @param _value uint256 the amount of tokens to be transferred
   */
  function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= balances[_from]);
    require(_value <= allowed[_from][msg.sender]);

    balances[_from] = balances[_from].sub(_value);
    balances[_to] = balances[_to].add(_value);
    allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
    Transfer(_from, _to, _value);
    return true;
  }

  /**
   * @dev Approve the passed address to spend the specified amount of tokens on behalf of msg.sender.
   *
   * Beware that changing an allowance with this method brings the risk that someone may use both the old
   * and the new allowance by unfortunate transaction ordering. One possible solution to mitigate this
   * race condition is to first reduce the spender's allowance to 0 and set the desired value afterwards:
   * https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
   * @param _spender The address which will spend the funds.
   * @param _value The amount of tokens to be spent.
   */
  function approve(address _spender, uint256 _value) public returns (bool) {
    allowed[msg.sender][_spender] = _value;
    Approval(msg.sender, _spender, _value);
    return true;
  }

  /**
   * @dev Function to check the amount of tokens that an owner allowed to a spender.
   * @param _owner address The address which owns the funds.
   * @param _spender address The address which will spend the funds.
   * @return A uint256 specifying the amount of tokens still available for the spender.
   */
  function allowance(address _owner, address _spender) public view returns (uint256) {
    return allowed[_owner][_spender];
  }

  /**
   * @dev Increase the amount of tokens that an owner allowed to a spender.
   *
   * approve should be called when allowed[_spender] == 0. To increment
   * allowed value is better to use this function to avoid 2 calls (and wait until
   * the first transaction is mined)
   * From MonolithDAO Token.sol
   * @param _spender The address which will spend the funds.
   * @param _addedValue The amount of tokens to increase the allowance by.
   */
  function increaseApproval(address _spender, uint _addedValue) public returns (bool) {
    allowed[msg.sender][_spender] = allowed[msg.sender][_spender].add(_addedValue);
    Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }

  /**
   * @dev Decrease the amount of tokens that an owner allowed to a spender.
   *
   * approve should be called when allowed[_spender] == 0. To decrement
   * allowed value is better to use this function to avoid 2 calls (and wait until
   * the first transaction is mined)
   * From MonolithDAO Token.sol
   * @param _spender The address which will spend the funds.
   * @param _subtractedValue The amount of tokens to decrease the allowance by.
   */
  function decreaseApproval(address _spender, uint _subtractedValue) public returns (bool) {
    uint oldValue = allowed[msg.sender][_spender];
    if (_subtractedValue > oldValue) {
      allowed[msg.sender][_spender] = 0;
    } else {
      allowed[msg.sender][_spender] = oldValue.sub(_subtractedValue);
    }
    Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
    return true;
  }

}


/**
 * @title Ownable
 * @dev The Ownable contract has an owner address, and provides basic authorization control
 * functions, this simplifies the implementation of "user permissions".
 */
contract Ownable {
    address public owner;
    address public newOwner;


    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);


    /**
     * @dev The Ownable constructor sets the original `owner` of the contract to the sender
     * account.
     */
    function Ownable() public {
        owner = msg.sender;
    }


    /**
     * @dev Throws if called by any account other than the owner.
     */
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }


    /**
     * @dev Allows the current owner to transfer control of the contract to a newOwner.
     * @param _newOwner The address to transfer ownership to.
     */
    function transferOwnership(address _newOwner) public onlyOwner {
        require(_newOwner != address(0));
        OwnershipTransferred(owner, _newOwner);
        newOwner = _newOwner;
    } 

    /**
     * @dev     
     */
    function acceptOwnership() public {
        require(msg.sender == newOwner);
        
        OwnershipTransferred(owner, newOwner);
        owner = newOwner;
        newOwner = address(0);
    }
}


/**
 * @title ACCAToken

 * @dev ACCA  
 */
contract ACCAToken is StandardToken, Ownable {
    //  
    string public constant name = "ACCA";
    
    //  
    string public constant symbol = "ACCA";
    
    //  . ETH 18 
    uint8 public constant decimals = 18;
    
    //  /    
    mapping (address => LockedInfo) public lockedWalletInfo;
    
    /**
     * @dev      
     */
    mapping (address => bool) public manoContracts;
    
    
    /**
     * @dev     
     * 
     * @param timeLockUpEnd timeLockUpEnd  /   .   
     * @param sendLock   (true : , false : )
     * @param receiveLock    (true : , false : )
     */
    struct LockedInfo {
        uint timeLockUpEnd;
        bool sendLock;
        bool receiveLock;
    } 
    
    
    /**
     * @dev     
     * @param from    
     * @param to    
     * @param value    (Satoshi)
     */
    event Transfer (address indexed from, address indexed to, uint256 value);
    
    /**
     * @dev   /     
     * @param target    
     * @param timeLockUpEnd   (UnixTimestamp)
     * @param sendLock    (true : , false : )
     * @param receiveLock     (true : , false : )
     */
    event Locked (address indexed target, uint timeLockUpEnd, bool sendLock, bool receiveLock);
    
    /**
     * @dev   /     
     * @param target    
     */
    event Unlocked (address indexed target);
    
    /**
     * @dev          
     * @param from    
     * @param to ( )    
     * @param value    (Satoshi)
     */
    event RejectedPaymentToLockedUpWallet (address indexed from, address indexed to, uint256 value);
    
    /**
     * @dev         
     * @param from ( )    
     * @param to    
     * @param value    (Satoshi)
     */
    event RejectedPaymentFromLockedUpWallet (address indexed from, address indexed to, uint256 value);
    
    /**
     * @dev  . 
     * @param burner    
     * @param value   (Satoshi)
     */
    event Burn (address indexed burner, uint256 value);
    
    /**
     * @dev          
     */
    event ManoContractRegistered (address manoContract, bool registered);
    
    /**
     * @dev    .      .
     *       
     */
    function ACCAToken() public {
        //  ACCA  (1)
        uint256 supplyACCA = 1000000000;
        
        // wei    .
        totalSupply = supplyACCA * 10 ** uint256(decimals);
        
        balances[msg.sender] = totalSupply;
        
        Transfer(0x0, msg.sender, totalSupply);
    }
    
    
    /**
     * @dev     .      .
     * @param _targetWallet    
     * @param _timeLockEnd   (UnixTimestamp)
     * @param _sendLock (true :     .) (false :  )
     * @param _receiveLock (true :     .) (false :  )
     */
    function walletLock(address _targetWallet, uint _timeLockEnd, bool _sendLock, bool _receiveLock) onlyOwner public {
        require(_targetWallet != 0x0);
        
        // If all locks are unlocked, set the _timeLockEnd to zero.
        if(_sendLock == false && _receiveLock == false) {
            _timeLockEnd = 0;
        }
        
        lockedWalletInfo[_targetWallet].timeLockUpEnd = _timeLockEnd;
        lockedWalletInfo[_targetWallet].sendLock = _sendLock;
        lockedWalletInfo[_targetWallet].receiveLock = _receiveLock;
        
        if(_timeLockEnd > 0) {
            Locked(_targetWallet, _timeLockEnd, _sendLock, _receiveLock);
        } else {
            Unlocked(_targetWallet);
        }
    }
    
    /**
     * @dev  /   .      .
     * @param _targetWallet    
     * @param _timeLockUpEnd   (UnixTimestamp)
     */
    function walletLockBoth(address _targetWallet, uint _timeLockUpEnd) onlyOwner public {
        walletLock(_targetWallet, _timeLockUpEnd, true, true);
    }
    
    /**
     * @dev  / (33658-9-27 01:46:39+00) .
     * @param _targetWallet    
     */
    function walletLockBothForever(address _targetWallet) onlyOwner public {
        walletLock(_targetWallet, 999999999999, true, true);
    }
    
    
    /**
     * @dev     
     * @param _targetWallet     
     */
    function walletUnlock(address _targetWallet) onlyOwner public {
        walletLock(_targetWallet, 0, false, false);
    }
    
    /**
     * @dev     .
     * @param _addr      
     * @return isSendLocked (true :  ,    ) (false :  ,    )
     * @return until  , UnixTimestamp
     */
    function isWalletLocked_Send(address _addr) public constant returns (bool isSendLocked, uint until) {
        require(_addr != 0x0);
        
        isSendLocked = (lockedWalletInfo[_addr].timeLockUpEnd > now && lockedWalletInfo[_addr].sendLock == true);
        
        if(isSendLocked) {
            until = lockedWalletInfo[_addr].timeLockUpEnd;
        } else {
            until = 0;
        }
    }
    
    /**
     * @dev     .
     * @param _addr      
     * @return (true :  ,    ) (false :  ,    )
     */
    function isWalletLocked_Receive(address _addr) public constant returns (bool isReceiveLocked, uint until) {
        require(_addr != 0x0);
        
        isReceiveLocked = (lockedWalletInfo[_addr].timeLockUpEnd > now && lockedWalletInfo[_addr].receiveLock == true);
        
        if(isReceiveLocked) {
            until = lockedWalletInfo[_addr].timeLockUpEnd;
        } else {
            until = 0;
        }
    }
    
    /**
     * @dev      .
     * @return (true :  ,    ) (false :  ,    )
     */
    function isMyWalletLocked_Send() public constant returns (bool isSendLocked, uint until) {
        return isWalletLocked_Send(msg.sender);
    }
    
    /**
     * @dev      .
     * @return (true :  ,    ) (false :  ,    )
     */
    function isMyWalletLocked_Receive() public constant returns (bool isReceiveLocked, uint until) {
        return isWalletLocked_Receive(msg.sender);
    }
    
    
    /**
     * @dev        .
     * @param manoAddr   
     * @param registered true : , false : 
     */
    function registerManoContract(address manoAddr, bool registered) onlyOwner public {
        manoContracts[manoAddr] = registered;
        
        ManoContractRegistered(manoAddr, registered);
    }
    
    
    /**
     * @dev _to  _accaWei   .
     * @param _to    
     * @param _accaWei   
     */
    function transfer(address _to, uint256 _accaWei) public returns (bool) {
        //    
        require(_to != address(this));
        
        //   , APIS    
        if(manoContracts[msg.sender] || manoContracts[_to]) {
            return super.transfer(_to, _accaWei);
        }
        
        //     .
        if(lockedWalletInfo[msg.sender].timeLockUpEnd > now && lockedWalletInfo[msg.sender].sendLock == true) {
            RejectedPaymentFromLockedUpWallet(msg.sender, _to, _accaWei);
            return false;
        } 
        //      
        else if(lockedWalletInfo[_to].timeLockUpEnd > now && lockedWalletInfo[_to].receiveLock == true) {
            RejectedPaymentToLockedUpWallet(msg.sender, _to, _accaWei);
            return false;
        } 
        //   ,  .
        else {
            return super.transfer(_to, _accaWei);
        }
    }
    
    /**
     * @dev _to  _accaWei  ACCA  _timeLockUpEnd   
     * @param _to    
     * @param _accaWei   (wei)
     * @param _timeLockUpEnd   
     */
    function transferAndLockUntil(address _to, uint256 _accaWei, uint _timeLockUpEnd) onlyOwner public {
        require(transfer(_to, _accaWei));
        
        walletLockBoth(_to, _timeLockUpEnd);
    }
    
    /**
     * @dev _to  _accaWei  APIS   
     * @param _to    
     * @param _accaWei   (wei)
     */
    function transferAndLockForever(address _to, uint256 _accaWei) onlyOwner public {
        require(transfer(_to, _accaWei));
        
        walletLockBothForever(_to);
    }
    
    
    /**
     * @dev     .
     * 
     * zeppelin-solidity/contracts/token/BurnableToken.sol 
     * @param _value   (Satoshi)
     */
    function burn(uint256 _value) public {
        require(_value <= balances[msg.sender]);
        require(_value <= totalSupply);
        
        address burner = msg.sender;
        balances[burner] -= _value;
        totalSupply -= _value;
        
        Burn(burner, _value);
    }
    
    
    /**
     * @dev Eth    .
     */
    function () public payable {
        revert();
    }
}








/**
 * @title WhiteList
 * @dev ICO     
 */
contract WhiteList is Ownable {
    
    mapping (address => uint8) internal list;
    
    /**
     * @dev     
     * @param backer    
     * @param allowed (true :  ) (false : )
     */
    event WhiteBacker(address indexed backer, bool allowed);
    
    
    /**
     * @dev   .
     * @param _target    
     * @param _allowed (true :  ) (false : ) 
     */
    function setWhiteBacker(address _target, bool _allowed) onlyOwner public {
        require(_target != 0x0);
        
        if(_allowed == true) {
            list[_target] = 1;
        } else {
            list[_target] = 0;
        }
        
        WhiteBacker(_target, _allowed);
    }
    
    /**
     * @dev   ()
     * @param _target   
     */
    function addWhiteBacker(address _target) onlyOwner public {
        setWhiteBacker(_target, true);
    }
    
    /**
     * @dev       .
     * 
     *    
     * @param _backers    
     * @param _allows       (true : ) (false : )
     */
    function setWhiteBackersByList(address[] _backers, bool[] _allows) onlyOwner public {
        require(_backers.length > 0);
        require(_backers.length == _allows.length);
        
        for(uint backerIndex = 0; backerIndex < _backers.length; backerIndex++) {
            setWhiteBacker(_backers[backerIndex], _allows[backerIndex]);
        }
    }
    
    /**
     * @dev     .
     * 
     *    .
     * @param _backers    
     */
    function addWhiteBackersByList(address[] _backers) onlyOwner public {
        for(uint backerIndex = 0; backerIndex < _backers.length; backerIndex++) {
            setWhiteBacker(_backers[backerIndex], true);
        }
    }
    
    
    /**
     * @dev       
     * @param _addr     
     * @return (true : ) (false :  )
     */
    function isInWhiteList(address _addr) public constant returns (bool) {
        require(_addr != 0x0);
        return list[_addr] > 0;
    }
    
    /**
     * @dev     .
     * @return (true : ) (false :  )
     */
    function isMeInWhiteList() public constant returns (bool isWhiteBacker) {
        return list[msg.sender] > 0;
    }
}



/**
 * @title APIS Crowd Pre-Sale
 * @dev     
 */
contract ACCACrowdSale is Ownable {
    
    //  . Eth 18 
    uint8 public constant decimals = 18;
    
    
    //    (APIS)
    uint256 public fundingGoal;
    
    //     
    // QTUM    ,  QTUM          
    uint256 public fundingGoalCurrent;
    
    // 1 ETH    APIS 
    uint256 public priceOfApisPerFund;
    

    //  Apis  ( + )
    //uint256 public totalSoldApis;
    
    //   APIS 
    //uint256 public totalReservedApis;
    
    //   APIS 
    //uint256 public totalWithdrawedApis;
    
    
    //    ( + )
    //uint256 public totalReceivedFunds;
    
    //     
    //uint256 public totalReservedFunds;
    
    //    
    //uint256 public totalPaidFunds;

    
    //   
    uint public startTime;
    
    //   
    uint public endTime;

    //      
    bool closed = false;
    
	SaleStatus public saleStatus;
    
    // APIS  
    ACCAToken internal tokenReward;
    
    //  
    WhiteList internal whiteList;

    
    
    mapping (address => Property) public fundersProperty;
    
    /**
     * @dev APIS       
     */
    struct Property {
        uint256 reservedFunds;   //   APIS   Eth ( )
        uint256 paidFunds;    	// APIS  Eth ( )
        uint256 reservedApis;   //   
        uint256 withdrawedApis; //   
        uint purchaseTime;      //  
    }
	
	
	/**
	 * @dev       .
	 * totalSoldApis  Apis  ( + )
	 * totalReservedApis    Apis
	 * totalWithdrawedApis   APIS 
	 * 
	 * totalReceivedFunds    ( + )
	 * totalReservedFunds     
	 * ttotalPaidFunds    
	 */
	struct SaleStatus {
		uint256 totalReservedFunds;
		uint256 totalPaidFunds;
		uint256 totalReceivedFunds;
		
		uint256 totalReservedApis;
		uint256 totalWithdrawedApis;
		uint256 totalSoldApis;
	}
    
    
    
    /**
     * @dev APIS   Eth    
     * @param beneficiary APIS    
     * @param amountOfFunds  Eth  (wei)
     * @param amountOfApis   APIS   (wei)
     */
    event ReservedApis(address beneficiary, uint256 amountOfFunds, uint256 amountOfApis);
    
    /**
     * @dev    Eth    
     * @param addr   
     * @param amount  (wei)
     */
    event WithdrawalFunds(address addr, uint256 amount);
    
    /**
     * @dev      
     * @param funder    
     * @param amountOfFunds    (wei)
     * @param amountOfApis     (wei)
     */
    event WithdrawalApis(address funder, uint256 amountOfFunds, uint256 amountOfApis);
    
    
    /**
     * @dev   ,     ,      
     * @param _backer     
     * @param _amountFunds   
     * @param _amountApis  APIS 
     */
    event Refund(address _backer, uint256 _amountFunds, uint256 _amountApis);
    
    
    /**
     * @dev      , APIS   .
     */
    modifier onSale() {
        require(now >= startTime);
        require(now < endTime);
        require(closed == false);
        require(priceOfApisPerFund > 0);
        require(fundingGoalCurrent > 0);
        _;
    }
    
    /**
     * @dev      
     */
    modifier onFinished() {
        require(now >= endTime || closed == true);
        _;
    }
    
    /**
     * @dev         .
     */
    modifier claimable() {
        require(whiteList.isInWhiteList(msg.sender) == true);
        require(fundersProperty[msg.sender].reservedFunds > 0);
        _;
    }
    
    
    /**
     * @dev    .
     * @param _fundingGoalApis    (APIS )
     * @param _startTime    
     * @param _endTime    
     * @param _addressOfVilTokenUsedAsReward APIS   
     * @param _addressOfWhiteList WhiteList  
     */
    function ApisCrowdSale (
        uint256 _fundingGoalApis,
        uint _startTime,
        uint _endTime,
        address _addressOfVilTokenUsedAsReward,
        address _addressOfWhiteList
    ) public {
        require (_fundingGoalApis > 0);
        require (_startTime > now);
        require (_endTime > _startTime);
        require (_addressOfVilTokenUsedAsReward != 0x0);
        require (_addressOfWhiteList != 0x0);
        
        fundingGoal = _fundingGoalApis * 10 ** uint256(decimals);
        
        startTime = _startTime;
        endTime = _endTime;
        
        //   
        tokenReward = ACCAToken(_addressOfVilTokenUsedAsReward);
        
        //   
        whiteList = WhiteList(_addressOfWhiteList);
    }
    
    /**
     * @dev   1  .        
     */
    function closeSale(bool _closed) onlyOwner public {
        require (closed == false);
        
        closed = _closed;
    }
    
    /**
     * @dev     1Eth  APIS  .
     */
    function setPriceOfApis(uint256 price) onlyOwner public {
        require(priceOfApisPerFund == 0);
        
        priceOfApisPerFund = price;
    }
    
    /**
     * @dev      .
     * @param _currentFundingGoalAPIS         .
     */
    function setCurrentFundingGoal(uint256 _currentFundingGoalAPIS) onlyOwner public {
        uint256 fundingGoalCurrentWei = _currentFundingGoalAPIS * 10 ** uint256(decimals);
        require(fundingGoalCurrentWei >= saleStatus.totalSoldApis);
        
        fundingGoalCurrent = fundingGoalCurrentWei;
    }
    
    
    /**
     * @dev APIS  
     * @param _addr    
     * @return balance   APIS  (wei)
     */
    function balanceOf(address _addr) public view returns (uint256 balance) {
        return tokenReward.balanceOf(_addr);
    }
    
    /**
     * @dev    
     * @param _addr    
     * @return addrIsInWhiteList true : , false :  
     */
    function whiteListOf(address _addr) public view returns (string message) {
        if(whiteList.isInWhiteList(_addr) == true) {
            return "The address is in whitelist.";
        } else {
            return "The address is *NOT* in whitelist.";
        }
    }
    
    
    /**
     * @dev   APIS    .
     * @param _addr  
     * @return message  
     */
    function isClaimable(address _addr) public view returns (string message) {
        if(fundersProperty[_addr].reservedFunds == 0) {
            return "The address has no claimable balance.";
        }
        
        if(whiteList.isInWhiteList(_addr) == false) {
            return "The address must be registered with KYC and Whitelist";
        }
        
        else {
            return "The address can claim APIS!";
        }
    }
    
    
    /**
     * @dev       , buyToken 
     */
    function () onSale public payable {
        buyToken(msg.sender);
    }
    
    /**
     * @dev    Qtum .
     * @param _beneficiary     
     */
    function buyToken(address _beneficiary) onSale public payable {
        //  
        require(_beneficiary != 0x0);
        
        //         
        bool isLocked = false;
        uint timeLock = 0;
        (isLocked, timeLock) = tokenReward.isWalletLocked_Send(this);
        
        require(isLocked == false);
        
        
        uint256 amountFunds = msg.value;
        uint256 reservedApis = amountFunds * priceOfApisPerFund;
        
        
        //     
        require(saleStatus.totalSoldApis + reservedApis <= fundingGoalCurrent);
        require(saleStatus.totalSoldApis + reservedApis <= fundingGoal);
        
        //   
        fundersProperty[_beneficiary].reservedFunds += amountFunds;
        fundersProperty[_beneficiary].reservedApis += reservedApis;
        fundersProperty[_beneficiary].purchaseTime = now;
        
        //  
        saleStatus.totalReceivedFunds += amountFunds;
        saleStatus.totalReservedFunds += amountFunds;
        
        saleStatus.totalSoldApis += reservedApis;
        saleStatus.totalReservedApis += reservedApis;
        
        
        //    
        if(whiteList.isInWhiteList(_beneficiary) == true) {
            withdrawal(_beneficiary);
        }
        else {
            //     
            ReservedApis(_beneficiary, amountFunds, reservedApis);
        }
    }
    
    
    
    /**
     * @dev    .     
     * 
     * @param _target     
     */
    function claimApis(address _target) public {
        //    
        require(whiteList.isInWhiteList(_target) == true);
        //    .
        require(fundersProperty[_target].reservedFunds > 0);
        
        withdrawal(_target);
    }
    
    /**
     * @dev      .
     * 
     * APIS   Qtum  ,    7  .
     *       .
     */
    function claimMyApis() claimable public {
        withdrawal(msg.sender);
    }
    
    
    /**
     * @dev   .
     * @param funder    
     */
    function withdrawal(address funder) internal {
        //    
        assert(tokenReward.transferFrom(owner, funder, fundersProperty[funder].reservedApis));
        
        fundersProperty[funder].withdrawedApis += fundersProperty[funder].reservedApis;
        fundersProperty[funder].paidFunds += fundersProperty[funder].reservedFunds;
        
        //  
        saleStatus.totalReservedFunds -= fundersProperty[funder].reservedFunds;
        saleStatus.totalPaidFunds += fundersProperty[funder].reservedFunds;
        
        saleStatus.totalReservedApis -= fundersProperty[funder].reservedApis;
        saleStatus.totalWithdrawedApis += fundersProperty[funder].reservedApis;
        
        // APIS    
        WithdrawalApis(funder, fundersProperty[funder].reservedFunds, fundersProperty[funder].reservedApis);
        
        //   APIS  0 , Qtum         .
        fundersProperty[funder].reservedFunds = 0;
        fundersProperty[funder].reservedApis = 0;
    }
    
    
    /**
     * @dev      ,    .
     * @param _funder    
     */
    function refundByOwner(address _funder) onlyOwner public {
        require(fundersProperty[_funder].reservedFunds > 0);
        
        uint256 amountFunds = fundersProperty[_funder].reservedFunds;
        uint256 amountApis = fundersProperty[_funder].reservedApis;
        
        // Eth 
        _funder.transfer(amountFunds);
        
        saleStatus.totalReceivedFunds -= amountFunds;
        saleStatus.totalReservedFunds -= amountFunds;
        
        saleStatus.totalSoldApis -= amountApis;
        saleStatus.totalReservedApis -= amountApis;
        
        fundersProperty[_funder].reservedFunds = 0;
        fundersProperty[_funder].reservedApis = 0;
        
        Refund(_funder, amountFunds, amountApis);
    }
    
    
    /**
     * @dev   ,   .
     * @param remainRefundable true :      . false :  
     */
    function withdrawalFunds(bool remainRefundable) onlyOwner public {
        require(now > endTime || closed == true);
        
        uint256 amount = 0;
        if(remainRefundable) {
            amount = this.balance - saleStatus.totalReservedFunds;
        } else {
            amount = this.balance;
        }
        
        if(amount > 0) {
            msg.sender.transfer(amount);
            
            WithdrawalFunds(msg.sender, amount);
        }
    }
    
    /**
	 * @dev      .
	 * @return isOpened true:   false :   ( )
	 */
    function isOpened() public view returns (bool isOpend) {
        if(now < startTime) return false;
        if(now >= endTime) return false;
        if(closed == true) return false;
        
        return true;
    }
}