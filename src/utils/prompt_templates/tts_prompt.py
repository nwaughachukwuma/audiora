from dataclasses import dataclass

from src.utils.chat_utils import ContentCategory, category_qualifiers


@dataclass
class Metadata:
    output_language: str = "English"


class TTSPromptMaker:
    category: ContentCategory

    def __init__(self, category: ContentCategory, metadata: Metadata):
        self.output_language = metadata.output_language
        self.category = category

    def get_tags(self) -> list[str]:
        """Get connection tags based on the number of speakers."""
        return [f"<Person{i}>" for i in range(1, 10)]

    def get_system_prompt(self, source_content: str) -> str:
        """
        Generate an optimized system prompt for converting a source content into the appropriate format.
        """
        return f"""Transform the following source content into an engaging {self.category} TTS-optimized audiocast script.

        Source Content: {source_content}

        Content Parameters:
        1. Format: Create {category_qualifiers[self.category]} in TTS-optomized audiocast flow
        2. Language: {self.output_language}
        3. Style: Expert-driven audio content maintaining the source accuracy and tone while optimizing for audio delivery
        4. Structure: Follow a natural speech transaction flow using the specified, neccesary speaker tags
        5. Characteristics to incorporate: informative, engaging, slight apt humor

        Optimization Requirements:
        1. Speaker Organization:
        - Use <Person1>, <Person2>, etc., tags for speaker identification
        - <Person1>: Main speaker/host/narrator
        - <Person2> (and others if needed): Supporting roles, discussants, or interviewers
        - Maximum 2 speakers unless content specifically requires more
        - Example Format:
            <Person1>[Expert introduction of topic]</Person1>
            <Person2>[Engaging follow-up, questions, or challenges]</Person2>
        - Use only <Person1> if the souce content or category requires only one speaker

        2. SSML Enhancement:
        - Add appropriate SSML tags for improved audio delivery
        - Include <break time="0.2s"> (max 0.3s) for natural pauses
        - Use <emphasis level="moderate"> for key points
        - Apply <phoneme> tags for complex terms
        - Ensure all tags are properly closed
        - Keep all SSML tags within the appropriate speaker tags

        3. Conversational Elements:
        - Insert natural speech patterns and filler words (um, uh, well)
        - Mild stuttering when appropriate
        - When more than 1 Speaker:
            a. Use verbal acknowledgments (uh-huh, I see) when relevant
            b. Maintain authentic dialogue flow
            c. Apply speaker interactions, respectful disagreements and challenges

        4. Content Flow:
        - Structure: Opening greeting → Topic introduction → Main points/discussion → Conclusion
        - Natural transitions between points
        - Maintain consistent pacing
        - Expert-level discussion of source material
        - Reference source material naturally
        - "Key terms" in quotation marks

        5. Quality Standards:
        - Verify SSML tag accuracy, opening and closure
        - Check speaker tag consistency
        - Clear, accessible language
        - Maintain accurate representation of source content, don't deviate
        - Appropriate word counnt for {self.category} format
        - Generate only the audiocast transcript
        - Ensure all SSML tags are properly formatted and within the speaker tags

        Output Format Example for 2 speakers:
        <Person1>Hello there! [Content Intro & Overview].</Person1>
        <Person2>I'm particularly excited about [Specific Aspect]. What caught your attention about this?</Person2>
        <Person1>Well <break time="0.2s"/> what really stands out is [Key Point]...</Person1>

        Remember: Focus solely on conveying the source content in an engaging audio format while optimizing for audio delivery.
        """
