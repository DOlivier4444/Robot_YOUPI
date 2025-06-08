import time

# Exemple avec 10 conditions simples
def test_conditions():
    for _ in range(1000000):  # Un million d'itérations
        if False:
            pass
        elif False:
            pass
        elif False:
            pass
        elif False:
            pass
        elif False:
            pass
        elif False:
            pass
        elif False:
            pass
        elif False:
            pass
        elif False:
            pass
        elif True:
            pass

start_time = time.time()
test_conditions()
end_time = time.time()

print(f"Temps écoulé avec 10 conditions: {end_time - start_time} secondes")

