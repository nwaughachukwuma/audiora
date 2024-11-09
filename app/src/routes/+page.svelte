<script lang="ts">
	import RenderExamples from '@/components/RenderExamples.svelte';
	import ChatContainer from '@/components/ChatContainer.svelte';
	import { getSessionContext } from '@/stores/sessionContext.svelte.js';

	const { sessionId$ } = getSessionContext();

	let searchTerm = '';
	$: sessionId = $sessionId$;

	function handleSearch() {
		if (searchTerm) {
			console.log(searchTerm);
		}
	}
</script>

<svelte:head>
	<title>Audiora</title>
</svelte:head>

<ChatContainer on:click={handleSearch} on:keypress={handleSearch}>
	<RenderExamples slot="content" {sessionId} />
</ChatContainer>
