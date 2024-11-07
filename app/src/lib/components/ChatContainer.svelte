<script>
	import ChatBoxContainer from './ChatBoxContainer.svelte';
	export let searchTerm = '';
	let navLoading = false;
</script>

<div
	class="mx-auto flex h-full max-w-full flex-col items-center gap-1 overflow-hidden px-2 sm:max-w-xl sm:px-1 lg:max-w-3xl"
>
	<div id="chatContainer1" class="overflow-auto scrollbar-y-1 w-full block">
		<div class="flex flex-col gap-y-2">
			<h1 class="text-5xl font-bold">🎧 Audiora</h1>
			<h2 class="text-lg">Listen to anything, anytime.</h2>
		</div>

		<slot name="content"></slot>

		<div class="h-32"></div>
	</div>

	<ChatBoxContainer bind:searchTerm loading={navLoading} showIcon on:keypress on:click />
</div>
