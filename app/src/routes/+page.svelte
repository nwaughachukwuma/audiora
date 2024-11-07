<script lang="ts">
	// import { browser } from '$app/environment';
	// import { goto } from '$app/navigation';
	// import { page } from '$app/stores';
	// import { sessionStore } from '$lib/stores/session';
	// import ChatInterface from '$lib/components/ChatInterface.svelte';
	// import AudioInterface from '$lib/components/AudioInterface.svelte';
	// $: userSpecification = $sessionStore.userSpecification;
	import RenderExamples from '@/components/RenderExamples.svelte';

	export let data;

	$: sessionId = data.sessionId;
</script>

<svelte:head>
	<title>Audiora</title>
</svelte:head>

<div class="relative overflow-hidden w-full flex flex-col h-full">
	<div class="overflow-auto px-10 w-full block h-[calc(85%-2.5rem)]">
		<div class="flex flex-col gap-y-2">
			<h1 class="text-5xl font-bold">🎧 Audiora</h1>
			<h2 class="text-lg">Listen to anything, anytime.</h2>
		</div>

		<RenderExamples {sessionId} />
	</div>

	<div class="h-[16%] fixed w-[calc(100%-24.5rem)] bottom-0 shrink-0">Chat Input Section</div>
	<!-- {#if !userSpecification}
	  <ChatInterface />
	{:else}
	  <AudioInterface />
	{/if} -->
</div>
