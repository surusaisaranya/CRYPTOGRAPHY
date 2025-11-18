# q16_mono_freq_attack.py
import random
import re
from collections import Counter

ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
EN_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
COMMON_WORDS = {"THE","AND","THAT","HAVE","FOR","NOT","WITH","YOU","THIS","BUT","ARE","FROM"}

def apply_mapping(text, mapping):
    res = []
    for ch in text.upper():
        if ch.isalpha():
            res.append(mapping.get(ch, '?'))
        else:
            res.append(ch)
    return ''.join(res)

def score_plaintext(txt):
    words = re.findall(r"[A-Z]+", txt)
    if not words:
        return 0
    # score: count common words occurrences + proportion of alphabetic characters
    common = sum(1 for w in words if w in COMMON_WORDS)
    alpha_ratio = sum(c.isalpha() for c in txt) / (len(txt)+1)
    return common * 100 + alpha_ratio * 10

def initial_mapping_by_freq(ciphertext):
    letters = [c for c in ciphertext.upper() if c.isalpha()]
    freq = Counter(letters)
    most_common = [p for p,_ in freq.most_common()]
    mapping = {}
    for i,ch in enumerate(most_common):
        if i < len(EN_FREQ_ORDER):
            mapping[ch] = EN_FREQ_ORDER[i]
    return mapping

def random_complete_mapping(seed_map):
    # fill unmapped letters randomly
    mapped_values = set(seed_map.values())
    remaining_vals = [c for c in ALPH if c not in mapped_values]
    remaining_keys = [c for c in ALPH if c not in seed_map]
    random.shuffle(remaining_vals)
    mapping = dict(seed_map)
    for k,v in zip(remaining_keys, remaining_vals):
        mapping[k] = v
    return mapping

def improve_mapping_hillclimb(cipher, mapping, iterations=2000):
    best_map = dict(mapping)
    best_score = score_plaintext(apply_mapping(cipher, best_map))
    letters = list(ALPH)
    for _ in range(iterations):
        # propose swap in mapping values
        a,b = random.sample(letters,2)
        # find keys with values a and b (inverse mapping)
        inv = {v:k for k,v in best_map.items()}
        ka, kb = inv[a], inv[b]
        # swap values
        cand = dict(best_map)
        cand[ka], cand[kb] = cand[kb], cand[ka]
        sc = score_plaintext(apply_mapping(cipher, cand))
        if sc > best_score or random.random() < 0.001:
            best_score = sc
            best_map = cand
    return best_map, best_score

def top_n_candidates(ciphertext, n=5):
    seed = initial_mapping_by_freq(ciphertext)
    candidates = []
    # generate several different hillclimbs from different random completions
    for _ in range(n*2):
        start = random_complete_mapping(seed)
        m,sc = improve_mapping_hillclimb(ciphertext, start, iterations=2500)
        pt = apply_mapping(ciphertext, m)
        candidates.append((sc, pt, m))
    # deduplicate by plaintext text and sort
    seen = {}
    for sc,pt,m in candidates:
        if pt not in seen or sc > seen[pt][0]:
            seen[pt] = (sc, m)
    out = sorted([(sc,pt) for pt,(sc,_) in seen.items()], reverse=True)[:n]
    return out

if __name__ == "__main__":
    ct = input("Enter monoalphabetic ciphertext:\n")
    top = top_n_candidates(ct, n=10)
    print("\nTop candidate plaintexts:")
    for sc,pt in top:
        print(f"score={sc:.1f}: {pt}")
    print("\nNote: This is a heuristic solver — results may require manual refinement.")
