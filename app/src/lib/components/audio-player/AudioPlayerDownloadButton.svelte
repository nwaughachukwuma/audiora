<script lang="ts" context="module">
	async function getImageBlob(url: string) {
		const response = await fetch(url);
		const blob = await response.blob();
		const downloadUrl = URL.createObjectURL(blob);
		return {
			downloadUrl,
			cleanup: () => URL.revokeObjectURL(downloadUrl)
		};
	}

	function downloadFile(url: string, title: string) {
		const link = document.createElement('a');
		link.href = url;
		link.download = `${slug(title).substring(0, 30)}_${Date.now()}.mp3`;

		document.body.appendChild(link);
		link.click();
		link.remove();
	}
</script>

<script lang="ts">
	import { Download } from 'lucide-svelte';
	import { slug } from 'github-slugger';
	import { Button } from '../ui/button';

	export let src: string;
	export let title: string;

	async function downloadAudio() {
		const { downloadUrl, cleanup } = await getImageBlob(src);
		downloadFile(downloadUrl, title);
		cleanup();
	}
</script>

<Button
	variant="ghost"
	size="icon"
	on:click={downloadAudio}
	class="text-gray-300 hover:text-white transition-colors"
>
	<Download class="h-5 w-5" />
</Button>
