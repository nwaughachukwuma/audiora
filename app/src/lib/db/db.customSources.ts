import { orderBy, type CollectionReference } from 'firebase/firestore';
import { distinctUntilChanged, shareReplay, of, catchError, switchMap, startWith } from 'rxjs';
import { dbRefs } from '@/services/firebase';
import { equals } from 'ramda';
import { collectionData, getQueryConstraints } from './db.utils';

export type LinkSource = {
	source_type: 'link';
	url: string;
};

export type CopyPasteSource = {
	source_type: 'copy/paste';
};

export type UploadSource = {
	source_type: 'file_upload';
};

export type Sources = (LinkSource | CopyPasteSource | UploadSource) & {
	id: string;
	content_type:
		| 'text/plain'
		| 'text/html'
		| 'application/pdf'
		| 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
	content: string;
	title?: string;
	created_at?: string;
};

export const getCustomSources$ = (sessionId: string) => {
	const colRef = dbRefs.colRef(
		`audiora_sessions/${sessionId}/custom_sources`
	) as CollectionReference<Sources>;

	const colData = collectionData(getQueryConstraints(colRef, orderBy('created_at', 'asc')));

	return colData.pipe(
		switchMap((v) => of(v)),
		distinctUntilChanged((a, b) => equals(a, b)),
		shareReplay(1),
		catchError(() => of(null)),
		startWith(null)
	);
};
