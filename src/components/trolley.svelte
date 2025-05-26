<script>
	import { onMount } from 'svelte';
	import Papa from 'papaparse';
	let allCategories = [];
	let input = '';
	let suggestions = [];
	let selected = [];

	let parsedRows = [];
	let displayTable = [];

	// Load and parse CSV
	onMount(async () => {
		const res = await fetch('/scraper/export/combined_data_final_priced.csv');
		const text = await res.text();

		const parsed = Papa.parse(text, {
			header: true,
			skipEmptyLines: true
		});

		parsedRows = parsed.data;

		// Extract unique best categories
		const values = new Set();
		for (const row of parsedRows) {
			if (row['Best Category']) values.add(row['Best Category'].trim());
		}

		allCategories = Array.from(values).sort();
	});

	function updateSuggestions() {
		if (input.length < 1) {
			suggestions = [];
			return;
		}
		const lower = input.toLowerCase();
		suggestions = allCategories
			.filter((c) => c.toLowerCase().includes(lower) && !selected.includes(c))
			.slice(0, 10);
	}

	function selectCategory(category) {
		selected = [...selected, category];
		input = '';
		suggestions = [];

		const entries = parsedRows.filter((row) => row['Best Category']?.trim() === category);

		if (entries.length > 0) {
			const prices = entries.map((e) => parseFloat(e.Price)).filter((p) => !isNaN(p));
			const min = Math.min(...prices);
			const max = Math.max(...prices);
			const priceRange =
				min === max ? `${min.toFixed(2)} DKK` : `${min.toFixed(2)}–${max.toFixed(2)} DKK`;

			const best = entries.find((e) => e.Img); // pick one with image

			// 🧠 Preferred unit logic
			const unitOrder = ['l', 'kg', 'other', ''];
			let chosenUnit = '';
			let unitPrices = [];

			for (const unit of unitOrder) {
				unitPrices = entries
					.filter((e) => (e['Unit Standardized'] || '').trim().toLowerCase() === unit)
					.map((e) => parseFloat(e['Price per Unit']))
					.filter((p) => !isNaN(p));

				if (unitPrices.length > 0) {
					chosenUnit = unit;
					break;
				}
			}

			let perUnitDisplay = 'N/A';
			if (unitPrices.length > 0) {
				const minPU = Math.min(...unitPrices);
				const maxPU = Math.max(...unitPrices);
				const unitLabel =
					chosenUnit === 'l' ? 'DKK/L' : chosenUnit === 'kg' ? 'DKK/kg' : 'DKK/piece';
				perUnitDisplay =
					minPU === maxPU
						? `${minPU.toFixed(2)} ${unitLabel}`
						: `${minPU.toFixed(2)}–${maxPU.toFixed(2)} ${unitLabel}`;
			}

			displayTable = [
				...displayTable,
				{
					category,
					img: best?.Img || '',
					priceRange,
					perUnitDisplay,
					unit: chosenUnit,
					quantity: 1
				}
			];
		}
	}

	function removeCategory(category) {
		selected = selected.filter((c) => c !== category);
		displayTable = displayTable.filter((row) => row.category !== category);
	}

	function getStoreOption(category, unit, quantity, store) {
	const rows = parsedRows
		.filter(row =>
			row['Best Category']?.trim() === category &&
			row.Retail?.trim() === store &&
			(row['Unit Standardized'] || '').trim().toLowerCase() === unit
		);

	const options = rows
		.map(row => {
			const unitQty = parseFloat(row['Unit Quantity Standardized']);
			const price = parseFloat(row.Price);
			const name = row['Product'] || row['Name'];
			if (isNaN(unitQty) || isNaN(price)) return null;

			const unitsNeeded = quantity / unitQty;
			const unitsToBuy = Math.ceil(unitsNeeded);
			const totalPrice = unitsToBuy * price;

			return {
				name,
				unitsToBuy,
				unitSize: unitQty,
				pricePerUnit: price,
				totalPrice
			};
		})
		.filter(Boolean);

	if (options.length === 0) return null;

	const best = options.reduce((a, b) => (a.totalPrice < b.totalPrice ? a : b));
	return best;
}


	function getPriceForItem(category, unit, quantity, store) {
		const rows = parsedRows
			.filter((row) => row['Best Category']?.trim() === category && row.Retail?.trim() === store)
			.filter((row) => (row['Unit Standardized'] || '').trim().toLowerCase() === unit);

		const prices = rows.map((r) => parseFloat(r['Price per Unit'])).filter((p) => !isNaN(p));

		if (prices.length === 0) return null;

		const minPrice = Math.min(...prices);
		return +(minPrice * quantity).toFixed(2);
	}
