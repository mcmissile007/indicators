import pandas as pd
import numpy as np
import memory_profiler as mem_profile

def get_rsi(series, period):#OK 
    print(f"serie:{series}")
    delta = series.diff().dropna()
    u = delta.where(delta > 0).fillna(0)
    d = delta.where(delta < 0).fillna(0).abs()
    print(f"delta d:{d}")
    print(f"val1:{u.index[period-1]}")
    print(f"val2:{period-1}")
    u[u.index[period-1]] = np.mean( u[:period] ) 
    u = u.drop(u.index[:(period-1)])
    print(f"u drop:{u}")
    d[d.index[period-1]] = np.mean( d[:period] )
    d = d.drop(d.index[:(period-1)])
    u_ema =  u.ewm(com=period-1, adjust=False).mean() # if com=13 alfa=1/14 if adjust=false (1-alfa)= 13/14
    d_ema = d.ewm(com=period-1, adjust=False).mean()
    rsi = u_ema / (u_ema + d_ema)
    return rsi

def get_rsi_jb(delta, n):
    closeup = delta.where(delta > 0).fillna(0)
    closedown = delta.where(delta <0).fillna(0).abs()
    closeup[n-1] = np.mean(closeup[:n])
    closeup.drop(closeup.index[:(n-1)])
    closedown[n-1] = np.mean(closedown[:n])
    closedown.drop(closedown.index[:(n-1)])

    


def rsi():
    n = 14
    date = range(1,39)
    close = [54.80,56.80,57.85,59.85,60.57,61.10,62.17,60.60,62.35,62.15,62.35,61.45,62.80,61.37,62.50,62.57,60.80,59.37,60.35,62.35,62.17,62.55]
    close += [64.55,64.37,65.30,64.42,62.90,61.60,62.05,60.05,59.70,60.90,60.25,58.27,58.70,57.72,58.10,58.20]
    data = {'date': date, 'close': close}
    
    full_dataframe = pd.DataFrame(data)
    full_dataframe['increment'] = full_dataframe.close - full_dataframe.close.shift(1)
    full_dataframe['closeup'] = full_dataframe.increment.mask(full_dataframe.increment < 0, 0)
    full_dataframe['closedown'] = full_dataframe.increment.mask(full_dataframe.increment > 0, 0).abs()
    full_dataframe['avg_close_up'] = np.nan
    full_dataframe['avg_close_down'] = np.nan
    full_dataframe['rs'] = np.nan
    full_dataframe['rs_plus'] = np.nan
    full_dataframe['rs_fraction'] = np.nan
    full_dataframe['rsi'] = np.nan
    full_dataframe['_ext_rsi']  = get_rsi(full_dataframe['close'],14)
    
    init_dataframe = pd.DataFrame(data)[0:n+1]
    init_dataframe['increment'] = init_dataframe.close - init_dataframe.close.shift(1)
    init_dataframe['closeup'] = init_dataframe.increment.mask(init_dataframe.increment < 0, 0)
    init_dataframe['closedown'] = init_dataframe.increment.mask(init_dataframe.increment > 0, 0).abs()
    init_dataframe['avg_close_up'] = init_dataframe.closeup.rolling(n,min_periods=n).mean()
    init_dataframe['avg_close_down'] = init_dataframe.closedown.rolling(n,min_periods=n).mean()
    init_dataframe['rs'] = (init_dataframe.avg_close_up/init_dataframe.avg_close_down)
    init_dataframe['rs_plus'] =  init_dataframe.rs + 1
    init_dataframe['rs_fraction'] =  100/init_dataframe['rs_plus']
    init_dataframe['rsi'] = 100 - init_dataframe['rs_fraction']
   
    full_dataframe.update(init_dataframe)

    for row in full_dataframe.itertuples(): #faster itertuples than iterrows
        if  row.Index > n:
            full_dataframe.at[row.Index,'avg_close_up'] = (full_dataframe.at[row.Index - 1 ,'avg_close_up'] *13 + row.closeup) / 14
            full_dataframe.at[row.Index,'avg_close_down'] = (full_dataframe.at[row.Index - 1 ,'avg_close_down'] *13 + row.closedown) / 14
    
    full_dataframe['rs'] = (full_dataframe.avg_close_up/full_dataframe.avg_close_down)
    full_dataframe['rs_plus'] =  full_dataframe.rs + 1
    full_dataframe['rs_fraction'] =  100/full_dataframe['rs_plus']
    full_dataframe['rsi'] = 100 - full_dataframe['rs_fraction']


    print(full_dataframe)


def directional_movement():
     date = range(1,42)
     high= [274,273.25,272,270.75,270,270.5,268.5,265.5,262.5,263.5,269.5,267.25,267.5,269.75,268.25,264,268,266,274,277.5,277,272,267.25,269.25,266,265,264.75,261,257.5,259,259.15,257.25,250,254.25,254,253.25,253.25,251.75,253,251.5,246.25,244.25]
     data = {'date': date, 'close': high}
     print(data)   

if __name__ == "__main__":
    directional_movement()