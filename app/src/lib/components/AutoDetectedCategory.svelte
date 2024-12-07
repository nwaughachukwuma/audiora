<script lang="ts" context="module">
	import type { ContentCategory } from '@/utils/types';

	export const categoryArticleMap: Record<ContentCategory, string> = {
		podcast: 'a podcast',
		sermon: 'a sermon',
		audiodrama: 'an audiodrama',
		lecture: 'a lecture',
		commentary: 'a commentary',
		voicenote: 'a voicenote',
		interview: 'an interview',
		soundbite: 'a soundbite'
	};
</script>

<script lang="ts">
	import ChatListItem from './ChatListItem.svelte';
	import { Button } from './ui/button';
	import { createEventDispatcher } from 'svelte';
	import { ArrowRight } from 'lucide-svelte';

	export let category: ContentCategory;

	const dispatch = createEventDispatcher<{ selectCategory: { value: ContentCategory } }>();

	$: categoryWithArticle = `"${categoryArticleMap[category]}"`;
</script>

<ChatListItem
	type="assistant"
	content="I auto-detected you want {categoryWithArticle}. Press NEXT to continue."
/>

<Button
	variant="ghost"
	class="text-base min-w-2/5 w-1/2 mx-auto mb-3 transition-all px-10 py-6 bg-gray-950/40 max-md:w-full hover:bg-gray-800"
	on:click={() => dispatch('selectCategory', { value: category })}
>
	<span> Next </span>
	<ArrowRight class="w-4 ml-1 inline" />
</Button>

<ChatListItem type="assistant" content="Or select your audiocast category" />
