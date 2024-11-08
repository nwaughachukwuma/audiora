<script lang="ts">
	import { page } from '$app/stores';
	import Logo from './Logo.svelte';
	import * as Breadcrumb from './ui/breadcrumb';
	import { PlusIcon } from 'lucide-svelte';
	import * as Tooltip from './ui/tooltip';
	import SearchSlideSheet from './SearchSlideSheet.svelte';
	import SearchSidebar from './SearchSidebar.svelte';
	import { Button } from './ui/button';
	import { getAppContext } from '$lib/stores/appContext.svelte';
	import cs from 'clsx';

	export let sessionId: string;

	const { openSettingsDrawer$ } = getAppContext();

	let openSheet = false;

	$: openSettingsDrawer$.set(openSheet);
	$: pathname = $page.url.pathname;
	$: pathSegments = pathname.replace(/^\/|\/$/, '').split('/');
</script>

<nav class="relative flex h-16 w-full items-center">
	<div class="flex h-full items-center">
		<div class="block pl-3 md:hidden">
			<SearchSlideSheet bind:open={openSheet}>
				<svelte-fragment>
					{#if openSheet}
						{#key sessionId}
							<SearchSidebar {sessionId} on:clickItem={() => (openSheet = false)} />
						{/key}
					{/if}
				</svelte-fragment>
			</SearchSlideSheet>
		</div>

		<div class="hidden pl-3 md:block">
			<Button variant="ghost" class="px-2" on:click={() => openSettingsDrawer$.update((v) => !v)}>
				<svg viewBox="0 0 24 24" fill="none" class="text-icon-secondary h-6">
					<path
						fill="currentColor"
						fill-rule="evenodd"
						clip-rule="evenodd"
						d="M2 6C2 5.44772 2.44772 5 3 5H21C21.5523 5 22 5.44772 22 6C22 6.55228 21.5523 7 21 7H3C2.44772 7 2 6.55228 2 6ZM2 12C2 11.4477 2.44772 11 3 11H21C21.5523 11 22 11.4477 22 12C22 12.5523 21.5523 13 21 13H3C2.44772 13 2 12.5523 2 12ZM2 18C2 17.4477 2.44772 17 3 17H11C11.5523 17 12 17.4477 12 18C12 18.5523 11.5523 19 11 19H3C2.44772 19 2 18.5523 2 18Z"
					></path>
				</svg>
			</Button>
		</div>

		<a class="block shrink-0" href="/">
			<Logo />
		</a>
	</div>

	<div class="ml-6 flex h-full max-h-full items-center justify-between px-3">
		<Breadcrumb.Root class="hidden [@media(min-width:682px)]:block">
			<Breadcrumb.List>
				<Breadcrumb.Item>
					<Breadcrumb.Link href="/">Home</Breadcrumb.Link>
				</Breadcrumb.Item>

				{#each pathSegments as segment, index}
					{@const lastItem = index === pathSegments.length - 1}
					{@const href = pathSegments.slice(0, index + 1).join('/')}

					<Breadcrumb.Separator></Breadcrumb.Separator>
					<Breadcrumb.Item>
						<Breadcrumb.Link
							class={cs({ 'pointer-events-none text-gray-700': lastItem })}
							href={`/${href}`}
						>
							{segment}
						</Breadcrumb.Link>
					</Breadcrumb.Item>
				{/each}
			</Breadcrumb.List>
		</Breadcrumb.Root>

		<Tooltip.Root>
			<Tooltip.Trigger>
				<a
					href="/search"
					class="ml-6 flex h-7 items-center justify-center rounded-md border border-gray-300 p-1 px-1.5 text-gray-500 transition-colors duration-200 hover:border-gray-500 hover:text-gray-600"
				>
					<PlusIcon class="h-4 w-4" />
				</a>
			</Tooltip.Trigger>
			<Tooltip.Content>
				<p>New Generation</p>
			</Tooltip.Content>
		</Tooltip.Root>
	</div>
</nav>
