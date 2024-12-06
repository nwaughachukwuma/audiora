<script context="module">
	const MAX_FILES = 5;
</script>

<script lang="ts">
	import { PaperclipIcon } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte';
	import { Button } from './ui/button';
	import { toast } from 'svelte-sonner';
	export let selectedFiles: File[] = [];

	const dispatch = createEventDispatcher<{
		attach: { files: File[] };
	}>();

	let fileInput: HTMLInputElement;

	function handleFileSelect(fileList: FileList | null) {
		if (!fileList) {
			return toast.error('No files selected');
		}

		const files = Array.from(fileList);

		if (selectedFiles.length + files.length > MAX_FILES) {
			return toast.info(`You can only upload up to ${MAX_FILES} files`);
		}

		selectedFiles = [...selectedFiles, ...files];
		dispatch('attach', { files: selectedFiles });

		// Reset input
		fileInput.value = '';
	}
</script>

<Button
	variant="ghost"
	size="icon"
	class="text-zinc-400 hover:text-white"
	disabled={selectedFiles.length >= MAX_FILES}
	on:click={() => fileInput.click()}
>
	<PaperclipIcon class="h-5 w-5" />
</Button>

<input
	type="file"
	accept=".pdf,.txt,.docx"
	multiple
	class="hidden"
	bind:this={fileInput}
	on:change={(e) => handleFileSelect(e.currentTarget.files)}
/>
