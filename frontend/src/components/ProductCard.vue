<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
});

const filledStarIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16px" height="16px"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>`;
const emptyStarIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16px" height="16px"><path d="M22 9.24l-7.19-.62L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21 12 17.27 18.18 21l-1.64-7.03L22 9.24zM12 15.4l-3.76 2.27 1-4.28-3.32-2.88 4.38-.38L12 6.1l1.71 4.04 4.38.38-3.32 2.88 1 4.28L12 15.4z"/></svg>`;


const colorNames = {
  yellow: 'Yellow Gold',
  white: 'White Gold',
  rose: 'Rose Gold'
};

const selectedColor = ref('yellow');


const selectedColorName = computed(() => {
  return colorNames[selectedColor.value] || '';
});


const productImage = computed(() => {
  return props.product.images[selectedColor.value] || props.product.images.yellow;
});

const formattedPrice = computed(() => {
  return props.product.price.toLocaleString('en-US', { style: 'currency', currency: 'USD' }) + ' USD';
});

const roundedRating = computed(() => {
  return Math.round(props.product.rating);
});

function selectColor(color) {
  selectedColor.value = color;
}
</script>

<template>
  <div class="product-card">
    <div class="image-container">
      <img :src="productImage" :alt="product.name" class="product-image" />
    </div>
    <div class="info-container">
      <h3 class="product-name">{{ product.name }}</h3>
      <p class="product-price">{{ formattedPrice }}</p>
      
      
      <div class="color-picker">
        <span
          v-for="(url, color) in product.images"
          :key="color"
          :class="['color-dot', color, { active: selectedColor === color }]"
          @click="selectColor(color)"
        ></span>
      </div>

      
      <p class="color-name-display">{{ selectedColorName }}</p>
      
      
      
      <div class="rating">
        <span
          v-for="i in 5"
          :key="i"
          v-html="i <= roundedRating ? filledStarIcon : emptyStarIcon"
        ></span>
        <span class="rating-text">{{ product.rating }}/5</span>
      </div>
    </div>
  </div>
</template>
<style scoped>

.product-card {
  background-color: #fff;
  border-radius: 16px;
  overflow: hidden;
  text-align: left;
}


.image-container {
  background-color: #f7f7f7;
  padding: 20px;
  margin: 10px 10px 15px 10px;
  border-radius: 12px;
}

.product-image {
  width: 100%;
  height: 180px;
  object-fit: contain;
}


.info-container {
  padding: 0 20px 20px 20px;
}


.product-name {
  color: #333;
  margin: 0 0 5px 0;
  font-family: 'Montserrat', sans-serif;
  font-weight: 500; /* Medium */
  font-size: 15px;
}


.product-price {
  color: #000;
  margin: 0 0 15px 0;
  font-family: 'Montserrat', sans-serif;
  font-weight: 400; /* Regular */
  font-size: 15px;
}


.color-picker {
  display: flex;
  gap: 8px;
  margin-bottom: 5px;
}

.color-dot {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  cursor: pointer;
  border: none; 
  transition: all 0.2s ease;
}

.color-dot.active {
  box-shadow: 0 0 0 2px #fff, 0 0 0 3px #333;
  transform: scale(1); 
}

.color-dot.yellow { background-color: #E6CA97; }
.color-dot.white { background-color: #D9D9D9; }
.color-dot.rose { background-color: #E1A4A9; }


.color-name-display {
  color: #757575;
  margin: 0 0 10px 0;
  height: 1em; 
  font-family: 'Avenir', serif;
  font-weight: 400; /* Book */
  font-size: 12px;
}


.rating,
.rating-text {
  font-family: 'Avenir', serif;
  font-weight: 400; /* Book */
  font-size: 14px;
}

.rating {
  display: flex;
  align-items: center;
  gap: 2px;
}

.rating-text {
  margin-left: 8px;
  color: #757575;
}


.rating span:deep(svg) { color: #e4e3df; } 
.rating span:deep(svg path[d*="M12 17.27"]) { color: #f2c94c; } 



@media (max-width: 768px) {
  .product-image { height: 160px; }
  .info-container { padding: 0 15px 15px 15px; }
  .product-name, .product-price { font-size: 14px; }
  .color-name-display { font-size: 11px; }
  .rating, .rating-text { font-size: 13px; }
}
</style>