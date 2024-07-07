<template>
  <div class="card-text">
    <form id="profile-form">
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" class="form-control" id="email" readonly>
      </div>
      <div class="form-group">
        <label for="address">Address</label>
        <input type="text" class="form-control" id="address">
      </div>
      <div class="form-group">
        <label for="phone">Phone</label>
        <input type="tel" class="form-control" id="phone">
      </div>
      <div class="form-group">
        <label for="gender">Gender</label>
        <select class="form-control" id="gender">
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary">Update Profile</button>
    </form>
    <hr>
    <button id="change-password-btn" class="btn btn-secondary">Change Password</button>
  </div>
</template>

<script setup>


</script>
