import { orderBy, where, type CollectionReference } from 'firebase/firestore';
import { distinctUntilChanged, shareReplay, of, catchError, switchMap, startWith } from 'rxjs';
import { dbRefs } from '@/services/firebase';
import { equals } from 'ramda';
import { collectionData, getQueryConstraints } from './db.utils';
import type { Sources } from '@/stores/customSources.svelte';

export const getCustomSources$ = (sessionId: string) => {
	const colRef = dbRefs.colRef(
		`audiora_sessions/${sessionId}/custom_sources`
	) as CollectionReference<Sources>;

	const colData = collectionData(
		getQueryConstraints(colRef, where('sessionId', '==', sessionId), orderBy('created_at', 'asc'))
	);

	return colData.pipe(
		switchMap((v) => of(v)),
		distinctUntilChanged((a, b) => equals(a, b)),
		shareReplay(1),
		catchError(() => of(null)),
		startWith(null)
	);
};
