export const CoverState = "States";
export const CoverTransition = "Transitions-Without-Loop";
export const CoverTransitionLoop = "Transitions-With-Loop";
export const BCOS_SUCCESS_STATUS = 0;


export const CMA_normal = `const assert = require("assert");
const hex2ascii = require('hex2ascii')
const Machine = require("xstate").Machine;
const createModel = require("@xstate/test").createModel;
const  EXPIRE_CREDIT = 400;
const  CLEAR_CREDIT = 500;
const  CLOSE_CREDIT = 600;
let asyncFlag = false;
const MAX_COUNT = 60;

function revertAsyncFlag() {
asyncFlag = !asyncFlag;
}


// contract interface 

class CreditController {
constructor(fuzzer) {
  this.address = "0xa7b692824ac1ff30f01c325ec7498005ee13e0bc";
  this.name = "CreditController";
  this.fuzzer = fuzzer;
}

async getCreditAddressByCreditNo() {
  let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "getCreditAddressByCreditNo");
  return fuzz;
}

async transferAndDiscountCheck() {
  let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "transferAndDiscountCheck");
  return fuzz;
}

async transferCredit() {
  let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "transferCredit");
  return fuzz;
}

async staticArrayToDynamicArray() {
  let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "staticArrayToDynamicArray");
  return fuzz;
}

async accountIsOk() {
  let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "accountIsOk");
  return fuzz;
}

async expireOrClearOrCloseCredit(option) {
  let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "expireOrClearOrCloseCredit", option);
  return fuzz;
}

async discountCredit() {
  let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "discountCredit");
  return fuzz;
}

async state() {
  let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "state");
  return fuzz;
}

async createCredit() {
  let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "createCredit");
  return fuzz;
}

}
// state machine context
class StateMachineCtx {
constructor(fsmreplayer, fuzzer) {
  this.CreditController = new CreditController(fuzzer);

  this.state = {
    "id": "FSM#1"
  };
  this.fuzzer = fuzzer;
  this.fsmreplayer = fsmreplayer;
}
async initialize() {
  this.CreditController.address = await this.fsmreplayer.initialize();
}
static getInstance(fsmreplayer, fuzzer) {
  if (!StateMachineCtx.instance)
    StateMachineCtx.instance = new StateMachineCtx(fsmreplayer, fuzzer);
  return StateMachineCtx.instance;
}
async getState() {
  //TO DO, set what your state means and how to get the state
  if (this.CreditController.state) {
    let ret = await this.CreditController.state();
    this.state = BigInt(ret.receipt.result.output.toString());
  } else if (this.CreditController.stage) {
    let ret = await this.CreditController.stage();
    this.state = BigInt(ret.receipt.result.output.toString());
  } else {
    this.state = null;
  }
  console.log("state:", this.state);
  return this.state;
}
// action_functions_mapping
async action_create() {
  let ret = [];
  if (asyncFlag) {
    // bcos passed status:0
    let executeStatus = BigInt(0);
    let ctx = StateMachineCtx.getInstance();
    let count = 0;
    // PreCondition. 
    let preState = await ctx.getState();
    assert(null == preState || preState == 0, "preCondition violated: current state is " + preState);

    let retcreateCredit = await StateMachineCtx.getInstance().CreditController.createCredit();
    ret.push(retcreateCredit);
    console.log("current test case: ", BigInt(retcreateCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
    executeStatus += BigInt(retcreateCredit.receipt.status.toString());
    while (executeStatus != 0 && count < MAX_COUNT) {
      count++;
      executeStatus = BigInt(0);
      let retcreateCredit = await StateMachineCtx.getInstance().CreditController.createCredit();
      ret.push(retcreateCredit);
      console.log("current test case: ", BigInt(retcreateCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
      executeStatus += BigInt(retcreateCredit.receipt.status.toString());
    }

    if (count >= MAX_COUNT) {
      throw "TIMEOUT,  too many failed test cases!";
    }
    let postState = await ctx.getState();
    assert(null == postState || postState == 1, "postCondition violated: current state is " + postState);
    // PostCondition. 
  }
  return ret;
}
async action_discount() {
  let ret = [];
  if (asyncFlag) {
    // bcos passed status:0
    let executeStatus = BigInt(0);
    let ctx = StateMachineCtx.getInstance();
    let count = 0;
    // PreCondition. 
    let preState = await ctx.getState();
    assert(null == preState || preState == 1, "preCondition violated: current state is " + preState);

    let retdiscountCredit = await StateMachineCtx.getInstance().CreditController.discountCredit();
    ret.push(retdiscountCredit);
    console.log("current test case: ", BigInt(retdiscountCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
    executeStatus += BigInt(retdiscountCredit.receipt.status.toString());
    while (executeStatus != 0 && count < MAX_COUNT) {
      count++;
      executeStatus = BigInt(0);
      let retdiscountCredit = await StateMachineCtx.getInstance().CreditController.discountCredit();
      ret.push(retdiscountCredit);
      console.log("current test case: ", BigInt(retdiscountCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
      executeStatus += BigInt(retdiscountCredit.receipt.status.toString());
    }

    if (count >= MAX_COUNT) {
      throw "TIMEOUT,  too many failed test cases!";
    }
    let postState = await ctx.getState();
    assert(null == postState || postState == 2, "postCondition violated: current state is " + postState);
    // PostCondition. 
  }
  return ret;
}
async action_transfer() {
  let ret = [];
  if (asyncFlag) {
    // bcos passed status:0
    let executeStatus = BigInt(0);
    let ctx = StateMachineCtx.getInstance();
    let count = 0;
    // PreCondition. 
    let preState = await ctx.getState();
    assert(null == preState || preState == 1, "preCondition violated: current state is " + preState);

    let rettransferCredit = await StateMachineCtx.getInstance().CreditController.transferCredit();
    ret.push(rettransferCredit);
    console.log("current test case: ", BigInt(rettransferCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
    executeStatus += BigInt(rettransferCredit.receipt.status.toString());
    while (executeStatus != 0 && count < MAX_COUNT) {
      count++;
      executeStatus = BigInt(0);
      let rettransferCredit = await StateMachineCtx.getInstance().CreditController.transferCredit();
      ret.push(rettransferCredit);
      console.log("current test case: ", BigInt(rettransferCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
      executeStatus += BigInt(rettransferCredit.receipt.status.toString());
    }

    if (count >= MAX_COUNT) {
      throw "TIMEOUT,  too many failed test cases!";
    }
    let postState = await ctx.getState();
    assert(null == postState || postState == 1, "postCondition violated: current state is " + postState);
    // PostCondition. 
  }
  return ret;
}
async action_expire() {
  let ret = [];
  if (asyncFlag) {
    // bcos passed status:0
    let executeStatus = BigInt(0);
    let ctx = StateMachineCtx.getInstance();
    let count = 0;
    // PreCondition. 
    let preState = await ctx.getState();
    assert(null == preState || preState == 1 || preState == 2, "preCondition violated: current state is " + preState);

    let retexpireOrClearOrCloseCredit = await StateMachineCtx.getInstance().CreditController.expireOrClearOrCloseCredit({static:[{index:3, value:EXPIRE_CREDIT}]});
    ret.push(retexpireOrClearOrCloseCredit);
    console.log("current test case: ", BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
    executeStatus += BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString());
    while (executeStatus != 0 && count < MAX_COUNT) {
      count++;
      executeStatus = BigInt(0);
      let retexpireOrClearOrCloseCredit = await StateMachineCtx.getInstance().CreditController.expireOrClearOrCloseCredit({static:[{index:3, value:EXPIRE_CREDIT}]});
      ret.push(retexpireOrClearOrCloseCredit);
      console.log("current test case: ", BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
      executeStatus += BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString());
    }

    if (count >= MAX_COUNT) {
      throw "TIMEOUT,  too many failed test cases!";
    }
    let postState = await ctx.getState();
    assert(null == postState || postState == 3 || postState == 3, "postCondition violated: current state is " + postState);
    // PostCondition. 
  }
  return ret;
}
async action_close() {
  let ret = [];
  if (asyncFlag) {
    // bcos passed status:0
    let executeStatus = BigInt(0);
    let ctx = StateMachineCtx.getInstance();
    let count = 0;
    // PreCondition. 
    let preState = await ctx.getState();
    assert(null == preState || preState == 1 || preState == 2, "preCondition violated: current state is " + preState);

    let retexpireOrClearOrCloseCredit = await StateMachineCtx.getInstance().CreditController.expireOrClearOrCloseCredit({static:[{index:3, value:CLOSE_CREDIT}]});
    ret.push(retexpireOrClearOrCloseCredit);
    console.log("current test case: ", BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
    executeStatus += BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString());
    while (executeStatus != 0 && count < MAX_COUNT) {
      count++;
      executeStatus = BigInt(0);
      let retexpireOrClearOrCloseCredit = await StateMachineCtx.getInstance().CreditController.expireOrClearOrCloseCredit({static:[{index:3, value:CLOSE_CREDIT}]});
      ret.push(retexpireOrClearOrCloseCredit);
      console.log("current test case: ", BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
      executeStatus += BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString());
    }

    if (count >= MAX_COUNT) {
      throw "TIMEOUT,  too many failed test cases!";
    }
    let postState = await ctx.getState();
    assert(null == postState || postState == 5 || postState == 5, "postCondition violated: current state is " + postState);
    // PostCondition. 
  }
  return ret;
}
async action_clear() {
  let ret = [];
  if (asyncFlag) {
    // bcos passed status:0
    let executeStatus = BigInt(0);
    let ctx = StateMachineCtx.getInstance();
    let count = 0;
    // PreCondition. 
    let preState = await ctx.getState();
    assert(null == preState || preState == 1 || preState == 2, "preCondition violated: current state is " + preState);

    let retexpireOrClearOrCloseCredit = await StateMachineCtx.getInstance().CreditController.expireOrClearOrCloseCredit({static:[{index:3, value:CLEAR_CREDIT}]});
    ret.push(retexpireOrClearOrCloseCredit);
    console.log("current test case: ", BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
    executeStatus += BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString());
    while (executeStatus != 0 && count < MAX_COUNT) {
      count++;
      executeStatus = BigInt(0);
      let retexpireOrClearOrCloseCredit = await StateMachineCtx.getInstance().CreditController.expireOrClearOrCloseCredit({static:[{index:3, value:CLEAR_CREDIT}]});
      ret.push(retexpireOrClearOrCloseCredit);
      console.log("current test case: ", BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
      executeStatus += BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString());
    }

    if (count >= MAX_COUNT) {
      throw "TIMEOUT,  too many failed test cases!";
    }
    let postState = await ctx.getState();
    assert(null == postState || postState == 4 || postState == 4, "postCondition violated: current state is " + postState);
    // PostCondition. 
  }
  return ret;
}
}
// state machine 
const createStateMachine = statectx => {
return Machine({
  id: "FSM#1",
  initial: "initial",
  context: {
    ctx: statectx
  },
  states: {

    initial: {
      on: {
        create: {
          target: "CREATED",
          actions: "action_create"
        }
      }
    },
    CREATED: {
      on: {
        transfer: {
          target: "CREATED",
          actions: "action_transfer"
        },
        discount: {
          target: "DISCOUNTED",
          actions: "action_discount"
        },
        expire: {
          target: "EXPIRED",
          actions: "action_expire"
        },
        clear: {
          target: "CLEARED",
          actions: "action_clear"
        },
        close: {
          target: "CLOSED",
          actions: "action_close"
        }
      }
    },
    DISCOUNTED: {
      on: {
        expire: {
          target: "EXPIRED",
          actions: "action_expire"
        },
        clear: {
          target: "CLEARED",
          actions: "action_clear"
        },
        close: {
          target: "CLOSED",
          actions: "action_close"
        }
      }
    },
    EXPIRED: {
      type: "final"
    },
    CLEARED: {
      type: "final"
    },
    CLOSED: {
      type: "final"
    }
  }
}, {
  actions: {
    action_create: statectx.action_create,
    action_discount: statectx.action_discount,
    action_transfer: statectx.action_transfer,
    action_expire: statectx.action_expire,
    action_close: statectx.action_close,
    action_clear: statectx.action_clear
  }
});
}

module.exports.StateMachineCtx = StateMachineCtx
module.exports.revertAsyncFlag = revertAsyncFlag;
module.exports.createStateMachine = createStateMachine`;

