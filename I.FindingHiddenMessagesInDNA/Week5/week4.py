
# coding: utf-8

# In[100]:


import numpy as np
import random


# In[101]:


NB_RUNS = 1000
PSEUDO_COUNT = True
# EPSILON = 10 ** -2

BASES = {'A': 0, 'C': 1, 'G': 2, 'T': 3}


# In[102]:


def form_profile(motifs):
    if PSEUDO_COUNT:
        counts = np.ones((4, len(motifs[0])))
    else:
        counts = np.zeros((4, len(motifs[0])))
    for line in motifs:
        for j, base in enumerate(line):
            counts[BASES[base]][j] += 1
    freqs = counts / counts.sum(axis=0, keepdims=True)
    return freqs.tolist()


# In[103]:


def profile_most_probable_kmer(text, k, profile):
    probabilities = dict()
    for i in range(len(text) - k + 1):
        kmer = text[i:i+k]
        if kmer not in probabilities.keys():
            probability = 1
            for j, base in enumerate(kmer):
                probability *= float(profile[BASES[base]][j])
            probabilities[kmer] = probability
    most_probable, _ = max(probabilities.items(), key=lambda x:x[1])
    return most_probable


# In[121]:


def form_motifs(profile, dna, t):
    k = len(profile[0])
    return [profile_most_probable_kmer(chunk, k, profile) for chunk in dna]        


# In[105]:


def score_motifs(motifs):
    n = len(motifs[0])
    counts = np.zeros((4, n))
    for line in motifs:
        for j, base in enumerate(line):
            counts[BASES[base]][j] += 1
    score = sum(len(motifs) - counts.max(axis=0))
    return score


# In[106]:


def random_motifs(dna, k, seed=-1):
    if seed >= 0:
        random.seed(seed)
    n = len(dna[0])
    motifs = list()
    for chunk in dna:
        i = random.choice(range(n - k + 1))
        motifs.append(chunk[i:i+k])
    return motifs


# In[107]:


def single_randomized_motif_search(dna, k, t, seed):
    best_motifs = random_motifs(dna, k, seed)
    best_score = score_motifs(best_motifs)
    
    motifs = best_motifs
    while True:
        profile = form_profile(motifs)
        motifs = form_motifs(profile, dna, t)
        score = score_motifs(motifs)
        if score < best_score:
            best_motifs = motifs
            best_score = score
        else: 
            return best_score, best_motifs


# In[108]:


def randomized_motif_search(dna, k, t, n=NB_RUNS):
    scores = list()
    motif_sets = list()
    for i in range(n):
        score, motifs = single_randomized_motif_search(dna, k, t, i)
        scores.append(score)
        motif_sets.append(motifs)
    return motif_sets[np.argmin(scores)]


# In[10]:


k = 8
t = 5
dna = [
    'CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA',
    'GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG',
    'TAGTACCGAGACCGAAAGAAGTATACAGGCGT',
    'TAGATCAAGTTTCAGGTGCACGTCGGTGAACC',
    'AATCCACCAGCTCCACGTGCAATGTTGGCCTA',
]
sample_in = (dna, k, t)
sample_out = [
    'TCTCGGGG',
    'CCAAGGTG',
    'TACAGGCG',
    'TTCAGGTG',
    'TCCACGTG',
]


# In[11]:


assert randomized_motif_search(*sample_in) == sample_out


#     RandomizedMotifSearch(Dna, k, t)
#         randomly select k-mers Motifs = (Motif1, …, Motift) in each string from Dna
#         BestMotifs ← Motifs
#         while forever
#             Profile ← Profile(Motifs)
#             Motifs ← Motifs(Profile, Dna)
#             if Score(Motifs) < Score(BestMotifs)
#                 BestMotifs ← Motifs
#             else
#                 return BestMotifs

# In[12]:


