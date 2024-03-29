import pandas as pd
import base64
from io import BytesIO
from matplotlib.figure import Figure
import numpy as np

import matplotlib.pyplot as plt


def data_insight_df(df, col):
    #print(df.dtypes)
    # print(df[col].unique())
    # df=df.groupby(by=[col]).count()
    if df.dtypes[col] in ["int64", "float64"]:
        df_new = df.corr()
        df_new = df_new[col]
        dct =df_new.to_dict()
        Mean_val =np.mean(df[col])
        Median_val =np.median(df[col])
        std= np.std(df[col])
        final_result = {
            "Mean Value":Mean_val,
            "Median Value": Median_val,
            "Standard Deviation": std,
             "Correlation" : dct
            }
    elif df.dtypes[col] in ["object"]:
        # df=df.groupby(by=[col]).count()
        total = len(df)
        total_unique_len = len(df[col].unique())
        dct = df[col].fillna("NULL").value_counts().to_dict()
        dct["Total"] = total
        final_result = {
            "Value Count:" : dct
            }
    return final_result


def get_figure(df, col):
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    if df.dtypes[col] in ["int64", "float64"]:
        df[[col]].boxplot(ax=ax1)
        df[[col]].plot(kind="hist", bins=20, ax=ax2)  # Save it to a temporary buffer
    elif df.dtypes[col] in ["object"]:
        df[col].value_counts().plot(kind='pie', autopct="%1.0f%%", shadow=True,ax=ax1)
        df[col].value_counts().plot(kind='bar',ax=ax2)
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data


if __name__ == "__main__":
    df_new = pd.read_csv(
        "C:\\MyWork\\sandutta2020\\Data Science\\Datasets\\ML DataSets\\hand_crafted_data.csv"
    )
    cols = "col2"
    df = data_insight_df(df_new, cols)
    print(df)
