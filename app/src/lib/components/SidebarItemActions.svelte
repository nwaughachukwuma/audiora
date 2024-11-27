<script lang="ts">
	import * as AlertDialog from './ui/alert-dialog';
	import { Trash } from 'lucide-svelte';
	import { goto } from '$app/navigation';
	import { SESSION_KEY } from '@/stores/sessionContext.svelte';
	import { env } from '@env';

	export let sessionId: string;

	let openDialog = false;

	async function deleteSession() {
		localStorage.removeItem(`${SESSION_KEY}_${sessionId}`);

		void fetch(`${env.API_BASE_URL}/delete-session/${sessionId}`, {
			method: 'DELETE'
		}).catch(() => {});

		openDialog = false;
		return goto('/', { invalidateAll: true, replaceState: true });
	}
</script>

<div
	class="absolute rounded-r-md hidden group/action bg-gray-800/80 hover:bg-gray-800 h-full group-hover:flex items-center right-0 p-2"
>
	<button
		class="text-gray-400 group-hover/action:text-gray-100"
		on:click={() => (openDialog = true)}
	>
		<Trash class="w-4 h-4 inline" />
	</button>
</div>

<AlertDialog.Root bind:open={openDialog}>
	<AlertDialog.Trigger>Open</AlertDialog.Trigger>
	<AlertDialog.Content class="border-neutral-800">
		<AlertDialog.Header>
			<AlertDialog.Title>Delete audiocast?</AlertDialog.Title>
			<AlertDialog.Description>
				This action cannot be undone. This will permanently delete your audiocast data.
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer>
			<AlertDialog.Cancel on:click={() => (openDialog = false)}>Cancel</AlertDialog.Cancel>
			<AlertDialog.Action class="bg-red-500 text-red-100 hover:bg-red-600" on:click={deleteSession}
				>Continue</AlertDialog.Action
			>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>
