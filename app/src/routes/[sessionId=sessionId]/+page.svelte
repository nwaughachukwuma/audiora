<script>
	import ChatContainer from '@/components/ChatContainer.svelte';
	import ChatBox from '@/components/ChatBox.svelte';

	export let data;
	$: category = data.category;
	$: sessionId = data.sessionId;

	let searchTerm = '';

	function handleSearch() {
		if (searchTerm) {
			console.log(searchTerm);
		}
	}
</script>

<ChatContainer on:click={handleSearch} on:keypress={handleSearch}>
	<div slot="content">
		{sessionId}: {category}
	</div>
</ChatContainer>
