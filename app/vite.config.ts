import { defineEnv } from './src/env/define.js';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	plugins: [sveltekit()],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	},
	define: {
		...defineEnv()
	},
	build: {
		minify: 'esbuild'
	},
	ssr: {
		noExternal: ['ramda', 'bits-ui', 'rxfire']
	},
	optimizeDeps: {
		include: ['copy-to-clipboard']
	}
});
