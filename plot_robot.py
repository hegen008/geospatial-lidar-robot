import pandas as pd
from matplotlib import pyplot as plt

file = "data/lidar_record_0.csv"

data = pd.read_csv(file)

plt.scatter(data['robot_x'], data['robot_y'])
plt.savefig('robot1.png')


