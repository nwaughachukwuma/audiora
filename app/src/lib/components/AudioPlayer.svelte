<script lang="ts">
	import { onMount } from 'svelte';
	import { Play, Pause, SkipBack, SkipForward } from 'lucide-svelte';
	import { Button } from '@/components/ui/button';
	import { Slider } from '@/components/ui/slider';

	export let src: string;

	let isPlaying = false;

	let audioRef: HTMLAudioElement;
	let duration = 0;
	let currentTime = 0;

	let previousSliderValue = 0;

	function setAudioData() {
		duration = audioRef.duration;
		currentTime = audioRef.currentTime;
	}

	function setAudioTime() {
		currentTime = audioRef.currentTime;
	}

	onMount(() => {
		audioRef.volume = 0.75;
	});

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

	const handleSliderChange = (newValue: number[]) => {
		const BUFFER = 1;
		const [value] = newValue;

		// It's a scrubbing event
		if (Math.abs(value - previousSliderValue) > BUFFER) {
			audioRef.currentTime = (value / 100) * audioRef.duration;
		}

		previousSliderValue = value;
	};

	const formatTime = (time: number) => {
		const minutes = Math.floor(time / 60);
		const seconds = Math.floor(time % 60);
		return `${minutes}:${seconds.toString().padStart(2, '0')}`;
	};
</script>

<div class="w-full p-6 pb-4 rounded-xl bg-gradient-to-br from-gray-900 to-gray-800 shadow-lg">
	<audio
		bind:this={audioRef}
		class="w-full animate-fade-in block"
		on:loadeddata={setAudioData}
		on:timeupdate={setAudioTime}
	>
		<source {src} type="audio/mpeg" />
		Your browser does not support the audio element.
	</audio>

	<div class="mb-3">
		<Slider
			value={[currentTime]}
			max={duration}
			step={1}
			onValueChange={handleSliderChange}
			class="w-full"
		/>
		<div class="flex justify-between text-xs text-gray-400 mt-2">
			<span>{formatTime(currentTime)}</span>
			<span>{formatTime(duration)}</span>
		</div>
	</div>

	<div class="flex justify-center items-center gap-x-4">
		<Button
			variant="ghost"
			size="icon"
			on:click={skipBackward}
			class="text-gray-300 hover:text-white transition-colors"
		>
			<SkipBack class="h-6 w-6" />
		</Button>
		<Button
			variant="ghost"
			size="icon"
			on:click={togglePlayPause}
			class="text-gray-300 hover:text-white transition-colors"
		>
			{#if isPlaying}
				<Pause class="h-8 w-8" />
			{:else}
				<Play class="h-8 w-8" />
			{/if}
		</Button>
		<Button
			variant="ghost"
			size="icon"
			on:click={skipForward}
			class="text-gray-300 hover:text-white transition-colors"
		>
			<SkipForward class="h-6 w-6" />
		</Button>
	</div>
</div>
