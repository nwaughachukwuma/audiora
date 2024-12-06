<script lang="ts" context="module">
	const MAX_FILES = 5;
	const TEN_MB = 10 * 1024 * 1024;
</script>

<script lang="ts">
	import { env } from '@env';
	import { Button } from './ui/button';
	import { PaperclipIcon } from 'lucide-svelte';
	import { slug } from 'github-slugger';
	import { onDestroy } from 'svelte';
	import { beforeNavigate } from '$app/navigation';
	import { toast } from 'svelte-sonner';
	import { getAttachmentsContext } from '@/stores/attachmentsContext.svelte';

	const { uploadedItems$ } = getAttachmentsContext();

	let fileInput: HTMLInputElement;

	async function handleFileSelect(fileList: FileList | null) {
		if (!fileList) return toast.error('No files selected');

		const files = Array.from(fileList);
		fileInput.value = '';

		if ($uploadedItems$.length + files.length > MAX_FILES) {
			return toast.info(`You can only upload up to ${MAX_FILES} files`);
		}

		for (const file of files) {
			if (file.size > TEN_MB) {
				toast.info(`File ${file.name} exceeds 10MB. Skipping...`);
				continue;
			}

			uploadedItems$.update((files) => {
				files.push({ id: slug(file.name), file: file, loading: true, errored: false });
				return files;
			});
		}

		return Promise.all(files.map(uploadFiles));
	}

	async function uploadFiles(file: File) {
		const fileId = slug(file.name);

		const formData = new FormData();
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
			.then((url) => {
				uploadedItems$.update((files) => {
					return files.map((f) => {
						if (f.id === fileId) f.gcsUrl = url;
						return f;
					});
				});
			})
			.catch((err) => {
				toast.error(err.message);

				uploadedItems$.update((files) => {
					return files.map((f) => {
						if (f.id === fileId) f.errored = true;
						return f;
					});
				});
			})
			.finally(() => {
				uploadedItems$.update((files) =>
					files.map((f) => {
						if (f.id === fileId) f.loading = false;
						return f;
					})
				);
			});
	}

	onDestroy(() => uploadedItems$.set([]));
	beforeNavigate(() => uploadedItems$.set([]));
</script>

<Button
	variant="ghost"
	size="icon"
	class="text-zinc-400 hover:text-white"
	disabled={$uploadedItems$.length >= MAX_FILES}
	on:click={() => fileInput.click()}
>
	<PaperclipIcon class="h-5 w-5" />
</Button>

<!-- TODO: add support for .docx -->
<input
	type="file"
	accept=".pdf,.txt"
	multiple
	class="hidden"
	bind:this={fileInput}
	on:change={(e) => handleFileSelect(e.currentTarget.files)}
/>
