/// <reference types="svelte" />

declare namespace svelteHTML {
	interface HTMLAttributes<T> {
		'on:intersect'?: (e: CustomEvent) => void;
	}
}
