<script>
	import Footer from "../components/footer.svelte";
	import Header from "../components/header.svelte";
	import Topnav from "../components/topnav.svelte";
	import "/src/css/global.scss"
	import 'leaflet/dist/leaflet.css';
	import 'leaflet-routing-machine/dist/leaflet-routing-machine.css';
	import 'bootstrap-icons/font/bootstrap-icons.css';
</script>

<header>

	<Header />
	<Topnav />

</header>

<main>
	<slot></slot>
</main>

<footer>

<Footer />

</footer>

<style lang="scss">

	main {
		padding: 32px;
		@media (min-width: 768px) {
			padding: 64px;
		}

		@media (min-width: 1200px) {
			max-width: 1200px;
			margin: 0 auto;
		}
	}

</style>