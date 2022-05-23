<template>
  <!-- bidirectional data binding（双向数据绑定） -->
  <!-- <codemirror v-model="code" :options="cmOptions"></codemirror> -->

  <!-- or to manually control the datasynchronization（或者手动控制数据流，需要像这样手动监听changed事件） -->
 <div id = "content" >
   <div class = "d-flex w-100 justify-content-center">
      <form class="form-inline d-flex w-75 justify-content-center">
             <label for = "search" class = "m-2 fs-3" > Ethereum Contract Address </label>
             <!-- <b-form-checkbox disabled v-model="checked" name="check-button" switch>
                Runtime Detection <b>({{ checked }})</b>
             </b-form-checkbox> -->
          
              <!-- <input v-show="checked" class="form-control m-2 fs-3 w-25" type="text" list = "analyzedcontracts" placeholder=" Ethereum Smart Contract(address..)" id="search" v-model="contractaddress" >
              <datalist id = "analyzedcontracts">
                    <option v-for="contract in analyzedcontracts" :key="contract">{{contract}}</option>
              </datalist> -->
              
              <select class="form-control m-2 fs-3 w-25" id="search" v-model="contractaddress">
                  <option value="" disabled selected hidden>Please select a contract to start</option>
                  <option v-for="contract in analyzedcontracts" :key="contract">{{contract}}</option>
              </select>
            <button class="btn btn-primary fs-3" type="button" @click="onSubmit">Search</button>
      </form>  
    </div>
    <div class = "container-fluid h-50 w-100" v-show = "hasSearched">
      <div id= "sourcecode" class = "mr-auto mt-2" style="width: 55%; float: left">
          <codemirror ref="myCm"
                      v-model="sourceCode" 
                      :options="cmOptions"
                      @ready="onCmReady"
                      @focus="onCmFocus"
                      @input="onCmCodeChange">
          </codemirror>
      </div>
       <div class="ml-auto m-2" style="width:40%; float: right;">
        <form>
          <div class ="form-group row">
            <label for="contractName" class="col-sm-4 col-form-label"> Contract name </label>
            <div class="col-sm-6">
              <input disabled type="text" class="form-control" id="contractName" placeholder="Contract Name..." v-model="contractName">
            </div>
          </div>
          <div class ="form-group row">
              <label for="compilerVersion" class="col-sm-4 col-form-label"> Compiler version </label>
            <div class="col-sm-6">
              <input disabled type="text" class="form-control" id="compilerVersion" placeholder="Compiler version..." v-model="compilerVersion">
            </div>
          </div>
        <div class ="form-group row">
            <label for="functionName" class="col-sm-4 col-form-label"> Function invariants </label>
            <div class="col-sm-6">
              <select class="form-control w-100" id="functionName" @change="onSelectChange($event)" aria-label=".form-select-lg example">
                <option selected>all functions</option>
                <option v-for="func in functions" :key="func">{{func}}</option>
              </select>
            </div>
        
          </div>
        </form>
         <codemirror
            ref = "myCmInv"
            v-model="contractInvariant"
           :options="cmOptions2"
            @ready="onCmReady"
            @focus="onCmFocus"
            @input="onCmInvChange"
        />
       </div>
    </div>

 </div>
 
</template>

<script>
// require component
import { codemirror } from 'vue-codemirror'

// require styles
import 'codemirror/lib/codemirror.css'

// require more codemirror resource...

