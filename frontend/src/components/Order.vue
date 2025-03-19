<script setup>
import axios from 'axios'
import {computed, ref} from 'vue'
import PopUp from "@/components/PopUp.vue"

const props = defineProps({
  title:{
    required: true,
    type: String
  },
  time:{
    required:true,
    type: String
  },
  seat_number:{
    required:true,
    type:Number
  },
  is_paid:{
    required:true,
    type:Boolean
  },
  price:{
    required:true,
    type:Number
  },
  id:{
    required: true,
    type: Number
  }
})

const emit = defineEmits(['order-state-changed'])
const source = {
  refund: 2,
  pay: 3,
}
async function cancel_order(){
  axios.delete("http://127.0.0.1:8000/user/cancel_order/", {
    requireAuth: true,
    params: {ticket_id: props.id}
  })
      .then(response => {
        console.log(response.data.message)
        emit('order-state-changed', source.refund, true)
      })
      .catch(e => {
        console.log(e)
        emit('order-state-changed', source.refund, false)
      })
}

async function pay_booked(){
  axios.post("http://127.0.0.1:8000/user/pay_booked/", {ticket_id: props.id},
        {requireAuth: true})
      .then(response => {
        console.log(response.data.message)
        emit('order-state-changed', source.pay, true)
      })
      .catch(e => {
        console.log(e)
        emit('order-state-changed', source.pay, false)
      })
}
</script>

<template>
<div class = 'container'>
  <p>电影名称：{{props.title}}</p>
  <p>时间：{{props.time}}</p>
  <p>座位号：{{props.seat_number}}</p>
  <p>支付状态：<span v-if="props.is_paid" style="color: #41af43">已支付</span>
    <span v-else style="color: #e00f0f">未支付</span></p>
  <p><button v-if="!props.is_paid" @click="pay_booked">支付</button>
    <button @click="cancel_order">退票</button></p>
</div>
</template>

<style scoped>
.container{
  padding-top: 3px;
  padding-left: 6px;
  padding-bottom: 2px;
  margin-bottom: 10px;
  font-size: 10px;
  font-weight: lighter;
  border-radius: 15px;
  box-shadow: 0 0 10px gray;
  background-color: white;
}
</style>