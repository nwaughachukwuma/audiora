<script context="module">
	const ONE_DAY_MS = 24 * 60 * 60 * 1000;
	const last24Hrs = Date.now() - ONE_DAY_MS;
	const last7Days = Date.now() - 4 * ONE_DAY_MS;
</script>

<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { browser } from '$app/environment';
	import { type Session, SESSION_KEY, getSessionContext } from '../stores/sessionContext.svelte';
	import SearchSidebarItem from './SidebarItem.svelte';
	import { getAppContext } from '../stores/appContext.svelte';
	import HeadphoneOff from 'lucide-svelte/icons/headphone-off';
	import cs from 'clsx';
	import { page } from '$app/stores';
	import NewAudiocastButton from './NewAudiocastButton.svelte';

	const dispatch = createEventDispatcher<{ clickItem: void }>();

	const { openSettingsDrawer$ } = getAppContext();

	$: ({ session$ } = getSessionContext());

	$: sessionItems = browser || $session$ ? getSessionItems() : [];

	$: sidebarItems = sessionItems
		.filter(([_, item]) => item.chats.length)
		.map(([sessionId, session]) => ({
			sessionId,
			title: session.title || 'Untitled',
			nonce: session.nonce,
			category: session.category,
			completed: session.completed
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
			)
			.filter(([_, v]) => Boolean(v));
	}

	function dispatchClickItem() {
		dispatch('clickItem');
	}

	$: rootPath = $page.url.pathname === '/';
</script>

<div
	class={cs('scrollbar-none block h-full shrink-0 overflow-x-hidden bg-gray-900', {
		'w-full overflow-y-auto px-2 md:w-72 xl:w-80': $openSettingsDrawer$,
		'w-0': !$openSettingsDrawer$
	})}
	style="transition: width 0.3s cubic-bezier(0.34, 1.47, 0.64, 1), padding 0.3s ease;"
>
	<nav
		class={cs('flex w-full flex-col gap-x-2 pt-2 lg:gap-x-0 lg:gap-y-1', {
			'opacity-100': $openSettingsDrawer$,
			'opacity-0': !$openSettingsDrawer$
		})}
		style="transition: opacity 0.1s ease"
		data-sveltekit-preload-data
	>
		{#if !rootPath}
			<NewAudiocastButton />
		{/if}

		{#if !inLast24Hrs.length && !inLast7Days.length && !inLast30Days.length}
			<div class="flex w-full h-screen items-center animate-fade-in">
				<div class="-mt-16 flex flex-col text-gray-300 items-center">
					<HeadphoneOff class="w-14 h-14" />
					<span class="px-2 mt-3 font-medium">Your audiocasts will appear here</span>
				</div>
			</div>
		{/if}

		<div class="flex w-full flex-col gap-y-1.5 pt-2" class:hidden={!inLast24Hrs.length}>
			<div class="px-2 text-sm font-medium">Today</div>
			{#each inLast24Hrs as item}
				<SearchSidebarItem {item} on:click={dispatchClickItem} />
			{/each}
		</div>

		<div class="flex w-full flex-col gap-y-1.5 pt-6" class:hidden={!inLast7Days.length}>
			<div class="px-2 text-sm font-medium">Last 7 days</div>
			{#each inLast7Days as item}
				<SearchSidebarItem {item} on:click={dispatchClickItem} />
			{/each}
		</div>

		<div class="flex w-full flex-col gap-y-1.5 pt-6" class:hidden={!inLast30Days.length}>
			<div class="px-2 text-sm font-medium">Last month</div>
			{#each inLast30Days as item}
				<SearchSidebarItem {item} on:click={dispatchClickItem} />
			{/each}
		</div>
		<div class="block h-20"></div>
	</nav>
</div>
