<script lang="ts">
	export let href: string;
	export let content: string;
</script>

<a
	{href}
	class="border no-underline hover:no-underline rounded-md group border-gray-600 p-4 bg-gray-900 hover:bg-gray-800"
>
	<span class="text-sm">
		{content}
	</span>
</a>
