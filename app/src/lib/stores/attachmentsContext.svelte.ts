import { getContext, setContext } from 'svelte';
import { writable } from 'svelte/store';

const CONTEXT_KEY = {};

export type UploadedItem = {
	id: string;
	file: File;
	loading?: boolean;
	errored?: boolean;
	gcsUrl?: string;
};

export const setAttachmentsContext = () => {
	const uploadedItems$ = writable<UploadedItem[]>([]);
	return setContext(CONTEXT_KEY, {
		uploadedItems$
	});
};

export type AttachmentsContext = ReturnType<typeof setAttachmentsContext>;

export const getAttachmentsContext = () => getContext<AttachmentsContext>(CONTEXT_KEY);
