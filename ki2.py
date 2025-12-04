from scipy.stats import chi2

def p_value_chi2(x2calc, ddl):
    """
    Calcule la p-value pour un test du χ².
    
    Paramètres :
    chi2_stat (float) : valeur de la statistique χ² observée
    ddl (int) : degrés de liberté
    
    Retour :
    float : p-value associée
    """
    return 1 - chi2.cdf(x2calc, ddl)

# Exemple d'utilisation :
#x2calc = 67.7  # ta statistique observée
#ddl = 63             # degrés de liberté
#print("p-value :", p_value_chi2(x2calc, ddl))

def test_khi2(ddl, obs, theo):
    x2calc = 0
    for i in range(len(obs)):
        x2calc += (obs[i]-theo[i])**2/(theo[i])
    x2crit = chi2.ppf(0.95, ddl)
    return x2calc < x2crit