</script>

<div class="autocomplete">
	<input
		type="text"
		bind:value={input}
		on:input={updateSuggestions}
		placeholder="Add grocery category..."
	/>
	{#if suggestions.length > 0}
		<ul class="suggestions">
			{#each suggestions as s}
				<li on:click={() => selectCategory(s)}>{s}</li>
			{/each}
		</ul>
	{/if}
</div>

{#if displayTable.length > 0}
	<table class="product-table">
		<thead>
			<tr>
				<th>Image</th>
				<th>Category</th>
				<th>Price Range</th>
				<th>Price per Unit</th>
				<th>Quantity</th>
				<th></th>
			</tr>
		</thead>
		<tbody>
			{#each displayTable as row}
				<tr>
					<td>
						{#if row.img}
							<img src={row.img} alt="Product" width="80" />
						{:else}
							<i>No image</i>
						{/if}
					</td>
					<td>{row.category}</td>
					<td>{row.priceRange}</td>
					<td>{row.perUnitDisplay}</td>
					<td>
						<input type="number" min="0" step="1" bind:value={row.quantity} style="width: 80px" />
						<span>
							{row.unit === 'l' ? 'liters' : row.unit === 'kg' ? 'kg' : 'pcs'}
						</span>
					</td>
					<td><button on:click={() => removeCategory(row.category)}>Del</button></td>
				</tr>
			{/each}
		</tbody>
	</table>
{/if}
<h3>Store Comparison</h3>
<table class="comparison-table">
	<thead>
		<tr>
			<th>Product</th>
			<th>Rema1000</th>
			<th>Coop</th>
		</tr>
	</thead>
	<tbody>
		{#each displayTable as row}
			<tr>
				<td>{row.category}</td>
				<td>
					{#if getPriceForItem(row.category, row.unit, row.quantity, 'Rema1000') !== null}
						{getPriceForItem(row.category, row.unit, row.quantity, 'Rema1000')} DKK
					{:else}
						–
					{/if}
				</td>
				<td>
					{#if getPriceForItem(row.category, row.unit, row.quantity, 'Coop') !== null}
						{getPriceForItem(row.category, row.unit, row.quantity, 'Coop')} DKK
					{:else}
						–
					{/if}
				</td>
			</tr>
		{/each}

		<tr>
			<th>Total</th>
			<th>
				{displayTable
					.map(r => getPriceForItem(r.category, r.unit, r.quantity, 'Rema1000') || 0)
					.reduce((a, b) => a + b, 0).toFixed(2)} DKK
			</th>
			<th>
				{displayTable
					.map(r => getPriceForItem(r.category, r.unit, r.quantity, 'Coop') || 0)
					.reduce((a, b) => a + b, 0).toFixed(2)} DKK
			</th>
		</tr>

	</tbody>
</table>

<style>
	.autocomplete {
		position: relative;
		width: 100%;
		margin-bottom: 1rem;
	}

	input {
		width: 100%;
		padding: 8px;
		font-size: 16px;
		border: 1px solid #ccc;
		border-radius: 4px;
	}

	.suggestions {
		position: absolute;
		background: white;
		border: 1px solid #ccc;
		border-top: none;
		width: 100%;
		max-height: 200px;
		overflow-y: auto;
		z-index: 10;
		list-style: none;
		margin: 0;
		padding: 0;
	}

	.suggestions li {
		padding: 8px;
		cursor: pointer;
	}

	.suggestions li:hover {
		background-color: #eee;
	}

	.product-table {
		width: 100%;
		border-collapse: collapse;
		margin-top: 1rem;
	}

	th,
	td {
		border: 1px solid #ccc;
		padding: 8px;
		text-align: left;
	}

	th {
		background-color: #f5f5f5;
	}

	td img {
		border-radius: 4px;
	}

	.comparison-table {
		width: 100%;
		border-collapse: collapse;
		margin-top: 2rem;
	}

	.comparison-table th,
	.comparison-table td {
		padding: 8px;
		border: 1px solid #ccc;
		text-align: left;
	}

	.comparison-table th {
		background-color: #f0f0f0;
	}
</style>
