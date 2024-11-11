<script>
	import { getSessionContext } from '@/stores/sessionContext.svelte';
	import ChatBoxContainer from './ChatBoxContainer.svelte';

	export let searchTerm = '';
	const { sessionCompleted$, fetchingSource$, audioSource$ } = getSessionContext();
	let navLoading = false;
</script>

<div
	class="mx-auto flex h-full w-full max-w-full flex-col items-center gap-1 overflow-hidden px-2 sm:max-w-xl sm:px-1 lg:max-w-3xl"
>
	<div id="chatContainer1" class="overflow-auto scrollbar-y-1 w-full h-[calc(100%-4rem)] block">
		<slot name="content"></slot>
		<div class="h-32"></div>
	</div>

	{#if !$sessionCompleted$ && !$fetchingSource$ && !$audioSource$}
		<ChatBoxContainer
			bind:searchTerm
			loading={navLoading}
			showIcon
			disabled={$sessionCompleted$}
			on:keypress
			on:click
		/>
	{/if}
</div>
