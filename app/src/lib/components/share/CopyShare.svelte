<script lang="ts">
	import { Button } from '../ui/button';
	import { CopyIcon } from 'lucide-svelte';
	import { copy } from '$lib/utils/copy';
	import { wait } from '$lib/utils/wait';
	import { toast } from 'svelte-sonner';
	import Spinner from '../Spinner.svelte';

	export let url: string;

	let copying = false;

	async function copyToClipboard() {
		if (copying) return;
		copying = true;

		await wait(400);
		return copy(url)
			.then(() => toast.success('Link copied to clipboard.'))
			.catch((err) => {
				toast.error('Failed to copy link to clipboard.', {
					description: err.message
				});
			})
			.finally(() => (copying = false));
	}
</script>

<Button
	variant="outline"
	aria-label="Copy link to clipboard"
	class="w-fit h-[42px] bg-neutral-800 text-base font-medium border-none transition-colors hover:bg-neutral-600/80 text-white px-3"
	on:click={copyToClipboard}
>
	{#if copying}
		<Spinner small />
	{:else}
		<CopyIcon class="inline w-4 h-4 m-0 align-middle" />
	{/if}
</Button>
