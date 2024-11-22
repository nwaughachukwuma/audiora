<script context="module">
	import '../app.css';
</script>

<script>
	import { browser } from '$app/environment';
	import { Toaster } from '$lib/components/ui/sonner';
	import { setSessionContext } from '@/stores/sessionContext.svelte';
	import RootNav from '@/components/RootNav.svelte';
	import SearchSidebar from '@/components/Sidebar.svelte';
	import { page } from '$app/stores';
	import Spinner from '@/components/Spinner.svelte';
	import { setAppContext } from '@/stores/appContext.svelte';

	export let data;

	$: sessionId = $page.params.sessionId || data.sessionId;

	$: setAppContext();
	$: setSessionContext(sessionId);
</script>

<svelte:head>
	<title>Audiora</title>
</svelte:head>

<div class="h-screen bg-background block w-full">
	<RootNav {sessionId} />

	<div class="relative flex h-full w-full gap-x-2">
		<span class="hidden md:block">
			{#if browser}
				{#key sessionId}
					<SearchSidebar />
				{/key}
			{/if}
		</span>

		{#if !browser}
			<div class="-mt-16 flex h-full w-full items-center justify-center sm:-mt-24">
				<Spinner />
			</div>
		{:else}
			{#key sessionId}
				<slot />
			{/key}
		{/if}
	</div>
</div>

<Toaster />
