<script setup>

import { ref, onMounted, reactive } from 'vue';
import axios from 'axios';
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Navigation } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/navigation';
import ProductCard from './ProductCard.vue';


const products = ref([]);
const error = ref(null);
const modules = [Navigation];


const filters = reactive({
  min_price: '',
  max_price: '',
  min_popularity: ''
});


const fetchProducts = async () => {
  try {
    error.value = null;
    products.value = [];
    
    
    const params = new URLSearchParams();
    if (filters.min_price) params.append('min_price', filters.min_price);
    if (filters.max_price) params.append('max_price', filters.max_price);
    if (filters.min_popularity) params.append('min_popularity', filters.min_popularity);
    
    
    const response = await axios.get('http://localhost:5000/products', { params });
    products.value = response.data;
  } catch (err) {
    console.error('Error while retrieving API data:', err);
    error.value = 'Products could not be loaded. Please try again later.';
  }
};


onMounted(fetchProducts);


</script>

<template>
  
  <div class="product-list-container">
    <h1 class="title">Product List</h1>
     <form class="filters-container" @submit.prevent="fetchProducts">
  
 
  <div class="filter-item">
    <label for="min_price" class="filter-label">Min Price ($)</label>
    <input id="min_price" v-model.number="filters.min_price" type="number" placeholder="Örn: 15000" />
  </div>
  
  <div class="filter-item">
    <label for="max_price" class="filter-label">Max Price ($)</label>
    <input id="max_price" v-model.number="filters.max_price" type="number" placeholder="Örn: 35000" />
  </div>
  
  
  <div class="filter-item span-two">
    <label for="min_popularity" class="filter-label">Min Popularity (0-100)</label>
    <input id="min_popularity" v-model.number="filters.min_popularity" type="number" placeholder="Örn: 80" />
  </div>

  <div class="filter-item span-two">
    <button type="submit" class="filter-button">Filter</button>
  </div>

</form>
    <div v-if="error" class="error-message">{{ error }}</div>
    <Swiper
      v-else-if="products.length"
      :modules="modules"
      :slides-per-view="4"
      :space-between="30"
      :navigation="true"
      :breakpoints="{
        320: { slidesPerView: 1, spaceBetween: 10 },
        768: { slidesPerView: 2, spaceBetween: 20 },
        1024: { slidesPerView: 4, spaceBetween: 30 }
      }"
      class="product-carousel"
    >
      <SwiperSlide v-for="product in products" :key="product.id">
        <ProductCard :product="product" />
      </SwiperSlide>
    </Swiper>
    <div v-else class="loading-message">
      Loading products...
    </div>
  </div>
</template>

<style scoped>

.filters-container {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
}
.filters-container input {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-family: 'Montserrat', sans-serif;
}
.filter-button {
  padding: 8px 20px;
  border: none;
  border-radius: 6px;
  background-color: #333;
  color: white;
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.filter-button:hover {
  background-color: #555;
}

.product-list-container {
  position: relative;
  width: 90%;
  max-width: 1200px;
  padding: 40px 60px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.title {
  text-align: center;
  margin-bottom: 40px;
  color: #333;
  font-family: 'Avenir', serif;
  font-weight: 400;
  font-size: 45px;
}
.product-carousel {
  padding: 10px 0;
}
:deep(.swiper-button-next),
:deep(.swiper-button-prev) {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: white;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  color: #333;
  transition: opacity 0.3s ease;
}
:deep(.swiper-button-next:after),
:deep(.swiper-button-prev:after) {
    font-size: 18px !important;
    font-weight: 600;
}
:deep(.swiper-button-prev) { left: 0; }
:deep(.swiper-button-next) { right: 0; }
:deep(.swiper:not(:hover) .swiper-button-next),
:deep(.swiper:not(:hover) .swiper-button-prev) { opacity: 0.7; }
.error-message, .loading-message {
  text-align: center;
  font-size: 1.2rem;
  color: #888;
  padding: 50px 0;
}


@media (max-width: 768px) {
  .product-list-container {
    width: 100%;
    padding: 20px 15px;
    border-radius: 0;
  }

  .title {
    font-size: 32px;
    margin-bottom: 20px;
  }
  
 
  .filters-container {
    display: grid; 
    grid-template-columns: 1fr 1fr; 
    gap: 15px; 
  }
  
  .filter-item {
    display: flex;
    flex-direction: column; 
  }
  
 
  .span-two {
    grid-column: 1 / -1; 
  }
  
  .filter-label {
    font-size: 12px;
    font-family: 'Montserrat', sans-serif;
    color: #666;
    margin-bottom: 5px;
  }


  .filters-container input,
  .filter-button {
    width: 100%;
    box-sizing: border-box; 
  }

  .filter-button {
    margin-top: 5px; 
  }
 
  :deep(.swiper-button-next),
  :deep(.swiper-button-prev) {
    background-color: rgba(255, 255, 255, 0.7);
    width: 36px;
    height: 36px;
  }

  :deep(.swiper-button-next:after),
  :deep(.swiper-button-prev:after) {
      font-size: 16px !important;
  }
  
  :deep(.swiper-button-prev) { left: 10px; }
  :deep(.swiper-button-next) { right: 10px; }
}
</style>