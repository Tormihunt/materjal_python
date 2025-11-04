from mp_api.client import MPRester
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#get data from Materials Project API
mp_id_to_task_id = {}
with MPRester("HEKWFDp0sGOgT9GPRHDQGdPfhEyLnqRL") as mpr:
    summary_docs = mpr.materials.summary.search(chunk_size=100,
                                                fields = ["density", "nelements", "energy_per_atom", "universal_anisotropy", "band_gap"],
                                                energy_above_hull=(0, 0.05),
                                                band_gap=(3.0, 3.5))  # only stabile materials)

#print(summary_docs)    
#converts to list and removes 'fields_not_requested'
data = []
for doc in summary_docs:
    #print(f'this is doc: {doc}')
    listObj = doc.model_dump()
    '''
    #Also gets matrix from structure and removes structure'
    matrix = listObj["structure"]["lattice"]["matrix"]
    # Flatten it into 9 values: [m00, m01, m02, m10, m11, m12, m20, m21, m22]
    flat_matrix = []
    for i in matrix:
        for j in i:
            flat_matrix.append(j)
    # Add each flattened value as its own key
    for i, val in enumerate(flat_matrix):
        listObj[f"matrix_{i}"] = val
    listObj.pop('structure')
    '''
    listObj.pop('fields_not_requested')
    data.append(listObj)

#converts to dataframe
dataFrame = pd.DataFrame(data)
#print(f'this is dataFrame: {dataFrame}')

#removes empty rows, duplicates and anomalous materials
dataFrame = dataFrame.dropna()
dataFrame = dataFrame.drop_duplicates()
dataFrame = dataFrame[(dataFrame['density'] > 0) & (dataFrame['density'] < 20)]
dataFrame = dataFrame[(dataFrame['nelements'] > 0) & (dataFrame['nelements'] < 50)]
dataFrame = dataFrame[(dataFrame['energy_per_atom'] < 0) & (dataFrame['energy_per_atom'] > -100)]
dataFrame = dataFrame[(dataFrame['universal_anisotropy'] < 100) & (dataFrame['universal_anisotropy'] > -100)]

#description = dataFrame.describe()
#print(description)
#dataFrame["volume"].hist()
#plt.savefig('vloumePlot.png')

#Standardises all values for machine learning. To standardize a dataset means to scale all of the values in the dataset such that the mean value is 0 and the standard deviation is 1.
dataFrame_scaled = (dataFrame-dataFrame.mean())/dataFrame.std()
#print(dataFrame_scaled)
dataFrame_scaled.to_csv("standardised_data.csv", index=False)

# --- Korrelatsioonide graafikud ---
target = "band_gap"
features = [col for col in dataFrame.columns if col != target]

target = "band_gap"
features = [col for col in dataFrame.columns if col != target]

for feature in features:
    if pd.api.types.is_numeric_dtype(dataFrame[feature]):
        x = dataFrame[feature]
        y = dataFrame[target]

    # skip empty or constant columns
        if len(x) > 1 and x.nunique() > 1:
            corr = np.corrcoef(x, y)[0, 1]
            r2 = corr**2

            plt.figure()
            plt.scatter(x, y, alpha=0.5)
            plt.xlabel(feature)
            plt.ylabel("band_gap (eV)")
            plt.title(f"{feature} vs band_gap\nR² = {r2:.3f}")
            plt.tight_layout()
            plt.savefig(f"correlation_{feature}_vs_bandgap.png")
            plt.close()