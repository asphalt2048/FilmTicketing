<script setup>
import {computed, ref} from 'vue'

const props = defineProps({
  number: {
    required: true
  },
  status: {
    type: Number,
    required: true
  }
})
const emit = defineEmits(['select-a-seat'])
const is_selected = ref(false)
const cur_state = computed(() => ({
  'available': props.status === 0,
  'occupied': props.status === 1,
  'cur_user_seat': props.status === 2
}))

function toggle(){
  is_selected.value = !is_selected.value;

  if(props.status === 0) {
    emit('select-a-seat', props.number, is_selected.value);
    //select-a-seat should change the list of chosen seats in the parent component
  }
}
</script>


<template>
  <div
    class = "seat"
    :class = "[{selected: is_selected}, cur_state]"
    @click = "toggle"
  >
  </div>
</template>


<style scoped>
  .seat{
    background-color: rgba(232, 241, 234, 0.89);
    border: 2px solid #999;
    border-radius: 5px;
    font-size: 70%;
    margin: 5px;
    width: 3%;
    height: 15px;
    cursor: pointer;
    display: flex;
    justify-content: center;
  }
  .selected{
    background-color: #4444ef;
  }
  .occupied{
    background-color: #e00f0f;
    cursor: not-allowed;
  }
  .cur_user_seat{
    background-color: #23592b;
    cursor: not-allowed;
  }
  .seat:hover{
    background-color: #ada6a6;
  }
  .selected:hover{
    background-color: #4444ef;
  }
</style>

