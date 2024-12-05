<script context="module">
	const TWO_MINUTES_MS = 120000;
</script>

<script lang="ts">
	import { UserIcon, BotIcon, RotateCw } from 'lucide-svelte';
	import cs from 'clsx';
	import { parse } from 'marked';
	import { Button } from './ui/button';

	export let type: 'user' | 'assistant';
	export let content: string;
	export let loading = false;
	export let createdAt: number | undefined = undefined;

	$: likelyErrored = loading && (!createdAt || Date.now() - createdAt > TWO_MINUTES_MS);
</script>

<div
	class={cs('flex gap-x-3 px-4 py-3 rounded-md min-h-14', {
		'bg-gray-800 ': type === 'user',
		'bg-slate-900': type === 'assistant'
	})}
>
	<div
		class={cs('rounded-full p-2 w-10 h-10', {
			'bg-rose-500': type === 'assistant',
			'bg-emerald-500': type === 'user'
		})}
	>
		{#if type === 'user'}
			<UserIcon class="w-6 h-6 " />
		{:else}
			<BotIcon class="w-6 h-6" />
		{/if}
	</div>

	<div class="max-w-full justify-center break-words text-gray-200 flex flex-col text-base">
		{#if likelyErrored}
			<span>
				Failed to generate response.
				<span class="text-red-300">Likely errored</span>
			</span>
		{:else if loading}
			<slot name="loading">
				<span class="animate-pulse">Generating response...</span>
			</slot>
		{:else}
			{#await parse(content) then parsedContent}
				{@html parsedContent}
			{:catch error}
				<p class="text-red-300">{String(error)}</p>
			{/await}
		{/if}
	</div>
</div>

{#if likelyErrored}
	<Button
		variant="ghost"
		class="w-fit bg-gray-800 flex gap-x-2 text-gray-400 items-center hover:bg-gray-700 transition-all px-4 py-0.5"
	>
		<span>Regenerate</span>
		<RotateCw class="inline w-4" />
	</Button>
{/if}
