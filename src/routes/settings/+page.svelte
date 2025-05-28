<script>
	let darkMode = false;
	let notifications = false;
	let locationAccess = true;
	let preferredTransport = 'bike';

	import { userName } from '$lib/stores/user.js';

	let tempName = $userName;
	let saved = false;

	function saveName() {
		userName.set(tempName);
		saved = true;
		setTimeout(() => (saved = false), 1500);
	}
</script>

<section class="settings">
	<div class="settings__infobox">
		<h3>You're using the <strong>Premium</strong> version</h3>
		<p>
			Thank you for supporting the development of this tool. Premium features include basket saving,
			store comparison, and more.
		</p>
		<p style="text-align: right;"><a href="#">Manage Plan</a></p>
	</div>

	<div class="settings__section">
		<h4>Profile</h4>
		<label class="settings__label">
			Name
			<input class="settings__input" type="text" bind:value={tempName} />
		</label>
	</div>

	<div class="settings__section">
		<h4>Preferences</h4>
		<label class="settings__toggle">
			<input type="checkbox" bind:checked={notifications} />
			<span>Enable Notifications</span>
		</label>

		<label class="settings__toggle">
			<input type="checkbox" bind:checked={darkMode} />
			<span>Dark Mode</span>
		</label>

		<label class="settings__toggle">
			<input type="checkbox" bind:checked={locationAccess} />
			<span>Allow Location Access</span>
		</label>

		<label class="settings__label">
			Language
			<select class="settings__input">
				<option selected>English</option>
				<option>Dansk</option>
			</select>
		</label>

		<label class="settings__label">
			Preferred Way of Travel
			<select class="settings__input" bind:value={preferredTransport}>
				<option value="bike">Bike</option>
				<option value="public">Public Transport</option>
				<option value="car">Car</option>
				<option value="walk">Walking</option>
			</select>
		</label>

		<label class="settings__label">
			Common Route
			<div class="settings__route">
				<input class="settings__input" placeholder="From (e.g. Home)" />
				<span>→</span>
				<input class="settings__input" placeholder="To (e.g. Work)" />
			</div>
		</label>
	</div>

	<button class="btn btn--success" on:click={saveName}>Save Settings</button>

	<div class="saved">
		{#if saved}
			<p class="saved__text">✅ Saved!</p>
		{/if}
	</div>
</section>

<style lang="scss">

	.saved {

		position: relative;
		&__text {
			position: absolute;
			top: 0.5em;
			left: 0;
			color: color('success');
		}


	}

	.settings {
		padding: 2rem;
		max-width: 700px;
		margin: auto;

		&__infobox {
			background-color: color('primary-light');
			border-left: 5px solid color('primary');
			padding: 1rem 1.5rem;
			border-radius: 8px;
			margin-bottom: 2rem;

			h3 {
				@include h3();
				margin-bottom: 0.4rem;
			}

			p {
				@include p();
			}
		}

		&__section {
			margin-bottom: 2.5rem;

			h4 {
				@include h4();
				margin-bottom: 1rem;
			}
		}

		&__label {
			display: block;
			margin-bottom: 1.2rem;
			font-weight: 500;
			font-family: $font-stack;

			input,
			select {
				margin-top: 0.4rem;
				width: 100%;
				padding: 0.5rem;
				border-radius: 6px;
				border: 1px solid lighten(color('text-dark'), 40%);
				font-size: 1rem;
				font-family: $font-stack;
				background-color: white;
			}
		}

		&__toggle {
			display: flex;
			align-items: center;
			gap: 0.6rem;
			margin-bottom: 1rem;
			cursor: pointer;

			input[type='checkbox'] {
				transform: scale(1.2);
			}

			span {
				font-size: 1rem;
				font-family: $font-stack;
			}
		}

		&__route {
			display: flex;
			align-items: center;
			gap: 0.6rem;

			input {
				flex: 1;
			}

			span {
				font-size: 1.5rem;
				font-weight: bold;
				color: color('text-dark');
			}
		}

		&__list {
			list-style: disc;
			padding-left: 1.5rem;

			li {
				margin-bottom: 0.5rem;
				font-family: $font-stack;
			}
		}
	}
</style>
