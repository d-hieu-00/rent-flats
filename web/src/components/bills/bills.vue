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
var inited = ref(false);

onMounted(() => {
  houseIdData.value = props.houseId;
  inited.value = true;
});

const close = () => {
  houseIdData.value = -1;
  emit('houseIdChange', -1);
}

</script>