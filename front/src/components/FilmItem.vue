<script setup>
import {onMounted, ref, computed} from 'vue'
import axios from 'axios'
import Timeslot from "@/components/Timeslot.vue"
import RatingFrom from "@/components/RatingForm.vue"
import {useStore} from "vuex"

const props = defineProps({
  film_id: {
    type: Number,
    required: true
  },
  name: {
    type: String,
    required: true
  },
  director: {
    type: String,
    required: true
  },
  release_date: {
    type: String,
    required: true
  }
});
const actor_list = ref([])
const rating = ref(0.0)
const show_timeslot = ref(false)
const buttonText1 = ref("订票")
const buttonText2 = ref("我要评分")
const show_ratingFrom = ref(false)
const store = useStore()
const loggedIn = computed(() => store.state.auth.status.loggedIn)

const imagePath = computed(() => {
  return new URL(`./images/film_post/${String(props.film_id)}.jpg`, import.meta.url).href
})
const actor_names = computed(() => {
  let names = "";
  for(let i=0; i<actor_list.value.length; i++){
    names += actor_list.value[i];
    if(i !== actor_list.value.length-1)
      names += "/"
  }
  return names;
})

const toggle_ratingFrom = () =>{
  if(show_ratingFrom.value)
    buttonText2.value = "我要评分"
  else
    buttonText2.value = "收起"
  show_ratingFrom.value = !show_ratingFrom.value;
}
const toggle_timeslot = () => {
  if(show_timeslot.value)
    buttonText1.value = "订票";
  else
    buttonText1.value = "收起";
  show_timeslot.value = !show_timeslot.value;
}
const fetch_actor = async ()=> {
  axios.get('http://127.0.0.1:8000/actor/', {params: {film_id: props.film_id}})
    .then(response => {
      actor_list.value = response.data;
    })
    .catch(error => {
      console.log(error)
    })

}
const fetch_rating = async () => {
  axios.get('http://127.0.0.1:8000/film_avg_rating/', {params: {film_id: props.film_id}})
      .then(response => {
        rating.value = response.data
      })
      .catch(error => {
        console.log(error)
      })
}

onMounted(async () => {
  await fetch_actor();
  await fetch_rating();
  console.log("actor/actress list fetched");
})
</script>

<template>
  <div class = 'basic_info'>
    <img :src="imagePath" alt="film post">
    <div class = 'content'>
      <p style="font-weight: bold; font-size: larger">电影名称： {{props.name}}</p>
      <p>导演： {{props.director}}</p>
      <p>主演： {{actor_names}}</p>
      <p>上映时间： {{props.release_date}}</p>
      <br />
      <div>评分：<span style="color: orange">{{rating}}</span>
        <button v-if="loggedIn" style="margin-left: 80px" @click="toggle_ratingFrom">{{buttonText2}}</button>
        <span v-else style="margin-left: 70px">登录后可以评分</span></div>
      <button @click="toggle_timeslot">{{buttonText1}}</button>
    </div>
    <div v-if="show_ratingFrom&loggedIn" class = 'RatingFrom'>
      <RatingFrom :film_id="props.film_id"></RatingFrom>
    </div>
  </div>
  <Timeslot v-if="show_timeslot"
    :film_id="props.film_id"></Timeslot>
</template>


<style scoped>
.basic_info{
  font-size: 12px;
  display: flex;
  align-items: flex-start;
  height: 200px;
  width: 600px;
  color: white;
  background-image: url("@/components/images/filmItem_background.jpg");
  margin-bottom: 3px;
  border-radius: 12px;
  box-shadow: 0 0 3px white;
}
img{
  height: 90%;
  margin-right: 25px;
  margin-top: 2px;
  margin-left: 8px;
}
.content{
  height: 80%;
  padding-bottom: 0;
}
.content p{
  margin-bottom: 1px;
}
.RatingFrom{
  margin-left: 10px;
  height: 80%;
  width: 150px;
  background-color: transparent;
}
</style>

