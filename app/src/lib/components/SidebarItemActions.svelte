<script lang="ts">
	import * as AlertDialog from './ui/alert-dialog';
	import { Trash } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher<{ deleteSession: void }>();

	let openDialog = false;

	function dispatchDeleteSession() {
		dispatch('deleteSession');
		openDialog = false;
	}
</script>

<div class="hidden h-full z-50 group-hover:flex items-center p-1">
	<button
		class="text-gray-400 hover:text-red-500"
		on:click|stopPropagation|preventDefault={() => (openDialog = true)}
	>
		<Trash class="w-4 h-4 inline" />
	</button>
</div>

{#if openDialog}
	<AlertDialog.Root open portal="body" closeOnOutsideClick closeOnEscape>
		<AlertDialog.Content class="border-neutral-800 overflow-hidden">
			<AlertDialog.Header>
				<AlertDialog.Title>Delete audiocast?</AlertDialog.Title>
				<AlertDialog.Description>
					This action cannot be undone. This will permanently delete your audiocast data.
				</AlertDialog.Description>
			</AlertDialog.Header>

			<AlertDialog.Footer>
				<AlertDialog.Cancel on:click={() => (openDialog = false)}>Cancel</AlertDialog.Cancel>
				<AlertDialog.Action
					class="bg-red-700 text-red-100 hover:bg-red-600"
					on:click={dispatchDeleteSession}
				>
					Continue
				</AlertDialog.Action>
			</AlertDialog.Footer>
		</AlertDialog.Content>
	</AlertDialog.Root>
{/if}
