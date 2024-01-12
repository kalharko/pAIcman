import matplotlib.pyplot as plt
import pickle

data = pickle.load(open('data/genetic/log_rewards.pkl', 'rb'))

# plot data
plt.plot(data)
plt.xlabel('iteration')
plt.ylabel('reward value')
plt.title('reward Plot')
plt.show()
