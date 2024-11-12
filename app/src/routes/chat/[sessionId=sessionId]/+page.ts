import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ parent }) => {
	const { category } = await parent();
	if (!category) error(400, 'Content category is not specified');
	return {
		category
	};
};
