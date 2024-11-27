<script>
	import { getSessionContext } from '@/stores/sessionContext.svelte';
	import ChatBoxContainer from './ChatBoxContainer.svelte';
	import { isfinalResponse } from '@/utils/session.utils';

	export let searchTerm = '';
	export let disableTextInput = false;

	const { sessionCompleted$, fetchingSource$, audioSource$, session$ } = getSessionContext();

	let navLoading = false;

	$: chats = $session$?.chats || [];
	$: hasFinalResponse = chats.some(isfinalResponse);
</script>

<div
	id="chatContainer1"
	class="mx-auto flex h-full w-full flex-col overflow-auto items-center gap-1 px-4"
>
	<div class="sm:max-w-xl lg:max-w-3xl max-w-full w-full">
		<div class="scrollbar-y-1 w-full h-[calc(100%-4rem)] block">
			<slot name="content"></slot>
			<div class="h-24"></div>
		</div>

		{#if !hasFinalResponse && !$sessionCompleted$ && !$fetchingSource$ && !$audioSource$}
			<ChatBoxContainer
				bind:searchTerm
				loading={navLoading}
				showIcon
				disabled={$sessionCompleted$ || disableTextInput}
				on:keypress
				on:click
			/>
		{/if}
	</div>
</div>
