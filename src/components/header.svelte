<script>

	import { base } from "$app/paths";
	import { userName } from '$lib/stores/user.js';

	let location = "2200"

</script>

<div class="header">
	<div class="header__left">
		<img src="{base}/images/Logo_main.png" alt="GroceryRunner Logo" width="64" height="48"/>
	</div>
	<div class="header__right">
		<p class="header__info">
			<a href="./settings/">@{$userName}</a>
		</p>
		<p class="header__info">Zip Code: {location}</p>
		<p class="header__info">Welcome!</p>
		<!-- There could potentially be like FB / LI / other links in the last one -->
	</div>
</div>

<style lang="scss">

	.header {

		$self: &;

		padding: 8px 32px;
		display: flex;
		justify-content: space-between;
		align-items: center;

		&__right {

			display: flex;
			align-items: center;
			justify-content: center;
			gap: 4px;

		}

		&__info {

			padding-left: .2em;
			border-left: 1px solid color("primary");
			@include p();
			font-size: .7em;

			@media (min-width: 768px) {
				font-size: .8em;
			}
			@media (min-width: 1200px) {
				font-size: .9em;
			}

			& a {

				font-size: 1em;

			}

		}

		&__left {

			width: 64px;
			height: 48px;

			@media (min-width: 768px) {
				width: auto;
				height: 60px;
			}
			@media (min-width: 1200px) {
				height: 80px;
			}

			& img {

				width: 100%;
				height: 100%;
				object-fit: contain;

			}

		}
	}

</style>