<script>

	import { base } from "$app/paths";

	let user = "Daniel";
	let location = "2200"

</script>

<div class="header">
	<div class="header__left">
		<img src="{base}/images/Logo_main.png" alt="GroceryRunner Logo" width="64" height="48"/>
	</div>
	<div class="header__right">
		<p class="header__info">
			<a href="./settings/">@{user}</a>
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

			& a {

				font-size: 1em;

			}

			// &:last-of-type {

			// 	padding-right: 8px;
			// 	border-right: 2px solid color("primary");

			// } Not to be used right now?

		}
	}

</style>