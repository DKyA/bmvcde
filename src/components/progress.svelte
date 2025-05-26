<script>
	let monthlyGoal = 200; // your team can adjust this freely
	let currentSavings = 110; // this can be dynamically updated later

	$: savingsProgress = Math.min((currentSavings / monthlyGoal) * 100, 100).toFixed(0);
</script>

<div class="savings-progress">
	<div class="savings-label">
		You've saved <strong>{currentSavings} DKK</strong> this month out of your
		<strong>{monthlyGoal} DKK</strong> goal!
	</div>
	<div class="progress-bar">
		<div class="progress-bar__fill" style="width: {savingsProgress}%"></div>
	</div>
	<div class="progress-label">{savingsProgress}%</div>
</div>

<style lang="scss">
	.savings-progress {
		margin: 2rem 0;
	}

	.savings-label {
		margin-bottom: 0.5rem;
		font-size: 1rem;
	}

	.progress-bar {
		background: #ddd;
		border-radius: 6px;
		overflow: hidden;
		height: 20px;
		position: relative;
	}

	.progress-bar__fill {
		background-color: #4caf50;
		height: 100%;
		transition: width 0.3s ease;
	}

	.progress-label {
		text-align: right;
		font-size: 0.9rem;
		color: #333;
		margin-top: 0.25rem;
	}
</style>
