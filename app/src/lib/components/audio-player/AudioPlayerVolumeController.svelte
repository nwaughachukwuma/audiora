<script lang="ts">
	import { Volume2, VolumeX } from 'lucide-svelte';
	import { Button } from '../ui/button';
	import { Slider } from '../ui/slider';

	export let audioRef: HTMLAudioElement;
	export let isMuted = false;
	export let volume = 0.75;

	const handleVolumeChange = (newValue: number[]) => {
		const [value] = newValue;
		volume = value / 100;
		audioRef.volume = volume;
		if (volume > 0) isMuted = false;
	};

	const toggleMute = () => {
		isMuted = !isMuted;
		audioRef.volume = isMuted ? 0 : volume;
	};
</script>

<div class="flex items-center gap-x-2 w-32">
	<Button
		variant="ghost"
		size="icon"
		on:click={toggleMute}
		class="text-gray-300 hover:text-white transition-colors"
	>
		{#if isMuted || volume === 0}
			<VolumeX class="h-5 w-5" />
		{:else}
			<Volume2 class="h-5 w-5" />
		{/if}
	</Button>

	<Slider
		value={[isMuted ? 0 : volume * 100]}
		max={100}
		step={1}
		onValueChange={handleVolumeChange}
		class="w-14 md:w-20"
		rangeClass="bg-white/70"
		thumbClass="bg-white border-white"
	/>
</div>
