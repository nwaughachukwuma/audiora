import { customAlphabet } from 'nanoid';

const alphabetSet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'; // all characters except - & _

export function uuid(length = 20): string {
	const nanoid = customAlphabet(alphabetSet, length);
	return nanoid();
}

export function* generateIds(transformer = (id: string) => id) {
	while (true) yield transformer(uuid());
}
