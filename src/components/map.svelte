<script>
	import { onMount } from 'svelte';
	import { tick } from 'svelte';

	let map, routingControl;

	let stores = [];
	let userLocation = null;

	let googleMapsUrl = '';
	let appleMapsUrl = '';

	let startInput = '📍 Your Location';
	let endInput = '';
	let startCoord = null;
	let endCoord = null;

	const chainColors = {
		Discount365: '#00c853',
		'Rema 1000': '#d50000',
		DEFAULT: '#888888'
	};

	export let onRouteCreated = () => {};

	async function geocode(text) {
	const res = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(text)}&format=json&limit=1`);
	const data = await res.json();
	if (data.length === 0) return null;
	return {
		lat: parseFloat(data[0].lat),
		lng: parseFloat(data[0].lon)
	};
}

	function guessChain(name) {
		if (!name) return 'Unknown';
		const lowered = name.toLowerCase();
		if (lowered.includes('discount')) return 'Discount365';
		if (lowered.includes('rema')) return 'Rema 1000';
		return 'Other';
	}

	async function updateRoute() {
		if (!map) return;

		// Geocode start if needed
		if (startInput === '📍 Your Location') {
			if (!userLocation) return;
			startCoord = L.latLng(userLocation.lat, userLocation.lng);
		} else {
			const geo = await geocode(startInput);
			if (!geo) return;
			startCoord = L.latLng(geo.lat, geo.lng);
		}

		// Geocode end
		if (!endInput) return;
		const geo = await geocode(endInput);
		if (!geo) return;
		endCoord = L.latLng(geo.lat, geo.lng);

		// Clear and re-add route
		if (routingControl) map.removeControl(routingControl);

		routingControl = L.Routing.control({
			waypoints: [startCoord, endCoord],
			routeWhileDragging: true
		}).addTo(map);

		googleMapsUrl = `https://www.google.com/maps/dir/${startCoord.lat},${startCoord.lng}/${endCoord.lat},${endCoord.lng}`;
		appleMapsUrl = `https://maps.apple.com/?saddr=${startCoord.lat},${startCoord.lng}&daddr=${endCoord.lat},${endCoord.lng}`;

		onRouteCreated({ start: startCoord, end: endCoord });

	}

	onMount(async () => {
		const L = await import('leaflet');
		window.L = L;
		await import('leaflet-routing-machine');

		map = L.map('map').setView([55.6761, 12.5683], 13);

		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: '&copy; OpenStreetMap contributors'
		}).addTo(map);

		// Try to get user location
		map.locate({ setView: true, maxZoom: 14 });

		map.on('locationfound', (e) => {
			userLocation = e.latlng;
			updateRoute();
		});

		// Load stores
		const res = await fetch('/data/stores.json');
		const geojson = await res.json();

		stores = geojson.features
			.filter((f) => f.geometry?.type === 'Point')
			.map((f) => {
				const [lng, lat] = f.geometry.coordinates;
				const name = f.properties?.name || 'Unknown';
				const chain = guessChain(name);
				return { name, lat, lng, chain };
			})
			.filter((store) => store.chain === 'Discount365' || store.chain === 'Rema 1000');

		// Plot markers
		stores.forEach((store) => {
			const icon = L.divIcon({
				className: 'custom-icon',
				html: `<div class="label" style="background:${chainColors[store.chain] || chainColors.DEFAULT};">${store.chain}</div>`
			});
			L.marker([store.lat, store.lng], { icon }).addTo(map);
		});

		await tick();
		updateRoute();
	});
</script>

<form on:submit|preventDefault={updateRoute}>
	<label>Start:</label>
	<input type="text" bind:value={startInput} placeholder="Your location or address" />

	<label>End:</label>
	<input type="text" bind:value={endInput} placeholder="Type address or store name" />

	<button type="submit">Submit</button>
</form>

<div id="map"></div>

{#if googleMapsUrl && appleMapsUrl}
	<div style="margin-top: 1rem; display: flex; gap: 1rem;">
		<a href={googleMapsUrl} target="_blank" rel="noopener noreferrer">
			<button>Open in Google Maps</button>
		</a>
		<a href={appleMapsUrl} target="_blank" rel="noopener noreferrer">
			<button>Open in Apple Maps</button>
		</a>
	</div>
{/if}

<style>
	#map {
		height: 500px;
		width: 100%;
		margin-top: 1rem;
	}

	.controls {
		display: flex;
		gap: 1rem;
		align-items: center;
		flex-wrap: wrap;
	}

	select {
		padding: 5px;
		font-size: 14px;
	}

	.custom-icon .label {
		color: white;
		padding: 3px 6px;
		border-radius: 4px;
		font-size: 12px;
		font-weight: bold;
		box-shadow: 0 0 3px rgba(0, 0, 0, 0.4);
		white-space: nowrap;
	}
</style>
