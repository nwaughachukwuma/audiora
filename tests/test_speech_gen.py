import asyncio
import shutil
import uuid
from pathlib import Path

from src.utils.audio_manager import AudioManager
from src.utils.audio_synthesizer import AudioSynthesizer

content = """
<Person1>Hello there! Today, we're diving into a personal reflection on justice as explored in Plato's <phoneme alphabet="ipa" ph="rɪˈpʌblɪk">Republic</phoneme>, and how it relates to today's political systems. <break time="0.2s"/> Exciting, right?</Person1> 
<Person2>Uh-huh, definitely! So, what's Plato's take on justice?</Person2> 
<Person1>Well, Plato sees justice as a "harmony," where each part of society plays its role for the greater good. He envisions an ideal state with rulers, warriors, and producers all contributing to a balanced whole. <emphasis level="moderate">The big question</emphasis> is: how do our modern systems measure up?</Person1> 
<Person2>Hmm, interesting. How about democracies?</Person2> <Person1>Good question! In democracies, justice often means "equality" and protecting individual rights. This aligns with Plato's idea of everyone fulfilling their role, but it's complex. Balancing personal freedoms and societal responsibilities is tough—something Plato might say needs wise leaders. <break time="0.2s"/> Easier said than done, huh?</Person1> 
<Person2>Definitely a tricky balance! What about authoritarian regimes?</Person2> 
<Person1>In authoritarian regimes, justice is often about maintaining "order" and control. The focus is on the collective, sometimes at the expense of individual freedoms. Plato's philosopher-king might like this in theory, but <emphasis level="moderate">in practice</emphasis>, it risks losing that harmony he valued. <break time="0.2s"/> A real paradox!</Person1> 
<Person2>Right! So, how does this all play out today?</Person2> 
<Person1>Today, we see a mix. Social justice movements push democracies to redefine "equality" and "fairness," aiming for inclusivity. Authoritarian states claim stability, but often face criticism for suppressing dissent. <break time="0.2s"/> Ultimately, Plato challenges us to examine our values and roles. Are we contributing to harmony, or caught in a tug-of-war between individual desires and collective needs?</Person1> 
<Person2>That's a powerful question.</Person2> 
<Person1>Exactly. Plato's insights remind us that true justice might lie in finding balance—a timeless pursuit. <break time="0.2s"/> Thanks for listening, and I hope this sparks some thoughts on justice in our world today!</Person1>
"""


async def test_speech_gen():
    audio_manager = AudioManager()
    filepath = await audio_manager.generate_speech(content)
    # Copy the file
    enhanced_filepath = f"/tmp/{str(uuid.uuid4())}.mp3"
    shutil.copy(filepath, enhanced_filepath)
    AudioSynthesizer().enhance_audio(Path(enhanced_filepath))

    print(f"filepath: {filepath}; enhanced_filepath: {enhanced_filepath}")
    return filepath, enhanced_filepath


if __name__ == "__main__":
    asyncio.run(test_speech_gen())
