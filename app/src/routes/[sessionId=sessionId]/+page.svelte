<script lang="ts">
	import ChatContainer from '@/components/ChatContainer.svelte';
	import { getChatSession, type ChatItem } from '$lib/stores/chatStore.svelte';
	import ChatListItem from '@/components/chat-list/ChatListItem.svelte';
	import { env } from '@env';
	import { uuid } from '@/utils/uuid';
	import { streamingResponse } from '$lib/utils/streamingResponse';

	export let data;

	const { chatSession$ } = getChatSession();
	let searchTerm = '';
	let loading = false;

	$: category = data.category;
	$: sessionId = data.sessionId;

	$: sessionId && handleFirstEntry();

	async function handleFirstEntry() {
		if ($chatSession$.length > 1) return;

		loading = true;
		await chatRequest($chatSession$[0]).finally(() => (loading = false));
	}

	async function handleSearch() {
		if (loading || !searchTerm) return;
		loading = true;

		const chatItem: ChatItem = { id: uuid(), content: searchTerm, role: 'user' };
		searchTerm = '';
		chatSession$.update((session) => [...session, chatItem]);

		return chatRequest(chatItem).finally(() => (loading = false));
	}

	async function chatRequest(message: ChatItem) {
		return fetch(`${env.API_BASE_URL}/chat/${sessionId}`, {
			method: 'POST',
			body: JSON.stringify({ message, content_category: category }),
			headers: { 'Content-Type': 'application/json' }
		}).then(handleStreamingResponse);
	}

	async function handleStreamingResponse(res: Response) {
		if (!res.ok) throw new Error('Failed to get response from the server');

		const __uid = uuid();
		chatSession$.update((session) => [...session, { id: __uid, content: '', role: 'assistant' }]);

		for await (const chunk of streamingResponse(res)) {
			chatSession$.update((session) => {
				const lastItem = session.find((item) => item.id === __uid);
				if (!lastItem) return session;

				const updatedMessage = { ...lastItem, content: lastItem.content + chunk };
				return session.map((item) => (item.id === __uid ? updatedMessage : item));
			});
		}
	}
</script>

<ChatContainer on:click={handleSearch} on:keypress={handleSearch}>
	<div slot="content" class="flex flex-col gap-y-4">
		<p class="mt-10 p-3 bg-sky-950 text-sky-200 rounded-md">
			Chat session to understand your preferences
		</p>

		{#key $chatSession$}
			{#each $chatSession$ as item (item.id)}
				<ChatListItem type={item.role} content={item.content} />
			{/each}
		{/key}
	</div>
</ChatContainer>
