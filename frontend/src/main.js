import Vue from 'vue'
import router from "./router"
import './plugins/element.js'
import store from "./store"
import api from "./api"
import _ from "lodash"

Vue.config.productionTip = false
Vue.prototype.$store = store
Vue.prototype.$api = api
Vue.prototype._ = _
new Vue({
    router,
    render(){
        return <router-view></router-view>
    }
}).$mount('#app')
