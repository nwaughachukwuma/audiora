<script lang="ts">
	import ChatContainer from '@/components/ChatContainer.svelte';
	import { getSessionContext, type ChatItem } from '@/stores/sessionContext.svelte.js';
	import ChatListItem from '@/components/chat-list/ChatListItem.svelte';
	import { env } from '@env';
	import { uuid } from '@/utils/uuid';
	import { streamingResponse } from '$lib/utils/streamingResponse';
	import CheckFinalResponse, {
		FINAL_RESPONSE_SUFFIX
	} from '@/components/CheckFinalResponse.svelte';
	import ChatListActionItems from '@/components/chat-list/ChatListActionItems.svelte';
	import { onMount } from 'svelte';
	import { debounce } from 'throttle-debounce';
	import Spinner from '@/components/Spinner.svelte';

	export let data;

	const { session$, addChatItem, updateChatContent, sessionId$, fetchingSource$, audioSource$ } =
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
		<p class="mt-6 p-3 bg-sky-950/70 text-sky-200 rounded-md mb-4 w-full">
			Help us understand your preferences to curate the best audiocast for you.
		</p>

		<div class="flex flex-col gap-y-3 h-full">
			{#key sessionChats}
				{#each sessionChats as item (item.id)}
					{@const finalResponse = item.content.includes(FINAL_RESPONSE_SUFFIX)}
					<ChatListItem type={item.role} content={item.content} loading={item.loading} />

					{#if finalResponse && $audioSource$}
						<!-- TODO: Render this in a bottom sheet and allow user modification -->
						{@html $audioSource$}
					{:else if finalResponse}
						{scrollChatContent()}
						<ChatListActionItems {sessionId} let:ongenerate let:onreviewSource let:onstartNew>
							{#if $fetchingSource$}
								<Spinner />
							{:else}
								<CheckFinalResponse
									content={item.content}
									on:startNew={onstartNew}
									on:generate={({ detail }) => ongenerate(detail.summary)}
									on:reviewSource={({ detail }) => onreviewSource(category, detail.summary)}
								/>
							{/if}
						</ChatListActionItems>
					{/if}
				{/each}
			{/key}
		</div>
	</div>
</ChatContainer>
