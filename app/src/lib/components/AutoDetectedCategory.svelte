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
	content="I auto-detected you want {categoryWithArticle}. Press NEXT to continue if correct."
/>

<Button
	variant="ghost"
	class="text-base px-10 py-6 bg-gray-800 w-fit hover:bg-gray-700"
	on:click={() => dispatch('selectCategory', { value: category })}
>
	<span> Next </span>
	<ArrowRight class="w-4 ml-1 inline" />
</Button>

<ChatListItem type="assistant" content="Else, select your audiocast category" />
