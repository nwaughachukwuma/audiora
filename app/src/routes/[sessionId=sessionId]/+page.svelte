<script lang="ts">
	import ChatContainer from '@/components/ChatContainer.svelte';
	import { getChatSession, type ChatItem } from '$lib/stores/chatStore.svelte';
	import ChatListItem from '@/components/chat-list/ChatListItem.svelte';
	import { env } from '@env';
	import { uuid } from '@/utils/uuid';

	export let data;

	const { chatSession$ } = getChatSession();
	let searchTerm = '';
	let loading = false;

	$: category = data.category;
	$: sessionId = data.sessionId;

	$: sessionId && handleFirstEntry();

	async function handleFirstEntry() {
		if ($chatSession$.length > 1) return;

		const firstMessage = $chatSession$[0];

		loading = true;
		await chatRequest(firstMessage)
			.then((data) => {
				chatSession$.update((session) => [
					...session,
					{
						id: uuid(),
						content: data.join(''),
						role: 'assistant'
					}
				]);
			})
			.finally(() => (loading = false));
	}

	async function handleSearch() {
		if (loading || !searchTerm) return;
		loading = true;

		const message: ChatItem = { id: uuid(), content: searchTerm, role: 'user' };
		searchTerm = '';
		chatSession$.update((session) => [...session, message]);

		return chatRequest(message)
			.then((data) => {
				chatSession$.update((session) => [
					...session,
					{
						id: uuid(),
						content: data.join(''),
						role: 'assistant'
					}
				]);
			})
			.finally(() => (loading = false));
	}

	async function chatRequest(message: ChatItem) {
		return fetch(`${env.API_BASE_URL}/chat/${sessionId}`, {
			method: 'POST',
			body: JSON.stringify({
				message,
				content_category: category
			}),
			headers: { 'Content-Type': 'application/json' }
		})
			.then<string[]>((res) => res.json())
			.then((data) => {
				console.log('data', data);
				return data;
			});
	}
</script>

<ChatContainer on:click={handleSearch} on:keypress={handleSearch}>
	<div slot="content" class="flex flex-col gap-y-4">
		<p class="mt-3 p-3 bg-sky-950 text-sky-200 rounded-md">
			Chat session to understand your preferences
		</p>

		{#key $chatSession$}
			{#each $chatSession$ as item (item.id)}
				<ChatListItem type={item.role} content={item.content} />
			{/each}
		{/key}
	</div>
</ChatContainer>
