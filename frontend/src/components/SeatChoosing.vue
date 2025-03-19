<script setup>
import axios from 'axios'
import {onMounted, ref} from 'vue'
import {useRoute} from "vue-router"
import Seat from "@/components/Seat.vue"
import TicketInfo from "@/components/TicketInfo.vue"
import PopUp from "@/components/PopUp.vue"

const route = useRoute();
const ts_id = route.params.id;

const rows = ref(0);
const columns = ref(0);
const seats_list = ref([]);
/*seats_list: two dimension array representing the layout of all seats
each element formed like [seat_number, is_occupied, seat_status_id]*/
const seats_selected = ref([]);
/*seats_selected: one dimension array recording seats currently selected
element are formed the same way above*/
const cur_user_seats = ref([])

const SR_name = ref("")     //screening room name
const film_title = ref("");
const time = ref("");
const price = ref(0)
const show_popUp = ref(false)
const order_success = ref(false)

async function show_seat() {
  try{
    const user_id = localStorage.getItem('user_id')
    const response1 = await axios.get('http://127.0.0.1:8000/seats_detail/', {params: {ts_id: ts_id}})
    const response2 = await axios.get('http://127.0.0.1:8000/user/timeslot/seats_number/',
        {requireAuth: true, params: {ts_id: ts_id, user_id: user_id}})
    cur_user_seats.value = response2.data
    let temp;
    temp = response1.data.seats_list;
    rows.value = response1.data.rows;
    columns.value = response1.data.columns;
    seats_list.value = [];
    for (let i = 0; i < rows.value; i++) {
      seats_list.value.push(temp.slice(i * columns.value, (i + 1) * columns.value));
    }
    let l = cur_user_seats.value.length
    for(let i = 0; i<l; i++){
      let row_number = Math.ceil(cur_user_seats.value[i] / columns.value);
      let column_number = cur_user_seats.value[i] % columns.value;
      seats_list.value[row_number-1][column_number-1][1] = 2
    }
  }catch (e){
    console.log(e)
  }
}
function select_a_seat(seat_number, is_select) {
  if (is_select) {
    let row_number = Math.ceil(seat_number / columns.value);
    let column_number = seat_number % columns.value;
    let new_item = seats_list.value[row_number - 1][column_number - 1];
    seats_selected.value.push(new_item);
  } else {
    for (let i = 0; i < seats_selected.value.length; i++) {
      if (seats_selected.value[i][0] === seat_number)
        seats_selected.value.splice(i, 1);
    }
  }
}
const close_popUp = () => {
  show_popUp.value = false;
}
async function update(is_paid) {
  const user_id = localStorage.getItem('user_id');
  const ss_id_list = [];
  let l = seats_selected.value.length
  for(let i=0; i<l; i++){
    ss_id_list.push(seats_selected.value[i][2]);
  }
  if(ss_id_list.length === 0){
    alert("请先选择座位");
    return;
  }
  axios.post('http://127.0.0.1:8000/order_seats/',
      {"ss_id_list": ss_id_list, "ts_id": ts_id, "user_id": user_id, "is_paid": is_paid},
      {requireAuth: true
  }).then(response => {
    console.log(response.data.message);
    show_seat();
    seats_selected.value = [];
    show_popUp.value = true;
    order_success.value = true;
  }).catch(error => {
    console.log(error);
    show_popUp.value = true;
    order_success.value = false;
  })
}
const book = async () => {
  await update(false)
}
const purchase = async ()=> {
  await update(true)
}
async function fetch_timeslotInfo(){
  try {
    const response = await axios.get('http://127.0.0.1:8000/timeslot_info/', {params: {ts_id: ts_id}});
    const data = response.data
    film_title.value = data.film_title
    SR_name.value = data.SR_name
    time.value = data.time
    price.value = data.ticketPrice
  } catch (error) {
    console.log(error);
  }
}

onMounted(async () => {
  await fetch_timeslotInfo();
  await show_seat();
  console.log('initialization done')
});
</script>


<template>
  <div class='container'>
    <div class='seats_choosing'>
      <div class='screen'><img src='./images/screen.png' alt="screen log"></div>
      <div class="demo">
        <p><img src="./images/available_seat.png" alt="available seat" width="24" height="20"> 空闲座位</p>
        <p><img src="./images/occupied_seat.png" alt="available seat" width="24" height="20"> 已被预订座位</p>
        <p><img src="./images/your_seat.png" alt="available seat" width="24" height="20"> 您购买的座位</p>
        <p><img src="./images/selected_seat.png" alt="available seat" width="24" height="20"> 您选择的座位</p>
      </div>
      <div class='seat_schema'>
        <div class='row' v-for="(row, rowindex) in seats_list" :key="rowindex">
          <Seat v-for="(item, colindex) in row" :key="colindex"
                :number="item[0]"
                :status="Number(item[1])"
                @select-a-seat="select_a_seat">
          </Seat>
        </div>
      </div>
    </div>

    <div class='side'>
      <div class='basic_info'>
        <div class='header1'>
          场次信息
        </div>
        <div class='divider'></div>
        <div class='content'>
          <p class='title'>电影名称： {{ film_title }}</p>
          <p>放映厅： {{ SR_name }}</p>
          <p>场次： {{ time }}</p>
        </div>
      </div>

      <div class='ticket_info'>
        <div class='header2'>已选座位</div>
        <TicketInfo v-for="(item, index) in seats_selected" :key="index"
                    :number="item[0]"
                    :price="Number(price)">
        </TicketInfo>
        <button class='book' @click="book">预定</button>
        <button class='purchase' @click="purchase">购票</button>
      </div>
    </div>
  </div>
<PopUp v-if="show_popUp"
       :is_success = 'order_success'
       :source="1"
  @close="close_popUp"></PopUp>
</template>


<style scoped>
.container {
  display: flex;
}
.seats_choosing {
  width: 70%;
  height: 700px;
  background-color: #ffffff;
  padding: 5px;
}
.screen {
  margin: 10px auto 10px auto;
  display: flex;
  justify-content: center;
}
.demo{
  display: flex;
}
.seat_schema {
  margin: 0 auto 0 auto;
}
.row {
  display: flex;
  margin: 0 auto 0 auto;
  justify-content: center;
  width: 95%;
}
.side {
  width: 30%;
  height: 700px;
  background-color: #999999;
}
.basic_info {
  max-height: 30%;
  background-color: #fffafa;
}
.content {
  padding-left: 15%;
  width: 100%;
  padding-bottom: 5%;
}
p.title {
  font-size: 80%;
  font-weight: bold;
}
p {
  font-size: 60%;
}
.header1 {
  height: 30px;
  padding: 10px 0;
  text-align: center;
  font-size: large;
  font-weight: bold;
  background-color: #d5cdcd;
}
.divider {
  border-bottom: 2px solid black;
  margin: 0 10px;
}
.ticket_info {
  min-height: 70%;
  background-color: rgba(232, 241, 234, 0.89);
}
.header2 {
  text-align: center;
  border-style: double;
  border-color: bisque;
  border-radius: 8px;
  background-color: aqua;
}
</style>