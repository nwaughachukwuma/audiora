<script context="module">
	export const FINAL_RESPONSE_PREFIX = 'Ok, thanks for clarifying!';
	export const FINAL_RESPONSE_SUFFIX =
		'Please click the button below to start generating the audiocast.';
</script>

<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { Button } from './ui/button';
	import { getSessionContext } from '@/stores/sessionContext.svelte';
	import RenderAudioSource from '@/components/RenderAudioSource.svelte';

	export let content: string;

	const dispatch = createEventDispatcher<{
		reviewSource: { summary: string };
		generate: { summary: string };
	}>();

	const { sessionId$, sessionCompleted$, audioSource$ } = getSessionContext();

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
	<div class="animate-fade-in grid sm:grid-cols-2 gap-3">
		<Button
			class="bg-emerald-600 text-emerald-100 hover:bg-emerald-700"
			on:click={() => dispatch('generate', { summary: getSummary() })}>Generate Audiocast</Button
		>

		{#if $audioSource$}
			<RenderAudioSource audioSource={$audioSource$} />
		{:else}
			<Button
				variant="ghost"
				class="bg-gray-800 hover:bg-gray-700 text-emerald-600 hover:text-emerald-600"
				on:click={() => dispatch('reviewSource', { summary: getSummary() })}
			>
				Review Source
			</Button>
		{/if}
	</div>
{/if}
