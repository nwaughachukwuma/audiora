<script lang="ts" context="module">
	import type { ContentCategory } from '@/utils/types';

	export const categories: ContentCategory[] = [
		'podcast',
		'sermon',
		'audiodrama',
		'lecture',
		'commentary',
		'voicenote',
		'interview',
		'soundbite'
	];
</script>

<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Button from './ui/button/button.svelte';
	const dispatch = createEventDispatcher<{ selectCategory: { value: ContentCategory } }>();
</script>

<div class="w-full h-full block animate-fade-in">
	<div class="flex flex-wrap gap-3">
		{#each categories as category (category)}
			<Button
				class="bg-sky-900/40 hover:bg-sky-900/60 text-sky-200 px-4 py-2 rounded-full"
				on:click={() => dispatch('selectCategory', { value: category })}
			>
				{category}
			</Button>
		{/each}
	</div>
</div>
