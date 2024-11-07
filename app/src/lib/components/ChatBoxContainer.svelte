<script lang="ts">
	import ChatBox from './ChatBox.svelte';
	import ChatBoxIcon from './ChatBoxIcon.svelte';

	export let loading = false;
	export let searchTerm: string;
	export let showIcon = false;
</script>

<div class="fixed bg-background bottom-0 block w-full max-w-full py-4 sm:max-w-xl lg:max-w-3xl">
	<div class="block w-full items-center">
		<ChatBox {showIcon} disabled={loading} bind:searchTerm on:keypress>
			<svelte:fragment slot="icon-right" let:disabled>
				<ChatBoxIcon iconType="send" {loading} {disabled} {searchTerm} on:click />
			</svelte:fragment>
		</ChatBox>

		<div class="h-6"></div>
	</div>
</div>
