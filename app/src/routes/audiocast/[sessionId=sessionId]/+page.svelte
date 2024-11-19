<script lang="ts" context="module">
	export type ChatMetadata = {
		source: string;
		transcript: string;
		info?: string;
		title?: string;
	};

	type GenerateAudiocastResponse = {
		script: string;
		source_content: string;
		chats: Array<Omit<ChatItem, 'loading'>>;
		category: ContentCategory;
		title: ChatMetadata['title'];
		created_at?: string;
	};

	function parseScript(script: string) {
		const matches = [...script.matchAll(/<(Speaker\d+)>(.*?)<\/Speaker\d+>/gs)];
		return matches.map(([, speaker, content]) => `**${speaker}**: ${content}`).join('\n\n');
	}
</script>

<script lang="ts">
	import { getSessionContext, type ChatItem } from '@/stores/sessionContext.svelte';
	import type { ContentCategory } from '@/utils/types';
	import { env } from '@env';
	import { parse } from 'marked';
	import * as Accordion from '@/components/ui/accordion';
	import RenderMedia from '@/components/RenderMedia.svelte';
	import { page } from '$app/stores';
	import AudiocastPageAction from '@/components/AudiocastPageAction.svelte';
	import AudiocastPageChat from '@/components/AudiocastPageChat.svelte';
	import AudiocastPageSkeletonLoader from '@/components/AudiocastPageSkeletonLoader.svelte';

	const { session$ } = getSessionContext();

	let generating = false;

	$: sessionId = $page.params.sessionId;

	async function generateAudiocast(sessionId: string, category: ContentCategory, summary: string) {
		if (generating) return;
		generating = true;

		return fetch(`${env.API_BASE_URL}/audiocast/generate`, {
			method: 'POST',
			body: JSON.stringify({ sessionId, summary, category }),
			headers: { 'Content-Type': 'application/json' }
		})
			.then<GenerateAudiocastResponse>((res) => {
				if (res.ok) return res.json();
				throw new Error('Failed to generate audiocast');
			})
			.finally(() => (generating = false));
	}

	async function getAudiocast(sessionId: string) {
		return fetch(`${env.API_BASE_URL}/audiocast/${sessionId}`).then<GenerateAudiocastResponse>(
			(res) => {
				if (res.status === 404 && $session$?.summary) {
					const { summary, category } = $session$;
					return generateAudiocast(sessionId, category, summary);
				} else if (res.ok) return res.json();

				throw new Error('Failed to get audiocast');
			}
		);
	}
</script>

<div class="mx-auto flex h-full w-full pb-40 overflow-auto mt-6 flex-col items-center px-2 sm:px-1">
	{#await getAudiocast(sessionId)}
		<div class="flex flex-col w-full items-center justify-center -mt-6">
			<AudiocastPageSkeletonLoader />

			{#if generating}
				<p class="mt-4 py-2 px-4 bg-sky-600/20 animate-pulse text-sky-300 rounded-sm">
					Generating your audiocast...Please wait
				</p>
			{/if}
		</div>
	{:then data}
		<div class="flex w-full px-4 flex-col gap-y-3 sm:max-w-xl lg:max-w-3xl max-w-full">
			<div class="mb-4 flex flex-col gap-y-2">
				<span class="capitalize bg-gray-800 text-gray-300 w-fit py-1 px-3 rounded-md">
					{data.category}
				</span>

				{#if data.title}
					<h1 class="text-2xl font-semibold text-sky-200">{data.title}</h1>
				{/if}
			</div>

			<RenderMedia filename={sessionId} let:uri>
				<audio controls class="w-full animate-fade-in block">
					<source src={uri} type="audio/mpeg" />
					Your browser does not support the audio element.
				</audio>
			</RenderMedia>

			<Accordion.Root>
				<Accordion.Item value="item-0" class="border-gray-800">
					<Accordion.Trigger>Show Waveform</Accordion.Trigger>
					<Accordion.Content>
						<RenderMedia filename="{sessionId}.mp4" let:uri>
							<video controls class="w-full h-64 animate-fade-in block">
								<source src={uri} type="video/mp4" />
								Your browser does not support the video element.

								<track kind="captions" />
							</video>
						</RenderMedia>
					</Accordion.Content>
				</Accordion.Item>

				<Accordion.Item value="item-1" class="border-gray-800">
					<Accordion.Trigger>Audio Transcript</Accordion.Trigger>
					<Accordion.Content>
						<div class="flex w-full flex-col gap-y-3 p-2 bg-gray-900/70 text-gray-300">
							{#await parse(parseScript(data.script)) then parsedContent}
								{@html parsedContent}
							{/await}
						</div>
					</Accordion.Content>
				</Accordion.Item>

				<Accordion.Item value="item-2" class="border-gray-800">
					<Accordion.Trigger>Source Content</Accordion.Trigger>
					<Accordion.Content>
						<div class="flex w-full flex-col gap-y-3 bg-gray-900/70 text-gray-300 p-2">
							{#await parse(data.source_content) then parsedContent}
								{@html parsedContent}
							{/await}
						</div>
					</Accordion.Content>
				</Accordion.Item>
			</Accordion.Root>

			<AudiocastPageAction {sessionId} sessionTitle={data.title || 'Untitled'} on:showChats>
				<AudiocastPageChat slot="chats-button" chats={data.chats} />
			</AudiocastPageAction>
		</div>
	{:catch error}
		<div>Error: {String(error)}</div>
	{/await}
</div>
