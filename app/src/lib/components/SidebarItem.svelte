<script lang="ts" context="module">
	export type SearchSidebarItem = {
		title: string;
		nonce: number;
		href: string;
		sessionId: string;
	};
</script>

<script lang="ts">
	import { cubicInOut } from 'svelte/easing';
	import { crossfade } from 'svelte/transition';
	import { page } from '$app/stores';
	import { Button } from './ui/button';
	import cs from 'clsx';
	import { cn } from '@/utils/ui.utils';

	export let item: SearchSidebarItem;

	const [send, receive] = crossfade({
		duration: 250,
		easing: cubicInOut
	});

	$: isActive = $page.url.href.includes(item.sessionId);
</script>

<Button
	href={item.href}
	variant="ghost"
	class="relative no-underline hover:no-underline justify-start px-2 hover:bg-gray-700 bg-gray-900"
	data-sveltekit-noscroll
	on:click
>
	{#if isActive}
		<div
			class="absolute inset-0 transition-all rounded-md bg-gray-800 hover:bg-gray-700"
			in:send={{ key: 'active-sidebar-tab' }}
			out:receive={{ key: 'active-sidebar-tab' }}
		/>
	{/if}
	<div
		class={cn('relative font-normal truncate text-gray-200', {
			'font-medium': isActive
		})}
		title={item.title}
	>
		{item.title}
	</div>
</Button>
