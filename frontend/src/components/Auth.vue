<script setup>
import Login from "@/components/Login.vue"
import Register from "@/components/Register.vue"
import {ref} from 'vue'

const currentTab = ref("Login")

const Tabs = {
  Login, Register
}
</script>

<template>
<div class="container">
  <button v-for="(_, tab) in Tabs"
          :key="tab"
          :class="['tab-button', { active: currentTab === tab }]"
          @click="currentTab = tab"
    >
    {{tab}}
  </button>
  <component :is="Tabs[currentTab]" class="tab"></component>
</div>
</template>

<style scoped>
.container{
  margin: 150px auto auto auto;
  width: 30%;
  height: 25%;
  box-shadow: 0 0 10px silver;
}
.tab-button {
  padding: 6px 10px;
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
  border: 1px solid #ccc;
  cursor: pointer;
  background: #f0f0f0;
  margin-bottom: -1px;
  margin-right: -1px;
}
.tab-button:hover {
  background: #e0e0e0;
}
.tab-button.active {
  background: #e0e0e0;
}
.tab {
  border: 1px solid #ccc;
  padding-top: 10px;
  padding-bottom: 40px;
}
</style>