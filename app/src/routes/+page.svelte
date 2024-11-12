<script lang="ts">
	import RenderExamples from '@/components/RenderExamples.svelte';
	import ChatContainer from '@/components/ChatContainer.svelte';
	import { getSessionContext } from '@/stores/sessionContext.svelte.js';
	import { uuid } from '@/utils/uuid';
	import { goto } from '$app/navigation';
	import type { ContentCategory } from '@/utils/types';
	import RenderCategorySelection from '@/components/RenderCategorySelection.svelte';

	const { sessionId$, addChatItem, startSession } = getSessionContext();

	let searchTerm = '';
	let triggerSelectCategory = false;
	let selectContent = '';

	$: sessionId = $sessionId$;

	function handleSearch() {
		selectContent = searchTerm;
		triggerSelectCategory = true;
		searchTerm = '';
	}

	function continueChat(category: ContentCategory) {
		startSession(category);
		addChatItem({ id: uuid(), content: selectContent, role: 'user', loading: false });

		const href = `/chat/${sessionId}?category=${category}`;
		goto(href);
	}
</script>

<svelte:head>
	<title>Audiora</title>
</svelte:head>

<ChatContainer bind:searchTerm on:click={handleSearch} on:keypress={handleSearch}>
	<svelte:fragment slot="content">
		{#if triggerSelectCategory && selectContent}
			<RenderCategorySelection
				content={selectContent}
				on:selectCategory={({ detail }) => continueChat(detail.value)}
			/>
		{:else}
			<RenderExamples {sessionId} />
		{/if}
	</svelte:fragment>
</ChatContainer>
