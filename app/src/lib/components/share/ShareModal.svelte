<!-- https://pchynoweth.github.io/svelte-share-buttons-component/ -->
<script lang="ts">
	import * as Dialog from '../ui/dialog';
	import FacebookShare from './FacebookShare.svelte';
	import HackerNewsShare from './HackerNewsShare.svelte';
	import LinkedinShare from './LinkedinShare.svelte';
	import RedditShare from './RedditShare.svelte';
	import TelegramShare from './TelegramShare.svelte';
	import WhatsAppShare from './WhatsAppShare.svelte';
	import XShare from './XShare.svelte';
	import CopyShare from './CopyShare.svelte';
	import { Share2Icon } from 'lucide-svelte';

	export let url: string;
	export let title: string;
</script>

<Dialog.Root>
	<Dialog.Trigger>
		<slot name="trigger" />
	</Dialog.Trigger>
	<Dialog.Content class="border-neutral-800 max-w-[90%] sm:max-w-[440px]">
		<Dialog.Header>
			<Dialog.Title>
				<span class="flex items-center text-gray-400 pb-2">
					<Share2Icon class="inline w-4 mr-2" /> Share on social media
				</span>
			</Dialog.Title>
		</Dialog.Header>
		<div class="w-full flex items-center flex-wrap max-sm:justify-center pt-6 pb-4 gap-2">
			<XShare
				text={title}
				{url}
				hashtags="try_audiora,ai_audio,generative_audio"
				via="username"
				related="other,users"
			/>

			<WhatsAppShare text="{title} {url}" />
			<FacebookShare quote={title} {url} />
			<TelegramShare text={title} {url} />
			<LinkedinShare {url} />
			<RedditShare {title} {url} />
			<HackerNewsShare {title} {url} />
			<CopyShare {url} />
		</div>
	</Dialog.Content>
</Dialog.Root>
