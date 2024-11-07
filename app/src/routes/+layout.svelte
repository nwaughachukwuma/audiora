<script lang="ts" context="module">
	import '../app.css';
</script>

<script>
	import { page } from '$app/stores';
	import { setChatSession } from '$lib/stores/chatStore.svelte';
	export let data;
	$: setChatSession(data.sessionId);
</script>

<svelte:head>
	<title>Audiora</title>
</svelte:head>

<div class="h-screen bg-background flex gap-x-2">
	<aside class="shrink-0 h-screen pt-10 w-96 bg-gray-900 p-4 px-8">
		<div class="text-muted-foreground px-3 py-4 rounded-lg bg-gray-700">
			A VeedoAI project. (c) 2024
		</div>

		<div class="pt-2">
			{#if $page.data.category}
				<h3 class="mt-4 text-lg font-medium capitalize">
					Content Category: {$page.data.category}
				</h3>
			{:else}
				<p class="mt-4 text-muted-foreground">
					Your preferences and audiocast metadata will appear here
				</p>
			{/if}
		</div>
	</aside>

	<main class="container p-0 pt-10">
		<slot />
	</main>
</div>
