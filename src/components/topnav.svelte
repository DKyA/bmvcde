<script>


</script>

<nav class="nav">

	<a href=# class="nav__link">Home</a>

	<a href=# class="nav__link">Shopping List</a>

	<a href=# class="nav__link">Map</a>

	<a href=# class="nav__link">Setup</a>

</nav>

<style lang="scss">

	.nav {

		display: flex;
		justify-content: center;
		gap: 16px;
		align-items: center;
		background-color: color("primary");
		padding: 10px 32px;
		position: relative;

		&__link {

			@include a('light');

			font-size: .95em;

		}


	}

</style>