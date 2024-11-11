<script context="module">
	export const FINAL_RESPONSE_PREFIX = 'Ok, thanks for clarifying!';
	export const FINAL_RESPONSE_SUFFIX =
		'Please click the button below to start generating the audiocast.';
</script>

<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { Button } from './ui/button';
	import { getSessionContext } from '@/stores/sessionContext.svelte';

	export let content: string;

	const dispatch = createEventDispatcher<{
		startNew: void;
		reviewSource: { summary: string };
		generate: { summary: string };
	}>();

	const { sessionId$, sessionCompleted$ } = getSessionContext();

	function getSummary() {
		const replacePrefixRegex = new RegExp(FINAL_RESPONSE_PREFIX, 'gi');
		const replaceSuffixRegex = new RegExp(FINAL_RESPONSE_SUFFIX, 'gi');
		return content.replace(replacePrefixRegex, '').replace(replaceSuffixRegex, '').trim();
	}
</script>

{#if $sessionCompleted$}
	<div class="mt-3 w-full items-center justify-center flex">
		<a
			href="/audiocast/{$sessionId$}"
			data-sveltekit-preload-data="hover"
			class="py-3 rounded-md px-16 no-underline hover:no-underline bg-emerald-600 text-emerald-100 hover:bg-emerald-700"
			>View Audiocast</a
		>
	</div>
{:else}
	<div class="animate-fade-in grid sm:grid-cols-3 gap-3">
		<Button
			class="bg-emerald-600 text-emerald-100 hover:bg-emerald-700"
			on:click={() => dispatch('generate', { summary: getSummary() })}>Generate Audiocast</Button
		>

		<Button
			variant="ghost"
			class="bg-gray-800 hover:bg-gray-700 text-emerald-600 hover:text-emerald-600"
			on:click={() => dispatch('reviewSource', { summary: getSummary() })}
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
