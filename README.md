# sv

Everything you need to build a Svelte project, powered by [`sv`](https://github.com/sveltejs/cli).

## Creating a project

If you're seeing this, you've probably already done this step. Congrats!

```bash
# create a new project in the current directory
npx sv create

# create a new project in my-app
npx sv create my-app
```

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://svelte.dev/docs/kit/adapters) for your target environment.

# Structure for export files

## Columns

- Retail
- Name: Name of the product
- Category: Type of the product
- Img: url to the image (test by pasting to browser)
- Link: Link to the product / page (if applicable, else leave blank)
- Price: The price of the product
- Quantity: Volume / Quantity / ...
- Unit: Unit of the quantity. Use g, ml, pcs, null (though try to put a unit there if possible. If it is not viable to put g there for instance, use whatever you can, we will sort that out on frontend.)
- Date of Update
- What did I forget?

So, as an example, this would work:
> 	export = pd.DataFrame(data, columns=["Retail", "Name", "Price", "Category", "Img", "Link", "Quantity", "Unit", "Date of Update"])
