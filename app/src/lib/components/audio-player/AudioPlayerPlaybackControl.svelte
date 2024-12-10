<script lang="ts">
	import { Play, Pause, SkipBack, SkipForward } from 'lucide-svelte';
	import { Button } from '../ui/button';

	export let audioRef: HTMLAudioElement;
	export let isPlaying = false;

	const togglePlayPause = () => {
		if (isPlaying) audioRef.pause();
		else audioRef.play();
		isPlaying = !isPlaying;
	};

	const skipForward = () => {
		audioRef.currentTime += 10;
	};

	const skipBackward = () => {
		audioRef.currentTime -= 10;
	};
</script>

<div class="flex justify-center items-center gap-x-4">
	<Button
		variant="ghost"
		size="icon"
		on:click={skipBackward}
		class="text-gray-300 hover:text-white transition-colors"
	>
		<SkipBack class="h-5 w-5" />
	</Button>

	<Button
		variant="ghost"
		size="icon"
		on:click={togglePlayPause}
		class="text-gray-300 hover:text-white transition-colors"
	>
		{#if isPlaying}
			<Pause class="h-7 w-7" />
		{:else}
			<Play class="h-7 w-7" />
		{/if}
	</Button>

	<Button
		variant="ghost"
		size="icon"
		on:click={skipForward}
		class="text-gray-300 hover:text-white transition-colors"
	>
		<SkipForward class="h-5 w-5" />
	</Button>
</div>
