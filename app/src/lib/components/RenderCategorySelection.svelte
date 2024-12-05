<script lang="ts">
	import ChatListItem from './ChatListItem.svelte';
	import type { ContentCategory } from '@/utils/types';
	import SelectCategory, { categories } from './SelectCategory.svelte';
	import { env } from '@env';
	import AutoDetectedCategory from './AutoDetectedCategory.svelte';

	export let content: string;

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
			<AutoDetectedCategory category={detectedCategory} on:selectCategory />
		{:else}
			<ChatListItem type="assistant" content="Please select your audiocast category" />
		{/if}
	</div>

	{#if !detectingCategory}
		<SelectCategory on:selectCategory />
	{/if}
</div>
