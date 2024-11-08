<script lang="ts" context="module">
	import '../app.css';
</script>

<script>
	import { Toaster } from '$lib/components/ui/sonner';
	import { setSessionContext } from '@/stores/sessionContext.svelte';
	export let data;
	$: setSessionContext(data.sessionId);
</script>

<svelte:head>
	<title>Audiora</title>
</svelte:head>

<div class="h-screen bg-background flex gap-x-2">
	<main class="container p-0 pt-10 max-sm:px-2">
		<slot />
	</main>
</div>

<Toaster />
