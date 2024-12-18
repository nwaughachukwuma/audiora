<script context="module">
	const SLIDER_STEP = 0.25;
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Slider } from '@/components/ui/slider';
	import AudioPlayerVolumeController from './AudioPlayerVolumeController.svelte';
	import AudioPlayerDownloadButton from './AudioPlayerDownloadButton.svelte';
	import AudioPlayerPlaybackControl from './AudioPlayerPlaybackControl.svelte';
	import { debounce } from 'throttle-debounce';

	export let src: string;
	export let title: string;

	let audioRef: HTMLAudioElement;

	let isPlaying = false;
	let volume = 0.75;
	let muted = false;

	let duration = 0;
	let currentTime = 0;
	let isDragging = false;

	$: if (audioRef) handleDragging(isDragging);

	const handleDragging = (dragging: boolean) => {
		if (dragging) audioRef.pause();
		else audioRef.play();
	};

	// Since the slider value = currentTime and max = duration, we can directly update the time
	const handleSliderChange = ([value]: number[]) => {
		const valueDiff = Math.abs(value - currentTime);
		const seekable = valueDiff > 2 * SLIDER_STEP;
		const acceptableValue = (v: number) => v >= 0 && v <= duration;

		if (seekable && acceptableValue(value)) {
			audioRef.pause();
			currentTime = value;
		}
	};

	const formatTime = (time: number) => {
		const minutes = Math.floor(time / 60);
		const seconds = Math.floor(time % 60);
		return `${minutes}:${seconds.toString().padStart(2, '0')}`;
	};

	function handleEnded() {
		isPlaying = false;
		currentTime = 0;
	}

	function handleError() {
		isPlaying = false;
	}

	onMount(() => {
		let thumbEl = document.querySelector('span[role="slider"]');
		if (thumbEl) {
			thumbEl.addEventListener('pointerdown', () => (isDragging = true));
			thumbEl.addEventListener('pointerup', () => (isDragging = false));
		}
		return () => {
			if (thumbEl) {
				thumbEl.removeEventListener('pointerdown', () => (isDragging = true));
				thumbEl.removeEventListener('pointerup', () => (isDragging = false));
			}
		};
	});
</script>

<div class="w-full pt-6 px-4 pb-3 rounded-xl bg-gradient-to-br from-gray-900 to-gray-800 shadow-lg">
	<audio
		class="hidden"
		bind:this={audioRef}
		bind:duration
		bind:currentTime
		bind:volume
		bind:muted
		on:loadeddata
		on:ended={handleEnded}
		on:error={handleError}
		on:playing={() => (isPlaying = true)}
		on:play={() => (isPlaying = true)}
		on:pause={() => (isPlaying = false)}
	>
		<source {src} type="audio/mpeg" />
		Your browser does not support the audio element.
	</audio>

	<div class="mb-2">
		<Slider
			value={[currentTime]}
			max={duration}
			step={SLIDER_STEP}
			onValueChange={handleSliderChange}
			class="w-full "
			rangeClass="bg-emerald-800"
			thumbClass="bg-zinc-800 slider-el cursor-pointer border-zinc-500 hover:scale-105 transition-all"
			disabled={!audioRef}
		/>
		<div class="flex justify-between text-xs text-gray-400 mt-2">
			<span>{formatTime(currentTime)}</span>
			<span>{formatTime(duration)}</span>
		</div>
	</div>

	<div class="flex justify-between md:justify-center relative items-center gap-x-3">
		<span class="max-md:hidden md:absolute md:left-0">
			<AudioPlayerVolumeController {audioRef} bind:volume bind:muted />
		</span>

		<AudioPlayerPlaybackControl bind:isPlaying {audioRef} />

		<div class="flex justify-between items-center gap-x-3">
			<span class="md:hidden">
				<AudioPlayerVolumeController {audioRef} bind:volume bind:muted />
			</span>
			<span class="md:absolute md:right-0">
				<AudioPlayerDownloadButton {src} {title} />
			</span>
		</div>
	</div>
</div>
