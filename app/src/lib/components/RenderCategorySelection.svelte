<script lang="ts">
	import ChatListItem from './ChatListItem.svelte';
	import SelectCategory from './SelectCategory.svelte';
	export let content: string;
</script>

<div class="flex flex-col gap-y-3 h-full">
	<div class="flex flex-col gap-y-3 w-full">
		<ChatListItem type="user" {content} />

		<ChatListItem type="assistant" content="Please select your audiocast category" />
	</div>

	<SelectCategory on:selectCategory />
</div>
