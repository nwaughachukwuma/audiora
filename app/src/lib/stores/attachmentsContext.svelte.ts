import { getContext, setContext } from 'svelte';
import { derived, writable } from 'svelte/store';

const CONTEXT_KEY = {};

export type UploadedItem = {
	id: string;
	file: File;
	loading?: boolean;
	errored?: boolean;
	gcsUrl?: string;
};

export const setAttachmentsContext = (sessionId: string) => {
	const uploadedItems$ = writable<UploadedItem[]>([]);

	const sessionUploadItems$ = derived(uploadedItems$, (items) =>
		items.filter((i) => i.file instanceof File && i.id.startsWith(sessionId))
	);

	return setContext(CONTEXT_KEY, {
		uploadedItems$,
		sessionUploadItems$,
		addUploadItem(item: UploadedItem) {
			uploadedItems$.update((files) => [...files, item]);
		},
		updateUploadItem(itemId: string, update: Partial<UploadedItem>) {
			uploadedItems$.update((files) => {
				return files.map((f) => (f.id === itemId ? { ...f, ...update } : f));
			});
		},
		removeUploadItem(itemId: string) {
			uploadedItems$.update((files) => {
				return files.filter((f) => f.id !== itemId);
			});
		}
	});
};

export type AttachmentsContext = ReturnType<typeof setAttachmentsContext>;

export const getAttachmentsContext = () => getContext<AttachmentsContext>(CONTEXT_KEY);
