<template>
  <div class="overlay" :hidden="houseId <= 0">
    <div id="bills">
      <div class="card">
        <button class="btn btn-danger" @click="close">Close</button>
        <p>{{ houseId }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url("../_scss/bills.scss");
</style>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { billApis } from '@/apis/bill.ts';

const props = defineProps({
  houseId: {
    type: Number,
    required: true,
    default: -1,
  },
});
const emit = defineEmits(['houseIdChange']);

const houseIdRef = ref(props.houseId);
watch(houseIdRef, (newHouseId) => {
  console.log('houseId changed to', newHouseId);
});

var houseIdData = ref(props.houseId);
var billData = ref({});

onMounted(() => {
  billApis.fetchBills(props.houseId).then((response) => {
    return response.json().then((data) => {
      billData.value = data.bills;
      console.log(billData.value);
    });
  }).catch((error) => {
    console.error(error);
  });
});

const close = () => {
  houseIdData.value = -1;
  emit('houseIdChange', -1);
}

</script>