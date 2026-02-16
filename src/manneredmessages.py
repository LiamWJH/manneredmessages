import keyboard as kb
import yaml, random

with open("config.yaml", "r") as f:
    data = yaml.safe_load(f)

messages = data["messages"]
schizomsg = data["schizowords"]

seed_N = data["auto-complete-start"]
profanityinclude = data["profanity-include"]
schizopercent = data["schizophrenia%"]
drunkmode = data["drunkmode"]

keywords = ["fuck", "shit"]

NEIGHBORS = {
    "q": ["w", "a"], "w": ["q", "e", "a", "s"], "e": ["w", "r", "s", "d"],
    "r": ["e", "t", "d", "f"], "t": ["r", "y", "f", "g"], "y": ["t", "u", "g", "h"],
    "u": ["y", "i", "h", "j"], "i": ["u", "o", "j", "k"], "o": ["i", "p", "k", "l"],
    "p": ["o", "l"],
    "a": ["q", "w", "s", "z"], "s": ["a", "w", "e", "d", "z", "x"], "d": ["s", "e", "r", "f", "x", "c"],
    "f": ["d", "r", "t", "g", "c", "v"], "g": ["f", "t", "y", "h", "v", "b"], "h": ["g", "y", "u", "j", "b", "n"],
    "j": ["h", "u", "i", "k", "n", "m"], "k": ["j", "i", "o", "l", "m"], "l": ["k", "o", "p"],
    "z": ["a", "s", "x"], "x": ["z", "s", "d", "c"], "c": ["x", "d", "f", "v"],
    "v": ["c", "f", "g", "b"], "b": ["v", "g", "h", "n"], "n": ["b", "h", "j", "m"], "m": ["n", "j", "k"]
}

def get_neighbor_key(k: str) -> str:
    k = k.lower()
    return random.choice(NEIGHBORS.get(k, [k]))

sentence_cache = ""
print("good luck mortal")

def on_key(event):
    global sentence_cache

    if event.event_type != "down":
        return

    key = event.name

    if key == "enter":
        kb.press_and_release("enter")
        return
    if key == "backspace":
        kb.press_and_release("backspace")
        return


    if key != "space" and (len(key) > 1):
        return

    if random.randint(1, 100) <= schizopercent:
        kb.press_and_release("ctrl+a")
        kb.press_and_release("backspace")

        if random.randint(1, 2) == 1:
            kb.write(random.choice(schizomsg))
            kb.press_and_release("enter")
            sentence_cache = ""
            return

        out = " " if key == "space" else key
        if drunkmode and len(out) == 1 and out.isalpha():
            out = get_neighbor_key(out)

        kb.write(out)
        sentence_cache = ""
        return

    out = " " if key == "space" else key
    if drunkmode and len(out) == 1 and out.isalpha() and random.randint(1,6) == 1:
        out = get_neighbor_key(out)

    kb.write(out)

    sentence_cache += out

    sentence_candidate = []
    for sentence_item in messages:
        if len(sentence_cache.strip().split()) < seed_N:
            return

        sentence_candidate = [
            s for s in messages
            if s.lower().startswith(sentence_cache.lower())
        ]


    if not sentence_candidate:
        return

    sentence_candidate.sort(key=len, reverse=True)
    pick = random.choice(sentence_candidate)

    if not profanityinclude and any(k in pick.lower() for k in keywords):
        pick2 = random.choice(sentence_candidate)
        if not any(k in pick2.lower() for k in keywords):
            pick = pick2
        else:
            pick = pick2

    kb.write(pick[len(sentence_cache):])
    kb.press_and_release("enter")
    sentence_cache = ""

kb.hook(on_key, suppress=True)
kb.wait()
