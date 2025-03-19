<script setup>
import axios from  'axios'
import {computed, onMounted, ref} from 'vue'
import FilmItem from "@/components/FilmItem.vue"
import Order from "@/components/Order.vue"
import PopUp from "@/components/PopUp.vue";
import { useStore } from 'vuex'
import { useRouter } from "vue-router"

const store = useStore()
const router = useRouter();
const isLoggedIn = computed(() => store.state.auth.status.loggedIn)
const username = computed(() => store.state.auth.username )
const film_list = ref([])
const is_film_list_empty = computed(() => film_list.value.length<=0)
const order_list = ref([])
const is_order_list_empty = ref(false)//to-do
const show_order = ref(false)
const search_input = ref("")

const source = ref(2)
const show_popUp = ref(false)
const is_payment_success = ref(false)
const is_refund_success = ref(false)
const is_success = computed(() => {
  if(source.value === 2)
    return is_refund_success.value
  else if(source.value === 3)
    return is_payment_success.value
})

const fetch = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/film_list/');
    film_list.value = response.data;
  } catch (error) {
    console.log(error);
  }
}
const search_film = async () => {
  axios.get("http://127.0.0.1:8000/search_film/", {params: {title: search_input.value}})
      .then(response => {
        console.log("search replied")
        film_list.value = response.data
      })
      .catch(error => {
        console.log(error)
      })
}
const get_orders = async () =>{
  const user_id = localStorage.getItem('user_id')
  axios.get('http://127.0.0.1:8000/user/user_orders/',
      {requireAuth: true,
        params: {user_id: user_id}})
      .then(response => {
        order_list.value = response.data;
      })
      .catch(error => {
        console.log(error);
      })
}
const close = () => {show_popUp.value = false}
const reply_to_change = (src, is_success) => {
  if(is_success)
    get_orders()
  source.value = src
  show_popUp.value = true
  if(src === 2)
    is_refund_success.value = is_success
  else if(src === 3)
    is_payment_success.value = is_success
}

const display_order = async () => {
  toggle()
  if(show_order.value)
    await get_orders()
}
const logout = () => {store.dispatch('auth/logout')};
const toLogin = () => {router.push("/login")}
const toggle =() => {show_order.value = !show_order.value}
onMounted(async () => {
  await fetch();
  console.log('successfully fetch film list');
})
</script>

<template>
  <div class='header'>
    <div class="logo">
      <img src="./images/logo.jpg" alt="logo">
    </div>
    <div class="nav">
      <div class="full_width" v-if="isLoggedIn">
        Hello, {{username}}!</div>
      <div class = "full_width">
        <input  v-model="search_input" type="text" value="searchFilm" placeholder="请输入电影名称">
        <button @click="search_film">搜索</button>
      </div>
      <div class="full_width">
        <button style="margin-right: 30px; margin-bottom: 30px;" v-if="isLoggedIn" @click="logout">登出</button>
        <button style="margin-right: 30px; margin-bottom: 30px;" v-else @click="toLogin">登录/注册</button>
        <button style="margin-bottom: 30px;" @click="display_order">我的订单</button>
      </div>
    </div>
  </div>

  <div class='wrapper'>
    <div v-if="is_film_list_empty" class="empty"></div>
    <div v-else class="filmItem" :class="{'show_order': show_order.value}">
      <FilmItem v-for="item in film_list"
                :film_id="Number(item[0])"
                :name="item[1]"
                :director="item[2]"
                :release_date="item[3]"></FilmItem>
    </div>
    <div v-if="show_order"  class="myOrder">
      <order v-for="item in order_list" :key="item[0]"
          :title="item[0]"
          :time="item[1]"
          :seat_number="item[2]"
          :price="Number(item[3])"
          :is_paid="Boolean(item[4])"
          :id="item[5]"
      @order-state-changed="reply_to_change">
      </order>
    </div>
  </div>
  <PopUp v-if="show_popUp"
  :source="source"
  :is_success="is_success"
  @close="close"></PopUp>
</template>

<style scoped>
.header{
  display: flex;
  padding-left: 40px;
  background-color: #030303;
  box-shadow: 0 0 5px #999999;
  border-style: solid;
  border-color: #e00f0f;
}
.wrapper{
  display: flex;
  padding-left: 50px;
  background-image: url("@/components/images/pexels-skitterphoto.jpg");
  background-size: 100% auto;
  background-repeat: no-repeat;
  background-position: right;
  min-height: 700px;
}
.logo{
  width: 60%;
}
.nav{
  width: 20%;
  margin-left: 250px;
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
}
.filmItem{
  padding-top: 6px;
  padding-left: 10px;
  width: 70%;
  margin: 0 7% 0 10%;
  min-height: 700px;
  box-shadow: 0 0 24px #6c6161,
              inset 5px 0 20px 10px black;
  border-radius: 15px;
  background-image: url("@/components/images/filmlist_background_test.jpg");
}
.myOrder{
  width: 20%;
  min-height: 500px;
  background-color: transparent;
}
button{
   background-color: #797777;
}
button:hover{
  background-color: #646161;
}
.full_width{
  color: white;
  width: 100%;
  flex-basis: 100%;
  padding-left: 40px;
}
.empty{
  background-image: url("@/components/images/no_data.jpg");
  padding-top: 6px;
  width: 60%;
  height: 700px;
}
</style>