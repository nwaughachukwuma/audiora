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
	class="border rounded-md min-h-[72px] md:h-24 group p-3 bg-zinc-800/50 border-zinc-700 text-zinc-300 hover:bg-zinc-700/50 transition-all hover:text-zinc-100"
>
	<span class="text-sm">
		{content}
	</span>
</button>
