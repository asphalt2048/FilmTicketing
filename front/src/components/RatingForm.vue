<script setup>
import axios from 'axios'
import {ref} from 'vue'
import {useStore} from "vuex"

const store = useStore()
const score = ref('')
const props = defineProps(['film_id'])
const submit_rating = async () => {
  const user_id = localStorage.getItem('user_id')
  axios.post('http://127.0.0.1:8000/submit_rating/',
      {user_id: user_id, film_id: props.film_id, score: Number(score.value)},
      {requireAuth: true})
      .then(response => {
        console.log(response.data.message)
        alert(response.data.message)
      })
      .catch(error => {
        console.log(error)
        const status = error.response.status
        if(status === 400)
          alert(error.response.data.error)
      })
}
</script>

<template>
  <form @submit.prevent="submit_rating">
    <fieldset>
      <legend>感谢您的评价</legend>
      <p>
        <label for="rating">您想为这部电影打几分？</label>
        <select id="rating" v-model="score">
          <option disabled value="">请选择</option>
          <option>1</option>
          <option>2</option>
          <option>3</option>
          <option>4</option>
          <option>5</option>
          <option>6</option>
          <option>7</option>
          <option>8</option>
          <option>9</option>
          <option>10</option>
        </select>
      </p>
      <br />
      <br />
      <input type="submit" value="提交">
    </fieldset>
  </form>
</template>

