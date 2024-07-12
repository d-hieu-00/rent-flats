<template>
  <div id="houses">
    <div class="row" v-for="it in housesDataShow">
      <div class="col-4" v-for="item in it">
        <div class="house-item shadow card" style="height: 100%;">
          <img :src="item.additional.images[0]" class="card-img-top">
          <div class="card-body">
            <div class="card-text">
              <h5 class="card-title" v-tooltip="`${item.additional.description} - ID: ${item.house_id}`">
                {{ `${item.additional.description} - ID: ${item.house_id}` }}
              </h5>
              <p class="fw-light">
                <font-awesome-icon :icon="['fas', 'location-dot']" />
                {{ item.address }}
              </p>
              <p class="fw-light"><font-awesome-icon :icon="['fas', 'person']" /> Peoples: {{ item.capacity }}</p>
              <p class="fw-light"><font-awesome-icon :icon="['fas', 'sack-dollar']" /> Price: <span class="fw-semibold">{{ priceToString(item.base_price) }} / Month</span></p>
              <button v-if="searchType == 0" class="btn btn-warning btn-detail" @click="showDetail(item)">Detail</button>
              <button v-if="searchType != 0" class="btn btn-primary btn-detail" @click="showBill(item)">View Bills</button>
              <button v-if="searchType != 0" class="btn btn-success btn-rented">Rented</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="house-item shadow card" hidden v-for="item in housesData">
      <img :src="item.additional.images[0]" class="card-img-top">
      <div class="card-body">
        <div class="card-text">
          <h5 class="card-title" v-tooltip="`${item.additional.description} - ID: ${item.house_id}`">
            {{ `${item.additional.description} - ID: ${item.house_id}` }}
          </h5>
          <p class="fw-light">
            <font-awesome-icon :icon="['fas', 'location-dot']" />
            {{ item.address }}
          </p>
          <p class="fw-light"><font-awesome-icon :icon="['fas', 'person']" /> Peoples: {{ item.capacity }}</p>
          <p class="fw-light"><font-awesome-icon :icon="['fas', 'sack-dollar']" /> Price: <span class="fw-semibold">{{ priceToString(item.base_price) }} / Month</span></p>
          <button v-if="searchType == 0" class="btn btn-warning btn-detail" @click="showDetail(item)">Detail</button>
          <button v-if="searchType != 0" class="btn btn-primary btn-detail" @click="showBill(item)">View Bills</button>
          <button v-if="searchType != 0" class="btn btn-success btn-rented">Rented</button>
        </div>
      </div>
    </div>
    <Bills :house-id="inputHouseId" @houseIdChange="updateInHouseId"/>
  </div>
</template>

<style scoped>
@import url("../_scss/houses.scss");
</style>

<script setup lang="ts">
import Bills from '@/components/bills/bills.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ref, onMounted } from 'vue';
import { houseApis } from '@/apis/house';
import { priceToString } from '@/utils'
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
  },
  searchType: {
    type: Number,
    required: false,
    default: 0
  }
});

var inputHouseId = ref<number>(0);
var housesData = ref<House[]>([]);
var housesDataShow = ref<any[]>([]);
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
    updateHousesDataShow();
  }
})

const fetchHouses = () => {
  if (props.searchType == 0) {
    houseApis.fetchHouses(searchData.value).then((res) => {
      return res.json().then((data) => {
        housesData.value = data.houses;
        updateHousesDataShow();
      });
    }).catch((err) => {
      toast.error(err ? err : 'Failed to fetch houses');
    });
  } else {
    // Fetch rented houses
    houseApis.fetchRentedHouses().then((res) => {
      return res.json().then((data) => {
        housesData.value = data.houses;
        updateHousesDataShow();
      });
    }).catch((err) => {
      toast.error(err ? err : 'Failed to fetch rented houses');
    });
  }
};

const updateHousesDataShow = () => {
  housesDataShow.value = [];
  let count = 0;
  let houses: any[] = [];
  for (let i = 0; i < housesData.value.length; i++) {
    if (count++ >= 3) {
      housesDataShow.value.push(houses);
    }
    houses.push(housesData.value[i]);
  }
};

const showDetail = (house: House) => {
  inputHouseId.value = house.house_id;
  console.log('Detail for house ID:', inputHouseId.value);
};

const showBill = (house: House) => {
  inputHouseId.value = house.house_id;
  console.log('Bill for house ID:', inputHouseId.value);
};

const updateInHouseId = (houseId: number) => {
  inputHouseId.value = houseId;
};

</script>