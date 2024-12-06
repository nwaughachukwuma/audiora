<script lang="ts">
	import { XIcon } from 'lucide-svelte';
	import { Button } from './ui/button';
	import { createEventDispatcher } from 'svelte';

	export let selectedFiles: File[] = [];

	const dispatch = createEventDispatcher<{ updateAttach: { files: File[] } }>();

	function removeFile(index: number) {
		selectedFiles = selectedFiles.filter((_, i) => i !== index);
		dispatch('updateAttach', { files: selectedFiles });
	}

	function formatFileSize(bytes: number): string {
		if (bytes === 0) return '0 Bytes';
		const k = 1024;
		const sizes = ['Bytes', 'KB', 'MB', 'GB'];
		const i = Math.floor(Math.log(bytes) / Math.log(k));
		return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
	}

	function parseFileType(file: File) {
		const fileType = file.type.split('/')[1];
		switch (fileType) {
			case 'pdf':
				return 'pdf';
			case 'vnd.openxmlformats-officedocument.wordprocessingml.document':
				return 'docx';
			case 'plain':
				return 'txt';
			default:
				return fileType;
		}
	}
</script>

<div class="p-2 flex flex-wrap gap-2 bg-zinc-800/30">
	{#each selectedFiles as file, index}
		<div class="flex items-center w-56 justify-between bg-zinc-700/30 rounded p-2">
			<div class="flex-1 min-w-0">
				<p class="text-sm text-white truncate">{file.name}</p>
				<p class="text-xs text-zinc-400">
					{formatFileSize(file.size)} • {parseFileType(file)}
				</p>
			</div>
			<Button
				variant="ghost"
				size="icon"
				class="text-zinc-400 hover:text-white hover:bg-zinc-700/70"
				on:click={() => removeFile(index)}
			>
				<XIcon class="h-4 w-4" />
			</Button>
		</div>
	{/each}
</div>
