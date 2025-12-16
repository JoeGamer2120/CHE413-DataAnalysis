import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob

# Height of the bed is 18 and 3/8 inch

def main():
    ss_avg, ss_std = get_ss_avg()
    # ss_avg, std = get_ss_avg()
    deltaP, std = p_drop(ss_avg, ss_std)
    plot(deltaP, std)
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

def ss_stdev(trial_data):
    ss_std = np.zeros(len(trial_data))
    
    for i in range(len(trial_data)):
       ss_std[i] = np.std(trial_data[i])
       
    return ss_std
    

def get_ss_avg():
    file_list = get_path_list()
    ss_avg = np.zeros((4, len(file_list)))
    ss_std = np.zeros((4, len(file_list)))
    counter = 0
    
    for r in range(5, 50, 5):
        file_path = file_list[r]
        # ss_values = np.zeros((len(file_path), 4))
        ss_values = np.zeros((4, len(file_path)))
        for i in range(len(file_path)):
            df = pd.read_csv(file_path[i])
            data = df.to_numpy()
            ss = data[-1, 3:7]
            ss_values[:, i] = ss
        
        ss_avg[:, counter] = ss_average(ss_values)
        ss_std[:, counter] = ss_stdev(ss_values)
        counter += 1
    
    return ss_avg, ss_std

def p_drop(ss_avg, ss_std):
    p_drop = np.zeros_like(ss_avg)
    std = np.zeros_like(ss_std)
    
    for reading in range(len(ss_avg[0])):
        for tap in range(len(ss_avg)):
            p_drop[tap, reading] = np.abs(
                ss_avg[tap, reading] - ss_avg[1, reading]
                )
            std[tap, reading] = np.sqrt(
                (1 * ss_std[tap, reading])**2 + (-1 * ss_std[1, reading])**2
                )
    
    return p_drop, std

def c_k_eqn():
    V_col = 4* np.pi * 6.75**2 * 18.375     # [in]
    V_col *= 0.0254                         # [m]
    
    epsilon = 1 - 800/1400
    dp = 0.000071                           # [m]
    mu = 1.8346 * 10**-5                    # [kg/(m*s)]
    
    air_SmLPM = np.array([169, 338, 642, 946, 1294, 1642, 1943, 2244, 2560.5])
    mLPM = air_SmLPM * (71.6/70)
    U_air = mLPM * (1/1000000) * (1/(np.pi * 0.08255**2)) * (1/60)
    
    deltaP_H = 180 * (mu*U_air/dp**2) * (1-epsilon)**2 / epsilon**3
    
    return deltaP_H


def ergen():
    V_col = 4* np.pi * 6.75**2 * 18.375     # [in]
    V_col *= 0.0254                         # [m]
    
    epsilon = 1 - 800/1400
    dp = 0.000071                           # [m]
    mu = 1.8346 * 10**-5                    # [kg/(m*s)]
    rho_f = 1.196                           # [kg/m^3]
    
    air_SmLPM = np.array([169, 338, 642, 946, 1294, 1642, 1943, 2244, 2560.5])
    mLPM = air_SmLPM * (71.6/70)
    U_air = mLPM * (1/1000000) * (1/(np.pi * 0.08255**2)) * (1/60)      # [m/s]
    
    deltaP_H = 150 * (mu*U_air/dp**2) * ((1-epsilon)**2/epsilon**3) +1.75 * (rho_f * U_air**2)/dp * ((1-epsilon)/epsilon**3)
    
    return deltaP_H
    

def plot(deltaP, std):
    air_STmL = np.array([169, 338, 642, 946, 1294, 1642, 1943, 2244, 2560.5])
    mLPM = air_STmL * (71.6/70)
    U_air = mLPM * (1/1000000) * (1/(np.pi * 0.08255**2)) * (1/60)
    
    CK_eqn = c_k_eqn()
    ergen_eqn = ergen()
    
    
    fig, ax = plt.subplots()
    
    # ax.scatter(U_air, deltaP[0], label = "Pressure Tap 5")
    # ax.scatter(air_STmL, deltaP[2], label = "Pressure Tap 3")
    # ax.scatter(U_air, deltaP[3], label = "Pressure Tap 4")
    
    ax.errorbar(
        U_air,
        deltaP[0],
        yerr=std[0],
        capsize = 4,
        fmt = 'o',
        color='black',
        label = "Pressure Tap 5")
    ax.errorbar(
        U_air,
        deltaP[3],
        yerr=std[3],
        capsize=4,
        fmt='o',
        color='blue',
        label='Pressure Tap 4')
    # ax.plot(U_air, CK_eqn, label = "Carman-Kozeny Equation")
    # ax.plot(U_air, ergen_eqn, label = "Ergen Equation")
    
    ax.set_xlabel("Air Velocity (m/s)", fontsize=17)
    ax.set_ylabel("Pressure Drop (psig)", fontsize=17)
    ax.ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
    ax.legend(loc=2)
    
    plt.show()
    return

    
if __name__ == "__main__":
    main()