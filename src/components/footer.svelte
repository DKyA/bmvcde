<script>
	import Underscore from "./underscore.svelte";


</script>

<div class="footer">

	<div class="footer__info">
		<div class="footer__col">
			<div class="footer__logo">
				<img src="/images/Logo_main.png" alt="GroceryRunner Logo" width="128" height="96"/>
			</div>
		</div>
		<div class="footer__col">
			<nav class="footer__nav">
				<div class="footer__headline">
					<Underscore> Where <i>Next?</i> </Underscore>
				</div>
				<a href="#" class="footer__link">Home</a>
				<a href="#" class="footer__link">Shopping Basket</a>
				<a href="#" class="footer__link">Map</a>
				<a href="#" class="footer__link">Settings</a>
			</nav>
		</div>
	</div>

</div>

<style lang="scss">

	.footer {

		color: color("text");

		&__info {
			display: flex;
			justify-content: space-between;
			align-items: center;
			gap: 32px;
			background-color: color("primary-light");
			padding: 10px 32px;

		}


		&__headline {

			margin-bottom: 8px;

		}

		&__nav {

			display: flex;
			flex-direction: column;
			justify-content: center;
			height: 100%;

			& a {

				font-size: .9em;

			}

		}

	}

</style>