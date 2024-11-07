import type { ParamMatcher } from '@sveltejs/kit';
export const match: ParamMatcher = (param: string) => param != null && param !== 'null';
