import pandas as pd
from matplotlib import pyplot as plt

file = "data/imu_integration.csv"

data = pd.read_csv(file)

plt.scatter(data['px'], data['py'])
plt.savefig('robot1.png')


