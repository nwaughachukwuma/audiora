<script context="module">
	const TEN_MB = 10 * 1024 * 1024;
</script>

<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { Button } from '../ui/button';
	import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
	import { FileIcon, LinkIcon, Upload } from 'lucide-svelte';
	import cs from 'clsx';
	import { toast } from 'svelte-sonner';
	import { getSessionContext } from '@/stores/sessionContext.svelte';

	const dispatch = createEventDispatcher<{
		useWebsiteURL: void;
		useCopyPaste: void;
		submitFiles: { files: File[] };
	}>();

	const { customSources$ } = getSessionContext();

	let dragActive = false;

	function handleDrag(e: DragEvent) {
		e.preventDefault();
		e.stopPropagation();
		if (e.type === 'dragenter' || e.type === 'dragover') {
			dragActive = true;
		} else if (e.type === 'dragleave') {
			dragActive = false;
		}
	}

	async function handleDrop(e: DragEvent) {
		e.preventDefault();
		e.stopPropagation();
		dragActive = false;

		const files = e.dataTransfer?.files;
		if (!files) return toast.error('No files found');

		const validFiles = getValidFiles(files);
		if (validFiles.length) {
			dispatch('submitFiles', { files: validFiles });
		}
	}

	function getValidFiles(files: FileList) {
		// ensure max 5 files with each less than 10mb
		const currentFilesCount = $customSources$?.length || 0;
		if (files.length + currentFilesCount > 5) {
			return toast.error('Max 5 files allowed'), [];
		}

		const validFiles: File[] = [];

		for (let i = 0; i < files.length; i++) {
			const file = files[i];
			if (file.size > TEN_MB) {
				toast.info(`File '${file.name}' exceeds 10MB. Skipping...`);
				continue;
			}

			if (file.type !== 'application/pdf' && !file.name.endsWith('.txt')) {
				toast.info(`Unsupported file type for ${file.name}. Skipping...`);
				continue;
			}
			validFiles.push(file);
		}
		return validFiles;
	}
</script>

<Card class="w-full bg-gray-900 border-none">
	<CardHeader>
		<CardTitle class="text-xl font-normal">Custom source</CardTitle>
		<CardDescription class="text-gray-400 text-base">
			Let's base Audiora's responses on the information that matters most to you. (E.g., marketing
			plans, research notes, meeting transcripts, etc.)
		</CardDescription>
	</CardHeader>
	<CardContent class="flex w-full flex-col gap-y-4">
		<div
			role="presentation"
			aria-dropeffect="move"
			on:dragenter={handleDrag}
			on:dragleave={handleDrag}
			on:dragover={handleDrag}
			on:drop={handleDrop}
			class={cs('border-2 border-dashed rounded-xl p-8 text-center', {
				'border-blue-500 bg-blue-500/10': dragActive,
				'border-gray-700': !dragActive
			})}
		>
			<div class="flex flex-col items-center gap-4">
				<div class="h-12 w-12 rounded-full bg-gray-800 flex items-center justify-center">
					<Upload class="h-6 w-6" />
				</div>
				<div class="space-y-2">
					<h3 class="text-xl">Upload sources</h3>
					<p class="text-gray-400">
						Drag & drop or{' '}
						<button class="text-blue-400 hover:text-blue-300">choose file</button> to upload
					</p>
				</div>
				<p class="text-sm text-gray-500">
					Supported file types: PDF, .txt, Markdown. (Max size: 10MB)
				</p>
			</div>
		</div>

		<div class="grid md:grid-cols-2 gap-4">
			<Button
				variant="outline"
				class="h-auto p-4 flex flex-col items-center gap-2 bg-gray-800/50 border-gray-700 hover:bg-gray-800"
				on:click={() => dispatch('useWebsiteURL')}
			>
				<div class="flex items-center gap-2 text-gray-300">
					<LinkIcon class="h-4 w-4" />
					<span>Website URL</span>
				</div>
				<div class="flex gap-2 text-sm text-blue-400">
					<span>including .pdf</span>
				</div>
			</Button>

			<Button
				variant="outline"
				class="h-auto p-4 flex flex-col items-center gap-2 bg-gray-800/50 border-gray-700 hover:bg-gray-800"
				on:click={() => dispatch('useCopyPaste')}
			>
				<div class="flex items-center gap-2 text-gray-300">
					<FileIcon class="h-4 w-4" />
					<span>Paste text</span>
				</div>
				<span class="text-sm text-blue-400">Copied text</span>
			</Button>
		</div>
	</CardContent>
</Card>
