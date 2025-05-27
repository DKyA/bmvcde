import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const dev = process.env.NODE_ENV === 'development';
const basePath = dev ? '' : '/bmvcde';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: '404.html',
			strict: false
		}),
		paths: {
			base: basePath
		}
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
