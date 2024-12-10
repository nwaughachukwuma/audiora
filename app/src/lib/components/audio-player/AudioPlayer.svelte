<script context="module">
	const SLIDER_STEP = 0.25;
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Slider } from '@/components/ui/slider';
	import AudioPlayerVolumeController from './AudioPlayerVolumeController.svelte';
	import AudioPlayerDownloadButton from './AudioPlayerDownloadButton.svelte';
	import AudioPlayerPlaybackControl from './AudioPlayerPlaybackControl.svelte';

	export let src: string;
	export let title: string;

	let isPlaying = false;
	let volume = 0.75;
	let isMuted = false;

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
		audioRef.volume = volume;
	});

	const handleSliderChange = (newValue: number[]) => {
		const BUFFER = 2 * SLIDER_STEP;
		const [value] = newValue;
		// Only update if there's a significant change to prevent unnecessary updates
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
			step={SLIDER_STEP}
			onValueChange={handleSliderChange}
			class="w-full "
			rangeClass="bg-emerald-800"
			thumbClass="bg-zinc-800 border-zinc-500"
		/>
		<div class="flex justify-between text-xs text-gray-400 mt-2">
			<span>{formatTime(currentTime)}</span>
			<span>{formatTime(duration)}</span>
		</div>
	</div>

	<div class="flex justify-between md:justify-center relative items-center gap-x-3">
		<span class="max-md:hidden md:absolute md:left-0">
			<AudioPlayerVolumeController {audioRef} bind:volume bind:isMuted />
		</span>

		<AudioPlayerPlaybackControl bind:isPlaying {audioRef} />

		<div class="flex justify-between items-center gap-x-4">
			<span class="md:hidden">
				<AudioPlayerVolumeController {audioRef} bind:volume bind:isMuted />
			</span>
			<span class="md:absolute md:right-0">
				<AudioPlayerDownloadButton {src} {title} />
			</span>
		</div>
	</div>
</div>
