<script>
	import { onMount } from 'svelte';
	import { tick } from 'svelte';
	import { base } from '$app/paths';

	let map, routingControl;

	let stores = [];
	let userLocation = null;

	let googleMapsUrl = '';
	let appleMapsUrl = '';

	let startInput = '📍 Your Location';
	let endInput = '';
	let startCoord = null;
	let endCoord = null;
	let userMarker = null;
	let stops = [];

	const chainFileNames = {
		Discount365: 'Coop_Marker',
		'Rema 1000': 'Rema_Marker'
	};

	export let onRouteCreated = () => {};

	async function geocode(text) {
		const res = await fetch(
			`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(text)}&format=json&limit=1`
		);
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

		// Waypoints: [start, ...stops, end]
		const waypoints = [startCoord, ...stops.map((s) => s.coord)];
		if (endCoord) waypoints.push(endCoord);

		routingControl = L.Routing.control({
			waypoints,
			routeWhileDragging: true
		}).addTo(map);

		googleMapsUrl =
			`https://www.google.com/maps/dir/` +
			[startCoord, ...stops.map((s) => s.coord), endCoord]
				.filter(Boolean)
				.map((c) => `${c.lat},${c.lng}`)
				.join('/');

		appleMapsUrl = `https://maps.apple.com/?saddr=${startCoord.lat},${startCoord.lng}&daddr=${endCoord.lat},${endCoord.lng}`;
		let all = [startCoord, ...stops.map((s) => s.coord), endCoord].filter(Boolean);
		if (all.length >= 2) {
			appleMapsUrl = `https://maps.apple.com/?saddr=${all[0].lat},${all[0].lng}&daddr=${all
				.slice(1)
				.map((c) => `${c.lat},${c.lng}`)
				.join('+to:')}`;
		}

		onRouteCreated({ start: startCoord, end: endCoord });
	}

	onMount(async () => {
		const L = await import('leaflet');
		window.L = L;
		await import('leaflet-routing-machine/dist/leaflet-routing-machine.js');
		
		map = L.map('map').setView([55.6761, 12.5683], 13);

		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: '&copy; OpenStreetMap contributors'
		}).addTo(map);

		// Try to get user location. Not goign to work probably ;)
		map.locate({ setView: true, maxZoom: 14 });

		map.on('locationfound', (e) => {
			userLocation = e.latlng;
			console.log('User location found:', userLocation);

			// If marker already exists, update it
			if (userMarker) {
				userMarker.setLatLng(userLocation);
			} else {
				userMarker = L.circleMarker(userLocation, {
					radius: 8,
					color: '#1976d2',
					fillColor: '#2196f3',
					fillOpacity: 0.8,
					weight: 2
				})
					.addTo(map)
					.bindTooltip('You are here', { permanent: false, direction: 'top' });
			}

			updateRoute();
		});

		// Load stores
		const res = await fetch('/data/stores.json');
		const geojson = await res.json();

		stores = geojson.features
			.filter((f) => f.geometry?.type === 'Point')
			.map((f) => {
				const [lng, lat] = f.geometry.coordinates;
				const rawName = f.properties?.name || 'Unknown';
				const branch = f.properties?.branch || '';
				const chain = guessChain(rawName);

				// If branch exists, append it to the chain
				const name = branch ? `${chain} ${branch}` : rawName;

				return { name, lat, lng, chain };
			})
			.filter((store) => store.chain === 'Discount365' || store.chain === 'Rema 1000');

		// Plot markers
		stores.forEach((store) => {
			const icon = L.divIcon({
				className: 'icon',
				html: `
				<img
					class="icon__image"
					src="${base}/images/${chainFileNames[store.chain]}.png"
					height=48 width=48
					style="
						position:absolute;
						bottom: 0;
						left: 50%;
						transform: translateX(-50%);
					"
				>`
			});

			const marker = L.marker([store.lat, store.lng], { icon }).addTo(map);

			marker.on('click', () => {
				const stopCoord = L.latLng(store.lat, store.lng);
				stops = [...stops, { name: store.name, coord: stopCoord }];
				updateRoute();
			});

			marker.bindTooltip(`Set Waypoint: ${store.name}`, {
				permanent: false,
				direction: 'top'
			});
		});

		await tick();
		updateRoute();
	});
