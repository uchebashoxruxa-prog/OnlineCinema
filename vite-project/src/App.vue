<template>
  <div>
    
    <div class="list_cats"> 
      <a v-for="cat in categories" :key="cat.id" href="" target="_blank"> 
        {{ cat.title }} 
      </a>
    </div>
    
    <div class="card" v-for="cinema in cinemas" :key="cinema.id">
      <img :src="cinema.photo" alt="">
      <h4>{{ cinema.title }}</h4>
      <p>{{ cinema.description }}</p>
    </div>

  </div>

</template>



<script setup>

import axios from 'axios';
import {ref, onMounted} from 'vue';

const categories = ref(null);
const cinemas = ref(null);

const getCategories = async() => {
  const list_cats = await axios.get('http://127.0.0.1:8000/api/v1/categories/');
  
  categories.value = list_cats.data;
}

const getCinemas = async() => {
  const list_cinemas = await axios.get('http://127.0.0.1:8000/api/v1/cinemas/');
  
  cinemas.value = list_cinemas.data;
}

onMounted(()=>{
  getCategories();
  getCinemas()
})



</script>




<style scoped>

.list_cats{
  display: flex;
  justify-content: space-between;
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
