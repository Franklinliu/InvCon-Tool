import {createApp} from "vue";
import App from "./App.vue";
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueCodemirror from 'vue-codemirror'
import { basicSetup } from '@codemirror/basic-setup'
  
const app = createApp(App)
app.use(VueAxios, axios)
app.use(VueCodemirror, {
  // optional default global options
  autofocus: true,
  disabled: false,
  indentWithTab: true,
  tabSize: 2,
  placeholder: 'Code goes here...',
  extensions: [basicSetup]
  // ...
})
app.mount("#app")