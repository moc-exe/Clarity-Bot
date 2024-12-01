global_emote_dict= {

    "zerotsu_yumyum" : 1312653697838219389,
    "zerotsu_smirk":1312653686782038077,
    "zerotsu_sadge":1312653671737327656,
    "zerotsu_poggers":1312653660517568542,
    "a:zerotsu_pffff_an":131265363893354503,
    "a:zerotsu_nodnod":1312653613385908324,
    "axolotl_wow":1312669299852312596

}

def get_emote_keys():
    out = ""
    for elem in list(global_emote_dict.keys()):    
        out += f"{elem}\n"

    return out
        