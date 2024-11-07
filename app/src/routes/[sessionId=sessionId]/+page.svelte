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

	function scrollChatContent() {
		const chatContent = document.getElementById('chatContainer1');
		if (!chatContent) return;
		requestAnimationFrame(() => {
			chatContent.scrollTo({ top: chatContent.scrollHeight, behavior: 'smooth' });
		});
	}

	async function handleSearch() {
		if (loading || !searchTerm) return;
		loading = true;
		scrollChatContent();

		const chatItem: ChatItem = { id: uuid(), content: searchTerm, role: 'user' };
		searchTerm = '';
		chatSession$.update((session) => [...session, chatItem]);

		return chatRequest(chatItem).finally(() => (loading = false));
	}

	async function chatRequest(message: ChatItem) {
		const __uid = uuid();
		chatSession$.update((session) => [
			...session,
			{
				id: __uid,
				content: '',
				role: 'assistant',
				loading: true
			}
		]);

		return fetch(`${env.API_BASE_URL}/chat/${sessionId}`, {
			method: 'POST',
			body: JSON.stringify({ message, content_category: category }),
			headers: { 'Content-Type': 'application/json' }
		}).then((res) => handleStreamingResponse(res, __uid));
	}

	async function handleStreamingResponse(res: Response, id: string) {
		if (!res.ok) throw new Error('Failed to get response from the server');

		for await (const chunk of streamingResponse(res)) {
			chatSession$.update((session) => {
				const lastItem = session.find((item) => item.id === id);
				if (!lastItem) return session;

				const updatedMessage = { ...lastItem, loading: false, content: lastItem.content + chunk };
				return session.map((item) => (item.id === id ? updatedMessage : item));
			});
		}

		scrollChatContent();
	}
</script>

<ChatContainer bind:searchTerm on:click={handleSearch} on:keypress={handleSearch}>
	<div slot="content" class="block w-full">
		<p class="mt-10 p-3 bg-sky-950/70 text-sky-200 rounded-md mb-4">
			Chat session to understand your preferences
		</p>

		<div class="flex flex-col gap-y-3">
			{#key $chatSession$}
				{#each $chatSession$ as item (item.id)}
					<ChatListItem type={item.role} content={item.content} loading={item.loading} />
				{/each}
			{/key}
		</div>
	</div>
</ChatContainer>
