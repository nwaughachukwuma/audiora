<script lang="ts">
	import { Button } from '@/components/ui/button';
	import { Card } from '@/components/ui/card';
	import { ArrowUpIcon } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte';
	import ChatBoxAttachment from './ChatBoxAttachment.svelte';
	import ChatBoxAttachmentPreview from './ChatBoxAttachmentPreview.svelte';
	import { getAttachmentsContext } from '@/stores/attachmentsContext.svelte';
	import Spinner from './Spinner.svelte';

	export let searchTerm = '';
	export let loading = false;
	export let disabled = false;

	const { sessionUploadItems$ } = getAttachmentsContext();

	$: resolveDisabled = loading || disabled;

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

	function auto_resize(element: EventTarget & HTMLTextAreaElement) {
		requestAnimationFrame(() => {
			element.style.height = 'auto';
			element.style.height = element.scrollHeight + 'px';
		});
	}
</script>

<Card class="bg-zinc-800/50 border-0 overflow-hidden">
	{#if $sessionUploadItems$.length > 0}
		<ChatBoxAttachmentPreview />
	{/if}

	<div class="flex items-center p-2">
		<div class="flex-1">
			<textarea
				placeholder="Message Audiora"
				rows="1"
				autofocus
				class="w-full outline-none bg-transparent border-0 focus:ring-0 text-white placeholder-zinc-400 resize-none py-3 px-4 max-h-72 overflow-hidden box-border"
				class:pointer-events-none={resolveDisabled}
				disabled={resolveDisabled}
				on:input={(e) => auto_resize(e.currentTarget)}
				bind:value={searchTerm}
				on:keypress={handleKeyPress}
			></textarea>
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
					disabled={!searchTerm || resolveDisabled}
					on:click={dispatchSearch}
				>
					{#if loading}
						<Spinner small />
					{:else}
						<ArrowUpIcon class="h-5 w-5" />
					{/if}
				</Button>
			</div>
		</slot>
	</div>
</Card>
