<script>
	import ChatContainer from '@/components/ChatContainer.svelte';
	import ChatBox from '@/components/ChatBox.svelte';

	export let data;
	$: category = data.category;
	$: sessionId = data.sessionId;

	let searchTerm = '';
</script>

<ChatContainer>
	<div slot="content">
		{sessionId}: {category}
	</div>

	<div slot="chat_box">
		<ChatBox bind:searchTerm placeholder="What would you like to listen to?" />
	</div>
</ChatContainer>
