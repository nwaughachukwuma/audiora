<script context="module">
	const examples = [
		{ icon: '🎨', text: 'Create image' },
		{ icon: '💡', text: 'Get advice' },
		{ icon: '🧠', text: 'Brainstorm' },
		{ icon: '🎲', text: 'Surprise me' },
		{ icon: '✍️', text: 'Help me write' },
		{ text: 'More' }
	];
</script>

<script lang="ts">
	import { Button } from '@/components/ui/button';
	import { Card } from '@/components/ui/card';
	import { ArrowUpIcon } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte';
	import ChatBoxAttachment from './ChatBoxAttachment.svelte';
	import ChatBoxAttachmentPreview from './ChatBoxAttachmentPreview.svelte';
	import { setAttachmentsContext } from '@/stores/attachmentsContext.svelte';

	export let searchTerm = '';

	const { uploadedItems$ } = setAttachmentsContext();

	const dispatch = createEventDispatcher<{
		submitSearch: { value: string };
	}>();

	function handleKeyPress(ev: KeyboardEvent) {
		if (ev.key === 'Enter' && !ev.shiftKey && searchTerm) {
			ev.preventDefault();
			dispatchSearch();
		}
	}

	function dispatchSearch() {
		if (!searchTerm.trim()) return;
		dispatch('submitSearch', { value: searchTerm });
	}
</script>

<div class="flex flex-col items-center max-lg:pt-16 md:justify-center h-full">
	<div class="w-full max-w-3xl space-y-8">
		<div class="text-center space-y-2">
			<h1 class="md:text-4xl text-3xl font-semibold text-white">What can I help with?</h1>
			<h3 class="text-base text-gray-400">Listen to anything, anytime</h3>
		</div>

		<Card class="bg-zinc-800/50 border-0 overflow-hidden">
			<div class="flex items-center p-2">
				<div class="flex-1">
					<textarea
						placeholder="Message Audiora"
						class="w-full outline-none bg-transparent border-0 focus:ring-0 text-white placeholder-zinc-400 resize-none py-3 px-4"
						rows={1}
						tabindex={0}
						bind:value={searchTerm}
						on:keypress={handleKeyPress}
					/>
				</div>
			</div>
			<div class="flex flex-row-reverse items-center justify-between p-2 bg-zinc-800/30">
				<slot name="tools">
					<div class="flex items-center gap-2 px-2">
						<ChatBoxAttachment />

						<Button
							variant="ghost"
							size="icon"
							class="text-zinc-400 hover:text-white"
							disabled={!searchTerm}
							on:click={dispatchSearch}
						>
							<ArrowUpIcon class="h-5 w-5" />
						</Button>
					</div>
				</slot>
			</div>

			{#if $uploadedItems$.length > 0}
				<ChatBoxAttachmentPreview />
			{/if}
		</Card>

		<slot name="examples">
			<div class="flex flex-wrap gap-2 justify-center">
				{#each examples as item, index (index)}
					<Button
						variant="outline"
						class="bg-zinc-800/50 border-zinc-700 text-zinc-300 hover:bg-zinc-700/50 hover:text-white"
					>
						{#if item.icon}
							<span class="mr-2">{item.icon}</span>
						{/if}
						{item.text}
					</Button>
				{/each}
			</div>
		</slot>
	</div>
</div>
