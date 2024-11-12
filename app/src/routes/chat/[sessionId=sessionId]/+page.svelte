<script lang="ts">
	import { onMount } from 'svelte';
	import ChatContainer from '@/components/ChatContainer.svelte';
	import { getSessionContext, type ChatItem } from '@/stores/sessionContext.svelte.js';
	import ChatListItem from '@/components/ChatListItem.svelte';
	import { env } from '@env';
	import { uuid } from '@/utils/uuid';
	import { streamingResponse } from '$lib/utils/streamingResponse';
	import ChatListActionItems, {
		FINAL_RESPONSE_SUFFIX
	} from '@/components/ChatListActionItems.svelte';
	import { debounce } from 'throttle-debounce';

	export let data;

	const { session$, addChatItem, updateChatContent, sessionId$, fetchingSource$ } =
		getSessionContext();

	let searchTerm = '';
	let loading = false;
	let mounted = false;

	$: category = data.category;
	$: sessionId = $sessionId$;
	$: sessionId && handleFirstEntry();

	$: mounted && scrollChatContent();

	async function handleFirstEntry() {
		if (!$session$ || $session$.chats.length > 1) return;
		loading = true;
		await chatRequest($session$.chats[0]).finally(() => (loading = false));
	}

	const scrollChatContent = debounce(500, () => {
		const chatContent = document.getElementById('chatContainer1');
		if (!chatContent) return;
		requestAnimationFrame(() => {
			chatContent.scrollTo({ top: chatContent.scrollHeight, behavior: 'smooth' });
		});
	});

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
		addChatItem(chatItem);
		searchTerm = '';

		return chatRequest(chatItem).finally(() => (loading = false));
	}

	async function chatRequest(uItem: ChatItem) {
		const aItem = addChatItem({
			id: uuid(),
			content: '',
			role: 'assistant',
			loading: true
		});

		return fetch(`${env.API_BASE_URL}/chat/${sessionId}`, {
			method: 'POST',
			body: JSON.stringify({ chatItem: uItem, contentCategory: category }),
			headers: { 'Content-Type': 'application/json' }
		}).then((res) => handleStreamingResponse(res, aItem.id));
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
</script>

<ChatContainer bind:searchTerm on:click={handleSearch} on:keypress={handleSearch}>
	<div slot="content" class="block w-full">
		<div class="mb-4 flex flex-col gap-y-2">
			<span class="capitalize bg-gray-800 text-gray-300 w-fit py-1 px-3 rounded-md">
				{data.category}
			</span>

			{#if $session$?.title}
				<h1 class="text-2xl font-semibold text-sky-200 mb-4">{$session$.title}</h1>
			{/if}
		</div>
		<p class="mt-6 p-3 bg-sky-950/70 text-sky-200 rounded-md mb-4 w-full">
			Help us understand your preferences to curate the best audiocast for you.
		</p>

		<div class="flex flex-col gap-y-3 h-full">
			{#key sessionChats}
				{#each sessionChats as item (item.id)}
					{@const finalResponse = item.content.includes(FINAL_RESPONSE_SUFFIX)}
					<ChatListItem type={item.role} content={item.content} loading={item.loading} />

					{#if finalResponse && $fetchingSource$}
						<div
							class="py-1 px-3 mx-auto w-fit bg-sky-600/20 animate-pulse text-sky-300 rounded-sm"
						>
							Fetching Audiocast Source...Please wait
						</div>
					{:else if finalResponse}
						<ChatListActionItems
							title={$session$?.title || 'Untitled'}
							{sessionId}
							{category}
							content={item.content}
						/>
					{/if}
				{/each}
			{/key}
		</div>
		<div class="h-24"></div>
	</div>
</ChatContainer>
