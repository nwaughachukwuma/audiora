<script lang="ts">
	import { onMount, tick } from 'svelte';
	import ChatContainer from '@/components/ChatContainer.svelte';
	import { getSessionContext, type ChatItem } from '@/stores/sessionContext.svelte.js';
	import ChatListItem from '@/components/ChatListItem.svelte';
	import { env } from '@env';
	import { uuid } from '@/utils/uuid';
	import { streamingResponse } from '$lib/utils/streamingResponse';
	import ChatListActionItems from '@/components/ChatListActionItems.svelte';
	import { debounce } from 'throttle-debounce';
	import AudiocastPageHeader from '@/components/AudiocastPageHeader.svelte';
	import { getSummary, isfinalResponse } from '@/utils/session.utils';
	import { getAttachmentsContext } from '@/stores/attachmentsContext.svelte.js';
	import { pluralize } from '@/utils/pluralize';

	export let data;

	const { session$, addChatItem, updateChatContent, sessionId$, removeChatItem } =
		getSessionContext();

	const { sessionUploadItems$ } = getAttachmentsContext();

	let searchTerm = '';
	let loading = false;
	let mounted = false;

	$: category = data.category;
	$: sessionId = $sessionId$;
	$: sessionId && handleFirstEntry();

	$: mounted && scrollChatContent();

	async function handleFirstEntry() {
		if (!$session$ || $session$.chats.length > 1) return;
		return chatRequest($session$.chats[0]);
	}

	const scrollChatContent = debounce(500, () => {
		const chatContent = document.getElementById('chatContainer1');
		if (!chatContent) return;
		requestAnimationFrame(() => {
			chatContent.scrollTo({ top: chatContent.scrollHeight, behavior: 'smooth' });
		});
	});

	async function handleSearch() {
		if (!searchTerm) return;

		scrollChatContent();

		const chatItem: ChatItem = {
			id: uuid(),
			content: searchTerm,
			role: 'user',
			loading: false,
			createdAt: Date.now()
		};
		addChatItem(chatItem);
		searchTerm = '';
		return chatRequest(chatItem);
	}

	async function chatRequest(uItem: ChatItem) {
		if (loading) return;
		loading = true;

		const aItem = addChatItem({
			id: uuid(),
			content: '',
			role: 'assistant',
			loading: true,
			createdAt: Date.now()
		});

		return fetch(`${env.API_BASE_URL}/chat/${sessionId}`, {
			method: 'POST',
			body: JSON.stringify({
				chatItem: uItem,
				contentCategory: category,
				attachments: $sessionUploadItems$.map((i) => i.gcsUrl).filter(Boolean)
			}),
			headers: { 'Content-Type': 'application/json' }
		})
			.then((res) => handleStreamingResponse(res, aItem.id))
			.finally(() => (loading = false));
	}

	async function handleStreamingResponse(res: Response, id: string) {
		if (!res.ok) throw new Error('Failed to get response from the server');

		for await (const chunk of streamingResponse(res)) {
			updateChatContent(id, chunk);
		}

		return Promise.resolve(scrollChatContent());
	}

	$: sessionChats = $session$?.chats || [];

	onMount(() => (mounted = true));

	async function onregenerate() {
		const chats = $session$?.chats;
		if (!chats || chats.length === 1) return;

		const curChatItem = chats[chats.length - 1];
		const prevChatItem = chats[chats.length - 2];
		removeChatItem(curChatItem.id);

		await tick();

		return chatRequest(prevChatItem);
	}
</script>

<ChatContainer bind:searchTerm on:click={handleSearch} on:keypress={handleSearch}>
	<div slot="content" class="block w-full">
		<AudiocastPageHeader category={data.category} title={$session$?.title} />

		<p class="mt-4 p-3 bg-sky-950/70 text-sky-200 rounded-md mb-4 w-full">
			Help us understand your preferences to curate the best audiocast for you.
		</p>

		<div class="flex flex-col gap-y-3 h-full">
			{#each sessionChats as item, ix (item.id)}
				{@const finalResponse = isfinalResponse(item)}
				{@const firstRequest = ix === 1}
				<ChatListItem
					type={item.role}
					content={item.content}
					loading={item.loading}
					createdAt={item.createdAt}
					on:regenerate={onregenerate}
				>
					<span class="animate-pulse" slot="loading">
						{#if firstRequest && $sessionUploadItems$.length}
							{@const count = $sessionUploadItems$.length}
							Evaluating {pluralize(count, 'attachment', 'attachments')}...
						{:else}
							Generating response...
						{/if}
					</span>
				</ChatListItem>

				{#if finalResponse}
					<ChatListActionItems
						title={$session$?.title || 'Untitled'}
						{sessionId}
						{category}
						summary={getSummary(item.content)}
					/>
				{/if}
			{/each}
		</div>
		<div class="h-24"></div>
	</div>
</ChatContainer>
