<script lang="ts" context="module">
	import type { ContentCategory } from '@/utils/types';
	export type SearchSidebarItem = {
		title: string;
		nonce: number;
		sessionId: string;
		category: ContentCategory;
		completed?: boolean;
	};
</script>

<script lang="ts">
	import { cubicInOut } from 'svelte/easing';
	import { crossfade } from 'svelte/transition';
	import { page } from '$app/stores';
	import { Button } from './ui/button';
	import { cn } from '@/utils/ui.utils';

	export let item: SearchSidebarItem;

	const [send, receive] = crossfade({
		duration: 250,
		easing: cubicInOut
	});

	$: href = item.completed
		? `/audiocast/${item.sessionId}`
		: `/chat/${item.sessionId}?category=${item.category}`;
	$: isActive = $page.url.href.includes(item.sessionId);
</script>

<Button
	{href}
	variant="ghost"
	class="relative no-underline group hover:no-underline justify-start py-6 flex items-center px-2 hover:bg-gray-700 bg-gray-900"
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

	<div class="text-[10px] px-2 hidden group-hover:block absolute bottom-0 right-0 text-sky-200">
		{item.category}
	</div>
</Button>
