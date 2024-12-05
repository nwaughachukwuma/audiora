<script lang="ts">
	import RenderExamples from '@/components/RenderExamples.svelte';
	import ChatContainer from '@/components/ChatContainer.svelte';
	import { getSessionContext } from '@/stores/sessionContext.svelte.js';
	import { uuid } from '@/utils/uuid';
	import { goto } from '$app/navigation';
	import type { ContentCategory } from '@/utils/types';
	import RenderCategorySelection from '@/components/RenderCategorySelection.svelte';
	import ChatBoxAndWidget from '@/components/ChatBoxAndWidget.svelte';

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

	async function continueChat(category: ContentCategory) {
		startSession(category);

		const content = `${selectContent}\nCategory: ${category} `;
		addChatItem({ id: uuid(), content, role: 'user', loading: false, createdAt: Date.now() });

		const href = `/chat/${sessionId}?category=${category}&chat`;
		return goto(href, { invalidateAll: true, replaceState: true });
	}
</script>

<svelte:head>
	<title>Audiora</title>
</svelte:head>

<ChatContainer
	disableTextInput={triggerSelectCategory}
	bind:searchTerm
	on:click={handleSearch}
	on:keypress={handleSearch}
>
	<svelte:fragment slot="content">
		{#if triggerSelectCategory && selectContent}
			<RenderCategorySelection
				content={selectContent}
				on:selectCategory={({ detail }) => continueChat(detail.value)}
			/>
		{:else}
			<ChatBoxAndWidget>
				<RenderExamples slot="examples" {sessionId} />
			</ChatBoxAndWidget>
		{/if}
	</svelte:fragment>
</ChatContainer>
