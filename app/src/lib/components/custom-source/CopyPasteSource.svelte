<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { ArrowLeft, X, MessageCircle } from 'lucide-svelte';
	import { Button } from '../ui/button';
	import { Card, CardContent, CardHeader } from '../ui/card';
	import { Textarea } from '../ui/textarea';

	const dispatch = createEventDispatcher<{
		submitCopyPaste: { text: string };
		closeCopyPaste: void;
	}>();

	let text = '';
</script>

<Card class="max-w-2xl mx-auto bg-gray-900 border-gray-800">
	<CardHeader>
		<div class="flex items-center justify-between">
			<div class="flex items-center gap-2">
				<Button
					variant="ghost"
					size="icon"
					class="text-gray-400 hover:text-white"
					on:click={() => dispatch('closeCopyPaste')}
				>
					<ArrowLeft class="h-5 w-5" />
				</Button>
				<h1 class="text-2xl font-normal">Paste copied text</h1>
			</div>
			<Button
				variant="ghost"
				size="icon"
				class="text-gray-400 hover:text-white"
				on:click={() => dispatch('closeCopyPaste')}
			>
				<X class="h-5 w-5" />
			</Button>
		</div>

		<p class="text-gray-400">Paste your copied text below to upload as a source</p>
	</CardHeader>

	<CardContent class="flex flex-col gap-y-4">
		<div class="flex flex-col gap-y-2">
			<label for="url" class="text-blue-400">Paste Text here*</label>

			<div class="relative">
				<Textarea
					id="text"
					bind:value={text}
					class="min-h-56 ring-0 focus:ring-0 focus-visible:ring-0 text-base bg-gray-900 border-blue-400/50 focus:border-blue-400 text-white resize-none"
					placeholder=""
				/>
				<div class="absolute bottom-3 right-3 flex items-center gap-1">
					<Button
						variant="ghost"
						size="icon"
						class="h-8 w-8 rounded-full bg-gray-800 hover:bg-gray-700"
					>
						<MessageCircle class="h-4 w-4" />
					</Button>
				</div>
			</div>

			<div class="flex justify-end">
				<Button
					on:click={() => {
						dispatch('submitCopyPaste', { text });
						requestAnimationFrame(() => {
							dispatch('closeCopyPaste');
						});
					}}
					disabled={!text}
					class="bg-blue-500 text-base px-8 text-blue-100 hover:bg-blue-600"
					>Insert
				</Button>
			</div>
		</div></CardContent
	>
</Card>
