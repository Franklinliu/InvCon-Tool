import Vue from 'vue'
import App from './App.vue'
import VueCodemirror from 'vue-codemirror'
// require styles
import 'codemirror/lib/codemirror.css'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import axios from 'axios'
import VueAxios from 'vue-axios'


// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)
Vue.config.productionTip = false
// you can set default global options and events when use
Vue.use(VueCodemirror, /* { 
    options: { theme: 'base16-dark', ... },
    events: ['scroll', ...]
  } */)
Vue.use(VueAxios, axios)
new Vue({
  render: h => h(App),
}).$mount('#app')
