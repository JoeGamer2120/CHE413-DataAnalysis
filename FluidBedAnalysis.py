import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob


def main():
    ss_avg = get_ss_avg()
    # ss_avg, std = get_ss_avg()
    deltaP = p_drop(ss_avg)
    plot(deltaP)
    return

def get_path_list():
    file_list = {}
    
    for r in range(5, 50, 5):
        pattern = f'./Data/AREA900_Trial[0-9]_Reading{r}.csv'
        file_list[r] = glob.glob(pattern)
        
    return file_list

def ss_average(trial_data):
    ss_avg = np.zeros(len(trial_data))
    # ss_std = np.zeros(len(trial_data))
    
    for i in range(len(trial_data)):
        ss_avg[i] = np.average(trial_data[i])
        # ss_std[i] = np.std(trial_data[i])
        
    return ss_avg
    

def get_ss_avg():
    file_list = get_path_list()
    ss_avg = np.zeros((4, len(file_list)))
    counter = 0
    
    for r in range(5, 50, 5):
        file_path = file_list[r]
        # ss_values = np.zeros((len(file_path), 4))
        ss_values = np.zeros((4, len(file_path)))
        # std = np.zeros((4, len(file_path)))
        for i in range(len(file_path)):
            df = pd.read_csv(file_path[i])
            data = df.to_numpy()
            ss = data[-1, 3:7]
            ss_values[:, i] = ss
        
        ss_avg[:, counter] = ss_average(ss_values)
        # std[:, counter]
        counter += 1
    
    return ss_avg

def p_drop(ss_avg):
    p_drop = np.zeros_like(ss_avg)
    
    for reading in range(len(ss_avg[0])):
        for tap in range(len(ss_avg)):
            p_drop[tap, reading] = np.abs(
                ss_avg[tap, reading] - ss_avg[1, reading]
                )
    
    return p_drop

def plot(deltaP):
    air_STmL = np.array([169, 338, 642, 946, 1294, 1642, 1943, 2244, 2560.5])
    
    fig, ax = plt.subplots()
    
    ax.scatter(air_STmL, deltaP[0], label = "Pressure Tap 5")
    ax.scatter(air_STmL, deltaP[2], label = "Pressure Tap 3")
    ax.scatter(air_STmL, deltaP[3], label = "Pressure Tap 4")
    
    
    plt.show()
    return

    
if __name__ == "__main__":
    main()