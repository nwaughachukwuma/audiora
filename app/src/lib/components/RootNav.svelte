<script lang="ts">
	import Logo from './Logo.svelte';
	import SearchSlideSheet from './SlideSheet.svelte';
	import Sidebar from './Sidebar.svelte';
	import { getAppContext } from '$lib/stores/appContext.svelte';
	import { invalidateAll } from '$app/navigation';
	import { mediaBreakPoints$ } from '@/utils/mediaBreakpoints';
	import SidebarToggleButton from './SidebarToggleButton.svelte';

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
		{:else}
			<div class="pl-3 block">
				<SidebarToggleButton on:click={() => openSettingsDrawer$.update((v) => !v)} />
			</div>
		{/if}

		<a class="block shrink-0" href="/" on:click={invalidateAll}>
			<Logo />
		</a>
	</div>
</nav>
