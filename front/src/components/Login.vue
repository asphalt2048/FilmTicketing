<script setup>
import {ref} from 'vue';
import {useRouter} from 'vue-router';
import {useStore} from 'vuex';

const username = ref('');
const password = ref('');
const store = useStore();
const router = useRouter();

const login = async () => {
  try {
    await store.dispatch('auth/login', {username: username.value, password: password.value});
    await router.push('/dashboard');
  } catch (error) {
    console.error(error);
    alert('Failed to login');
  }
};
</script>


<template>
  <div >
    <p>登录</p>
    <form @submit.prevent="login">
      <input id='username' v-model="username" placeholder="用户名" required/>
      <input id="password" type="password" v-model="password" placeholder="密码" required/>
      <input class='button' type="submit" value="登录">
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
