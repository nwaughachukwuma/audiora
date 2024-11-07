<script lang="ts">
	import { onMount } from 'svelte';
	import { Button } from '$lib/components/ui/button';
	import { Textarea } from '$lib/components/ui/textarea';
	import { toast } from 'svelte-sonner';
	import { sessionStore, type Message } from '$lib/stores/session';
	import { contentCategories, type ContentCategory } from '$lib/types';
	import { nanoid } from 'nanoid';
	import { debounce } from 'throttle-debounce';

	let messageInput = '';
	let isLoading = false;
	let selectedCategory: ContentCategory | null = null;

	const examplePrompts = {
		'professional-development': 'I want to learn about effective leadership',
		'self-improvement': 'Help me understand mindfulness meditation',
		'knowledge-synthesis': 'Explain quantum computing basics',
		'creative-writing': 'Create a story about space exploration'
	};

	const debouncedSendMessage = debounce(500, async (content: string) => {
		if (!selectedCategory) {
			toast.error('Please select a content category first');
			return;
		}

		try {
			isLoading = true;

			const response = await fetch('/api/chat', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					sessionId: $sessionStore.id,
					message: content,
					contentCategory: selectedCategory
				})
			});

			if (!response.ok) throw new Error('Failed to send message');

			const aiResponse = await response.text();

			sessionStore.update((state) => ({
				...state,
				messages: [...state.messages, { role: 'assistant', content: aiResponse }]
			}));
		} catch (error) {
			toast.error('Failed to send message');
			console.error(error);
		} finally {
			isLoading = false;
		}
	});

	async function handleSubmit() {
		if (!messageInput.trim()) return;

		const message: Message = {
			role: 'user',
			content: messageInput
		};

		sessionStore.update((state) => ({
			...state,
			messages: [...state.messages, message]
		}));

		const content = messageInput;
		messageInput = '';

		await debouncedSendMessage(content);
	}

	function setExamplePrompt(category: ContentCategory) {
		selectedCategory = category;
		messageInput = examplePrompts[category] || '';
	}
</script>

<div class="flex flex-col gap-4">
	<div class="flex gap-2 flex-wrap">
		{#each contentCategories as category}
			<Button
				variant={selectedCategory === category ? 'default' : 'outline'}
				on:click={() => setExamplePrompt(category)}
			>
				{category}
			</Button>
		{/each}
	</div>

	<div class="h-[400px] overflow-y-auto border rounded-lg p-4 bg-card">
		{#if $sessionStore.messages.length === 0}
			<p class="text-muted-foreground text-center">
				Start a conversation by selecting a category and sending a message
			</p>
		{/if}

		{#each $sessionStore.messages as message}
			<div class="mb-4 last:mb-0">
				<div class="font-semibold mb-1">
					{message.role === 'user' ? 'You' : 'Assistant'}:
				</div>
				<div class="pl-4">
					{message.content}
				</div>
			</div>
		{/each}

		{#if isLoading}
			<div class="flex items-center gap-2 text-muted-foreground">
				<div class="animate-spin">⌛</div>
				Thinking...
			</div>
		{/if}
	</div>

	<form class="flex gap-2" on:submit|preventDefault={handleSubmit}>
		<Textarea
			bind:value={messageInput}
			placeholder="Type your message..."
			rows="3"
			class="flex-1"
		/>
		<Button type="submit" disabled={isLoading || !messageInput.trim()}>Send</Button>
	</form>
</div>
