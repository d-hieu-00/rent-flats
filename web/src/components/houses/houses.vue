<template>
  hehe
  <div id="houses" class="row">
    <div class="col-3 house-item shadow card" v-for="item in housesData">
      <div class="card-body">
        <h5 class="card-title">{{ `${item.additional.description} - ID: ${item.house_id}` }}</h5>
        <p class="card-text">
          <img :src="item.additional.images[0]" class="card-img-top">
          <!-- <h5 class="card-title">{{ item.address }}</h5> -->
          Capacity: {{ item.capacity }} person(s) <br>
          Base Price: {{ item.base_price }} won/day <br>
          Additional: {{ JSON.stringify(item.additional) }}
        </p>
        <button class="btn btn-primary" @click="showDetail(item)">Detail</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url("../_scss/houses.scss");
</style>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { houseApis } from '@/apis/house';
import { toast } from 'vue3-toastify';

interface House {
  house_id: number;
  address: string;
  capacity: number;
  base_price: number;
  additional: any;
}

interface SearchParams {
  address: string;
  houseType: string;
  houseOption: string;
  houseCapacity: number;
  minPrice: number;
  maxPrice: number;
  sortBy: number;
}

const props = defineProps({
  houses: {
    type: Array,
    required: false,
    default: undefined,
    validator: (value: any) => {
      if (value === undefined || value === null) {
        return true;
      }
      Array.isArray(value) && value.every((house: House) => {
        let ok = true;
        ok = ok && typeof house === 'object';
        ok = ok && 'house_id' in house && typeof house.house_id === 'number';
        ok = ok && 'address' in house && typeof house.address ==='string';
        ok = ok && 'capacity' in house && typeof house.capacity === 'number';
        ok = ok && 'base_price' in house && typeof house.base_price === 'number';
        ok = ok && 'additional' in house && typeof house.additional === 'object';
        return ok;
      });
      return false;
    }
  },
  search: {
    type: Object,
    required: false,
    default: {},
  }
});

var housesData = ref<House[]>([]);
var searchData = ref<SearchParams>({
  address: '',
  houseType: '',
  houseOption: '',
  houseCapacity: -1,
  minPrice: -1,
  maxPrice: -1,
  sortBy: -1
});

onMounted(() => {
  if (props.houses === undefined || props.houses === null) {
    housesData.value = [];
    fetchHouses();
  } else {
    housesData.value = [...props.houses] as House[];
  }
})

const fetchHouses = () => {
  houseApis.fetchHouses(searchData.value).then((res) => {
    return res.json().then((data) => {
      housesData.value = data.houses;
    });
  }).catch((err) => {
    toast.error(err ? err : 'Failed to fetch houses');
  });
};
</script>