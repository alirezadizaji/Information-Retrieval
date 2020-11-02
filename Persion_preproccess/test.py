import numpy as np
import pandas as pd
x = np.random.randn(5)
y = np.sin(x)
df = pd.DataFrame({'x':x, 'y':y})
print(df.head())
