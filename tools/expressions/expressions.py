"""Expression sheet plan: 12 clips x 4 expressions, timed windows inside an 8 s (192-frame) clip."""

SECONDS = 8.0          # snaps to 192 frames at 24 fps
NEUTRAL_END = 0.5      # the clip opens on the reference pose
WINDOWS = [(0.5, 2.4), (2.4, 4.3), (4.3, 6.2), (6.2, 8.0)]

# Concrete facial cues work better than bare labels. Lingering states (tears, blush) go last in a clip.
CUES = {
    "smile": "a gentle, relaxed closed-mouth smile",
    "happy smile": "a bright, open happy smile with cheeks lifted and eyes softly crinkled",
    "joyful": "beaming with joy, a wide open-mouthed smile, eyebrows raised, eyes sparkling",
    "laughing": "laughing out loud, mouth wide open, eyes squeezed shut, head tipped back slightly, shoulders shaking",
    "smirk": "a lopsided smirk, one corner of the mouth raised, eyes narrowed knowingly",
    "smug": "a smug, self-satisfied look, chin lifted, half-lidded eyes, a tight pleased smile",
    "proud": "a proud expression, chin up, chest out, a confident closed smile",
    "evil smile": "a sinister grin, eyes narrowed and shadowed, a wide toothy menacing smile",
    "seductive smile": "a sultry smile, heavy-lidded eyes looking straight at the viewer, head tilted slightly",
    "lovestruck": "lovestruck, soft dreamy eyes, a faint blush and a tender, dazed little smile",
    "aroused": "flushed cheeks, heavy-lidded glossy eyes, lips slightly parted, breathing a little heavier",
    "full-face blush": "blushing deep red across the whole face up to the ears, eyes wide, mouth a small tense line",
    "blushing shyly": "a shy pink blush across the cheeks, eyes lowered, a small bashful smile",
    "looking away shyly": "turning the face to the side and glancing away shyly, cheeks pink",
    "fidgeting shyly": "fidgeting shyly, shoulders hunched, tugging at the scarf, eyes darting down, cheeks pink",
    "embarrassed": "embarrassed, wincing smile, eyebrows pinched upward, a blush and a bead of sweat",
    "flustered": "flustered, eyes wide and wobbling, mouth open in a wavy line, cheeks red",
    "nervous smile": "a nervous, strained smile, eyebrows raised and tilted up, a drop of sweat on the temple",
    "nervous pout": "a nervous pout, lower lip pushed out, eyebrows tilted up, eyes glancing aside",
    "nervous": "nervous and uneasy, eyes darting, lips pressed together, eyebrows knitted upward",
    "forced smile": "a stiff forced smile, the mouth smiling but the eyes flat and unamused, a twitching brow",
    "guilty": "guilty, eyes averted downward, eyebrows tilted up, lips pressed tight, head lowered a little",
    "worried": "worried, eyebrows drawn together and upturned, mouth a small frown",
    "scared": "scared, eyes wide with shrunken pupils, mouth open, eyebrows high, pulling back slightly",
    "surprised": "surprised, eyes wide, eyebrows raised high, mouth in a small round 'o'",
    "shocked": "shocked, eyes huge with tiny pupils, mouth dropped wide open, frozen in place",
    "confused": "confused, one eyebrow raised and the other lowered, head tilted, mouth slightly skewed",
    "dazed": "dazed, eyes unfocused and half-closed, mouth hanging slightly open, head swaying a little",
    "curious": "curious, leaning in slightly, eyes wide and bright, eyebrows raised, a small interested smile",
    "thinking": "thinking, eyes looking up and to the side, lips pursed, a hand raised to the chin",
    "serious": "serious, a level steady gaze, eyebrows straight and low, mouth a firm flat line",
    "indifferent": "indifferent, blank half-lidded eyes, a flat neutral mouth, no emotion at all",
    "bored": "bored, droopy half-closed eyes, a slack mouth, head slumping a little to one side",
    "sleepy": "sleepy, eyelids drooping almost shut, a soft yawn, head nodding",
    "annoyed": "annoyed, eyes narrowed, eyebrows lowered, mouth a tight frown, a small vein on the temple",
    "contemptuous": "contemptuous, looking down the nose, one lip curled in a sneer, eyes cold and half-lidded",
    "disgusted": "disgusted, nose wrinkled, upper lip curled, leaning back, eyes squinting",
    "angry": "angry, eyebrows slammed down, eyes glaring, teeth bared in a scowl",
    "disappointed": "disappointed, eyes lowered, eyebrows slightly upturned, a small downturned mouth, shoulders sinking",
    "pout": "pouting, cheeks puffed, lower lip pushed out, eyes looking up sulkily",
    "comforted": "comforted, eyes softly closed, a gentle relieved smile, shoulders relaxing",
    "giggling": "giggling, eyes squeezed into happy arcs, a hand over the mouth, shoulders shaking lightly",
    "coughing": "coughing, eyes squeezed shut, a fist raised to the mouth, body jolting forward",
    "childlike whining": "whining like a child, eyes squeezed shut, mouth wide in a wobbly wail, cheeks puffed",
    "sad": "sad, eyebrows tilted up, eyes glossy and downcast, a small trembling frown",
    "depressed": "depressed, a hollow empty stare, dark heavy eyelids, head hanging low, no smile at all",
    "crying with eyes closed": "crying with eyes squeezed shut, tears streaming down the cheeks, mouth trembling",
    "crying with eyes open": "crying with eyes open and glossy, tears spilling down the cheeks, eyebrows tilted up",
}

