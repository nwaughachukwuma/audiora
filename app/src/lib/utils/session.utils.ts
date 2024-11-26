import type { ChatItem } from '@/stores/sessionContext.svelte';

export const FINAL_RESPONSE_PREFIX = 'Ok, thanks for clarifying!';
export const FINAL_RESPONSE_SUFFIX =
	'Please click the button below to start generating the audiocast.';

export const isfinalResponse = (v: ChatItem) => v.content.includes(FINAL_RESPONSE_SUFFIX);

export function getSummary(content: string) {
	const replacePrefixRegex = new RegExp(FINAL_RESPONSE_PREFIX, 'gi');
	const replaceSuffixRegex = new RegExp(FINAL_RESPONSE_SUFFIX, 'gi');
	return content.replace(replacePrefixRegex, '').replace(replaceSuffixRegex, '').trim();
}
