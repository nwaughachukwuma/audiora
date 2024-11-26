import type { DocumentReference } from 'firebase/firestore';
import { distinctUntilChanged, shareReplay, of, catchError, switchMap, startWith } from 'rxjs';
import { equals } from 'ramda';
import { dbRefs } from '@/services/firebase';
import { docData } from './db.utils';
import type { SessionModel } from '@/utils/types';

export const getSession$ = (sessionId: string, startValue: SessionModel | null = null) => {
	const ref = dbRefs.docRef('audiora_sessions', sessionId) as DocumentReference<SessionModel>;
	const obs = docData(ref).pipe(
		switchMap((v) => of(v)),
		distinctUntilChanged((a, b) => equals(a, b)),
		shareReplay(1),
		catchError(() => of(null))
	);
	return startValue ? obs.pipe(startWith(startValue)) : obs;
};
