import {
	type CollectionReference,
	type DocumentData,
	type DocumentReference,
	type QueryConstraint,
	type Query,
	onSnapshot,
	query
} from 'firebase/firestore';
import { Observable } from 'rxjs';

let DEFAULT_OPTIONS = { includeMetadataChanges: false };

export const docData = <T>(
	docRef: DocumentReference<T, DocumentData>,
	options = DEFAULT_OPTIONS
): Observable<T> =>
	new Observable((subscriber) => {
		let unsubscribe = onSnapshot(docRef, options, {
			next: (snap) => {
				if (snap.exists()) {
					subscriber.next(snap.data() as NonNullable<T>);
				} else {
					subscriber.next(null as T);
				}
			},
			error: subscriber.error.bind(subscriber),
			complete: subscriber.complete.bind(subscriber)
		});
		return { unsubscribe };
	});

export const collectionData = <T>(query: Query<T>, options = DEFAULT_OPTIONS): Observable<T[]> =>
	new Observable((subscriber) => {
		let unsubscribe = onSnapshot(query, options, {
			next: (snap) => {
				subscriber.next(snap.docs.map((doc) => doc.data() as NonNullable<T>));
			},
			error: subscriber.error.bind(subscriber),
			complete: subscriber.complete.bind(subscriber)
		});
		return { unsubscribe };
	});

export const getQueryConstraints = <T>(
	colRef: CollectionReference<T>,
	...queryConstraint: QueryConstraint[]
) => query(colRef, ...queryConstraint);
