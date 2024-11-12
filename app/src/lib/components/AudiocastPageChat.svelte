<script lang="ts">
	import * as Sheet from '$lib/components/ui/sheet';
	import { MessageSquareText } from 'lucide-svelte';
	import { Button } from './ui/button';
	import type { ChatItem } from '@/stores/sessionContext.svelte';
	import ChatListItem from './ChatListItem.svelte';

	export let chats: ChatItem[];
</script>

<Sheet.Root>
	<Sheet.Trigger>
		<Button
			variant="ghost"
			class="py-6 rounded-md w-16 text-base no-underline text-center hover:no-underline bg-gray-800 text-gray-200 hover:bg-gray-700"
		>
			<MessageSquareText class="w-4 inline" />
		</Button>
	</Sheet.Trigger>
	<Sheet.Content class="border-neutral-800 overflow-auto">
		<Sheet.Header>
			<Sheet.Description class="mt-6 p-3 bg-sky-950/70 text-sky-200 rounded-md mb-4 w-full">
				Chats that generated user preferences
			</Sheet.Description>
		</Sheet.Header>

		<div class="block w-full overflow-auto">
			<div class="flex flex-col gap-y-3 h-full overflow-auto">
				{#each chats as item (item.id)}
					<ChatListItem type={item.role} content={item.content} loading={item.loading} />
				{/each}
			</div>
		</div>
	</Sheet.Content>
</Sheet.Root>
