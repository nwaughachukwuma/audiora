<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import ChatListItem from './ChatListItem.svelte';
	import SelectCategory, { categories } from './SelectCategory.svelte';
	import type { ContentCategory } from '@/utils/types';
	import { env } from '@env';

	export let content: string;

	const dispatch = createEventDispatcher<{ detectedCategory: ContentCategory }>();

	let detectingCategory = false;

	$: getCategorySelection();

	async function getCategorySelection() {
		if (detectingCategory) return;
		detectingCategory = true;

		const response = await fetch(`${env.API_BASE_URL}/detect-category`, {
			method: 'POST',
			body: JSON.stringify({ content }),
			headers: { 'Content-Type': 'application/json' }
		})
			.then<ContentCategory>((res) => {
				if (res.ok) return res.json();
				throw new Error(res.statusText);
			})
			.catch(() => void 0)
			.finally(() => (detectingCategory = false));

		if (response && categories.includes(response)) {
			dispatch('detectedCategory', response);
		}
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
		{:else}
			<ChatListItem type="assistant" content="Please select your audiocast category" />
		{/if}
	</div>

	{#if !detectingCategory}
		<SelectCategory on:selectCategory />
	{/if}
</div>
