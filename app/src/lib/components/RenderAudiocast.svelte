<script context="module">
	const BLOB_BASE_URI = 'audiora/assets';
</script>

<script lang="ts">
	import { env } from '@env';
	import Spinner from './Spinner.svelte';

	export let sessionId: String;

	async function getSignedURL() {
		const blobname = `${BLOB_BASE_URI}/${sessionId}`;
		return fetch(`${env.API_BASE_URL}/get-signed-url?blobname=${blobname}`).then<string>((res) => {
			if (res.ok) return res.json();
			throw new Error('Failed to get signed Audiocast URL');
		});
	}
</script>

{#await getSignedURL()}
	<Spinner />
{:then audioURL}
	<audio controls class="w-full animate-fade-in block">
		<source src={audioURL} type="audio/mpeg" />
		Your browser does not support the audio element.
	</audio>
{:catch error}
	<div>{String(error)}</div>
{/await}
