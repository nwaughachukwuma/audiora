<script lang="ts" context="module">
	import type { ContentCategory } from '@/utils/types';

	export const contentExamples: Record<ContentCategory, string> = {
		podcast: 'Podcast exploring the intersection of ancient philosophy and AI',
		sermon: 'Sermon connecting the teachings of Augustine with modern digital ethics',
		audiodrama: "Reimagining of Homer's Odyssey set in a cyberpunk future",
		lecture: "Lecture comparing Shakespeare's influence on modern social media",
		commentary: 'Commentary on how Classical music influences contemporary electronic genres',
		voicenote: "Personal reflection on reading Plato's Republic in today's political climate.",
		interview: 'Interview with an archaeologist using AI to uncover ancient Roman artifacts',
		soundbite: 'Quick take on how ancient Greek democracy shapes modern blockchain governance'
	};
</script>

<script lang="ts">
	import ExampleCard from './ExampleCard.svelte';
	export let sessionId: string;

	$: contentExamplesDict = (
		Object.entries(contentExamples) as Array<[category: ContentCategory, content: string]>
	).slice(0, 6);
</script>

<div class="w-full h-full block">
	<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 pb-4">
		{#each contentExamplesDict as [category, content]}
			{@const href = `/chat/${sessionId}?category=${category}&chat`}
			<ExampleCard {content} {href} {category} />
		{/each}
	</div>
</div>
