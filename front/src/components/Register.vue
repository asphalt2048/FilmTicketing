<script setup>
import axios from "axios";
import {ref} from 'vue'
import {useRouter} from "vue-router"
import {useStore} from "vuex"

const store = useStore()
const router = useRouter()
const username = ref("")
const password = ref("")
const password2 = ref("")

const submit = async () => {
  if (password2.value !== password.value) {
    alert("两次输入密码不一样");
  } else {
    try {
      const response = await axios.post('http://127.0.0.1:8000/user/register/',
          {"username": username.value, "password": password.value})
      console.log(response.data.message)
      await store.dispatch('auth/login', {username: username.value, password: password.value})
      await router.push('/dashboard')
    } catch (err) {
      console.log(err);
    }
  }
}
</script>

<template>
  <div>
    <p>注册</p>
    <form @submit.prevent="submit">
      <input
        v-model="username"
        type="text"
        placeholder="请输入用户名/手机号">
      <input
        v-model="password"
        type="password"
        placeholder="请输入密码">
      <input
        v-model="password2"
        type="password"
        placeholder="请再次输入密码">
      <input class='button' type="submit" value="注册">
    </form>
  </div>
</template>



<style scoped>
div{
}
input{
  display: block;
  margin: 0 auto 15px auto;
  border-radius: 10px;
  border-style: solid;
}
.button{
  border-radius: 2px;
  background-color: #4444ef;
}
p{
  font-size: larger;
  font-family: 'Consolas', 'Menlo', 'DejaVu Sans Mono', 'Bitstream Vera Sans Mono', monospace;
  text-align: center;
}
</style>