k = 15
t = 20
dna_ = """
ATACGCGGTGCTAGCTGGGCGAGAGGATCACCCATAGAGCTTTTTCACGGGAGGTCCCGCAGTACGGTAGCCATAATCCTCTGAGTCTCGAGCGCAACATTCAGGGCTATTTTACAGTCGATTCCTATGTCCTGTTTGCTCGCCCGTCGCATGTAATGCGGGAATACGCGGTGCTAGC
TGCATAAGGATACGCGAGGCGAGAGGATCACCCATAGAGCTTTTTCACGGGAGGTCCCGCAGTACGGTAGCCATAATCCTCTGAGTCTCGAGCGCAACATTCAGGGCTATTTTACAGTCGATTCCTATGTCCTGTTTGCTCGCCCGTCGCATGTAATGCGGGAATACGCGGTGCTAGC
AATTAGGCCTGTGGTCGTGTTTGCAGAACCCGCTCATCGAAGCACTGTGGACATAGACTCGTGGGCTACGGCCAGACCGAAGGCCGATCGACGGAATCAGGCGGCTTCTGACACCGAAGTAATGCTCGTCAGTCATCCGCAGTGACGACTTAAGCATCGCGATAATTGAGATCACATG
TAGGGACATTGTGCCTAATCACGGCTGTAGAACATCCTCCGCCCACAATCTAGCGTGCGTGGCGGTTATGTAAACCTTCTGGTGCGAGAGGGGATGATACCTGATTAGCAGGCAGACGAACCGGGTTGTCTGGCATTAATCATCATACAGATACGCGATTCGCAAAGTCGGCCCCTGC
TGGTTGCTCCCGTACTTGTGCGGAGGAATAGCACGTGGGAGTCTTCTGGGTTCGAGTGGAGTTCATCATCGCTCAACGCGACCTACGACCTTTAGAGTGACCGCCCGATAGGGACAGCGCTCCCCAACATTCTGTGCGTCCGTAGGGCTTTGGTGTGTTCAATACTAATAACGCTATG
CTCCGATCGAAGAGCACGCTTTCAAGTCGTAACTCGAACAATCATGACTGCTCATCGCGCGGCGCGAGACGTCTGCAGTGTTCTTACTGTGGCTTTACAGTGCACCCGTGCGTATCACTGAAGAGCATAAGCGACTCACACTATAAACCAACCCGGTAGCTTGATCATAGATCGAACG
CTTGGGACAATGTGCACGTTGCTCATAATCCCATCGGAGTACGCGACGTTGTACGCCTCACAGAAAGTATAAGTTAGAGCGCGGTTCCTGTAGTAGCGCGAAGCGGCTCGCTATCACTCGGAGCCGGCACAGGGCTTTGACCCGCGTAGAGAGGACGACGCTTGGATCTTTAGTTTAC
AATGCCCCACTTTGTCAAGCGCTGGAAGCGCGCGATACGCGAGCCTCTAATGCATGGTAGCCGCAATCAATGTAAGGGAATATGAAGAGAAAGTATGTGTGTTATCGATCTAACTGAGAGCAAGTCTCTCAAGTGTGGTAGCCGGTTTCGCCTGCTAGGTCATGCGCTTCCTGAGGTG
TCATCCTCACGAATGCAGGTAATCGAAATTACGGGTCTGTGATGCACGTCACGCTTTCACAAAAATGATTATCTGCTGGTGTTCCAATTGAGGGTTAAAATCCGTAAAATTGTCACTGGAATTAATTTAGCTAGCCTGCCGATCCGGGGGTAACATCGGATTACGCGAGACCGCTGAG
TGATGATTCGTAAGGGCTCTGAGCGTGCGTAATGCGTTCAAAAAGGCACTGACCGCTTATTAGGGTAAACCCTTTTTGTATCGGATATGTATGCCGGGAGTGAACGCGCCGACATCTTCACCTTAACTGTGGACTTTCTGGAGCTGCTCATCGCGATCTACGACCGGTTGCTTATCGG
CCTACATGTTCTTAAGCATCCACATACGCGACCAGTGTTATAAGCCCTGCACGAAGCCAAGCAATCGATAGCATTAACTCGTACCGCGCCTATCGAGCTCAACGACGGGAGCGTAGGGCCTAACCCACATCAGTTTTGTTATCCGGTAAATGGTAAGTAGCTCAGCCCTAGCAGAAAT
CATGAAAATAGATCTCGATTAACCTGTAATGTCATTCCTACGTCATGGGGGGAATTATACGGCTGGATCATCCTGACATTACCTGGTACGCTACTCGGCGGGCGAGCCGACGAGCGACATGGTGAAATAGCTCGCGATACGCGTATTTAAACAATGATTGGCTCCAGCGCTAGTGTTG
TATGACATCTTCATACGCGATAGGGTTGCCTTTCACATTGCGGATCTAAACCGGTAACTTGCAGGTGATGACGCCGCATAAAGTCCACAACTCACTCTGTCTACCTTTCGGCTCTCCCAAGACTGGCTAGTGCGCGTCAAATCGGCACTCCCCAAACGCCCTCTGGTCGTTATTTAAA
CGACCATGTGAATTGCTGAGTTACTATACCGCGATCGCGATACGCCTCGCGCCGCGTAGTTGCAGGCAATCAATGACTCCTTACAACTATAGGCCCCGCTCTCCCGCGGCGTCTCTGAGTCGCTCTTTGCTGAGGAACGAGCCTTCGTGTAAAGTCCATTCTGTTCCTCACAAGACCA
TTGTCAGGCCACCGCAGATAAATAGCCGTGCGGAGACTCTCGTAGGCTCTTCCCTTGCTCGCGGAGAGATAGCAACTTATCTACATTTAAGAGGCTGAATACTTGCTGTCGCGTCTGTGATTTGCAACGCCACAACGATACGCGAGGGCGGGCCGAACTGGCATACGTTAACCAAGTG
CAGCTCTCACTCCCTGACAAGAAACGCTGCTAAGATGGAATACCGCGACTGAACGGAGTTTATGGTTTTACGCATTGGCCATCGCGATACCTAAGGCACAGGGCGCTTTGCCATGCAAAAGACAACGGTGGGAATCCGCACTAAAGGAGGAATGACCAACTTAAAAATTACAACCACG
AGATCTTAGGTCACCAGACCTAGCTTTACGTAATTGGTAGAACAAGCGCGTTTGGTCTGCACCTAGAGTTTGTCCCATCGCGATACGGAGCTATCGCCTCATAAATCCCACATCATGGATAATGGTAGAGTGAGGTAAGAGTAGATTTTCAAGGTCGCGTTTAGTTGCGAGTTTGAGT
AACTTCTGGTCTAGTTAGGTGACCGGATATCAGAGCAGCAACGCGTATCTACAACCCGCCAGAATGAAATGGATGGGAAGTGGGCATCGAGCACTGAATCTTACGCCTGTTCCTACAATGTAAATAGGGAATCTTCATGCGTTTCTGGGACATCGCGACGGGCGAAGTGCGTAGACTC
AGGAACGCATGCGATTCTCTACCTGAAATTATGCAAAAATAACTGGCTTAATCAGGTCCGCATAGTTCGTCTCACAGACATCGCTTAACGCGAGGAAACTCCGCTAATCCATAGGGTGGACACTTCAAAAACGGGAAAGAATCGCCATTAAAACAAGTAACACTTGGGTGGTTCTAAA
AATCCTCAAGGTCCCACCACCGGTGTTATATACAGCGAATGTAATGACCGGCTGCATGGGCAAACTACTTTTTGATACTCTGCTACTAGCCAGCCCTCTGAGCTGAGTGGGGTGTCCGTGCGATACGCGATGGCCCTTAATCAGGGCTCGCCCTGCGCTTGCGCGGCCCAGTTATTCT
"""
dna = [line for line in dna_.split('\n') if line]


