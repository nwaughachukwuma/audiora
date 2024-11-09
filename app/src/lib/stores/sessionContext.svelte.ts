import { setContext, getContext } from 'svelte';
import { persisted } from 'svelte-persisted-store';

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
	chats: ChatItem[];
	title: string;
	nonce: number;
};

export function setSessionContext(sessionId: string) {
	const session$ = persisted<Session | null>(`${SESSION_KEY}_${sessionId}`, null);

	return setContext(CONTEXT_KEY, {
		session$,
		addChatItem(chatItem: ChatItem) {
			session$.update((session) => {
				if (session) {
					session.chats.push(chatItem);
					return session;
				}
				return {
					id: sessionId,
					title: 'Untitled',
					nonce: Date.now(),
					chats: [chatItem]
				};
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
				console.log('updateChatContent', chatId, chunk, session);
				if (!session) return session;

				const chats = session.chats.map((i) =>
					i.id === chatId ? { ...i, content: i.content + chunk } : i
				);
				session.chats = chats;
				return session;
			});
		}
	});
}

export type SessionContext = ReturnType<typeof setSessionContext>;
export const getSessionContext = (): SessionContext => getContext(CONTEXT_KEY);
