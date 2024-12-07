<script>
	import { getSessionContext } from '@/stores/sessionContext.svelte';
	import { isfinalResponse } from '@/utils/session.utils';
	import ChatBoxAndWidget from './ChatBoxAndWidget.svelte';

	export let searchTerm = '';
	export let disableTextInput = false;

	const { sessionCompleted$, fetchingSource$, session$ } = getSessionContext();

	$: chats = $session$?.chats || [];
	$: hasFinalResponse = chats.some(isfinalResponse);
</script>

<div
	class="mx-auto flex h-full w-full flex-col overflow-hidden justify-between items-center gap-1 relative"
>
	<div id="chatContainer1" class="overflow-auto w-full flex justify-center mx-auto px-4">
		<div class="sm:max-w-xl lg:max-w-3xl max-w-full w-full">
			<div class="scrollbar-y-1 w-full h-full block">
				<slot name="content"></slot>
			</div>
		</div>
	</div>

	<slot name="chatbox">
		{#if !hasFinalResponse && !$sessionCompleted$ && !$fetchingSource$}
			<div class="shrink-0 w-full sm:max-w-xl lg:max-w-3xl max-w-full max-sm:px-4 px-1 py-4">
				<ChatBoxAndWidget
					bind:searchTerm
					loading={false}
					disabled={$sessionCompleted$ || disableTextInput}
					on:submitSearch
				/>
			</div>
		{/if}
	</slot>
</div>
