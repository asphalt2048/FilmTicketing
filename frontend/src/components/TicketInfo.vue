<script setup>
const props = defineProps({
  number: {
    type: Number,
    required: true
  },
  price: {
    type: Number,
    required: true
  }
})
</script>

<template>
  <div class = 'wrapper'>
    <div class = 'head'>CINEMA TICKET</div>
    <div class = 'ticket_content'>
      <p>座位号： {{props.number}}</p>
      <p>单价： {{props.price}}</p>
    </div>
  </div>
</template>

<style scoped>
  .wrapper{
    border-style: double;
    border-radius: 6px;
    border-color: black;
    height: 90px;
    width: 100%;
    background-color: white;
  }
  .head{
    background-color: #23592b;
    height: 17%;
    width: 100%;
    text-align: center;
    padding-top: 5px;
    font-weight: bold;
    font-size: 12px;
    border-bottom: 2px solid black;
  }
  .ticket_content{
    margin: 0 auto 0 auto;
    background-color: white;
    padding-top: 7px;
    width: 70%;
    height: 60%;
    font-size: 12px;
  }
</style>