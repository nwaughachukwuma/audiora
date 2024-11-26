<script lang="ts">
	import type { ContentCategory } from '@/utils/types';

	export let title: string = 'Untitled';
	export let category: ContentCategory;
</script>

<div class="flex w-full flex-col gap-y-3 sm:max-w-xl lg:max-w-3xl max-w-full">
	<div class="mb-4 flex flex-col gap-y-2">
		<span class="capitalize bg-gray-800 text-gray-300 w-fit py-1 px-3 rounded-md">
			{category}
		</span>

		<h1 class="text-2xl font-semibold text-sky-200">{title}</h1>
	</div>
</div>
