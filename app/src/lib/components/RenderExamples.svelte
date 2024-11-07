<script lang="ts" context="module">
	export type ContentCategory =
		| 'podcast'
		| 'sermon'
		| 'audiodrama'
		| 'lecture'
		| 'commentary'
		| 'voicenote'
		| 'interview'
		| 'soundbite';

	export const content_examples: Record<ContentCategory, string> = {
		podcast:
			'Create a podcast exploring the intersection of ancient philosophy and artificial intelligence.',
		sermon: 'Write a sermon connecting the teachings of Augustine with modern digital ethics.',
		audiodrama: "A reimagining of Homer's Odyssey set in a cyberpunk future.",
		lecture: "A lecture comparing Shakespeare's influence on modern social media communication.",
		commentary: 'A commentary on how Classical music influences contemporary electronic genres.',
		voicenote: "A personal reflection on reading Plato's Republic in today's political climate.",
		interview: 'An interview with an archaeologist using AI to uncover ancient Roman artifacts.',
		soundbite: 'A quick take on how ancient Greek democracy shapes modern blockchain governance.'
	};
</script>

<script>
	import ExampleCard from './ExampleCard.svelte';
</script>

<div class="w-full h-full block">
	<p class="font-medium text-xl mb-3">You can start with one of the following</p>
	<div class="grid grid-cols-2 gap-4 pb-4">
		{#each Object.entries(content_examples) as [category, content]}
			<ExampleCard {content} href="/" />
		{/each}
	</div>
</div>
