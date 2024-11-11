<script lang="ts" context="module">
	type GenerateAudiocastResponse = {
		url: string;
		script: string;
		source_content: string;
		created_at?: string;
	};

	function parseScript(script: string) {
		const matches = [...script.matchAll(/<(Speaker\d+)>(.*?)<\/Speaker\d+>/gs)];
		return matches.map(([, speaker, content]) => `**${speaker}**: ${content}`).join('\n\n');
	}
</script>

<script lang="ts">
	import Spinner from '@/components/Spinner.svelte';
	import { getSessionContext } from '@/stores/sessionContext.svelte';
	import type { ContentCategory } from '@/utils/types';
	import { env } from '@env';
	import { parse } from 'marked';
	import * as Accordion from '@/components/ui/accordion';
	import RenderMedia from '@/components/RenderMedia.svelte';

	const { session$ } = getSessionContext();

	let generating = false;

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

	async function getAudiocast(sessionId: string, category: ContentCategory, summary: string) {
		return fetch(`${env.API_BASE_URL}/audiocast/${sessionId}`).then<GenerateAudiocastResponse>(
			(res) => {
				if (res.status === 404) return generateAudiocast(sessionId, category, summary);
				else if (res.ok) return res.json();
				throw new Error('Failed to get audiocast');
			}
		);
	}
</script>

<div class="mx-auto flex h-full w-full pb-40 overflow-auto mt-6 flex-col items-center px-2 sm:px-1">
	{#if $session$?.summary}
		{@const { summary, category } = $session$}
		{#await getAudiocast($session$.id, category, summary)}
			<div class="-mt-16 flex h-full w-full items-center justify-center sm:-mt-24">
				<Spinner />
			</div>
		{:then data}
			{@const script = data.script}
			{@const sourceContent = data.source_content}
			<div class="flex w-full px-4 flex-col gap-y-3 sm:max-w-xl lg:max-w-3xl max-w-full">
				{#if $session$.title}
					<h1 class="text-2xl font-semibold text-sky-200 mb-4">{$session$.title}</h1>
				{/if}

				<RenderMedia filename="{$session$.id}.mp4" let:uri>
					<audio controls class="w-full animate-fade-in block">
						<source src={uri} type="audio/mpeg" />
						Your browser does not support the audio element.
					</audio>
				</RenderMedia>

				<Accordion.Root>
					<Accordion.Item value="item-0" class="border-gray-800">
						<Accordion.Trigger>Show Waveform</Accordion.Trigger>
						<Accordion.Content>
							<RenderMedia filename="{$session$.id}.mp4" let:uri>
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
								{#await parse(parseScript(script)) then parsedContent}
									{@html parsedContent}
								{/await}
							</div>
						</Accordion.Content>
					</Accordion.Item>

					<Accordion.Item value="item-2" class="border-gray-800">
						<Accordion.Trigger>Source Content</Accordion.Trigger>
						<Accordion.Content>
							<div class="flex w-full flex-col gap-y-3 bg-gray-900/70 text-gray-300 p-2">
								{#await parse(sourceContent) then parsedContent}
									{@html parsedContent}
								{/await}
							</div>
						</Accordion.Content>
					</Accordion.Item>
				</Accordion.Root>
			</div>
		{:catch error}
			<div>{String(error)}</div>
		{/await}
	{/if}
</div>
