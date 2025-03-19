import store from '../store'
import {createRouter, createWebHistory} from "vue-router";
import Dashboard from '@/components/Dashboard.vue'
import FilmSelectPage from "@/components/FilmSelectPage.vue";
import SeatChoosing from "@/components/SeatChoosing.vue";
import Auth from "@/components/Auth.vue";

const routes = [
    {
        path: '/',
        component: FilmSelectPage
    },
    {
        path: '/login',
        component: Auth,
        meta: {beforeLogin: true}
    },
    {
        path: '/dashboard',
        component: Dashboard,
        meta: { requiresAuth: true}
    },
    {
        path: '/SeatChoosing/:id',
        component: SeatChoosing,
        meta: { requiresAuth: true}
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) =>{
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const beforeLogin = to.matched.some(record => record.meta.beforeLogin)
    const isAuthenticated = store.state.auth.status.loggedIn;

    if(requiresAuth && !isAuthenticated){
        next('/login');
    }
    else if(beforeLogin && isAuthenticated){
        alert("您已登陆")
        next(false)
    }
    else {
        next();
    }
});

export default  router