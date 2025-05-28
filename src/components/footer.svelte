<script>
	import Underscore from "./underscore.svelte";
	import { base } from "$app/paths";


</script>

<div class="footer">

	<div class="footer__info">
		<div class="footer__col">
			<div class="footer__logo">
				<img src="{base}/images/Logo_main.png" alt="GroceryRunner Logo"/>
			</div>
		</div>
		<div class="footer__right">
			<div class="footer__col">
				<nav class="footer__nav">
					<div class="footer__headline">
						<Underscore> Where <i>Next?</i> </Underscore>
					</div>
					<a href="/" class="footer__link">Home</a>
					<a href="#" class="footer__link">Scan Receipt</a>
					<a href="#" class="footer__link">Shopping Analytics</a>
					<a href="./settings/" class="footer__link">Settings</a>
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
		background-color: color("primary-light");
		max-width: 100vw;
		overflow: hidden;

		&__info {
			display: flex;
			justify-content: space-between;
			align-items: center;
			gap: 32px;
			padding: 10px 32px;

			@media (min-width: 768px) {
				padding: 16px 64px;
			}

			@media (min-width: 1200px) {
				max-width: 1200px;
				margin: 0 auto;
		}

		}

		&__right {
			display: flex;
			justify-content: center;
			text-align: center;
			padding: 16px;
			gap: 64px;
		}

		&__col {
			&--socials {
				display: flex;
				flex-direction: column;
				justify-content: flex-start;
				align-items: center;
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

			@media (min-width: 768px) {
				top: -32px;
				bottom: -32px;
				width: calc(100% + 80px);
			}

			@media (min-width: 1200px) {

				width: calc(100vw + 100% - 1200px);

		}
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

				@media (min-width: 768px) {
					font-size: 1.05em;
				}

			}

		}

		&__logo {

			width: 128px;
			height: 96px;

			& > img {
				width: 100%;
				height: 100%;
				object-fit: contain;
			}

			@media (min-width: 768px) {
				width: auto;
				height: 180px;
			}

		}

	}

</style>