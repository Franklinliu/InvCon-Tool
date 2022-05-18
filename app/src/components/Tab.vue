<template>
  <div id = "content">
    <!-- The form -->
    <form id ="searchinv"  class="example" style="padding: 10px; max-width:1200px">
        <label class = "intro">Ethereum Smart Contract </label>
        <input type="text" placeholder="address.." name="search" v-model="contractaddress">
        <button type="button" @click="submit" ><i class="fa fa-search"></i></button>
        <label class = "normal"> {{ contractName }} </label>
        <label class = "normal"> {{ compilerVersion }} </label>
    </form>
    <div>
    <codemirror
      v-model="sourceCode"
      placeholder="Code goes here..."
      :style="{ padding: `10px`, float:`left`, height:'900px', width:`49%` }"
      :autofocus="true"
      :indent-with-tab="true"
      :tabSize="2"
      :extensions="extensions"
      @ready="log('ready', $event)"
      @change="log('change', $event)"
      @focus="log('focus', $event)"
      @blur="log('blur', $event)"
    />
    <codemirror
      v-model="contractInvariant"
      placeholder="Invariant goes here..."
      :style="{ padding: `10px`, float:`right`, height:'900px', width:`49%` }"
      :autofocus="true"
      :indent-with-tab="true"
      :tabSize="2"
      :extensions="extensions"
      @ready="log('ready', $event)"
      @change="log('change', $event)"
      @focus="log('focus', $event)"
      @blur="log('blur', $event)"
    />
   </div>
  </div>
</template>


<script>
  import { Codemirror } from 'vue-codemirror'
  import { javascript } from '@codemirror/lang-javascript'
  // import { oneDark } from '@codemirror/theme-one-dark'
  import { ref } from 'vue'
  export default {
    name: "Tab",
    components: {
      Codemirror
    },
    setup() {
      const code = ref(`console.log('Hello, world!')`)
      // const extensions = [javascript(), oneDark]
      const extensions = [javascript()]
      return {
        code,
        extensions,
        log: console.log
      }
   },
   data: function () {
      return {
        contractaddress: "address..",
        sourceCode: "",
        contractInvariant: "",
        contractName : "",
        compilerVersion: ""
      }
   },
   methods: {
     submit: function(){
      console.log("contract address: " + this.contractaddress)
      this.$http
        .get("http://155.69.148.241:8080/?address="+this.contractaddress)
        .then((response) => {
          console.log("response success")
          var todos = response.data
          console.log(todos)
          if (todos.source){
            this.sourceCode = todos.source
          }
          if (todos.inv){
            this.contractInvariant = todos.inv 
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
  }
  }
</script>

<style scoped>
* {
  box-sizing: border-box;
}

/* Style the search field */
form.example input[type=text] {
  padding: 10px;
  font-size: 17px;
  border: 1px solid grey;
  float: left;
  width: 45%;
  background: #f1f1f1;
}

.intro{
  padding: 10px;
  font-size: 17px;
  border: 1px solid grey;
  float: left;
  width: 20%;
}

.normal{
  padding: 10px;
  font-size: 17px;
  /* border: 1px solid grey; */
  float: left;
  width: 15%;
  text-align: center;
}

/* Style the submit button */
form.example button {
  float: left;
  width: 5%;
  padding: 10px;
  background: #2196F3;
  color: white;
  font-size: 17px;
  border: 1px solid grey;
  border-left: none; /* Prevent double borders */
  cursor: pointer;
}

form.example button:hover {
  background: #0b7dda;
}

/* Clear floats */
form.example::after {
  content: "";
  clear: both;
  display: table;
}
</style>