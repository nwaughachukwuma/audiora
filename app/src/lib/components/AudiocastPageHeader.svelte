<script lang="ts">
	import type { SessionModel } from '@/utils/types';
	export let session: SessionModel;
</script>

<div class="flex w-full px-4 flex-col gap-y-3 sm:max-w-xl lg:max-w-3xl max-w-full">
	<div class="mb-4 flex flex-col gap-y-2">
		<span class="capitalize bg-gray-800 text-gray-300 w-fit py-1 px-3 rounded-md">
			{session.category}
		</span>

		{#if session.metadata?.title}
			<h1 class="text-2xl font-semibold text-sky-200">{session.metadata.title}</h1>
		{/if}
	</div>
</div>
