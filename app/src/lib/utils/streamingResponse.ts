export async function* streamingResponse(response: Response) {
	if (!response.body) return response.text();

	const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
	let exitLoop = false;
	while (!exitLoop) {
		const { done, value: chunk } = await reader.read();
		if (done) {
			exitLoop = true;
			break;
		}
		yield chunk;
	}
}
