import Vuex from 'vuex'
import {auth} from "@/store/auth";
import {createStore} from "vuex";

export default createStore({
    modules: {
        auth
    }
});

