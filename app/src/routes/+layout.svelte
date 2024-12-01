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

	export let data;

	const { openSettingsDrawer$ } = getAppContext();

	$: sessionId = $page.params.sessionId || data.sessionId;

	$: setAppContext();
	$: setSessionContext(sessionId);

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
	<div class={cs('w-full', { 'md:hidden': $openSettingsDrawer$ })}>
		<RootNav {sessionId} />
	</div>
	<div
		class={cs('flex w-full relative', {
			'h-full': $openSettingsDrawer$,
			'h-[calc(100vh-4rem)]': !$openSettingsDrawer$
		})}
	>
		{#if browser}
			<span class="hidden md:block">
				<Sidebar />
			</span>

			{#key sessionId}
				<div class={cs('w-full max-w-screen-2xl mx-auto', { 'md:mt-16': $openSettingsDrawer$ })}>
					<slot />
				</div>
			{/key}
		{:else}
			<div class="-mt-16 flex h-full w-full items-center justify-center sm:-mt-24">
				<Spinner />
			</div>
		{/if}
	</div>
</div>

<Toaster />
