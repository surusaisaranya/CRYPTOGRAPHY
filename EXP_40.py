# q40_mono_top10.py
# Lightweight wrapper around heuristic solver (similar to Q37), returning top-10.

from q37_monoattack_topN import top_n  # if saved as module; otherwise copy Q37 into same file

if __name__ == "__main__":
    ct = input("Enter monoalphabetic ciphertext:\n")
    results = top_n(ct, n=10)
    print("Top candidates:")
    for sc,pt in results:
        print("Score:", sc, "->", pt)
    print("\nIf q37_monoattack_topN was not saved, copy its code into the same file or run it directly.")
