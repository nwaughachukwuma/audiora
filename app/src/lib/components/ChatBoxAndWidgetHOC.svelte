<script context="module">
	const examples = [
		{ icon: '🎨', text: 'Create image' },
		{ icon: '💡', text: 'Get advice' },
		{ icon: '🧠', text: 'Brainstorm' },
		{ icon: '🎲', text: 'Surprise me' },
		{ icon: '✍️', text: 'Help me write' },
		{ text: 'More' }
	];
</script>

<script lang="ts">
	import { Button } from '@/components/ui/button';
	import ChatBoxAndWidget from './ChatBoxAndWidget.svelte';

	export let searchTerm = '';
	export let loading = false;
	export let disabled = false;
</script>

<div class="flex flex-col items-center max-lg:pt-16 md:justify-center h-full">
	<div class="w-full max-w-3xl space-y-8">
		<div class="text-center space-y-2">
			<h1 class="md:text-4xl text-3xl font-semibold text-white">What can I help with?</h1>
			<h3 class="text-base text-gray-400">Listen to anything, anytime</h3>
		</div>

		<ChatBoxAndWidget bind:searchTerm {loading} {disabled} on:submitSearch />

		<slot name="examples">
			<div class="flex flex-wrap gap-2 justify-center">
				{#each examples as item, index (index)}
					<Button
						variant="outline"
						class="bg-zinc-800/50 border-zinc-700 text-zinc-300 hover:bg-zinc-700/50 hover:text-white"
					>
						{#if item.icon}
							<span class="mr-2">{item.icon}</span>
						{/if}
						{item.text}
					</Button>
				{/each}
			</div>
		</slot>
	</div>
</div>
