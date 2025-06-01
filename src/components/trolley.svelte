<script>
	import { onMount } from 'svelte';
	import Papa from 'papaparse';
	let allCategories = [];
	let input = '';
	let suggestions = [];
	let selected = [];

	let parsedRows = [];
	let displayTable = [];

	const presetBasket = [
		{
			category: 'Milk',
			img: '',
			priceRange: '',
			perUnitDisplay: '',
			unit: 'l',
			quantity: 2,
			manualOverrides: {
				rema: null,
				coop: null
			}
		},
		{
			category: 'Beef',
			img: '',
			priceRange: '',
			perUnitDisplay: '',
			unit: 'kg',
			quantity: 0.5,
			manualOverrides: {
				rema: null,
				coop: null
			}
		},
		{
			category: 'Yogurt',
			img: '',
			priceRange: '',
			perUnitDisplay: '',
			unit: 'kg',
			quantity: 1,
			manualOverrides: {
				rema: null,
				coop: null
			}
		}
	];

	let savedBaskets = [{ name: 'Last Week', items: presetBasket }];

	let newBasketName = '';
	let selectedBasketIndex = null;

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
			const unitOrder = ['l', 'kg', 'unit', 'other', ''];
			let chosenUnit = '';
			let unitPrices = [];

			for (const unit of unitOrder) {
				unitPrices = entries
					.filter((e) => (e['Unit Standardized'] || '').trim().toLowerCase().replace('.', '') === unit)
					.map((e) => parseFloat(e['Price per Unit']))
					.filter((p) => !isNaN(p));

					console.log(unitPrices, unit)


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
						: `${minPU.toFixed(2)}-${maxPU.toFixed(2)} ${unitLabel}`;
			}

			displayTable = [
				...displayTable,
				{
					category,
					img: best?.Img || '',
					priceRange,
					perUnitDisplay,
					unit: chosenUnit,
					quantity: 1,
					manualOverrides: {
						rema: null,
						coop: null
					}
				}
			];
			console.log(displayTable)
		}
	}

	function removeCategory(category) {
		selected = selected.filter((c) => c !== category);
		displayTable = displayTable.filter((row) => row.category !== category);
	}

	function getStoreOption(category, preferredUnit, quantity, store) {
		const unitOrder = ['l', 'kg', 'other', '']; // Fallback logic
		const unitList = [preferredUnit, ...unitOrder.filter((u) => u !== preferredUnit)];

		for (const unit of unitList) {
			const rows = parsedRows.filter(
				(row) =>
					row['Best Category']?.trim() === category &&
					row.Retail?.trim() === store &&
					(row['Unit Standardized'] || '').trim().toLowerCase() === unit
			);

			const options = rows
				.map((row) => {
					const unitQty = parseFloat(row['Quantity (Standardized)']);
					const price = parseFloat(row.Price);
					const name = row['Name'].charAt(0) + row['Name'].toLowerCase().slice(1);
					const packImg = row.Img;
					const packSize = row['Quantity (Standardized)'];

					if (isNaN(unitQty) || isNaN(price)) return null;

					const unitsNeeded = quantity / unitQty;
					const unitsToBuy = Math.ceil(unitsNeeded);
					const totalPrice = unitsToBuy * price;

					return {
						name,
						unitSize: unitQty,
						unitsToBuy,
						pricePerUnit: price,
						totalPrice,
						img: packImg,
						packSize,
						unit
					};
				})
				.filter(Boolean);

			if (options.length > 0) {
				return options.reduce((a, b) => (a.totalPrice < b.totalPrice ? a : b));
			}
		}

		return null; // nothing found at all
	}

	$: comparisonTable = displayTable.map((row, index) => {
		const remaOverride = row.manualOverrides.rema;
		const coopOverride = row.manualOverrides.coop;

		const compute = (store, override) => {
			if (override) {
				const unitsToBuy = Math.ceil(row.quantity / override.unitQty);
				return {
					name: override.name,
					unit: override.unit,
					pricePerUnit: override.price,
					unitsToBuy,
					totalPrice: unitsToBuy * override.price,
					img: override.img,
					packSize: override.packSize
				};
			}
			return getStoreOption(row.category, row.unit, row.quantity, store);
		};

		const rema = compute('Rema1000', remaOverride);
		const coop = compute('Coop', coopOverride);

		let highlight = null;
		if (rema && coop) {
			highlight =
				rema.totalPrice < coop.totalPrice
					? 'rema'
					: coop.totalPrice < rema.totalPrice
						? 'coop'
						: null;
		} else if (rema) {
			highlight = 'rema';
		} else if (coop) {
			highlight = 'coop';
		}

		return {
			index,
			category: row.category,
			quantity: row.quantity,
			unit: row.unit,
			rema,
			coop,
			highlight
		};
	});

	function getStoreAlternatives(category, preferredUnit, store) {
		const unitOrder = ['l', 'kg', 'other', ''];
		const unitList = [preferredUnit, ...unitOrder.filter((u) => u !== preferredUnit)];

		for (const unit of unitList) {
			const rows = parsedRows.filter(
				(row) =>
					row['Best Category']?.trim() === category &&
					row.Retail?.trim() === store &&
					(row['Unit Standardized'] || '').trim().toLowerCase() === unit
			);

			const options = rows
				.map((row) => {
					const unitQty = parseFloat(row['Quantity (Standardized)']);
					const price = parseFloat(row.Price);
					const name = row['Name'];
					const img = row.Img;
					const packSize = row.Quantity;
					if (isNaN(unitQty) || isNaN(price)) return null;

					return {
						name,
						unit: unit,
						unitQty,
						price,
						img,
						packSize
					};
				})
				.filter(Boolean);

			if (options.length > 0) return options;
		}

		return [];
	}

	async function loadPresetBasket(presetItems) {
		displayTable = [];

		for (const item of presetItems) {
			// Mimic selectCategory logic
			const entries = parsedRows.filter((row) => row['Best Category']?.trim() === item.category);
			if (entries.length === 0) continue;

			const prices = entries.map((e) => parseFloat(e.Price)).filter((p) => !isNaN(p));
			const min = Math.min(...prices);
			const max = Math.max(...prices);
			const priceRange =
				min === max ? `${min.toFixed(2)} DKK` : `${min.toFixed(2)}–${max.toFixed(2)} DKK`;

			const best = entries.find((e) => e.Img);

			const unitOrder = ['l', 'kg', 'unit', 'other', ''];
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
						: `${minPU.toFixed(2)} - ${maxPU.toFixed(2)} ${unitLabel}`;
			}

			displayTable.push({
				category: item.category,
				img: best?.Img || '',
				priceRange,
				perUnitDisplay,
				unit: chosenUnit,
				quantity: item.quantity,
				manualOverrides: {
					rema: null,
					coop: null
				}
			});
		}
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
	<table class="table">
		<thead class="table__thead">
			<tr>
				<th>Image</th>
				<th>Category</th>
				<th>Price Range</th>
				<th>Price per Unit</th>
				<th>Quantity</th>
				<th></th>
			</tr>
		</thead>
		<tbody class="table__tbody">
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
					<td
						><button class="btn btn--delete" on:click={() => removeCategory(row.category)}
							><i class="bi bi-trash"></i></button
						></td
					>
				</tr>
			{/each}
		</tbody>
	</table>

	<hr class="separate" />
	<div class="comparator">
		<div class="comparator__head comparator__head--rema">Rema1000</div>
		<div class="comparator__head comparator__head--coop">Coop</div>

		<div class="comparator__body comparator__body--rema">
			{#each comparisonTable as row}
				<div class="comparator__row {row.highlight === 'rema' ? 'comparator__row--highlight' : ''}">
					<div class="comparator__row-category">{row.category}</div>

					{#if row.rema}
						<div class="comparator__cell comparator__cell--image">
							{#if row.rema.img}
								<img src={row.rema.img} width="60" alt="Image of {row.rema.name}" />
							{:else}
								<i>No image</i>
							{/if}
						</div>
						<div class="comparator__cell comparator__cell--name">
							{row.rema.name}, {row.rema.packSize}{row.rema.unit}
						</div>
						<div
							class="comparator__cell comparator__cell--price {row.highlight === 'rema'
								? 'comparator__cell--cheapest'
								: ''}"
						>
							{row.rema.pricePerUnit.toFixed(2)} DKK × {row.rema.unitsToBuy} =
							<strong>{row.rema.totalPrice.toFixed(2)} DKK</strong>
						</div>
						<div class="comparator__cell comparator__cell--selector">
							<select
								on:change={(e) =>
									(displayTable[row.index].manualOverrides.rema = JSON.parse(e.target.value))}
							>
								<option value={null}
									>Auto: {row.rema?.name} ({row.rema?.packSize}{row.rema?.unit})</option
								>
								{#each getStoreAlternatives(row.category, row.unit, 'Rema1000') as alt}
									<option value={JSON.stringify(alt)}>
										{alt.name
											.split(' ')
											.map((w) => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase())
											.join(' ')}, {alt?.price}dkk
									</option>
								{/each}
							</select>
						</div>
					{:else}
						<div class="comparator__cell comparator__cell--unavailable" colspan="4">
							<i>Not available</i>
						</div>
					{/if}
				</div>
			{/each}
			<div class="comparator__row comparator__row--total">
				<div class="comparator__cell comparator__cell--label">Total</div>
				<div class="comparator__cell comparator__cell--spacer" colspan="2"></div>
				<div class="comparator__cell comparator__cell--total" colspan="1">
					<strong>
						{comparisonTable
							.map((r) => r.rema?.totalPrice || 0)
							.reduce((a, b) => a + b, 0)
							.toFixed(2)} DKK
					</strong>
				</div>
			</div>
		</div>

		<div class="comparator__body comparator__body--coop">
			{#each comparisonTable as row}
				<div class="comparator__row {row.highlight === 'coop' ? 'comparator__row--highlight' : ''}">
					<div class="comparator__row-category">{row.category}</div>

					{#if row.coop}
						<div class="comparator__cell comparator__cell--image">
							{#if row.coop.img}
								<img src={row.coop.img} width="60" alt="Advertising image of {row.coop.name}" />
							{:else}
								<i>No image</i>
							{/if}
						</div>
						<div class="comparator__cell comparator__cell--name">
							{row.coop.name}, {row.coop.packSize}{row.coop.unit}
						</div>
						<div
							class="comparator__cell comparator__cell--price {row.highlight === 'coop'
								? 'comparator__cell--cheapest'
								: ''}"
						>
							{row.coop.pricePerUnit.toFixed(2)} DKK × {row.coop.unitsToBuy} =
							<strong>{row.coop.totalPrice.toFixed(2)} DKK</strong>
						</div>
						<div class="comparator__cell comparator__cell--selector">
							<select
								on:change={(e) =>
									(displayTable[row.index].manualOverrides.coop = JSON.parse(e.target.value))}
							>
								<option value={null}
									>Auto: {row.coop?.name} ({row.coop?.packSize}{row.coop?.unit})</option
								>
								{#each getStoreAlternatives(row.category, row.unit, 'Coop') as alt}
									<option value={JSON.stringify(alt)}>
										{alt.name
											.split(' ')
											.map((w) => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase())
											.join(' ')}, {alt?.price}dkk
									</option>
								{/each}
							</select>
						</div>
					{:else}
						<div class="comparator__cell comparator__cell--unavailable" colspan="4">
							<i>Not available</i>
						</div>
					{/if}
				</div>
			{/each}
			<div class="comparator__row comparator__row--total">
				<div class="comparator__cell comparator__cell--label">Total</div>
				<div class="comparator__cell comparator__cell--spacer" colspan="2"></div>
				<div class="comparator__cell comparator__cell--total" colspan="1">
					<strong>
						{comparisonTable
							.map((r) => r.coop?.totalPrice || 0)
							.reduce((a, b) => a + b, 0)
							.toFixed(2)} DKK
					</strong>
				</div>
			</div>
		</div>
	</div>
{/if}

<hr class="separate" />
<h3>Manage Baskets</h3>
<div class="basket-layout">
	<div class="basket">
		<input
			class="basket__intext"
			type="text"
			bind:value={newBasketName}
			placeholder="Basket name (e.g. Week 22)"
		/>
		<button
			class="btn btn--success"
			on:click={() => {
				if (!newBasketName || displayTable.length === 0) return;
				savedBaskets = [
					...savedBaskets,
					{ name: newBasketName, items: JSON.parse(JSON.stringify(displayTable)) }
				];
				newBasketName = '';
			}}
		>
			Save Current Basket
		</button>
	</div>

	{#if savedBaskets.length > 0}
		<div class="basketlist">
			<select class="basketlist__select" bind:value={selectedBasketIndex}>
				<option value={null} disabled selected>Select saved basket</option>
				{#each savedBaskets as basket, index}
					<option value={index}>{basket.name}</option>
				{/each}
			</select>

			<button
				class="btn btn--neutral"
				on:click={() => {
					if (selectedBasketIndex !== null) {
						loadPresetBasket(savedBaskets[selectedBasketIndex].items);
					}
				}}
			>
				Load Basket
			</button>

			<button
				class="btn btn--delete"
				on:click={() => {
					if (selectedBasketIndex !== null) {
						savedBaskets.splice(selectedBasketIndex, 1);
						selectedBasketIndex = null;
					}
				}}
			>
				Delete Basket
			</button>
		</div>
	{/if}
</div>

<style lang="scss">
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

	.table {
		width: 100%;
		border-collapse: collapse;
		font-family: $font-stack;
		font-size: 0.95rem;
		color: color('text-dark');
		background-color: color('background');

		th,
		td {
			padding: 0.5rem 0.75rem;
			text-align: left;
			vertical-align: top;
			border: 1px solid lighten(color('text-dark'), 65%);
			word-break: break-word;
		}

		thead {
			display: none; // Hide complex thead on mobile
		}

		tbody {
			display: flex;
			flex-direction: column;
			gap: 1rem;

			tr {
				display: flex;
				flex-direction: column;
				background: white;
				border: 1px solid #eee;
				box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
				border-radius: 8px;
				overflow: hidden;

				td {
					border: none;
					display: flex;
					justify-content: space-between;
					align-items: center;
					padding: 0.75rem 1rem;
					border-bottom: 1px solid #eee;

					&:last-child {
						border-bottom: none;
					}
				}
			}

			tr:last-child {
				background-color: lighten(color('success'), 45%);
				font-weight: 600;

				td {
					justify-content: center;
					color: color('text-dark');

					strong {
						color: color('primary');
					}

					& > span {
						margin-left: 8px;
					}
				}
			}
		}

		// Desktop styling
		@media screen and (min-width: 768px) {
			thead {
				display: table-header-group;

				th {
					background-color: lighten(color('primary'), 42%);
					font-weight: 600;
					font-size: 0.95rem;
					text-align: center;
					color: color('black');
				}
			}

			tbody {
				display: table-row-group;

				tr {
					display: table-row;
					border: none;
					box-shadow: none;

					td {
						display: table-cell;
						border: 1px solid lighten(color('text-dark'), 65%);
						padding: 0.6rem 0.75rem;

						img {
							width: 50px;
							height: auto;
							border-radius: 3px;
						}
					}
				}
			}
		}
	}

	.comparator {
		display: grid;
		grid-template-columns: 100%;
		width: 100%;

		@include p;

		@media (min-width: 768px) {
			grid-template-columns: 1fr 1fr;
			gap: 1rem;
		}

		&__head {
			font-weight: bold;
			font-size: 1.2rem;
			padding: 0.75rem 1rem;
			background-color: #f5f5f5;
			border-bottom: 1px solid #ddd;

			&--coop {
				grid-row: 3;
				@media (min-width: 768px) {
					grid-row: 1;
				}
			}
		}

		&__body {
			display: flex;
			flex-direction: column;
			padding: 0.5rem 1rem;
			gap: 1rem;
			&--coop {
				grid-row: 4;
				@media (min-width: 768px) {
					grid-row: 2;
				}
			}
		}

		&__row {
			display: grid;
			grid-template-columns: auto 1fr;
			row-gap: 0.5rem;
			column-gap: 1rem;
			align-items: center;
			padding-bottom: 1rem;
			border-bottom: 1px solid #eee;
			position: relative;

			&:last-child {
				border-bottom: none;
			}

			&--highlight {
				&:after {
					content: '';
					position: absolute;
					top: 0;
					right: -16px;
					bottom: 0;
					width: 2px;
					background-color: color('success');
				}
			}
		}

		&__row-category {
			grid-column: 1 / -1;
			font-weight: 600;
			color: #666;
		}

		&__cell--image {
			grid-column: 1 / 2;
			height: 100px;
			img {
				max-width: 60px;
				height: auto;
			}
			i {
				font-size: 0.9rem;
				color: #999;
			}
		}

		&__cell--name,
		&__cell--price,
		&__cell--selector {
			grid-column: 2 / 3;
			font-size: 0.95rem;
			line-height: 1.3;

			& > select {
				width: 100%;
				padding: 0.25rem;
				border: 1px solid #ccc;
				border-radius: 4px;
				font-size: 0.9rem;
			}
		}

		&__cell--cheapest {
			color: color('success');
		}

		&__cell--unavailable {
			grid-column: 1 / -1;
			text-align: center;
			color: #999;
			font-style: italic;
		}

		&__row--total {
			border-top: 2px solid #ccc;
			padding-top: 0.75rem;
			margin-top: 1rem;
			font-weight: bold;
			grid-template-columns: 1fr auto;

			.comparator__cell--label {
				font-size: 1rem;
			}

			.comparator__cell--total {
				justify-self: end;
			}
		}
	}

	.basket {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		margin: 1rem 0;
	}

	.basket-layout {
		@media (min-width: 768px) {
			display: grid;
			grid-template-columns: 1fr 1fr;
			gap: 1rem;
		}

		input.basket__intext {
			padding: 0.6rem 0.9rem;
			border-radius: 6px;
			border: 1px solid lighten(color('text-dark'), 60%);
			font-size: 1rem;
			font-family: $font-stack;
			color: color('text-dark');
			background-color: color('white');

			&::placeholder {
				color: lighten(color('text-dark'), 30%);
			}

			&:focus {
				outline: none;
				border-color: color('primary');
				box-shadow: 0 0 0 2px rgba(217, 129, 2, 0.2);
			}
		}

		button {
			width: 100%;
		}
	}

	.basketlist {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		margin-top: 1rem;

		select.basketlist__select {
			padding: 0.6rem 0.9rem;
			border-radius: 6px;
			border: 1px solid lighten(color('text-dark'), 60%);
			font-size: 1rem;
			font-family: $font-stack;
			color: color('text-dark');
			background-color: color('white');

			&:focus {
				outline: none;
				border-color: color('primary');
				box-shadow: 0 0 0 2px rgba(217, 129, 2, 0.2);
			}
		}

		button {
			width: 100%;
		}
	}
</style>
