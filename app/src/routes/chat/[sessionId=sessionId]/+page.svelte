<script lang="ts">
	import ChatContainer from '@/components/ChatContainer.svelte';
	import { getSessionContext, type ChatItem } from '@/stores/sessionContext.svelte.js';
	import ChatListItem from '@/components/chat-list/ChatListItem.svelte';
	import { env } from '@env';
	import { uuid } from '@/utils/uuid';
	import { streamingResponse } from '$lib/utils/streamingResponse';
	import { MessageSquareOff } from 'lucide-svelte';

	export let data;

	const { session$, addChatItem, updateChatContent } = getSessionContext();
	let searchTerm = '';
	let loading = false;

	$: category = data.category;
	$: sessionId = data.sessionId;
	$: sessionId && handleFirstEntry();

	async function handleFirstEntry() {
		if (!$session$ || $session$.chats.length > 1) return;
		loading = true;
		await chatRequest($session$.chats[0]).finally(() => (loading = false));
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

		const chatItem: ChatItem = {
			id: uuid(),
			content: searchTerm,
			role: 'user',
			loading: false
		};
		searchTerm = '';
		addChatItem(chatItem);

		return chatRequest(chatItem).finally(() => (loading = false));
	}

	async function chatRequest(uChatItem: ChatItem) {
		const aChatItem = addChatItem({
			id: uuid(),
			content: '',
			role: 'assistant',
			loading: true
		});

		return fetch(`${env.API_BASE_URL}/chat/${sessionId}`, {
			method: 'POST',
			body: JSON.stringify({ chatItem: uChatItem, contentCategory: category }),
			headers: { 'Content-Type': 'application/json' }
		}).then((res) => handleStreamingResponse(res, aChatItem.id));
	}

	async function handleStreamingResponse(res: Response, id: string) {
		if (!res.ok) throw new Error('Failed to get response from the server');

		for await (const chunk of streamingResponse(res)) {
			updateChatContent(id, chunk);
		}

		return Promise.resolve(scrollChatContent());
	}

	$: sessionChats = $session$?.chats || [];
</script>

<ChatContainer bind:searchTerm on:click={handleSearch} on:keypress={handleSearch}>
	<div slot="content" class="block w-full">
		<p class="mt-10 p-3 bg-sky-950/70 text-sky-200 rounded-md mb-4 w-full">
			Chat session to understand your preferences
		</p>

		<div class="flex flex-col gap-y-3">
			{#key sessionChats}
				{#each sessionChats as item (item.id)}
					<ChatListItem type={item.role} content={item.content} loading={item.loading} />
				{:else}
					<div class="flex flex-col text-gray-300 h-40 mt-16 gap-y-3 items-center justify-center">
						<MessageSquareOff class="w-16 h-16" />
						<p class="text-center text-gray-400 text-xl md:text-2xl">No chat history</p>
					</div>
				{/each}
			{/key}
		</div>
	</div>
</ChatContainer>
