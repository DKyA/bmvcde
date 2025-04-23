<script>

</script>

<div class="underscore">
	<h4 class="underscore__headline">
		<slot></slot>
	</h4>
	<div class="underscore__border"></div>
</div>

<style lang="scss">

	.underscore {

		position: relative;

		&__headline {

			font-size: 1em;
			font-weight: bold;
			color: color("text-dark");

		}

		&__border {

			position: absolute;
			width: 100%;
			height: 100%;
			top: 1px;
			left: 2px;
			border-bottom: 2px solid color("primary");
			pointer-events: none;

		}

	}

</style>