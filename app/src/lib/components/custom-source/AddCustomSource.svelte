<script lang="ts">
	import AddCustomSourceForm from './AddCustomSourceForm.svelte';
	import WebsiteURLSource from './WebsiteURLSource.svelte';
	import CopyPasteSource from './CopyPasteSource.svelte';
	import GeneratingSourceSkeleton from './GeneratingSourceSkeleton.svelte';

	export let generatingSource = false;

	let showWebsiteURLForm = false;
	let showCopyPasteForm = false;
</script>

<div class="h-full bg-gray-950 pt-2">
	{#if generatingSource}
		<GeneratingSourceSkeleton />
	{:else if showWebsiteURLForm}
		<WebsiteURLSource on:closeWebsiteURL={() => (showWebsiteURLForm = false)} on:submitURL />
	{:else if showCopyPasteForm}
		<CopyPasteSource on:closeCopyPaste={() => (showCopyPasteForm = false)} on:submitCopyPaste />
	{:else}
		<AddCustomSourceForm
			on:useWebsiteURL={() => (showWebsiteURLForm = true)}
			on:useCopyPaste={() => (showCopyPasteForm = true)}
		/>
	{/if}
</div>
