<script setup>
const props = defineProps({
  source:{
    required: true,
    type: Number
    //this prop define the source business that trigger the Popup
    //1: the ordering action in SeatChoosing
    //2: the refunding action, triggered in Order.vue
    //3: the payment for booked seat, triggered in Order.vue
  },
  is_success:{
    required:true,
    type: Boolean
  }
});
const emit = defineEmits(['close'])

const close = () =>{
  emit('close');
}
</script>

<template>
  <div v-if="props.source===1" class = 'wrapper'>
    <div class='text' v-if="props.is_success">
      <p style="font-size:25px;font-weight: bolder">订票成功</p>
      <p style="font-size: 20px;">您可以在首页的“我的订单”中查看票务信息</p>
    </div>
    <div class='text' v-else>
      <p style="color: #e00f0f;font-size: 20px">订票失败</p>
    </div>
    <button @click="close">关闭</button>
  </div>

  <div v-if="props.source===2" class = 'wrapper'>
    <div class='text' v-if="props.is_success">
      <p style="font-size:25px;font-weight: bolder">退票成功</p>
      <p style="font-size: 20px;">您可以在首页的“我的订单”中查看票务信息</p>
    </div>
    <div class='text' v-else>
      <p style="color: #e00f0f;font-size: 20px">退票失败</p>
    </div>
    <button @click="close">关闭</button>
  </div>

  <div v-if="props.source===3" class = 'wrapper'>
    <div class='text' v-if="props.is_success">
      <p style="font-size:25px;font-weight: bolder">支付成功</p>
      <p style="font-size: 20px;">您可以在首页的“我的订单”中查看票务信息</p>
    </div>
    <div class='text' v-else>
      <p style="color: #e00f0f;font-size: 20px">支付失败</p>
    </div>
    <button @click="close">关闭</button>
  </div>
</template>

<style scoped>
.wrapper{
  position: fixed;
  top: 15%;
  left: 37%;
  right: 37%;
  bottom: 40%;
  padding-left: 50px;
  padding-right: 50px;
  border-style: double;
  border-radius: 20px;
  box-shadow: 0 0 10px #d5cdcd;
  background-color: white;
}
.text{
  margin: 50px auto 0 auto;
}
p{
  text-align: center;
}
button{
  display: block;
  margin: 20px auto 20px auto;
  border-radius: 0;
  background-color: #1e4cc7
}
</style>
