<script lang="ts" context="module">
	import { browser } from '$app/environment';
	import { SESSION_KEY } from '@/stores/sessionContext.svelte';

	const ONE_DAY_MS = 24 * 60 * 60 * 1000;
	const last24Hrs = Date.now() - ONE_DAY_MS;
	const last7Days = Date.now() - 4 * ONE_DAY_MS;

	export function getSessionItems() {
		if (!browser) return [];

		return Object.entries(localStorage)
			.filter(([key]) => key.startsWith(SESSION_KEY))
			.map(
				([key, value]) =>
					[key.replace(`${SESSION_KEY}_`, ''), JSON.parse(value) as Session] as const
			)
			.filter(([_, v]) => Boolean(v));
	}

	function getSidebarItems(sessionItems: (readonly [string, Session])[]) {
		return sessionItems
			.filter(([_, item]) => item.chats.length)
			.map(([sessionId, session]) => ({
				sessionId,
				title: session.title || 'Untitled',
				nonce: session.nonce,
				category: session.category,
				completed: session.completed
			}))
			.sort((a, b) => b.nonce - a.nonce);
	}
</script>

<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { getSessionContext, type Session } from '../stores/sessionContext.svelte';
	import SidebarItem from './SidebarItem.svelte';
	import { getAppContext } from '../stores/appContext.svelte';
	import HeadphoneOff from 'lucide-svelte/icons/headphone-off';
	import cs from 'clsx';
	import { page } from '$app/stores';
	import NewAudiocastButton from './NewAudiocastButton.svelte';
	import { goto, invalidateAll } from '$app/navigation';
	import { env } from '@env';
	import SidebarToggleButton from './SidebarToggleButton.svelte';
	import Logo from './Logo.svelte';

	const dispatch = createEventDispatcher<{ clickItem: void }>();
	const { openSettingsDrawer$ } = getAppContext();
	const { session$, refreshSidebar$ } = getSessionContext();

	$: sidebarItems = getSidebarItems(getSessionItems());

	$: if ($refreshSidebar$ || $session$?.title) {
		sidebarItems = getSidebarItems(getSessionItems());
	}

	$: inLast24Hrs = sidebarItems.filter((i) => i.nonce > last24Hrs);
	$: inLast7Days = sidebarItems.filter((i) => i.nonce < last24Hrs && i.nonce > last7Days);
	$: inLast30Days = sidebarItems.filter((i) => i.nonce < last24Hrs && i.nonce < last7Days);

	function dispatchClickItem() {
		dispatch('clickItem');
	}

	$: rootPath = $page.url.pathname === '/';

	function deleteSession(sessionId: string) {
		return async () => {
			localStorage.removeItem(`${SESSION_KEY}_${sessionId}`);
			sidebarItems = getSidebarItems(getSessionItems());

			void fetch(`${env.API_BASE_URL}/delete-session/${sessionId}`, {
				method: 'DELETE'
			}).catch(() => void 0);

			return goto('/', { invalidateAll: true, replaceState: true });
		};
	}
</script>

<div
	class={cs('scrollbar-none block h-full shrink-0 overflow-y-auto overflow-x-hidden bg-gray-900', {
		'w-full px-2 md:w-72 xl:w-80': $openSettingsDrawer$,
		'w-0 opacity-0': !$openSettingsDrawer$
	})}
	style="transition: width 0.3s cubic-bezier(0.34, 1.47, 0.64, 1), padding 0.3s ease;"
>
	<div
		class="flex pl-1 max-md:hidden mt-[6px] animate-fade-in mb-2 items-center"
		class:hidden={!$openSettingsDrawer$}
	>
		<SidebarToggleButton on:click={() => openSettingsDrawer$.update((v) => !v)} />

		<a class="block shrink-0" href="/" on:click={invalidateAll}>
			<Logo />
		</a>
	</div>

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
		{:else}
			<div class="flex w-full flex-col gap-y-1.5 pt-2" class:hidden={!inLast24Hrs.length}>
				<div class="px-2 text-sm font-semibold">Last 24 hrs</div>
				{#each inLast24Hrs as item (item.sessionId)}
					<SidebarItem
						{item}
						on:click={dispatchClickItem}
						on:deleteSession={deleteSession(item.sessionId)}
					/>
				{/each}
			</div>

			<div class="flex w-full flex-col gap-y-1.5 pt-6" class:hidden={!inLast7Days.length}>
				<div class="px-2 text-sm font-semibold">Last 7 days</div>
				{#each inLast7Days as item (item.sessionId)}
					<SidebarItem
						{item}
						on:click={dispatchClickItem}
						on:deleteSession={deleteSession(item.sessionId)}
					/>
				{/each}
			</div>

			<div class="flex w-full flex-col gap-y-1.5 pt-6" class:hidden={!inLast30Days.length}>
				<div class="px-2 text-sm font-semibold">Last 30 days</div>
				{#each inLast30Days as item (item.sessionId)}
					<SidebarItem
						{item}
						on:click={dispatchClickItem}
						on:deleteSession={deleteSession(item.sessionId)}
					/>
				{/each}
			</div>
			<div class="block h-20"></div>
		{/if}
	</nav>
</div>
