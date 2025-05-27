<script>
	import { onMount } from 'svelte';
	import Map from '../components/map.svelte';
	import Trolley from '../components/trolley.svelte';
	import Progress from '../components/progress.svelte';

	let user = 'Daniel'; // Replace with dynamic user data if available
	let userPosition = { lat: 0, lng: 0 };

	onMount(() => {
		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition((position) => {
				userPosition = {
					lat: position.coords.latitude,
					lng: position.coords.longitude
				};
			});
		}
	});

	function handleRouteCreated({ start, end }) {
		// console.log('Start coord:', start);
		// console.log('End coord:', end);
		// do something useful here, potentially :)
		let x = 0;
		x += 1; // Just to avoid unused variable warning
	}
</script>

<div class="header">
	<h1>Hi {user},</h1>
	<h2>Here is the overview of Your Shopping:</h2>

	<hr>

	<Progress />

	<hr>

</div>
<div class="col-2">
	<div class="col-2-left">
		<h2>Shopping List</h2>
		<Trolley />
	</div>
</div>
<div class="col-1">
	<h2>Nearby Stores</h2>

	<Map onRouteCreated={handleRouteCreated} />
</div>

<style lang="scss">
	.container {
		display: flex;
		justify-content: space-between;
		margin: 20px 0;
	}

	.left-column,
	.right-column {
		width: 45%;
	}

	.map-container {
		margin-top: 20px;
	}

	h1, h2 {

		margin-bottom: 8px;
		text-align: center;

	}
</style>
