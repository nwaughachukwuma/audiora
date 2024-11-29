<script lang="ts">
	import ChatBox from './ChatBox.svelte';
	import ChatBoxIcon from './ChatBoxIcon.svelte';

	export let loading = false;
	export let searchTerm: string;
	export let showIcon = false;
	export let disabled = false;
</script>

<div class="bg-background block w-full max-sm:px-2 py-4">
	<div class="block w-full items-center">
		<ChatBox {showIcon} disabled={loading || disabled} bind:searchTerm on:keypress>
			<svelte:fragment slot="icon-right" let:disabled>
				<ChatBoxIcon iconType="send" {loading} {disabled} {searchTerm} on:click />
			</svelte:fragment>
		</ChatBox>
	</div>
</div>
