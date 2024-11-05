<script lang="ts" context="module">
	import '../app.css';
	import { page } from '$app/stores';
	// import { browser } from '$app/environment';
	// import { goto } from '$app/navigation';
	// import { sessionStore } from '$lib/stores/session';
	// import ChatInterface from '$lib/components/ChatInterface.svelte';
	// import AudioInterface from '$lib/components/AudioInterface.svelte';

	// $: userSpecification = $sessionStore.userSpecification;
</script>

<svelte:head>
	<title>Audiora</title>
</svelte:head>

<div class="min-h-screen bg-background flex gap-x-2">
	<aside class="shrink-0 h-screen pt-10 w-64 bg-gray-900 p-4">
		<div class="text-sm text-muted-foreground p-3 rounded-lg bg-gray-700">
			A VeedoAI project. (c) 2024
		</div>

		<div class="pt-2">
			{#if $page.data.contentCategory}
				<h3 class="mt-4 text-lg font-semibold">Content Category:</h3>
				<p class="capitalize">{$page.data.contentCategory}</p>
			{:else}
				<p class="mt-4 text-sm text-muted-foreground">
					Your preferences and audiocast metadata will appear here
				</p>
			{/if}
		</div>
	</aside>

	<main class="container mx-auto px-6 pt-10 md:px-10">
		<slot />
	</main>
</div>
