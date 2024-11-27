<script lang="ts">
	import Logo from './Logo.svelte';
	import SearchSlideSheet from './SlideSheet.svelte';
	import Sidebar from './Sidebar.svelte';
	import { Button } from './ui/button';
	import { getAppContext } from '$lib/stores/appContext.svelte';
	import { invalidateAll } from '$app/navigation';
	import { mediaBreakPoints$ } from '@/utils/mediaBreakpoints';

	export let sessionId: string;

	const { openSettingsDrawer$ } = getAppContext();

	const mdAndUp = mediaBreakPoints$('md');
</script>

<nav class="relative flex h-16 w-full items-center">
	<div class="flex h-full items-center">
		{#if !$mdAndUp}
			<div class="block pl-3">
				<SearchSlideSheet bind:open={$openSettingsDrawer$}>
					<svelte-fragment>
						{#if $openSettingsDrawer$}
							{#key sessionId}
								<Sidebar on:clickItem={() => ($openSettingsDrawer$ = false)} />
							{/key}
						{/if}
					</svelte-fragment>
				</SearchSlideSheet>
			</div>
		{/if}

		{#if $mdAndUp}
			<div class="pl-3 block">
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
		{/if}

		<a class="block shrink-0" href="/" on:click={invalidateAll}>
			<Logo />
		</a>
	</div>
</nav>
