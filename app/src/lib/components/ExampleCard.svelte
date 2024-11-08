<script lang="ts">
	import { goto } from '$app/navigation';
	import { getSessionContext } from '@/stores/sessionContext.svelte';
	import { uuid } from '@/utils/uuid';

	export let href: string;
	export let content: string;

	const { addChatItem } = getSessionContext();

	function handleClick() {
		addChatItem({ id: uuid(), content, role: 'user', loading: false });
		goto(href);
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
