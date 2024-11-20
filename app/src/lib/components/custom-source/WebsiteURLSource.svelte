<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { ArrowLeft, X } from 'lucide-svelte';
	import { Button } from '../ui/button';
	import { Card, CardContent, CardHeader } from '../ui/card';
	import { Input } from '../ui/input';

	const dispatch = createEventDispatcher<{ closeWebsiteURL: void }>();
</script>

<Card class="max-w-2xl mx-auto bg-gray-900 border-gray-800">
	<CardHeader>
		<div class="flex items-center justify-between">
			<div class="flex items-center gap-2">
				<Button
					variant="ghost"
					size="icon"
					class="text-gray-400 hover:text-white"
					on:click={() => dispatch('closeWebsiteURL')}
				>
					<ArrowLeft class="h-5 w-5" />
				</Button>
				<h1 class="text-2xl font-normal">Website URL</h1>
			</div>
			<Button
				variant="ghost"
				size="icon"
				class="text-gray-400 hover:text-white"
				on:click={() => dispatch('closeWebsiteURL')}
			>
				<X class="h-5 w-5" />
			</Button>
		</div>

		<p class="text-gray-400">Paste in a Web Link below to upload as a source</p>
	</CardHeader>

	<CardContent class="flex flex-col gap-y-4">
		<div class="flex flex-col gap-y-2">
			<label for="url" class="text-blue-400">Paste URL*</label>
			<Input
				id="url"
				placeholder="https://"
				class="bg-gray-900 focus:ring-0 focus-visible:ring-0 border-blue-400 text-white placeholder:text-gray-600"
			/>
		</div>

		<div class="flex flex-col gap-y-2">
			<div class="font-medium text-xl">Notes</div>
			<ul class="list-disc list-inside space-y-1 text-gray-400">
				<li>Only the visible text on the website will be imported at this moment</li>
				<li>Content behind paywalls are not supported</li>
				<li>Content requiring authentication are not supported</li>
				<li>Supports .pdf url</li>
			</ul>
		</div>

		<div class="flex justify-end">
			<Button class="bg-blue-500 text-base px-8 text-blue-100 hover:bg-blue-600">Insert</Button>
		</div>
	</CardContent>
</Card>
