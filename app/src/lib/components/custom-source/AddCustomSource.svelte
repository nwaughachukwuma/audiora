<script lang="ts">
	import AddCustomSourceForm from './AddCustomSourceForm.svelte';
	import WebsiteURLSource from './WebsiteURLSource.svelte';
	import CopyPasteSource from './CopyPasteSource.svelte';

	let showWebsiteURLForm = false;
	let showCopyPasteForm = false;
</script>

<div class="h-full bg-gray-950 pt-2">
	{#if !showWebsiteURLForm && !showCopyPasteForm}
		<AddCustomSourceForm
			on:useWebsiteURL={() => (showWebsiteURLForm = true)}
			on:useCopyPaste={() => (showCopyPasteForm = true)}
		/>
	{:else if showWebsiteURLForm}
		<WebsiteURLSource on:closeWebsiteURL={() => (showWebsiteURLForm = false)} />
	{:else if showCopyPasteForm}
		<CopyPasteSource on:closeCopyPaste={() => (showCopyPasteForm = false)} />
	{/if}
</div>
