export type ContentCategory =
	| 'podcast'
	| 'sermon'
	| 'audiodrama'
	| 'lecture'
	| 'commentary'
	| 'voicenote'
	| 'interview'
	| 'soundbite';

export interface ChatMetadata {
	source: string;
	transcript: string;
	info?: string;
	title: string;
}

export interface SessionChatItem {
	id: string;
	role: 'user' | 'assistant';
	content: string;
}

export interface SessionModel {
	id: string;
	category: ContentCategory;
	chats: Array<SessionChatItem>;
	completed?: boolean;
	metadata?: ChatMetadata;
	created_at?: string;
}
