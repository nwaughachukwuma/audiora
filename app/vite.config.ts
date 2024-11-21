import { defineEnv } from './src/env/define.js';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	plugins: [sveltekit()],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	},
	define: {
		'process.env.USE_EMULATORS': `'${process.env.USE_EMULATORS || false}'`,
		'process.env.FIREBASE_CONFIG': `'${process.env.FIREBASE_CONFIG || {}}'`,
		...defineEnv()
	},
	build: {
		minify: 'esbuild'
	},
	ssr: {
		noExternal: ['ramda', 'bits-ui']
	},
	optimizeDeps: {
		include: [
			'copy-to-clipboard',
			'firebase/app',
			'firebase/analytics',
			'firebase/firestore',
			'firebase/auth',
			'firebase/storage'
		]
	}
});
