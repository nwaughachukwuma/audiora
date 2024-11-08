<script lang="ts" context="module">
	export type SearchSidebarItem = {
		title: string;
		nonce: number;
		href: string;
	};
</script>

<script lang="ts">
	import { cubicInOut } from 'svelte/easing';
	import { crossfade } from 'svelte/transition';
	import { page } from '$app/stores';
	import { Button } from './ui/button';
	import cs from 'clsx';

	export let item: SearchSidebarItem;

	const [send, receive] = crossfade({
		duration: 250,
		easing: cubicInOut
	});

	$: isActive = $page.url.href.includes(item.href);
</script>

<Button
	href={item.href}
	variant="ghost"
	class="relative justify-start px-2 hover:bg-gray-200/90"
	data-sveltekit-noscroll
	on:click
>
	{#if isActive}
		<div
			class="absolute inset-0 rounded-md bg-gray-200"
			in:send={{ key: 'active-sidebar-tab' }}
			out:receive={{ key: 'active-sidebar-tab' }}
		/>
	{/if}
	<div
		class={cs('relative truncate', {
			'text-indigo-600': isActive,
			'font-normal text-gray-700 ': !isActive
		})}
		title={item.title}
	>
		{item.title}
	</div>
</Button>
