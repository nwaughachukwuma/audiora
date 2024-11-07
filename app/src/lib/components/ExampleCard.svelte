<script lang="ts">
	export let href: string;
	export let content: string;
</script>

<a
	{href}
	class="border no-underline hover:no-underline rounded-md group border-gray-600 p-6 bg-gray-900 hover:bg-gray-800"
	style="height: 125px;"
>
	<span class="text-lg">
		{content}
	</span>
</a>
