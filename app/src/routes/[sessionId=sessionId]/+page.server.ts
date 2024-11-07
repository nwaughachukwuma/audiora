import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = ({ url }) => {
	const category = url.searchParams.get('category');
	if (!category) error(400, 'Audio category was not found');

	return {
		category
	};
};
