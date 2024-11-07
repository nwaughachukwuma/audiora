<script>
	import { afterNavigate } from '$app/navigation';
	import ChatBoxContainer from './ChatBoxContainer.svelte';

	let searchTerm = '';
	let navLoading = false;

	// async function askQuestion() {
	// 	navLoading = true;
	// 	return goto(`/search?q=${searchTerm}`, {
	// 		invalidateAll: true,
	// 		replaceState: true
	// 	});
	// }

	afterNavigate(() => {
		navLoading = false;
	});
</script>

<div
	class="mx-auto flex h-full max-w-full flex-col items-center gap-1 overflow-hidden px-2 sm:max-w-xl sm:px-1 lg:max-w-3xl"
>
	<div class="overflow-auto scrollbar-y-1 w-full block">
		<div class="flex flex-col gap-y-2">
			<h1 class="text-5xl font-bold">🎧 Audiora</h1>
			<h2 class="text-lg">Listen to anything, anytime.</h2>
		</div>

		<slot name="content"></slot>
	</div>

	<ChatBoxContainer bind:searchTerm loading={navLoading} showIcon on:keypress on:click />
</div>