export const CMA_dummy = `const assert = require("assert");
const hex2ascii = require('hex2ascii')
const Machine = require("xstate").Machine;
const createModel = require("@xstate/test").createModel;
const  EXPIRE_CREDIT = 400;
const  CLEAR_CREDIT = 500;
const  CLOSE_CREDIT = 600;
let asyncFlag = false;
const MAX_COUNT = 60;

function revertAsyncFlag() {
  asyncFlag = !asyncFlag;
}


// contract interface 

class CreditController {
  constructor(fuzzer) {
    this.address = "0xa7b692824ac1ff30f01c325ec7498005ee13e0bc";
    this.name = "CreditController";
    this.fuzzer = fuzzer;
  }

  async getCreditAddressByCreditNo() {
    let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "getCreditAddressByCreditNo");
    return fuzz;
  }

  async transferAndDiscountCheck() {
    let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "transferAndDiscountCheck");
    return fuzz;
  }

  async transferCredit() {
    let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "transferCredit");
    return fuzz;
  }

  async staticArrayToDynamicArray() {
    let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "staticArrayToDynamicArray");
    return fuzz;
  }

  async accountIsOk() {
    let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "accountIsOk");
    return fuzz;
  }


  async expireOrClearOrCloseCredit(option) {
    let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "expireOrClearOrCloseCredit", option);
    return fuzz;
  }

  async discountCredit() {
    let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "discountCredit");
    return fuzz;
  }

  async state() {
    let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "state");
    return fuzz;
  }

  async createCredit() {
    let fuzz = await this.fuzzer.full_fuzz_fun("CreditController", this.address, "createCredit");
    return fuzz;
  }

}
// state machine context
class StateMachineCtx {
  constructor(fsmreplayer, fuzzer) {
    this.CreditController = new CreditController(fuzzer);

    this.state = {
      "id": "FSM#1"
    };
    this.fuzzer = fuzzer;
    this.fsmreplayer = fsmreplayer;
  }
  async initialize() {
    this.CreditController.address = await this.fsmreplayer.initialize();
  }
  static getInstance(fsmreplayer, fuzzer) {
    if (!StateMachineCtx.instance)
      StateMachineCtx.instance = new StateMachineCtx(fsmreplayer, fuzzer);
    return StateMachineCtx.instance;
  }
  async getState() {
    //TO DO, set what your state means and how to get the state
    if (this.CreditController.state) {
      let ret = await this.CreditController.state();
      this.state = BigInt(ret.receipt.result.output.toString());
    } else if (this.CreditController.stage) {
      let ret = await this.CreditController.stage();
      this.state = BigInt(ret.receipt.result.output.toString());
    } else {
      this.state = null;
    }
    console.log("state:", this.state);
    return this.state;
  }
  // action_functions_mapping
  async action_create() {
    let ret = [];
    if (asyncFlag) {
      // bcos passed status:0
      let executeStatus = BigInt(0);
      let ctx = StateMachineCtx.getInstance();
      let count = 0;
      // PreCondition. 
      let preState = await ctx.getState();
      assert(null == preState || preState == 0, "preCondition violated: current state is " + preState);

      let retcreateCredit = await StateMachineCtx.getInstance().CreditController.createCredit();
      ret.push(retcreateCredit);
      console.log("current test case: ", BigInt(retcreateCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
      executeStatus += BigInt(retcreateCredit.receipt.status.toString());
      while (executeStatus != 0 && count < MAX_COUNT) {
        count++;
        executeStatus = BigInt(0);
        let retcreateCredit = await StateMachineCtx.getInstance().CreditController.createCredit();
        ret.push(retcreateCredit);
        console.log("current test case: ", BigInt(retcreateCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
        executeStatus += BigInt(retcreateCredit.receipt.status.toString());
      }

      if (count >= MAX_COUNT) {
        throw "TIMEOUT,  too many failed test cases!";
      }
      let postState = await ctx.getState();
      assert(null == postState || postState == 1, "postCondition violated: current state is " + postState);
      // PostCondition. 
    }
    return ret;
  }
  async action_discount() {
    let ret = [];
    if (asyncFlag) {
      // bcos passed status:0
      let executeStatus = BigInt(0);
      let ctx = StateMachineCtx.getInstance();
      let count = 0;
      // PreCondition. 
      let preState = await ctx.getState();
      assert(null == preState || preState == 1, "preCondition violated: current state is " + preState);

      let retdiscountCredit = await StateMachineCtx.getInstance().CreditController.discountCredit();
      ret.push(retdiscountCredit);
      console.log("current test case: ", BigInt(retdiscountCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
      executeStatus += BigInt(retdiscountCredit.receipt.status.toString());
      while (executeStatus != 0 && count < MAX_COUNT) {
        count++;
        executeStatus = BigInt(0);
        let retdiscountCredit = await StateMachineCtx.getInstance().CreditController.discountCredit();
        ret.push(retdiscountCredit);
        console.log("current test case: ", BigInt(retdiscountCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
        executeStatus += BigInt(retdiscountCredit.receipt.status.toString());
      }

      if (count >= MAX_COUNT) {
        throw "TIMEOUT,  too many failed test cases!";
      }
      let postState = await ctx.getState();
      assert(null == postState || postState == 2, "postCondition violated: current state is " + postState);
      // PostCondition. 
    }
    return ret;
  }
  async action_transfer() {
    let ret = [];
    if (asyncFlag) {
      // bcos passed status:0
      let executeStatus = BigInt(0);
      let ctx = StateMachineCtx.getInstance();
      let count = 0;
      // PreCondition. 
      let preState = await ctx.getState();
      assert(null == preState || preState == 1, "preCondition violated: current state is " + preState);

      let rettransferCredit = await StateMachineCtx.getInstance().CreditController.transferCredit();
      ret.push(rettransferCredit);
      console.log("current test case: ", BigInt(rettransferCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
      executeStatus += BigInt(rettransferCredit.receipt.status.toString());
      while (executeStatus != 0 && count < MAX_COUNT) {
        count++;
        executeStatus = BigInt(0);
        let rettransferCredit = await StateMachineCtx.getInstance().CreditController.transferCredit();
        ret.push(rettransferCredit);
        console.log("current test case: ", BigInt(rettransferCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
        executeStatus += BigInt(rettransferCredit.receipt.status.toString());
      }

      if (count >= MAX_COUNT) {
        throw "TIMEOUT,  too many failed test cases!";
      }
      let postState = await ctx.getState();
      assert(null == postState || postState == 1, "postCondition violated: current state is " + postState);
      // PostCondition. 
    }
    return ret;
  }
  async action_expire() {
    let ret = [];
    if (asyncFlag) {
      // bcos passed status:0
      let executeStatus = BigInt(0);
      let ctx = StateMachineCtx.getInstance();
      let count = 0;
      // PreCondition. 
      let preState = await ctx.getState();
      assert(null == preState || preState == 1 || preState == 2, "preCondition violated: current state is " + preState);

      let retexpireOrClearOrCloseCredit = await StateMachineCtx.getInstance().CreditController.expireOrClearOrCloseCredit({static:[{index:3, value:EXPIRE_CREDIT}]});
      ret.push(retexpireOrClearOrCloseCredit);
      console.log("current test case: ", BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
      executeStatus += BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString());
      while (executeStatus != 0 && count < MAX_COUNT) {
        count++;
        executeStatus = BigInt(0);
        let retexpireOrClearOrCloseCredit = await StateMachineCtx.getInstance().CreditController.expireOrClearOrCloseCredit({static:[{index:3, value:EXPIRE_CREDIT}]});
        ret.push(retexpireOrClearOrCloseCredit);
        console.log("current test case: ", BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
        executeStatus += BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString());
      }
  
      if (count >= MAX_COUNT) {
        throw "TIMEOUT,  too many failed test cases!";
      }
      let postState = await ctx.getState();
      assert(null == postState || postState == 3 || postState == 3, "postCondition violated: current state is " + postState);
      // PostCondition. 
    }
    return ret;
  }
  async action_close() {
    let ret = [];
    if (asyncFlag) {
      // bcos passed status:0
      let executeStatus = BigInt(0);
      let ctx = StateMachineCtx.getInstance();
      let count = 0;
      // PreCondition. 
      let preState = await ctx.getState();
      assert(null == preState || preState == 1 || preState == 2, "preCondition violated: current state is " + preState);

    
      let retexpireOrClearOrCloseCredit = await StateMachineCtx.getInstance().CreditController.expireOrClearOrCloseCredit({static:[{index:3, value:CLOSE_CREDIT}]});
      ret.push(retexpireOrClearOrCloseCredit);
      console.log("current test case: ", BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
      executeStatus += BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString());
      while (executeStatus != 0 && count < MAX_COUNT) {
        count++;
        executeStatus = BigInt(0);
        let retexpireOrClearOrCloseCredit = await StateMachineCtx.getInstance().CreditController.expireOrClearOrCloseCredit({static:[{index:3, value:CLOSE_CREDIT}]});
        ret.push(retexpireOrClearOrCloseCredit);
        console.log("current test case: ", BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
        executeStatus += BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString());
      }

      if (count >= MAX_COUNT) {
        throw "TIMEOUT,  too many failed test cases!";
      }
      let postState = await ctx.getState();
      assert(null == postState || postState == 5 || postState == 5, "postCondition violated: current state is " + postState);
      // PostCondition. 
    }
    return ret;
  }
  async action_clear() {
    let ret = [];
    if (asyncFlag) {
      // bcos passed status:0
      let executeStatus = BigInt(0);
      let ctx = StateMachineCtx.getInstance();
      let count = 0;
      // PreCondition. 
      let preState = await ctx.getState();
      assert(null == preState || preState == 1 || preState == 2, "preCondition violated: current state is " + preState);

      let retexpireOrClearOrCloseCredit = await StateMachineCtx.getInstance().CreditController.expireOrClearOrCloseCredit({static:[{index:3, value:CLEAR_CREDIT}]});
      ret.push(retexpireOrClearOrCloseCredit);
      console.log("current test case: ", BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
      executeStatus += BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString());
      while (executeStatus != 0 && count < MAX_COUNT) {
        count++;
        executeStatus = BigInt(0);
        let retexpireOrClearOrCloseCredit = await StateMachineCtx.getInstance().CreditController.expireOrClearOrCloseCredit({static:[{index:3, value:CLEAR_CREDIT}]});
        ret.push(retexpireOrClearOrCloseCredit);
        console.log("current test case: ", BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString()) == BigInt(0) ? "passed" : "failed");
        executeStatus += BigInt(retexpireOrClearOrCloseCredit.receipt.status.toString());
      }

      if (count >= MAX_COUNT) {
        throw "TIMEOUT,  too many failed test cases!";
      }
      let postState = await ctx.getState();
      assert(null == postState || postState == 4 || postState == 4, "postCondition violated: current state is " + postState);
      // PostCondition. 
    }
    return ret;
  }
}
// state machine 
const createStateMachine = statectx => {
  return Machine({
    id: "FSM#1",
    initial: "initial",
    context: {
      ctx: statectx
    },
    states: {

      initial: {
        on: {
          create: {
            target: "dummy_CREATED_initial",
            actions: "action_create"
          }
        }
      },
      CREATED: {
        on: {
          transfer: {
            target: "CREATED",
            actions: "action_transfer"
          },
          discount: {
            target: "DISCOUNTED",
            actions: "action_discount"
          },
          expire: {
            target: "EXPIRED",
            actions: "action_expire"
          },
          clear: {
            target: "CLEARED",
            actions: "action_clear"
          },
          close: {
            target: "CLOSED",
            actions: "action_close"
          }
        }
      },
      DISCOUNTED: {
        on: {
          expire: {
            target: "EXPIRED",
            actions: "action_expire"
          },
          clear: {
            target: "CLEARED",
            actions: "action_clear"
          },
          close: {
            target: "CLOSED",
            actions: "action_close"
          }
        }
      },
      EXPIRED: {
        type: "final"
      },
      CLEARED: {
        type: "final"
      },
      CLOSED: {
        type: "final"
      },
      dummy_CREATED_initial: {
        on: {
          transfer: {
            target: "CREATED",
            actions: "action_transfer"
          }
        }
      }
    }
  }, {
    actions: {
      action_create: statectx.action_create,
      action_discount: statectx.action_discount,
      action_transfer: statectx.action_transfer,
      action_expire: statectx.action_expire,
      action_close: statectx.action_close,
      action_clear: statectx.action_clear
    }
  });
}

module.exports.StateMachineCtx = StateMachineCtx;
module.exports.revertAsyncFlag = revertAsyncFlag;
module.exports.createStateMachine = createStateMachine;`;