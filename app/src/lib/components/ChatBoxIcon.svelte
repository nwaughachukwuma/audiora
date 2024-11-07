<script lang="ts">
	import { SearchIcon, SendIcon } from 'lucide-svelte';
	import cs from 'clsx';
	import Spinner from './Spinner.svelte';

	export let loading = false;
	export let disabled = false;
	export let searchTerm = '';
	export let iconType: 'search' | 'send' = 'search';
</script>

<button
	class={cs(
		'my-2 flex h-8 w-8 items-center justify-center rounded-md outline-none transition duration-200 ease-in-out hover:scale-[1.02] active:translate-y-1',
		{
			'p-1': iconType === 'search',
			'p-2': iconType === 'send',
			'bg-gray-600': (searchTerm || loading) && iconType === 'send'
		}
	)}
	disabled={disabled || !searchTerm}
	on:click
>
	{#if loading}
		<span class:text-white={iconType === 'send'}>
			<Spinner small />
		</span>
	{:else if iconType === 'send'}
		<svg
			class="h-6 w-6 fill-gray-600 transition-colors duration-200"
			class:opacity-50={!searchTerm}
			class:text-white={searchTerm}
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
		>
			<path fill="currentColor" d="m2 21l21-9L2 3v7l15 2l-15 2v7Z" />
		</svg>
	{:else}
		<SendIcon
			class="h-full w-full rounded-sm opacity-70 transition-colors duration-200 hover:bg-gray-400/40"
		/>
	{/if}
</button>
