<template>
    <div> This is Home Page - {{ title }}</div>
</template>


<style scoped>
</style>

<script setup lang="ts">

</script>

<script lang="ts">
import { toast } from 'vue3-toastify';

var backupData = {
};

export default {
    components: {},
    data() {
        return {
            title: "Ahehe",
        }
    },
    methods: {
    }
}
</script>
