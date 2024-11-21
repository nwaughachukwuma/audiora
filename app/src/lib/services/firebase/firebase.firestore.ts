import { doc, collection, type Firestore } from 'firebase/firestore';
export function refs(firestore: Firestore) {
	return {
		docRef: (col: string, id: string) => doc(firestore, col, id),
		colRef: (col: string) => collection(firestore, col)
	};
}
