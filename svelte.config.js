import adapter from '@sveltejs/adapter-cloudflare';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
			config: undefined, // Use default Cloudflare adapter configuration
			platformProxy: {
				configPath: undefined,
				environment: undefined,
				persist: undefined
			},
			fallback: 'plaintext',
			routes: {
				include: ['/*'],
				exclude: ['<all>']
			}
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
