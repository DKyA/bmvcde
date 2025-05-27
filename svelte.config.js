import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: undefined,
			precompress: false,
			strict: true
		}),
	},
	preprocess: [
		vitePreprocess({
			scss: {
				prependData: `@use "src/css/variables.scss" as *;`
			},
			postcss: true
		})
	]
};

export default config;
