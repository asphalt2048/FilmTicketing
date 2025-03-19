import { createApp } from 'vue'
import axios from "axios"
import AuthService from "@/api/authService.js"
import App from './App.vue'

import store from './store'
import router from './router'

axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.withCredentials = true
axios.defaults.baseURL='http://127.0.0.1:8000/'
axios.defaults.timeout = 10000

const app = createApp(App)

axios.interceptors.request.use(
    async (config) => {
        if(config.requireAuth){
            let accessToken = localStorage.getItem('access_token')
            if(!accessToken)
                await router.push('/login')
            accessToken = JSON.parse(accessToken)
            if(AuthService.is_accessToken_expired(accessToken)){
                try{
                    accessToken = await AuthService.refreshToken()
                }catch (e){
                    console.log(e)
                    await store.dispatch('auth/logout')
                    await router.push('/login')
                }
            }
            config.headers.Authorization = 'Bearer ' + accessToken
        }
        return config
    },(error) => {
        return Promise.reject(error)
    })

app.config.globalProperties.$axios = axios
app.use(store)
app.use(router)
app.mount('#app')
