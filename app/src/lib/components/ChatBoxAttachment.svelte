<script lang="ts" context="module">
	const MAX_FILES = 5;
	const TEN_MB = 10 * 1024 * 1024;
</script>

<script lang="ts">
	import { env } from '@env';
	import { Button } from './ui/button';
	import { PaperclipIcon } from 'lucide-svelte';
	import { slug } from 'github-slugger';
	import { toast } from 'svelte-sonner';
	import { getAttachmentsContext } from '@/stores/attachmentsContext.svelte';
	import { getSessionContext } from '@/stores/sessionContext.svelte';

	export let disabled = false;

	const { sessionId$ } = getSessionContext();
	const { addUploadItem, sessionUploadItems$, updateUploadItem } = getAttachmentsContext();

	let fileInput: HTMLInputElement;

	$: sessionId = $sessionId$;

	async function handleFileSelect(fileList: FileList | null) {
		if (!fileList) return toast.error('No files selected');

		const files = Array.from(fileList);
		fileInput.value = '';

		if ($sessionUploadItems$.length + files.length > MAX_FILES) {
			return toast.info(`You can only upload up to ${MAX_FILES} files`);
		}

		for (const file of files) {
			if (file.size > TEN_MB) {
				toast.info(`File ${file.name} exceeds 10MB. Skipping...`);
				continue;
			}

			addUploadItem({
				id: `${sessionId}_${slug(file.name)}`,
				file: file,
				loading: true,
				errored: false
			});
		}

		return Promise.all(files.map(uploadFiles));
	}

	async function uploadFiles(file: File) {
		const fileId = `${sessionId}_${slug(file.name)}`;

		const formData = new FormData();
		// const newFile = new File([file], fileId, { type: file.type });
		formData.append('file', file);
		formData.append('filename', fileId);

		return fetch(`${env.API_BASE_URL}/store-file-upload`, {
			method: 'POST',
			body: formData
		})
			.then<string>((res) => {
				if (res.ok) return res.json();
				throw new Error('Failed to upload files');
			})
			.then((url) => updateUploadItem(fileId, { gcsUrl: url }))
			.catch((err) => {
				toast.error(err.message);
				updateUploadItem(fileId, { errored: true });
			})
			.finally(() => updateUploadItem(fileId, { loading: false }));
	}

	$: resolveDisabled = $sessionUploadItems$.length >= MAX_FILES || disabled;
</script>

<Button
	variant="ghost"
	size="icon"
	class="text-zinc-400 hover:text-white"
	disabled={resolveDisabled}
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
