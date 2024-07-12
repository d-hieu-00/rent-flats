<template>
  <div id="home">
    <div id="search-container">
      <div class="home-bg">
        <div class="search">
          <p>Search Properties</p>
          <form @submit.prevent="doSearch" class="container">
            <div class="row">
              <div class="col-6">
                <div class="input-group has-validation">
                  <input class="form-control border-radius-3"
                    :class="errorData.addressErr ? 'is-invalid' : ''"
                    type="text" v-model="searchData.address"
                    placeholder="Enter an address, street..."
                    autocomplete="off">
                </div>
              </div>
              <div class="col-3 btn-group">
                <button type="button" class="btn btn-light border-radius-3 dropdown-toggle"
                  :class="errorData.houseTypeError ? 'is-invalid' : ''"
                  data-bs-toggle="dropdown" aria-expanded="false">{{ searchData.houseType }}
                </button>
                <ul class="dropdown-menu">
                  <li v-for="(it, idx) in HOUSE_TYPES">
                    <a class="dropdown-item" :class="idx == 0 ? 'fw-semibold' : ''" href="#" @click="searchData.updateHouseType(idx)">{{ it }}</a>
                  </li>
                </ul>
              </div>
              <div class="col-3 btn-group">
                <button type="button" class="btn btn-light border-radius-3 dropdown-toggle"
                  :class="errorData.houseOptionError ? 'is-invalid' : ''"
                  data-bs-toggle="dropdown" aria-expanded="false">{{ searchData.houseOption }}
                </button>
                <ul class="dropdown-menu">
                  <li v-for="(it, idx) in HOUSE_OPTIONS">
                    <a class="dropdown-item" :class="idx == 0 ? 'fw-semibold' : ''" href="#" @click="searchData.updateHouseOption(idx)">{{ it }}</a>
                  </li>
                </ul>
              </div>
            </div>
            <div class="row mt-2">
              <div class="col-3 btn-group">
                <button type="button" class="btn btn-light border-radius-3 dropdown-toggle"
                  :class="errorData.houseCapacityError ? 'is-invalid' : ''"
                  data-bs-toggle="dropdown" aria-expanded="false">{{ searchData.houseCapacity }}
                </button>
                <ul class="dropdown-menu">
                  <li v-for="(it, idx) in HOUSE_CAPACITY">
                    <a class="dropdown-item" :class="idx == 0 ? 'fw-semibold' : ''" href="#" @click="searchData.updateHouseCapacity(idx)">{{ it }}</a>
                  </li>
                </ul>
              </div>
              <div class="col-3 btn-group">
                <button type="button" class="btn btn-light border-radius-3 dropdown-toggle"
                  :class="errorData.minPriceError ? 'is-invalid' : ''"
                  data-bs-toggle="dropdown" aria-expanded="false">{{ priceToString(searchData.minPrice) }}
                </button>
                <ul class="dropdown-menu">
                  <li v-for="(it, idx) in HOUSE_MIN_PRICES">
                    <a class="dropdown-item" :class="idx == 0 ? 'fw-semibold' : ''" href="#" @click="searchData.updateMinPrice(idx)">{{ priceToString(it) }}</a>
                  </li>
                </ul>
              </div>
              <div class="col-3 btn-group">
                <button type="button" class="btn btn-light border-radius-3 dropdown-toggle"
                  :class="errorData.minPriceError ? 'is-invalid' : ''"
                  data-bs-toggle="dropdown" aria-expanded="false">{{ priceToString(searchData.maxPrice) }}
                </button>
                <ul class="dropdown-menu">
                  <li v-for="(it, idx) in HOUSE_MAX_PRICES">
                    <a class="dropdown-item" :class="idx == 0 ? 'fw-semibold' : ''" href="#" @click="searchData.updateMaxPrice(idx)">{{ priceToString(it) }}</a>
                  </li>
                </ul>
              </div>
              <div class="col">
                <input class="w-100 btn btn-success border-radius-3" type="submit" :value="searchText" :disabled="searchText !== 'Search'">
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="home-body">
      <div class="home-header">
        <h1><span>Apartment&nbsp;</span>For rent In<span>&nbsp;Ho Chi Minh&nbsp;</span>City -<span>&nbsp;Saigon</span></h1>
        <img src="@/assets/house.png" alt="Home Header" />
      </div>
      <h3>Feature Apartment For Rent</h3>
      <House style="margin-top: 3rem; margin-bottom: 3rem;" ></House>
    </div>
  </div>
</template>

<style scoped>
@import url("./_scss/homeView.scss");
</style>

<script setup lang="ts">
import House from '@/components/houses/houses.vue'
import { priceToString } from '@/utils'
import { RouterLink } from 'vue-router'
import { CUSTOM_LINK_CLASS } from '@/config'

const HOUSE_TYPES = ['All Types', 'Apartment', 'House', 'Townhouse'];
const HOUSE_OPTIONS = ['More Option'];
const HOUSE_CAPACITY = ['Peoples', '1', '2', '3', '4', '5', 'Any']
const HOUSE_MIN_PRICES = ['Min. Price', 1000000, 1500000, 2000000, 2500000, 3000000];
const HOUSE_MAX_PRICES = ['Max. Price', 2000000, 2500000, 3000000, 3500000, 4000000];

var searchText = 'Search';
var errorData = {
  addressErr: false,
  houseTypeError: false,
  houseOptionError: false,
  houseCapacityError: false,
  minPriceError: false,
  maxPriceError: false,
};
var searchData = {
  address: '',
  houseType: HOUSE_TYPES[0],
  houseOption: HOUSE_OPTIONS[0],
  houseCapacity: HOUSE_CAPACITY[0],
  minPrice: HOUSE_MIN_PRICES[0],
  maxPrice: HOUSE_MAX_PRICES[0],
  updateHouseType: function (idx: number) {
    this.houseType = HOUSE_TYPES[idx];
  },
  updateHouseOption: function (idx: number) {
    this.houseOption = HOUSE_OPTIONS[idx];
  },
  updateHouseCapacity: function (idx: number) {
    this.houseCapacity = HOUSE_CAPACITY[idx];
  },
  updateMinPrice: function (idx: number) {
    this.minPrice = HOUSE_MIN_PRICES[idx];
  },
  updateMaxPrice: function (idx: number) {
    this.maxPrice = HOUSE_MAX_PRICES[idx];
  },
};

const doSearch = () => {
  const data = {
    address: searchData.address,
    houseType: searchData.houseType,
    houseOption: searchData.houseOption,
    houseCapacity: searchData.houseCapacity,
    minPrice: searchData.minPrice,
    maxPrice: searchData.maxPrice,
  }

  console.log('Search Data:', data);
};

</script>
