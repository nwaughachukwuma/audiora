<script context="module">
	export const FINAL_RESPONSE_PREFIX = 'Ok, thanks for clarifying!';
	export const FINAL_RESPONSE_SUFFIX =
		'Please click the button below to start generating the audiocast.';
</script>

<script lang="ts">
	import { createEventDispatcher, onMount } from 'svelte';
	import { Button } from './ui/button';

	export let content: string;

	const dispatch = createEventDispatcher<{
		finalResponse: void;
		reviewSource: void;
		startNew: void;
		generate: { summary: string };
	}>();
	let mounted = false;

	$: finalResponse = content.includes(FINAL_RESPONSE_SUFFIX);
	$: if (mounted && finalResponse) dispatch('finalResponse');

	function ongenerate() {
		const replacePrefixRegex = new RegExp(FINAL_RESPONSE_PREFIX, 'gi');
		const replaceSuffixRegex = new RegExp(FINAL_RESPONSE_SUFFIX, 'gi');
		const summary = content.replace(replacePrefixRegex, '').replace(replaceSuffixRegex, '').trim();

		dispatch('generate', { summary });
	}

	onMount(() => (mounted = true));
</script>

{#if finalResponse}
	<div class="animate-fade-in grid sm:grid-cols-3 gap-3">
		<Button class="bg-emerald-600 text-emerald-100 hover:bg-emerald-700" on:click={ongenerate}
			>Generate Audiocast</Button
		>

		<Button
			variant="ghost"
			class="bg-gray-800 hover:bg-gray-700 text-emerald-600 hover:text-emerald-600"
			on:click={() => dispatch('reviewSource')}
		>
			Review Source
		</Button>

		<Button
			variant="ghost"
			class="text-emerald-600 hover:text-emerald-600 hover:bg-gray-800/40"
			on:click={() => dispatch('startNew')}>Start New Session</Button
		>
	</div>
{/if}
