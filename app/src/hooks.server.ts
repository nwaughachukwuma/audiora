import 'dotenv/config';
import type { HandleServerError, Handle } from '@sveltejs/kit';
import { sequence } from '@sveltejs/kit/hooks';
import ejs from 'ejs';
import { uuid } from '$lib/utils/uuid';

const baseHandle: Handle = async ({ event, resolve }) => {
	return resolve(event, {
		transformPageChunk: ({ html }) =>
			ejs.render(html, {
				env: { COMMIT_SHA: process.env.COMMIT_SHA }
			})
	});
};

const handleSession: Handle = async ({ event, resolve }) => {
	event.locals.sessionId = event.params.sessionId || uuid();
	return resolve(event);
};

export const handle = sequence(baseHandle, handleSession);

export const handleError: HandleServerError = ({ error, status, event, message }) => {
	console.error('handleServerError', { error, event });
	const errorId = crypto.randomUUID();
	return {
		status,
		message: `Internal Server Errors.\n${message}`,
		errorId
	};
};
