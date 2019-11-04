import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './views/Home.vue'
import Login from "./views/Login.vue"
import store from "./store"
import api from "./api"

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

router.beforeEach(async (to,from,next)=>{
    if (from.name == null){
        store.user = await api.get()
    }
    if (to.name != "login" && !store.user){
        next("/login")
    } else {
        next()
    }
})
export default router