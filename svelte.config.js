import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const config = { 
	kit: {
		adapter: adapter({
			fallback: 'index.html', // 👈 This enables SPA behavior
			strict: false
		})
	},
	preprocess: [vitePreprocess(
		{
			scss: {
				prependData: `@import '/src/css/variables.scss';`
			},
			postcss: true
		}
	)]
};

export default config;
