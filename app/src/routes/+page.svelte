<script lang="ts">
	import RenderExamples from '@/components/RenderExamples.svelte';
	import { getSessionContext } from '@/stores/sessionContext.svelte.js';
	import { uuid } from '@/utils/uuid';
	import { goto } from '$app/navigation';
	import type { ContentCategory } from '@/utils/types';
	import RenderCategorySelection from '@/components/RenderCategorySelection.svelte';
	import ChatBoxAndWidgetHOC from '@/components/ChatBoxAndWidgetHOC.svelte';
	import { cn } from '@/utils/ui.utils';

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

<div
	class={cn('overflow-auto w-full h-full flex items-center justify-center mx-auto px-4', {
		'flex-col justify-start': triggerSelectCategory && selectContent
	})}
>
	<div class="sm:max-w-xl lg:max-w-3xl max-w-full w-full max-h-full">
		<div class="scrollbar-y-1 w-full h-full block">
			{#if triggerSelectCategory && selectContent}
				<RenderCategorySelection
					content={selectContent}
					on:selectCategory={({ detail }) => continueChat(detail.value)}
				/>
			{:else}
				<ChatBoxAndWidgetHOC bind:searchTerm on:submitSearch={handleSearch}>
					<RenderExamples slot="examples" {sessionId} />
				</ChatBoxAndWidgetHOC>
			{/if}
		</div>
	</div>
</div>
