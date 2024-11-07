<script lang="ts">
	import UserAvatar from './UserAvatar.svelte';
	import AssistantAvatar from './AssistantAvatar.svelte';
	export let type: 'user' | 'assistant';
	export let content: string;
</script>

<div class="flex gap-x-3 p-4 bg-gray-800">
	{#if type === 'user'}
		<UserAvatar />
	{:else}
		<AssistantAvatar />
	{/if}
	<div class="max-w-full break-words flex text-base">
		{content}
	</div>
</div>