</script>

<form class="controller" on:submit|preventDefault={updateRoute}>
	<div class="controller__section">
		<label class="controller__label">Start:</label>
		<input
			class="controller__input"
			type="text"
			bind:value={startInput}
			placeholder="Your location or address"
		/>
	</div>

	{#if stops.length > 0}
		<div class="controller__stops">
			{#each stops as stop, index}
				<div class="controller__stop">
					<img
						src={`${base}/images/${chainFileNames[guessChain(stop.name)]}.png`}
						alt="Stop Icon"
						width="24"
						height="24"
					/>
					<span>{stop.name}</span>
					<button
						type="button"
						class="controller__remove"
						on:click={() => {
							stops.splice(index, 1);
							updateRoute();
						}}
						aria-label="Remove stop"
					>
						✕
					</button>
				</div>
			{/each}
		</div>
	{/if}

	<div class="controller__section">
		<label class="controller__label">End:</label>
		<input
			class="controller__input"
			type="text"
			bind:value={endInput}
			placeholder="Type address or store name"
		/>
	</div>

	<button class="controller__submit" type="submit">Go!</button>
</form>

<div id="map" class="map"></div>

{#if googleMapsUrl && appleMapsUrl}
	<div class="opener">
		<a class="opener__link" href={googleMapsUrl} target="_blank" rel="noopener noreferrer">
			<button class="opener__button">Open in Google Maps</button>
		</a>
		<a class="opener__link" href={appleMapsUrl} target="_blank" rel="noopener noreferrer">
			<button class="opener__button">Open in Apple Maps</button>
		</a>
	</div>
{/if}

<style lang="scss">
	.opener {
		display: flex;
		justify-content: space-around;

		gap: 1rem;
		margin-top: 1rem;

		&__link {
			text-decoration: none;
			color: inherit;
			border-bottom: none;
			&:hover {
				text-decoration: none;
				border-bottom: none;
			}
		}

		&__button {
			padding: 8px 16px;
			background-color: color('primary');
			color: white;
			border: none;
			outline: none;
			border-radius: 4px;
			cursor: pointer;
			font-size: 16px;
			transition: 0.3s ease;

			&:hover {
				background-color: darken(color('primary'), 10%);
			}
		}
	}

	.controller {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		padding: 8px;
		background-color: color('primary-light');

		&__section {
			display: flex;
			flex-direction: column;
			gap: 0.5rem;
		}

		&__label {
			@include p;
			font-weight: bold;
			color: color('primary-dark');
		}

		&__input {
			padding: 8px;
			border: 1px solid color('primary-dark');
			border-radius: 4px;
			font-size: 16px;
			color: color('primary-dark');
		}

		&__submit {
			padding: 8px 16px;
			background-color: color('primary');
			color: white;
			border: none;
			border-radius: 4px;
			cursor: pointer;
			font-size: 16px;

			&:hover {
				background-color: darken(color('primary'), 10%);
			}
		}
	}

	.map {
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

	.user-marker {
		font-size: 20px;
		line-height: 24px;
	}

	.controller__stops {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		margin-bottom: 1rem;
		padding: 0.5rem;
		background-color: color('primary-lightest');
		border: 1px solid color('primary-dark');
		border-radius: 6px;
	}

	.controller__stop {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		justify-content: space-between;
		background-color: white;
		padding: 4px 8px;
		border: 1px solid color('primary-dark');
		border-radius: 4px;

		span {
			flex-grow: 1;
			font-size: 14px;
			color: color('primary-dark');
		}

		button.controller__remove {
			background: none;
			border: none;
			font-size: 16px;
			color: red;
			cursor: pointer;
		}
	}
</style>
