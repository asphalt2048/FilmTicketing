<script setup>
import {onMounted, ref} from 'vue'
import axios from 'axios'
import {useRouter} from "vue-router";

const props = defineProps(['film_id']);

const timeslot_list = ref([]);
const A_seats_list = ref(new Map());  //the list of available seats number of different timeslots
const T_seats_list = ref(new Map());  //the list of total seats number of different timeslots

const router = useRouter();
function goToSeatChoosing(id){
  router.push(`/SeatChoosing/${id}`);
}
function is_valid(time){
  return (new Date(time).getTime()<new Date().getTime())
}

const available_seats = async (timeslot_id) => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/avai_seat/', {params: {ts_id: timeslot_id}});
    const key = `${timeslot_id}`;
    A_seats_list.value.set(key, response.data);
  }
  catch (error){
    console.log(error);
    console.log("failed to fetch available seats number");
  }
}
const total_seats = async (timeslot_id) => {
  try{
    const response = await axios.get('http://127.0.0.1:8000/total_seat/', {params: {ts_id: timeslot_id}});
    let rows = response.data.rows;
    let columns = response.data.columns;
    const key = `${timeslot_id}`;
    T_seats_list.value.set(key, rows*columns);
  }
  catch (error){
    console.log(error);
    console.log("failed to fetch total seats number");
  }
}
const fetch = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/timeslot_list/', {params: {film_id: props.film_id}});
    timeslot_list.value = response.data;
  } catch (error) {
    console.log(error);
  }
}

function sort_ts_list() {
  timeslot_list.value = timeslot_list.value.slice().sort((a, b) => new Date(a[1]) - new Date(b[1]));
}

onMounted(async () => {
  await fetch();
  sort_ts_list();
  for (let i = 0; i < timeslot_list.value.length; i++) {
    await available_seats(timeslot_list.value[i][0]);
    await total_seats(timeslot_list.value[i][0]);
  }
})
</script>

<template>
  <div class='timeslot_list'>
    <table>
      <thead>
        <tr>
          <td>放映厅</td>
          <td>时间</td>
          <td>座位</td>
          <td></td>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ts in timeslot_list">
          <td>{{ ts[2] }}</td>
          <td>{{ ts[1] }}</td>
          <td>{{ A_seats_list.get(String(ts[0])) }}/{{ T_seats_list.get(String(ts[0])) }}</td>
          <td>
            <button :disabled="is_valid(ts[1])" @click="goToSeatChoosing(ts[0])">选座</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div>
    <RouterView />
  </div>
</template>

<style scoped>
.timeslot_list{
  font-size: 15px;
  margin-left: 50px;
  margin-right: 240px;
  color: #d5cdcd;
  background-color: #363535;
}
table{
  border-collapse: collapse;
}
th, td {
  border: 1px solid #000;
  padding: 3px 15px 3px 8px;
  text-align: left;
}
thead{
  background-color: #363535;
}
</style>