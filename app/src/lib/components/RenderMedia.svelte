<script context="module">
	const BLOB_BASE_URI = 'audiora/assets';
</script>

<script lang="ts">
	import { env } from '@env';
	import Spinner from './Spinner.svelte';

	export let filename: String;

	async function getSignedURL() {
		const blobname = `${BLOB_BASE_URI}/${filename}`;
		return fetch(`${env.API_BASE_URL}/get-signed-url?blobname=${blobname}`).then<string>((res) => {
			if (res.ok) return res.json();
			throw new Error('Failed to get signed Audiocast URL');
		});
	}
</script>

<div class="w-full flex items-center flex-col gapy-3">
	{#await getSignedURL()}
		<Spinner />
	{:then uri}
		<slot {uri} />
	{:catch error}
		<div>{String(error)}</div>
	{/await}
</div>