# In[13]:


# result = randomized_motif_search(dna, k, t)


# In[14]:


# print('\n'.join(result))


# ---

# In[15]:


def generate_random_profile_kmer(text, profile, k):
    weights = list()
    n = len(text) - k + 1
    for i in range(n):
        kmer = text[i:i+k]
        weight = np.product([profile[BASES[base]][j] for j, base in enumerate(kmer)])
        weights.append(weight)
    norm = sum(weights)
    probabilities = np.array(weights) / norm # [w/norm for w in weights]
    z = np.random.choice(n, p=probabilities)
    motif = text[z:z+k]
    return motif


# In[80]:


def gibbs_sampler(dna, k, t, n):
    best_motifs = randomized_motif_search(dna, k, t, n//5)
    best_score = score_motifs(best_motifs)
    
    motifs = best_motifs
    for _ in range(n):
        i = random.randint(0, t-1)
        old_motif = motifs.pop(i)
        profile = form_profile(motifs)
        motif_i = generate_random_profile_kmer(old_motif, profile, k)
        motifs.insert(i, motif_i)
        score = score_motifs(motifs)
        if score < best_score:
            best_motifs = motifs
            best_score = score
        else:
            # print('Best score: ', best_score)
            return best_motifs


#     GibbsSampler(Dna, k, t, N)
#         randomly select k-mers Motifs = (Motif1, …, Motift) in each string from Dna
#         BestMotifs ← Motifs
#         for j ← 1 to N
#             i ← Random(t)
#             Profile ← profile matrix constructed from all strings in Motifs except for Motifi
#             Motifi ← Profile-randomly generated k-mer in the i-th sequence
#             if Score(Motifs) < Score(BestMotifs)
#                 BestMotifs ← Motifs
#         return BestMotifs

# In[81]:


k = 8 
t = 5 
n = 100
dna = [
    'CGCCCCTCTCGGGGGTGTTCAGTAACCGGCCA',
    'GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG',
    'TAGTACCGAGACCGAAAGAAGTATACAGGCGT',
    'TAGATCAAGTTTCAGGTGCACGTCGGTGAACC',
    'AATCCACCAGCTCCACGTGCAATGTTGGCCTA',
]

sample_in = (dna, k, t, n)
sample_out = ['TCTCGGGG', 'CCAAGGTG', 'TACAGGCG', 'TTCAGGTG', 'TCCACGTG']


# In[82]:


gibbs_sampler(*sample_in) == sample_out


# In[83]:


k = 15
t = 20
n = 2000
dna_ = """
TCTGAGTCACACATGGTCACTGAGCTGATCGGAACCTCTGCGGATTTTTGCCTGCGTGTTTTTAGCGCCCATGATATTGTATCCTTCAACAACTCAACTCCCCAGAAGACAGTTATTGTTACGCTACGAATATAGTGCGCAGGGAATGGTAAATGGTATTCCTACGCGAATGAGTCGGACGCTGCGTACAATAATACTCTGCCACCTTTTCAACATCTAACCACACTAGAAGTCGCCAACGGGAGTACTATCACCCAAGCGCATTACTGCGTGCTTCCAAATTGATGTTTACTACGTTTGGCCCCAAGATCTATTCTGAGTCACACATG
GTCACTGAGCTGATCGGAACCTCTGCGGATTTTTGCCTGCGTGTTTTTAGCGCCCATGATATTGTATCCTTCAACAACTCAACTCCCCAGAAGACAGTTATTGTTACGCTACGAATATAGTGCGCAGGGAATGGTAAATGGTATTCCTACGCGAATGAGTCGGACGCTGCGTACAATAATACTCTGCCACCTTTTCAACATCTAACCACACTAGAAGTCGCCAACGGGAGTACTATCACCCAAGCGCATTACTGCGTGCTTCCAAATTGATGTTTACTACGTTTGGCCCCAAGATCTATCGCCTTTAGCGCAGATCTGAGTCACACATG
TATGGAAGTATGTATTTTAGCTGGGACAATTAGTGTTATGGACTCTATTAGGGCCTCCAACCGACGACTGTCGACCACGTAGTATCGCATGCGAAAGGATAACTAAAAGTTGATACCCACTCATTATTTCTAACTAGTGCCACGGTCTATCCCGCTGCGCACGAACGCTGCTTCTGCAGACTCTCATCACAGGATGCAGCTATAGATGTGATCCTAGCCGGACGGTATTGTACCGAGAGGTCAAGCGCGCTCCAGAGTCGCCGAAACAGCAATCTATGGCTCAATAAGTACGAAATCCCCATCGAGTACTGACGCAGACGACTGTGAGC
TTCCAAGGGGACCCGCACCTAAGAGAGGGGGGGGAACAGGCGGAAACTCAGAACTTAACCTGCGCCGTCACTCGGTGAGGTGGTGTGATCGCCCTAGAAAGTCCGCACCGACCCTCCGAGGATTACTCCTAAGAGAGAATCGAGCGCTCGGAAAGAGCACTCGCCGTTGCTCTCGCAACGGGTGCATTCTCAGATGAGCGGACTTTGCTTAGTCGCCATTAGCGCAGAGTCACTGTCTTAATCTGGTACATGCTTCGCTAAGGCCAACATTACCAGTCGCGTTTTCCCCACACGTAGAGCCGTCTGAACTTCGTCCCTGTGGAAGGATG
TTCCAAAGGCCCGACGATCGGCCAACGTTATCTAGTCATACTTTGCAAATTGGTTGGGAATCTTTTCCGGCTTGCTAAATGTTTTGCTTTAAAGTGTCTAGTCGAGTCCTTGTCATGAAGAAAAGTAATTTGGCCGTGAATGCTAGCGCAGATTGTCCGTTGAGTGCAACAAAAATGCTGTTCCATAAGCGGTCTTGGCCCAAACGAGGTCGGTCTTTACGCATAGCTGCATATTGGGTCTCTACGTTAAACCCCCTTGTGTGCACGCATTACAGTTAAACATTTGTGTGTTTCCCAGTCGGAAACGGTGGATTCGGGGAGGTAGTGGC
AAGTCCAGCGAACGCCTGTATGTCGGGTCACTTAGTGATAGCAAAGGTGCCTCCCACTTTCGCTTATAGTGATCTGCTAGCGCAGCTGCGGTCGTGCCGTCGATGCATACTGAACATTGCGTAGGTCGTGGGCACGTTGCCGGTGCGATGGCGATAGAGTGCACTCGTCCGAGCGATTGAATTTATCTCGGGAGACAAGGTTCACAGGCCCTGGTGAGTTCAATGCGTGTTAAGAGTCCAAAAATGAATGGGATCTCCATTCCCAATAATGGGAATGTCTCTGGCACGTCGAGGTCGGCTGGGTGATACAATGTTCTGAAGGTTGTCAG
TTACTTTAACTGTTGGGGAAGGTGGTCCGCCAGGACGGAAAAGAACCTATACCTGATCGCTAGCTATCCTTCGCGACCGTCGCTGGCTCTGCGACCGCCGCTTGTTACCTGCAAGGAATTGCACGGTCACGTAGCGAACTCGTATCTAACTTATCCCGCTGCACACGCAGATAGATGATGTTTAAAGTAGAGGTTACCAATCACGGCTGCGTTCTTTCGACCAGGATGTTCCGCCCAAGGACAAGTAAGAATGGTTTAGATAAGCAAGATCACTTACCCCACAAACCTTGTTGATTGTCCCGTTGGGCGCGTTTTTAGGCATCGTCTGG
GTTGATGACGGCGGAGACCAGTCCATACAGCTGCCGTGGCATGCTCGAAAGCCATACGGCGATCGCTGATCTAGCTGTACCACGGTCTTTACTCACATATGCCTTTGCTATTATAGTTTGCTCTAAGTTTCTTTCGTAAACTTACCACGCTTAGCTAATTGATTCTTACCCGAACCCCACGCTGGGTGAGCTGTACTTGGTATCCGCCGTTGTCACTCCGAAAACAATGACACTTGGGGATAGCATGTGGTCATATTTATGTGAGGGTTATGACCATCTCGTTCTTAGACGTGCCTGTATATTTCCGACAGTCGCTAGCAGCGCAGAGC
TTTCGCTGACACCCGAGATATAGTGGCAGGATTATTTGGGAATCTTGGTTAAGCTAGGAAACACCACGGCACGAGTAGCGGACCTTCCGGCCGTAGCTCCAGCTCTATAACCGTAATTGTGTAGTGATTGTCCAGATACCGCTGCCTCCGCAGAGACCAGCTCCATCAGGAAAAGCTCATGGCTCCGAGTCACTTGTAGAAAGACACCAGCAGGACCCAGAAATGGGCATTTTTTGATTGATAGCATTTCTAGTTGTCCTCTTATGTGACCCAGGAACTATGATGGTCCAGATCATCAACTATTGCCACGGAAGTTTTATTTGTAGGAA
TTGACCGCCGTGTTCAACTGGTCGAACAAATAACACAATAGATCTCATGGCCGCTGTCGATAAGCTCACGGCGAATATGGAAGGAAGGTGAAATGCGGGGAGTAAACGTCCAACTAAGTGGTGCACCCCGCGTCCCTAGCGCAGAGCAGTGTATTGGACAGGTAGGGCGCGTTCCGGAGCTTCGTCGTGGCCTGCCCCGATCGCTCATTGCGTCAGGGTCTCGCCCGGGGTAATCTCCGGTCGCGTTGGCGGGCTCAAATCACAACTTCTTTGCCACCACGCCGCAGGAGGCAGATGAGTGCAGTTCGAGCTTCTATGGTGCCCCAGTG
TTGTGGGATCCACCTTGTCATAGTGGCACCGCGTACAGGGCTATGATTCTGGGGACGGCGGGGAAATCCGGCGCGGCAGTCAGAGTGTCATCTCGACTGGACATGGATAGACTCTCATCGCACTCTCCTAGTCATTCCTCGGAGCAGTGTGCGTTTTCCAATAGAAGAGAACGACGCTGCTAGCGTCTACTTTTCGCTACGCCCATGAGACCACTCGCTTACTTGTTGCGTGATCAACTGATCGAGACAGTGATACGGCAAGAGCGCCGCCCCCGATTCTATGTCTTTCTGGCTTAGGTCTGGGCCGGCGCGGCTGCCCACGGCGAACC
AGAACCACCGCCTCAACTGATCATCTCCGCACGGGGCTGCTAGCGCAAGGGCGAATGCAGGCTTGAATACCGGGGATAATCTTAGTGTGGTATCCGGTACGCCCACTCTTGCGCCGTGCTGGCGGGCGGATAAGGGTAGTTTGAGCCGGAGCAACACGTCGCGGCCCTTTCAATTCATTCTGCTTGTAGGGTGTCCGGTGGTCGGTGTTACCCATATACGGCAGTATCCGGGTTAGCCGAGAAGATAAGGCATCTATAACTGTCTAGGTTGAGGTCACTCTGTATCCTTACCACGCCAACGTAATCTTGAGCTATTTCAGCGAAGCGAT
CCTGAGCTTCCTTGCACACGGTGGCCAGCACCCCTGGTTTAGAACTTACTAAATGTGAAGCTGTAATGATCGGGATTAGAATAAAGCTACTATGACACATGCCAACCGCCGCGTAGAAGCCAGGGACCGAGACGGTACCCTGTGAGGCCATCCGAGCTGTCGGAGTTAGGAGGTCCGAACGTTATTGCATCATGTGAAGAGGTTGGTGAGTCGCACGGTTTTCGCTGCTAGCAAGGAAGCGGTTGCTGCGACCATTCCCCTAGGGTTAATTCTGCAGGCACTTGTTCAAGTCTATCAGACGTACAAGAACGACCCTCTTCTGATAGTAC
GTTAAAGCCCGAGGGCGTCTGGCGAAGCAATAGGCACGCCAACTTAACGTCATGGACCACTTTTTTTACACATGTTAGTCCAGCAGTGCTCGCCTACTACTCCAGGTTTTCCTACGGCACTTTTGTGGACGAGGATTATTAGAGTGCATAATGCACTACGCTAGCGCAGACTGATCTCGCGATGGTGGGACGCGAGCAGCCTGATGATCATTCGTGCACTATCAGCACAATATGGCACTAAGGATTTTCTATTATGCCAACCCTCCATTCTATTGCCCCGCCTACGACTGCAAATCAATAATATCCGGATTATGCATCCTTATGGGCGC
GTTGATCGGACCGGTGTTGTCATTCATGATACCTGTTATGGTGCTGGCTTTACATGGTGAATTACATCTGTTGAGTGAAAGGCGGTGCCGCTTGCAGCGCAGATTTCACAGAATACGTGAGAAGCACGGGACGGGAGCGAGACCGTCAGAGGTGGTAGCAAGTTCAGTCAGCACCCTAAAGCCCCGTAGAGTAGAAATCTCGAATGTCTAGACCTTTTCGCCACCTGGTGCGGGCGTGTGTGCAGCTAAGAGCCAAAAGCCATCTCCTTTAAATTTTTGCTGCATTTGCACAATCACCGGTTTTTCTCATCCTTGCGAGGCAATTTTGC
CACTATAACGGGTCGGAATGGGCGCCTAACACGCAAAGAGGTCGGCTTTCCAGTAGGAGTACCAACAAGACTTCCGAGTGGGAATAACCCTGATATACCTTACTGGGGAGACCTGTTCCGGCCACGGCATACGCTGCTACTTCAGATGGCTTGGTAGAAGCCTACTTATAGTGGCGTTTTCCCGCATGGAGAATCGGTTAATGCCCTGAGCTCTATCACCTGCTAGTCTGCCTCATCCTACCCGATTCTAGCTACAAAAGGGACTTGTCAAGTGTAGAATGTTTGGTTGCGGACGCGAACTGAGAACAGACCAGAGTAACCGGAGCATA
GTGGCGAGCAATTACCGCGGACAGCAAAGGGAGGGAGTCTCAGGCATCTAAAAGGTCGTGATGTCGTCCGACGTCCGATAGACATACATTTACCTTCATGTTAGATGGACGATCCGCAGCCGTTTCCCCCTCGCCGCAAGACGTGACGGCTTGTCCAGCATCGTGGCCGCAACACTTGATTAGGACGTGCAAAGCGGGGGCCGCGGTTATAAGTCATATAGAAAAACCCGTAAAATTAAATGACATTTTCCGATGTCATTCTTCCGCGTGCCCCCCGGCAGGTACTACTTCGCTGCTAGCGCCAGCTTATCTTCATAGAGATTATGTTT
TAAAGATGAAGTGGAAGTTTGAAAGCCTAATATACTGGACGCTAGTAATCTCCCGCGGTATTACCTGCGGACGAGTTCTCCGGGCTGGTCATTACGCTGGTTAGGAGTAGCGGAGGACAATTCGGCTAATGAAACCGTTAATACAAGGCTCGAGTCTTAGAAACGCGGAGGATTTGTAGACCGGCTGTTGTGATATGAGCGCACATCCCTGTCGAATTACAGTCCCAAAGTAACATGATATATGACTGGTATGCTATCTCGCGCTCAATTCGCTGGGGGCGCAGAGCTTCCTGCGTTAACAACATGGGTGCTGCACACCGCACTTCTTC
GACAATATATAGAATAGTCCAACGGAGCCGAAGAACTGTCGGGTCGTGCCCTCCGCTGGATATATGTGTTGCGTAGGTTAGGGAGTCGCTGTGTGCGCAGAGACGAGGAGTAGCGCTCGTTATTTGGCAGTGGCGTATTCAATGTTTAGAGTTTACAGGTGGGAACTAAAGAATATCATTTGATTTGCGACCCGCTCACGAACGTAAGTTCCTATCCTAATTGATGTTTCACTGGATTTTCGAATTATACCACCACTCTGAGCTGCCGGGCTCGAGTGACATATAGATGCTTTCTAGTGCCGCCGGGAGGACGTGAAAGCCGAGCACGC
GAGACAGACTCTTGTACCCGAAGTACGTAAGAGGCTCGTCTCCCGCGCGACTAAGCACCGCACAACTATTGTTACGGGCGCGTCTGAGTGGGATCGGCAGGTAATAGTGTCCCACACGAGACTAGTGACCGGTGTACGCTGCTAGGATAGACAAACCAAGGTTTAGAACAAATGTTGAGGATTAAGTGTAGCACCCCACTAACCATTAACCATTGCCCCTTCTTGAACGCGGTTCTGGGGATTGAATGCCCTCAATGCAGAACTAGGTGCTATCGATTGGCAATCACATTCGCTTAGGACGAGCTCTGCCCTGACCTCCTTGCTCGAAG
"""
dna = [line for line in dna_.split('\n') if line]


# In[84]:


result = gibbs_sampler(dna, k, t, n)


# In[85]:


print('\n'.join(result))


# ---
# ### Quiz

# In[127]:


dna = [
    'AAGCCAAA',
    'AATCCTGG',
    'GCTACTTG',
    'ATGTTTTG',
]
start_motifs = ['CCA', 'CCT', 'CTT', 'TTG']
profile = form_profile(start_motifs)
next_motifs = form_motifs(profile, dna, 4)
print(' '.join(next_motifs))

