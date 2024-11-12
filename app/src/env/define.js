import 'dotenv/config';
import { env } from './setup.js';

/**@type () => Record<`process.env.${string}`, string> **/
export const defineEnv = () =>
	Object.entries(env).reduce(
		(acc, [key, value]) => ({ ...acc, [`process.env.${key}`]: `'${value}'` }),
		{}
	);
