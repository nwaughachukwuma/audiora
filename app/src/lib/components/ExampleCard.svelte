<script lang="ts">
	import { goto } from '$app/navigation';
	import { getChatSession } from '@/stores/chatStore.svelte';
	import { uuid } from '@/utils/uuid';

	export let href: string;
	export let content: string;

	const { chatSession$ } = getChatSession();

	function handleClick() {
		chatSession$.set([{ id: uuid(), content, role: 'user' }]);
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