// language js
import 'codemirror/mode/javascript/javascript.js'
import 'codemirror/addon/selection/mark-selection'
// theme css
import 'codemirror/theme/base16-dark.css'
import 'codemirror/theme/eclipse.css'
// more codemirror resources
// import 'codemirror/some-resource...'
import Analyzedcontracts from "../assets/erc20-analyzed.json"
const MAX_LINE_LENGTH = 100
function jumpToLine(editor, i) { 
    var t = editor.charCoords({line: i, ch: 0}, "local").top; 
    var middleHeight = editor.getScrollerElement().offsetHeight / 2; 
    editor.scrollTo(null, t - middleHeight - 5); 
} 
var oldmarker 
function highlightLines(editor, start, end){
  if (oldmarker){
    oldmarker.clear()
  }
  const from = {line: start, ch: 0}
  const to = {line: end, ch: MAX_LINE_LENGTH}
  oldmarker = editor.markText(from, to, {className: "styled-background"});
}
export default {
  name: 'MyCodeMirror',
  components: {
    codemirror
  },
  data () {
    return {
        checked: false,
        sourceCode: 'const a = 10',
        contractaddress: "",
        globalInvariants: "",
        contractInvariant: "",
        functionInvariants: "",
        functions : "",
        contractName : "",
        compilerVersion: "",
        hasSearched: false,
        analyzedcontracts: Analyzedcontracts,
        cmOptions: {
          // codemirror options
          tabSize: 4,
          mode: 'text/javascript',
          theme: 'eclipse',
          lineNumbers: true,
          line: true,
          // more codemirror options, 更多 codemirror 的高级配置...
        },
        cmOptions2: {
          // codemirror options
          tabSize: 4,
          mode: 'text/javascript',
          theme: 'eclipse',
          lineNumbers: true,
          line: true,
          // more codemirror options, 更多 codemirror 的高级配置...
        },
    }
  },
  methods: {
    onCmReady(cm) {
      console.log('the editor is readied!', cm)
    },
    onCmFocus(cm) {
      console.log('the editor is focus!', cm)
    },
    onCmCodeChange(newCode) {
      this.sourceCode = newCode
    },
    onCmInvChange(newCode) {
      this.contractInvariant = newCode
    },
    onSelectChange(event) {
            // console.log(event.target.value)
            var funcName = event.target.value
            // console.log(this.functionInvariants)
            console.log(funcName, this.functions.includes(funcName))
            // this.contractInvariant = this.functionInvariants[funcName]
            if (this.functionInvariants[funcName]){
              this.contractInvariant = this.functionInvariants[funcName]
              var lines = this.sourceCode.split("\n")
              var lineno = 1
              // var concName = funcName.split(".")[1]
              var shortName = " "+ funcName.split(".")[1].split("(")[0]+"("
              console.log(funcName.split(".")[1].split("(")[0])
              for (var line of lines){
                if (line.includes(shortName) && line.includes("function") ){
                    if (line.includes("{") || lines[lineno+1].includes("{") || lines[lineno+2].includes("{")){
                      console.log(line)
                      jumpToLine(this.codemirror, lineno)
                      highlightLines(this.codemirror, lineno-1, lineno)
                      break 
                    }
                }
                lineno += 1
                // console.log(lineno)
              }
            }else{
              this.contractInvariant = this.globalInvariants
            }

      },
    onSubmit(){
      this.hasSearched = true
      console.log("contract address: " + this.contractaddress)
      this.$http
        .get("/api/?address="+this.contractaddress)
        // .get("http://155.69.148.241:8080/?address="+this.contractaddress)
        .then((response) => {
          console.log("response success")
          var todos = response.data
          console.log(todos)
          if (todos.source){
            this.sourceCode = todos.source
            // if (this.sourceCode.split("\n").length>100)
            this.codemirror.setSize("100%", 0.76*screen.height)
            // else
            //     this.codemirror.setSize("100%", 600)
          }
          if (todos.inv){
            var headers =`Daikon version 5.8.6, released December 2, 2020; http://plse.cs.washington.edu/daikon.
Reading declaration files Processing trace data; reading 1 dtrace file:
Warning: Daikon is using a dataflow hierarchy analysis on a data trace that does not appear to be over a program execution, consider running Daikon with the --nohierarchy flag.

`
            var inv = todos.inv.replace(headers, "")
            var deli = "==========================================================================="
            var invs = inv.split(deli)
            this.functionInvariants = {}
            console.log(invs)
            for (var item of invs){
              if (item.includes(":::EXIT1")){
                  var funcName = item.split(":::EXIT1")[0].trim()
                  console.log(funcName)
                  this.functionInvariants[funcName] = item 
              }
            }
            console.log(this.functionInvariants)
            this.functions = Object.keys(this.functionInvariants)
            this.globalInvariants = inv 
            this.contractInvariant = this.globalInvariants
            // if (this.contractInvariant.split("\n").length>100)
                this.invcodemirror.setSize("100%", 0.6*screen.height)
            // else
            //     this.invcodemirror.setSize("100%", 400)
          }
          if (todos.contractName){
            this.contractName = todos.contractName
          }
          if (todos.compilerVersion){
            this.compilerVersion = todos.compilerVersion
          }
        })
        .catch((err) => console.log(err));
   }
  },
  computed: {
    codemirror() {
      return this.$refs.myCm.codemirror
    },
    invcodemirror(){
      return this.$refs.myCmInv.codemirror
    }
  },
  mounted() {
    console.log('this is current codemirror object', this.codemirror)
    // you can use this.codemirror to do something...
  }
}



</script>
<style>
.styled-background { background-color: #ff7; }
.styled-white { background-color: white; }
</style>