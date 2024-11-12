import adapterNode from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),

	kit: {
		adapter: adapterNode(),
		alias: {
			'@/*': './src/lib/*',
			'@env': './src/env/index.ts'
		}
	}
};

export default config;
