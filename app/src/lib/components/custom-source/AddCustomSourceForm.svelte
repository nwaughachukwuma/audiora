<script lang="ts">
	import { Button } from '../ui/button';
	import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
	import { FileIcon, LinkIcon, Upload, X } from 'lucide-svelte';
	import cs from 'clsx';

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

	function handleDrop(e: DragEvent) {
		e.preventDefault();
		e.stopPropagation();
		dragActive = false;
		// Handle file upload here
	}
</script>

<div class="h-full bg-gray-950 pt-2">
	<Card class="w-full bg-gray-900 border-none">
		<CardHeader>
			<CardTitle class="text-2xl font-normal">Custom source</CardTitle>
			<CardDescription class="text-gray-400 text-lg">
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
						Supported file types: PDF, .txt, Markdown, Audio (e.g. mp3)
					</p>
				</div>
			</div>

			<div class="grid md:grid-cols-2 gap-4">
				<Button
					variant="outline"
					class="h-auto p-4 flex flex-col items-center gap-2 bg-gray-800/50 border-gray-700 hover:bg-gray-800"
				>
					<LinkIcon class="h-6 w-6" />
					<span>Link</span>
					<div class="flex gap-2 text-sm text-blue-400">
						<span>Website</span>
						<span>•</span>
						<span>YouTube</span>
					</div>
				</Button>

				<Button
					variant="outline"
					class="h-auto p-4 flex flex-col items-center gap-2 bg-gray-800/50 border-gray-700 hover:bg-gray-800"
				>
					<FileIcon class="h-6 w-6" />
					<span>Paste text</span>
					<span class="text-sm text-blue-400">Copied text</span>
				</Button>
			</div>
		</CardContent>
	</Card>
</div>
