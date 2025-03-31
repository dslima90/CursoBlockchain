



# prime_candidates = [n for n in range(3, 10000, 2) if fermat(n)]

# print (prime_candidates)

    
primes_save = [2]

fake_primes = []

miller_rabin_prime = [2]

# fórmula de fermat
fermat = lambda n: (2**(n-1) % n) == 1

factors = lambda n: [p for p in primes_save if n % p == 0]

def muller_rabin_k(n, max_try=100000):
    # reescreve em n - 1 = 2**k m em que m é impar
    n_par = n-1 
    for k in range(max_try):
        m_candidate = n_par // (2**k)
        if (m_candidate% 2) == 1: # m é impar
            return k, int(m_candidate)
    
def miller_rabin(n):
    
    k, m = muller_rabin_k(n)
    
    a = n//2 # deveria ser random, vamos pegar alguma coisa no centro do range
    
    
    if (a**m) % n == 1:
        return True

    if any([a**((2**i)*m) % n == n-1 for i in range(k)]):
        return True
    
    return False



def find_primes(max):
    
    for n in range(3, max, 2):
        
        if miller_rabin(n):
            miller_rabin_prime.append(n)
            
        # verifica fermat
        if not fermat(n):
            continue # não é primo
        
        # se passar em fermat verifica na lista de primos conhecidos se tem algum fator

        if len(factors(n)) > 0:
            fake_primes.append(n)
            continue # tem fator
            
        # salva se for primo
        primes_save.append(n)
        

    return primes_save, fake_primes


real_primes, fake_primes = find_primes(100000)

fps_miller = [fp for fp in miller_rabin_prime if not (fp in real_primes)]

print(len(real_primes), len(fake_primes), len(fps_miller))

for fp in fps_miller:
    print (fp, factors(fp))
    

