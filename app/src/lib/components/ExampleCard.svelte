<script lang="ts">
	import { goto } from '$app/navigation';
	import { getSessionContext } from '@/stores/sessionContext.svelte';
	import type { ContentCategory } from '@/utils/types';
	import { uuid } from '@/utils/uuid';

	export let href: string;
	export let content: string;
	export let category: ContentCategory;

	const { addChatItem, startSession } = getSessionContext();

	async function handleClick() {
		startSession(category);
		addChatItem({ id: uuid(), content, role: 'user', loading: false, createdAt: Date.now() });
		return goto(href, { invalidateAll: true, replaceState: true });
	}
</script>

<button
	on:click={handleClick}
	class="border no-underline hover:no-underline rounded-md group border-gray-600 p-4 bg-gray-900 hover:bg-gray-800"
>
	<span class="text-sm">
		{content}
	</span>
</button>
