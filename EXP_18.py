# q18_des_subkey_bit_origin.py
PC1 = [57,49,41,33,25,17,9,
       1,58,50,42,34,26,18,
       10,2,59,51,43,35,27,
       19,11,3,60,52,44,36,
       63,55,47,39,31,23,15,
       7,62,54,46,38,30,22,
       14,6,61,53,45,37,29,
       21,13,5,28,20,12,4]

PC2 = [14,17,11,24,1,5,
       3,28,15,6,21,10,
       23,19,12,4,26,8,
       16,7,27,20,13,2,
       41,52,31,37,47,55,
       30,40,51,45,33,48,
       44,49,39,56,34,53,
       46,42,50,36,29,32]

SHIFTS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

def build_pc1_inverse():
    # produce mapping: position in 56-bit -> original 1..64 index
    return PC1[:]  # values are original bit indices

def generate_bit_origin_map():
    # Build initial C and D indices (based on PC1)
    pc1 = build_pc1_inverse()
    C_init = pc1[:28]  # these originate from these original positions
    D_init = pc1[28:]
    origins_per_round = []
    C = C_init[:]
    D = D_init[:]
    for sh in SHIFTS:
        C = C[sh:] + C[:sh]
        D = D[sh:] + D[:sh]
        CD = C + D
        # PC2 picks 48 positions from CD (indices are 1..56 referencing CD)
        # Map each of PC2 entries (1..56) to original bit position
        selected = [CD[i-1] for i in PC2]
        origins_per_round.append(selected)
    return origins_per_round

if __name__ == "__main__":
    origins = generate_bit_origin_map()
    for r,sel in enumerate(origins, start=1):
        first24 = sel[:24]
        second24 = sel[24:]
        print(f"Round {r}:")
        print(" First 24 subkey bits come from original positions (examples):", first24[:6], "...")
        print(" Second 24 subkey bits come from original positions (examples):", second24[:6], "...")
        # Check whether first24 subset intersects second24
        inter = set(first24).intersection(set(second24))
        print(" Intersection size between first24 and second24:", len(inter))
        print("-"*60)
    print("\nObservation: For each round, the first 24 bits are selected from some original subset (mostly C part) and the second 24 from the other (mostly D part). Their intersection is zero (disjoint).")
