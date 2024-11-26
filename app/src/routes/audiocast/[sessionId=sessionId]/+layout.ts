import { error } from '@sveltejs/kit';
import type { LayoutLoad } from './$types';
import { getSession$ } from '@/db/db.session';
import { firstValueFrom } from 'rxjs';

export const load: LayoutLoad = async ({ params }) => {
	const sessionModel = await firstValueFrom(getSession$(params.sessionId));
	if (!sessionModel) error(404, 'Session not found');

	return {
		sessionModel
	};
};
