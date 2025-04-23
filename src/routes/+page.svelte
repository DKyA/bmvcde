<script>
  import { onMount } from 'svelte';

  let user = 'Daniel'; // Replace with dynamic user data if available
  let groceries = ['Milk', 'Bread', 'Eggs', 'Cheese']; // Replace with dynamic data if available
  let userPosition = { lat: 0, lng: 0 };
  let stores = [
    { name: 'Store A', lat: 0.1, lng: 0.1 },
    { name: 'Store B', lat: -0.1, lng: -0.1 },
  ];

  onMount(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        userPosition = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };
      });
    }
  });
</script>

<div class="header">
  <h1>Hi {user},</h1>
  <h2>Here is the overview of Your Shopping</h2>
</div>
<div class="col-2">
  <div class="col-2-left">
    <h2>Shopping List</h2>
    <ul>
      {#each groceries as grocery}
        <li>{grocery}</li>
      {/each}
    </ul>
  </div>
  <div class="col-2-right">
    <h2>What is on your mind today?</h2>
  </div>
</div>
<div class="col-1">
  <h2>Nearby Stores</h2>
</div>

<style lang="scss">
  .container {
    display: flex;
    justify-content: space-between;
    margin: 20px 0;
  }

  .left-column, .right-column {
    width: 45%;
  }

  .map-container {
    margin-top: 20px;
  }

  #map {
    width: 100%;
    height: 400px;
    background-color: #eaeaea;
  }
</style>