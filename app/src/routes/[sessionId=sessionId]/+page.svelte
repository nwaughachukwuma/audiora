<script>
	import ChatContainer from '@/components/ChatContainer.svelte';
	export let data;

	$: category = data.category;
	$: sessionId = data.sessionId;
</script>

<ChatContainer>
	<div slot="content">
		{sessionId}: {category}
	</div>

	<div slot="chat_input" class="h-[16%] fixed w-[calc(100%-24.5rem)] bottom-0 shrink-0">
		Chat Input Section
	</div>
</ChatContainer>
