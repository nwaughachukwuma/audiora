<script lang="ts">
	import { FileIcon, XIcon } from 'lucide-svelte';
	import { Button } from './ui/button';
	import { getAttachmentsContext } from '@/stores/attachmentsContext.svelte';
	import Spinner from './Spinner2.svelte';

	const { removeUploadItem, sessionUploadItems$ } = getAttachmentsContext();

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

	$: validItems = $sessionUploadItems$.filter((item) => !item.errored);
</script>

<div class="p-2 flex flex-wrap gap-2 bg-zinc-800/30">
	{#each validItems as { file, id, loading }, ix (id + ix)}
		<div class="flex items-center w-56 gap-2 justify-between bg-zinc-700/30 rounded p-2">
			<div class="p-1">
				{#if loading}
					<Spinner />
				{:else}
					<FileIcon class="w-6 h-6 text-emerald-800 animate-fade-in" />
				{/if}
			</div>
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
				disabled={loading}
				on:click={() => removeUploadItem(id)}
			>
				<XIcon class="h-4 w-4" />
			</Button>
		</div>
	{/each}
</div>
