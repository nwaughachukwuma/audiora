<script>
	import ChatContainer from '@/components/ChatContainer.svelte';
	import { getChatSession } from '$lib/stores/chatStore.svelte';
	import ChatListItem from '@/components/chat-list/ChatListItem.svelte';

	export let data;

	const { chatSession$ } = getChatSession();
	$: category = data.category;
	$: sessionId = data.sessionId;

	let searchTerm = '';

	function handleSearch() {
		if (searchTerm) {
			console.log(searchTerm);
		}
	}
</script>

<ChatContainer on:click={handleSearch} on:keypress={handleSearch}>
	<div slot="content">
		{#each $chatSession$ as chatItem}
			<ChatListItem type={chatItem.role} content={chatItem.content} />
		{:else}
			<p class="text-muted-foreground">No chat messages yet</p>
		{/each}
	</div>
</ChatContainer>
