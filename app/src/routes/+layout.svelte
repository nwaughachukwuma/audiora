<script context="module">
	import '../app.css';
</script>

<script>
	import { browser } from '$app/environment';
	import { Toaster } from '$lib/components/ui/sonner';
	import { setSessionContext } from '@/stores/sessionContext.svelte';
	import RootNav from '@/components/RootNav.svelte';
	import Sidebar from '@/components/Sidebar.svelte';
	import { page } from '$app/stores';
	import Spinner from '@/components/Spinner.svelte';
	import { getAppContext, setAppContext } from '@/stores/appContext.svelte';
	import { onMount } from 'svelte';
	import { getAnalytics, logEvent } from 'firebase/analytics';
	import cs from 'clsx';
	import { setAttachmentsContext } from '@/stores/attachmentsContext.svelte';

	export let data;

	const { openSettingsDrawer$ } = getAppContext();

	$: sessionId = $page.params.sessionId || data.sessionId;

	$: setAppContext();
	$: ({ session$ } = setSessionContext(sessionId));

	$: sessionTitle = $session$?.title;
	$: setAttachmentsContext(sessionId);

	onMount(() => {
		logEvent(getAnalytics(), 'page_view', {
			page_title: 'Welcome',
			page_path: '/'
		});
	});
</script>

<svelte:head>
	<title>Audiora</title>
</svelte:head>

<div class="h-screen bg-background block w-full">
	<div class={cs('w-full flex-none', { 'md:hidden': $openSettingsDrawer$ })}>
		<RootNav {sessionId} />
	</div>
	<div
		class={cs('flex w-full relative flex-1 overflow-hidden', {
			'h-full': $openSettingsDrawer$,
			'h-[calc(100dvh-4rem)]': !$openSettingsDrawer$
		})}
	>
		{#if browser}
			<span class="hidden md:block">
				{#key sessionTitle}
					<Sidebar />
				{/key}
			</span>

			{#key sessionId}
				<div
					class={cs('w-full slot-container max-w-screen-2xl mx-auto', {
						'md:mt-16': $openSettingsDrawer$
					})}
				>
					<slot />
				</div>
			{/key}
		{:else}
			<div class="-mt-14 flex h-full w-full items-center justify-center sm:-mt-20">
				<Spinner />
			</div>
		{/if}
	</div>
</div>

<Toaster />

<style>
	@media only screen and (max-width: 424px) {
		.slot-container {
			padding-bottom: env(safe-area-inset-bottom);
		}
	}
</style>