CLIPS = [
    ["smile", "happy smile", "joyful", "laughing"],
    ["smirk", "smug", "proud", "evil smile"],
    ["seductive smile", "lovestruck", "aroused", "full-face blush"],
    ["blushing shyly", "looking away shyly", "fidgeting shyly", "embarrassed"],
    ["flustered", "nervous smile", "nervous pout", "nervous"],
    ["forced smile", "guilty", "worried", "scared"],
    ["surprised", "shocked", "confused", "dazed"],
    ["curious", "thinking", "serious", "indifferent"],
    ["bored", "sleepy", "annoyed", "contemptuous"],
    ["disgusted", "angry", "disappointed", "pout"],
    ["comforted", "giggling", "coughing", "childlike whining"],
    ["sad", "depressed", "crying with eyes closed", "crying with eyes open"],
]

# Your numbering from the request, so output files sort the way you listed them.
ORDER = [
    "annoyed", "aroused", "blushing shyly", "bored", "confused", "contemptuous", "curious", "angry",
    "fidgeting shyly", "crying with eyes closed", "dazed", "crying with eyes open", "depressed", "disappointed",
    "disgusted", "embarrassed", "coughing", "flustered", "forced smile", "full-face blush", "giggling", "guilty",
    "happy smile", "indifferent", "joyful", "laughing", "looking away shyly", "lovestruck", "nervous pout",
    "nervous smile", "nervous", "pout", "proud", "sad", "scared", "seductive smile", "serious", "shocked",
    "sleepy", "smile", "smirk", "smug", "surprised", "thinking", "worried", "evil smile", "comforted",
    "childlike whining",
]
assert sorted(ORDER) == sorted(sum(CLIPS, [])) == sorted(CUES), "plan out of sync"

CHARACTER = (
    "the character shown in <Picture 1>, appearing exactly as in <Picture 1> in the same chest-up framing, "
    "preserving the messy, shaggy platinum-white hair with long bangs falling over the eyes, the bright blue eyes, "
    "the warm brown skin, the cream-white robe with a V-shaped collar edged in gold, the thin gold necklace with "
    "a small bar pendant, and the royal-blue scarf wrapped loosely around the shoulders"
)


def prompt_for(clip: list[str]) -> str:
    beats = []
    for (start, end), name in zip(WINDOWS, clip):
        beats.append(f"At {start:.1f} seconds the face changes quickly to {CUES[name]}, "
                     f"and holds that expression very still until {end:.1f} seconds.")
    return (
        "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\n"
        "integrated_multimodal_description: [Shot 1] Anime illustration style, crisp black ink line art with fine "
        "hatching and clean cel shading, on a plain pure-white background. "
        f"The video shows {CHARACTER}. From 0.0 to {NEUTRAL_END:.1f} seconds the character keeps the calm, faint "
        "smile from <Picture 1>. " + " ".join(beats) + " Each change of expression happens in a brief moment and "
        "is then held clearly, like a sequence of character portraits; the head and shoulders stay in the same "
        "place and only the face and small natural movements change. The camera stays completely static "
        "throughout, keeping the same chest-up framing as <Picture 1>, and the plain background stays constant "
        "and empty. No other characters, objects or scenery appear, and there are no cuts. No visual effects, "
        "overlays, particles, motion blur, speed lines, comic symbols, text or floating symbols.\n\n"
        "overall_soundscape: Silence throughout. No dialogue, vocals, ambience or sound effects.\n\n"
        "non_diegetic_music: N/A"
    )
