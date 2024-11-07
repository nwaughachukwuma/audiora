<script lang="ts">
	// import { browser } from '$app/environment';
	// import { goto } from '$app/navigation';
	// import { page } from '$app/stores';
	// import { sessionStore } from '$lib/stores/session';
	// import ChatInterface from '$lib/components/ChatInterface.svelte';
	// import AudioInterface from '$lib/components/AudioInterface.svelte';
	// $: userSpecification = $sessionStore.userSpecification;
	import RenderExamples from '@/components/RenderExamples.svelte';
</script>

<svelte:head>
	<title>Audiora</title>
</svelte:head>

<div class="relative overflow-hidden w-full flex flex-col h-full">
	<div class="overflow-auto px-10 w-full block h-[calc(80%-2.5rem)]">
		<div class="flex flex-col gap-y-4">
			<h1 class="text-5xl font-bold">🎧 Audiora</h1>
			<h2 class="text-3xl">Listen to anything, anytime, leveraging AI</h2>
		</div>

		<h3 class="text-lg mt-6">
			Tell me what you'd like to listen to, and I'll create an audiocast for you!
		</h3>

		<RenderExamples />
	</div>

	<div class="h-[calc(16%)] fixed w-[calc(100%-24.5rem)] bottom-0 shrink-0 border">
		Chat Input Section
	</div>
	<!-- {#if !userSpecification}
	  <ChatInterface />
	{:else}
	  <AudioInterface />
	{/if} -->
</div>
