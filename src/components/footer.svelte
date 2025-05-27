<script>
	import Underscore from "./underscore.svelte";
	import { base } from "$app/paths";


</script>

<div class="footer">

	<div class="footer__info">
		<div class="footer__col">
			<div class="footer__logo">
				<img src="{base}/images/Logo_main.png" alt="GroceryRunner Logo" width="128" height="96"/>
			</div>
		</div>
		<div class="footer__right">
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
			<div class="footer__col footer__col--socials">
				<a href="#" class="footer__soclink"><i class="bi bi-facebook"></i></a>
				<a href="#" class="footer__soclink"><i class="bi bi-instagram"></i></a>
				<a href="#" class="footer__soclink"><i class="bi bi-snapchat"></i></a>
				<a href="#" class="footer__soclink"><i class="bi bi-bluesky"></i></a>
				<div class="footer__bg"></div>
			</div>
		</div>
	</div>

</div>

<style lang="scss">

	.footer {

		color: color("text");
		position: relative;

		&__info {
			display: flex;
			justify-content: space-between;
			align-items: center;
			gap: 32px;
			background-color: color("primary-light");
			padding: 10px 32px;

		}

		&__right {
			display: flex;
			justify-content: center;
			text-align: center;
			padding: 16px;
			gap: 16px;
		}

		&__col {
			&--socials {
				display: flex;
				flex-direction: column;
				justify-content: center;
				align-items: center;
				height: 100%;
				position: relative;
				padding: 0 8px 0 16px;
			}
		}

		&__bg {

			position: absolute;
			top: -26px;
			left: 0;
			bottom: -26px;
			width: calc(100% + 48px);
			background-color: color("primary");
		}

		&__soclink {

		font-size: 1.2em;
		color: white;
		z-index: 2;

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