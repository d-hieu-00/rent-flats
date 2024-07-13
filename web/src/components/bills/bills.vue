<template>
  <div class="overlay" :hidden="houseId <= 0">
    <div id="bills">
      <div class="card">
        <button class="btn btn-danger" @click="close">Close</button>
        <p>{{ houseId }}</p>
        <div class="card-body">
          <div v-for="bill in billData" :key="bill.bill_id" class="bill-card">
            <h3>Bill for House ID: {{ bill.house_id }}</h3>
            <p><strong>Base:</strong> {{ bill.bill_data.base }}</p>
            <p><strong>Total:</strong> {{ bill.bill_data.total }}</p>
            <p><strong>Water:</strong> {{ bill.bill_data.water }}</p>
            <p><strong>Service:</strong> {{ bill.bill_data.service }}</p>
            <p><strong>Electric:</strong> {{ bill.bill_data.electric }}</p>
            <p><strong>Init Date:</strong> {{ bill.init_date }}</p>
            <p><strong>State:</strong> {{ bill.state }}</p>
          </div>
        </div>
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
import { billApis } from '@/apis/bill';

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