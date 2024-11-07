<script lang="ts">
	import { UserIcon, BotIcon } from 'lucide-svelte';
	import Spinner from '../Spinner.svelte';

	export let type: 'user' | 'assistant';
	export let content: string;
	export let loading = false;
</script>

<div class="flex gap-x-3 p-4 bg-gray-800 rounded-md">
	{#if type === 'user'}
		<UserIcon class="w-6 h-6 " />
	{:else}
		<BotIcon class="w-10 h-6" />
	{/if}

	<div class="max-w-full break-words text-gray-200 flex text-base">
		{#if loading}
			<Spinner small />
		{:else}
			{content}
		{/if}
	</div>
</div>
