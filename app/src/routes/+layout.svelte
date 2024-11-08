<script lang="ts" context="module">
	import '../app.css';
</script>

<script>
	import { Toaster } from '$lib/components/ui/sonner';
	import { setSessionContext } from '@/stores/sessionContext.svelte';
	import RootNav from '@/components/RootNav.svelte';
	import SearchSidebar from '@/components/SearchSidebar.svelte';

	export let data;

	$: sessionId = data.sessionId;
	$: setSessionContext(sessionId);
</script>

<svelte:head>
	<title>Audiora</title>
</svelte:head>

<!-- <main class="container p-0 pt-10 max-sm:px-2"></main> -->
<div class="h-screen bg-background block w-full">
	<RootNav {sessionId} />

	<div class="relative flex h-full w-full gap-x-2">
		<span class="hidden md:block">
			<SearchSidebar {sessionId} />
		</span>
		<slot />
	</div>
</div>
<Toaster />
