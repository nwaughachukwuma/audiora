<script lang="ts">
	import { Download } from 'lucide-svelte';
	import { slug } from 'github-slugger';
	import { Button } from '../ui/button';

	export let src: string;
	export let title: string;

	const downloadAudio = () => {
		const link = document.createElement('a');
		link.href = src;
		link.download = `${slug(title).substring(0, 30)}_${Date.now()}.mp3`;
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	};
</script>

<Button
	variant="ghost"
	size="icon"
	on:click={downloadAudio}
	class="text-gray-300 hover:text-white transition-colors"
>
	<Download class="h-5 w-5" />
</Button>
