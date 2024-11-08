<script context="module">
	const ONE_DAY_MS = 24 * 60 * 60 * 1000;
	const last24Hrs = Date.now() - ONE_DAY_MS;
	const last7Days = Date.now() - 4 * ONE_DAY_MS;
</script>

<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { browser } from '$app/environment';
	import {
		type Session,
		SESSION_KEY,
		setSessionContext,
		getSessionContext
	} from '../stores/sessionContext.svelte';
	import SearchSidebarItem from './SearchSidebarItem.svelte';
	import { getAppContext } from '../stores/appContext.svelte';
	import cs from 'clsx';

	export let sessionId: string;

	const dispatch = createEventDispatcher<{ clickItem: void }>();

	const { openSettingsDrawer$ } = getAppContext();

	$: ({ session$ } = getSessionContext() || setSessionContext(sessionId));

	$: sessionItems = browser || $session$ ? getSessionItems() : [];

	$: sidebarItems = sessionItems
		.filter(([_, item]) => item.chats.length)
		.map(([sessionId, item]) => ({
			title: item.title || 'Untitled',
			nonce: item.nonce,
			href: `/chat/${sessionId}`
		}))
		.sort((a, b) => b.nonce - a.nonce);

	$: inLast24Hrs = sidebarItems.filter((i) => i.nonce > last24Hrs);
	$: inLast7Days = sidebarItems.filter((i) => i.nonce < last24Hrs && i.nonce > last7Days);
	$: inLast30Days = sidebarItems.filter((i) => i.nonce < last24Hrs && i.nonce < last7Days);

	function getSessionItems() {
		return Object.entries(localStorage)
			.filter(([key]) => key.startsWith(SESSION_KEY))
			.map(
				([key, value]) =>
					[key.replace(`${SESSION_KEY}_`, ''), JSON.parse(value) as Session] as const
			);
	}
</script>

<div
	class={cs('scrollbar-none block h-full shrink-0 overflow-x-hidden bg-gray-50', {
		'w-full overflow-y-auto px-2 md:w-64': $openSettingsDrawer$,
		'w-0': !$openSettingsDrawer$
	})}
	style="transition: width 0.3s cubic-bezier(0.34, 1.47, 0.64, 1), padding 0.3s ease;"
>
	<nav
		class={cs('flex w-full flex-col gap-x-2 lg:gap-x-0 lg:gap-y-1', {
			'opacity-100': $openSettingsDrawer$,
			'opacity-0': !$openSettingsDrawer$
		})}
		style="transition: opacity 0.1s ease"
		data-sveltekit-preload-data
	>
		<div class="flex w-full flex-col pt-2" class:hidden={!inLast24Hrs.length}>
			<div class="px-2 text-sm font-medium">Today</div>
			{#each inLast24Hrs as item}
				<SearchSidebarItem {item} on:click={() => dispatch('clickItem')} />
			{/each}
		</div>

		<div class="flex w-full flex-col pt-6" class:hidden={!inLast7Days.length}>
			<div class="px-2 text-sm font-medium">Last 7 days</div>
			{#each inLast7Days as item}
				<SearchSidebarItem {item} on:click={() => dispatch('clickItem')} />
			{/each}
		</div>

		<div class="flex w-full flex-col pt-6" class:hidden={!inLast30Days.length}>
			<div class="px-2 text-sm font-medium">Last month</div>
			{#each inLast30Days as item}
				<SearchSidebarItem {item} on:click={() => dispatch('clickItem')} />
			{/each}
		</div>
		<div class="block h-20"></div>
	</nav>
</div>
