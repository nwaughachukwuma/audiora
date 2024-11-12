import type { ContentCategory } from '@/utils/types';
import { setContext, getContext } from 'svelte';
import { persisted } from 'svelte-persisted-store';
import { derived, writable } from 'svelte/store';

const CONTEXT_KEY = {};
export const SESSION_KEY = 'AUDIOCAST_SESSION';

export type ChatItem = {
	id: string;
	content: string;
	role: 'user' | 'assistant';
	loading?: boolean;
};

export type Session = {
	id: string;
	category: ContentCategory;
	chats: ChatItem[];
	title: string;
	nonce: number;
	completed?: boolean;
	summary?: string;
};

export function setSessionContext(sessionId: string) {
	const session$ = persisted<Session | null>(`${SESSION_KEY}_${sessionId}`, null);
	const sessionId$ = writable(sessionId);
	const sessionCompleted$ = derived(session$, ($session) => !!$session?.completed);

	const fetchingSource$ = writable(false);
	const audioSource$ = persisted<string>(`AUDIOCAST_SOURCE_${sessionId}`, '');

	return setContext(CONTEXT_KEY, {
		session$,
		sessionId$,
		sessionCompleted$,
		fetchingSource$,
		audioSource$,
		startSession: (category: ContentCategory) => {
			session$.set({
				id: sessionId,
				category,
				title: 'Untitled',
				nonce: Date.now(),
				chats: []
			});
			return session$;
		},
		addChatItem(chatItem: ChatItem) {
			session$.update((session) => {
				if (session) session.chats.push(chatItem);
				return session;
			});
			return chatItem;
		},
		updateChatItem(update: { id: string } & Partial<ChatItem>) {
			session$.update((session) => {
				if (!session) return session;

				const chats = session.chats.map((item) =>
					item.id === update.id ? { ...item, ...update } : item
				);
				session.chats = chats;
				return session;
			});
		},
		updateChatContent: (chatId: string, chunk: string) => {
			session$.update((session) => {
				if (!session) return session;

				const chats = session.chats.map((i) =>
					i.id === chatId ? { ...i, loading: false, content: i.content + chunk } : i
				);
				session.chats = chats;
				return session;
			});
		}
	});
}

export type SessionContext = ReturnType<typeof setSessionContext>;
export const getSessionContext = (): SessionContext => getContext(CONTEXT_KEY);