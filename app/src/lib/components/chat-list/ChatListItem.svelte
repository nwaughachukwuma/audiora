<script lang="ts">
	import { UserIcon, BotIcon } from 'lucide-svelte';
	import cs from 'clsx';
	import { parse } from 'marked';

	export let type: 'user' | 'assistant';
	export let content: string;
	export let loading = false;
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
		{#if loading}
			<span class="animate-pulse">Generating response...</span>
		{:else}
			{#await parse(content) then parsedContent}
				{@html parsedContent}
			{/await}
		{/if}
	</div>
</div>
