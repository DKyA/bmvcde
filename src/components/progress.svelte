<script>
	let monthlyGoal = 200; // your team can adjust this freely
	let currentSavings = 110; // this can be dynamically updated later
	let fee = 20;
	let fee_pct = Math.min((fee / monthlyGoal) * 100, 100).toFixed(0);

	$: savingsProgress = Math.min(((currentSavings - fee) / monthlyGoal) * 100, 100).toFixed(0);
</script>

<div class="savings">
	<div class="savings__label">
		You saved {currentSavings} DKK this month so far:
	</div>
	<div class="savings__progress">
		<div class="savings__fee" style="width: {fee_pct}%"><p>Fee</p></div>
		<div class="savings__fill" style="width: {savingsProgress}%"><p>Savings: {currentSavings - fee} DKK</p></div>
	</div>
</div>

<style lang="scss">

	.savings {

		display: flex;
		align-items: center;
		flex-direction: column;
		margin-bottom: 16px;

		&__label {

			@include p;
			margin-top: 8px;

		}
		&__progress {

			width: 90%;
			height: 28px;
			background-color: color('primary-light');
			border: 2px solid color('primary');
			border-radius: 4px;
			display: flex;
			justify-content: left;
			overflow: hidden;

		}

		&__fee {

			height: 100%;
			background-color: color('error');
			display: flex;
			justify-content: center;
			align-items: center;

			& > p {
				@include p;
				color: white;
				opacity: 0.6;
				font-size: 0.6em;
				letter-spacing: 0.1em;
				font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
			}

		}

		&__fill {

			height: 100%;
			background-color: color('success');
			display: flex;
			justify-content: center;
			align-items: center;

			& > p {
				@include p;
				color: white;
				opacity: 0.6;
				font-size: 0.6em;
				letter-spacing: 0.1em;
				font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
			}

		}

	}

</style>
