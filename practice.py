import numpy as np 
from scipy.stats import norm

# Close form by martingale pricing method

def Close_form(S0, r, q, sigma, T, k1, k2, k3, k4):
  """
  """
  d11 = ((np.log(S0/k1) + (r-q-(sigma**2)/2)*T))/(sigma*(T**0.5))
  d12 = ((np.log(S0/k2) + (r-q-(sigma**2)/2)*T))/(sigma*(T**0.5))
  d13 = ((np.log(S0/k3) + (r-q-(sigma**2)/2)*T))/(sigma*(T**0.5))
  d14 = ((np.log(S0/k4) + (r-q-(sigma**2)/2)*T))/(sigma*(T**0.5))

  d21 = ((np.log(S0/k1) + (r-q+(sigma**2)/2)*T))/(sigma*(T**0.5))
  d22 = ((np.log(S0/k2) + (r-q+(sigma**2)/2)*T))/(sigma*(T**0.5))
  d23 = ((np.log(S0/k3) + (r-q+(sigma**2)/2)*T))/(sigma*(T**0.5))
  d24 = ((np.log(S0/k4) + (r-q+(sigma**2)/2)*T))/(sigma*(T**0.5))

  fn_1 = S0*np.exp((r-q)*T)*(norm.cdf(d21)-norm.cdf(d22))
  fn_2 = k1*(norm.cdf(d11)-norm.cdf(d12))
  fn_3 = (k2-k1)*(norm.cdf(d12)-norm.cdf(d13))
  fn_4 = (k2-k1)/(k4-k3)*S0*np.exp((r-q)*T)*(norm.cdf(d23)-norm.cdf(d24))
  fn_5 = (k2-k1)/(k4-k3)*k4*(norm.cdf(d13)-norm.cdf(d14))
  
  option_price = np.exp(-r*T)*(fn_1 - fn_2 + fn_3 - fn_4 + fn_5)
  
  print('The close form solution is:', round(option_price, 4))
  
  
  # Monte Carlo Simulation

def sampling(S0, r, q, sigma, T, k1, k2, k3, k4):
    '''
    '''
    mu = np.log(S0) + (r-q-sigma**2*0.5)*T
    std = sigma * (T**0.5)
    log_ST = np.random.normal(loc=mu, scale=std, size=10000)
    sample = np.exp(log_ST)
    
    sample[(sample<=k1) | (sample>=k4)] = 0
    sample[(sample>k1) & (sample<=k2)] = sample[(sample>k1) & (sample<=k2)]-k1
    sample[(sample>k2) & (sample<=k3)] = k2-k1
    sample[(sample>k3) & (sample<k4)] = (k2-k1)/(k4-k3) * (k4-sample[(sample>k3)&(sample<k4)])

    return np.mean(sample)

def MonteCarlo(S0, r, q, sigma, T, k1, k2, k3, k4):
    '''
    '''
    sample_mean = []
    for _ in range(20):
      sample_mean.append(sampling(S0, r, q, sigma, T, k1, k2, k3, k4))
    
    print('Sample mean:', round(np.mean(sample_mean)*np.exp(-r*T), 4))
    print('Upper Bound:', round(np.mean(sample_mean)*np.exp(-r*T) + 2*np.std(sample_mean)*np.exp(-r*T), 4))
    print('Lower Bound:', round(np.mean(sample_mean)*np.exp(-r*T) - 2*np.std(sample_mean)*np.exp(-r*T), 4))
    

S0, r, q, sigma, T, k1, k2, k3, k4 = 100, 0.05, 0.02, 0.5, 0.4, 90, 98, 102, 110
Close_form(S0, r, q, sigma, T, k1, k2, k3, k4)
MonteCarlo(S0, r, q, sigma, T, k1, k2, k3, k4)
"""
S0, r, q, sigma, T, k1, k2, k3, k4 = 100, 0.05, 0.02, 0.5, 0.4, 90, 98, 102, 104
Close_form(S0, r, q, sigma, T, k1, k2, k3, k4)
MonteCarlo(S0, r, q, sigma, T, k1, k2, k3, k4)
"""

