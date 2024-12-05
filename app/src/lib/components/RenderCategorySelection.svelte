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
	import { createEventDispatcher } from 'svelte';
	import { ArrowRight } from 'lucide-svelte';
	import ChatListItem from './ChatListItem.svelte';
	import SelectCategory, { categories } from './SelectCategory.svelte';
	import { env } from '@env';
	import { Button } from './ui/button';

	export let content: string;

	const dispatch = createEventDispatcher<{ selectCategory: { value: ContentCategory } }>();

	let detectingCategory = false;
	let detectedCategory: ContentCategory | null = null;

	$: getCategorySelection();

	async function getCategorySelection() {
		if (detectingCategory) return;
		detectingCategory = true;

		return fetch(`${env.API_BASE_URL}/detect-category`, {
			method: 'POST',
			body: JSON.stringify({ content }),
			headers: { 'Content-Type': 'application/json' }
		})
			.then<ContentCategory>((res) => {
				if (res.ok) return res.json();
				throw new Error(res.statusText);
			})
			.then((res) => categories.includes(res) && (detectedCategory = res))
			.catch(() => void 0)
			.finally(() => (detectingCategory = false));
	}
</script>

<!-- Rename to get_category_selection.svelte -->

<div class="flex flex-col gap-y-3 h-full">
	<div class="flex flex-col gap-y-3 w-full">
		<ChatListItem type="user" {content} />

		{#if detectingCategory}
			<ChatListItem type="assistant" content="Auto-detecting content category..." loading>
				<span slot="loading" class="animate-pulse">
					Auto-detecting content category...Please wait
				</span>
			</ChatListItem>
		{:else if detectedCategory}
			{@const categoryWithArticle = `"${categoryArticleMap[detectedCategory]}"`}
			{@const _detectedCategory = detectedCategory}
			<p class="text-gray-300">
				<ChatListItem
					type="assistant"
					content="I auto-detected you want {categoryWithArticle}. Press NEXT to continue if correct."
				/>
			</p>

			<Button
				variant="ghost"
				class="text-base px-10 py-6 bg-gray-800 w-fit hover:bg-gray-700"
				on:click={() => dispatch('selectCategory', { value: _detectedCategory })}
			>
				<span> Next </span>
				<ArrowRight class="w-4 ml-1 inline" />
			</Button>

			<ChatListItem type="assistant" content="Else, select your audiocast category" />
		{:else}
			<ChatListItem type="assistant" content="Please select your audiocast category" />
		{/if}
	</div>

	{#if !detectingCategory}
		<SelectCategory on:selectCategory />
	{/if}
</div>
