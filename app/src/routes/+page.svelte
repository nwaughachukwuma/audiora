<script lang="ts">
	import RenderExamples from '@/components/RenderExamples.svelte';
	import ChatContainer from '@/components/ChatContainer.svelte';
	import ChatBox from '@/components/ChatBox.svelte';
	import ChatBoxIcon from '@/components/ChatBoxIcon.svelte';

	export let data;

	let searchTerm = '';
	$: sessionId = data.sessionId;

	function handleSearch() {
		if (searchTerm) {
			console.log(searchTerm);
		}
	}
</script>

<svelte:head>
	<title>Audiora</title>
</svelte:head>

<ChatContainer>
	<RenderExamples slot="content" {sessionId} />

	<div slot="chat_box">
		<ChatBox bind:searchTerm placeholder="What would you like to listen to?">
			<svelte:fragment slot="icon-right">
				<ChatBoxIcon iconType="send" {searchTerm} on:click={handleSearch} />
			</svelte:fragment>
		</ChatBox>
	</div>
</ChatContainer>
