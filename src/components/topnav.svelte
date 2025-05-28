<script>


</script>

<nav class="nav">

	<a href="/" class="nav__link">Home</a>

	<a href=# class="nav__link">Scan Receipt</a>
	
	<a href=# class="nav__link">Shopping Analytics</a>

	<a href="./settings/" class="nav__link">Setup</a>

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

			@media (min-width: 768px) {
				font-size: 1rem;
			}
			@media (min-width: 1200px) {
				font-size: 1.05rem;
			}

		}


	}

</style>