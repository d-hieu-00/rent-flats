<template>
  <div id="footer">
    <div class="content">
      <div class="left">
        <img src="@/assets/alogo.png" alt="Rent Apartment Logo">
      </div>
      <div class="mid">
        <h4>Contact Us</h4>
        <div class="contact-info">
            <p><font-awesome-icon :icon="['fas', 'location-dot']" />&nbsp;123 Võ Văn Tần St, Tân Bình Dist, Hồ Chí Minh</p>
            <p><font-awesome-icon :icon="['fas', 'phone']" />&nbsp;0965690984</p>
            <p><font-awesome-icon :icon="['fas', 'envelope']" />&nbsp;contact@rent-house.vn</p>
        </div>
      </div>
      <div class="right">
        <h4>Newsletter</h4>
        <div class="newsletter">
            <input type="email" placeholder="Enter your email">
            <button type="submit">Submit</button>
        </div>
        <p class="m-0">Join over 4000+ people who receive rental advice and best property. Don't forget to follow us on:</p>
        <div class="social-icons">
            <a href="#"><font-awesome-icon :icon="['fab', 'facebook-f']" /></a>
            <a href="#"><font-awesome-icon :icon="['fab', 'twitter']" /></a>
            <a href="#"><font-awesome-icon :icon="['fab', 'youtube']" /></a>
            <a href="#"><font-awesome-icon :icon="['fab', 'linkedin-in']" /></a>
            <a href="#"><font-awesome-icon :icon="['fab', 'google-plus-g']" /></a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url("../_scss/footer.scss");
</style>

<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
</script>