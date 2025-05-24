<script>
	import Footer from "../components/footer.svelte";
	import Header from "../components/header.svelte";
	import Topnav from "../components/topnav.svelte";
	import "/src/css/global.scss"
	import 'leaflet/dist/leaflet.css';
	import 'leaflet-routing-machine/dist/leaflet-routing-machine.css';
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
	}

</style>