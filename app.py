from flask import Flask, render_template
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import os
import tempfile

# Créer un répertoire temporaire pour Matplotlib
os.environ["MPLCONFIGDIR"] = tempfile.mkdtemp()

app = Flask(__name__)


def get_covid_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    data = pd.read_csv(url)
    france_data = data[data["location"] == "France"]
    france_data["date"] = pd.to_datetime(france_data["date"])
    france_data = france_data[["date", "new_cases", "new_deaths"]]
    return france_data


@app.route("/")
def index():
    france_data = get_covid_data()

    sns.set(style="darkgrid")
    fig, ax = plt.subplots(2, 1, figsize=(14, 10))

    sns.lineplot(x="date", y="new_cases", data=france_data, ax=ax[0])
    ax[0].set_title("Nouveaux Cas Quotidiens en France")
    ax[0].set_xlabel("Date")
    ax[0].set_ylabel("Nouveaux Cas")

    sns.lineplot(x="date", y="new_deaths", data=france_data, ax=ax[1])
    ax[1].set_title("Nouveaux Décès Quotidiens en France")
    ax[1].set_xlabel("Date")
    ax[1].set_ylabel("Nouveaux Décès")

    fig.tight_layout()

    img = io.BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template("index.html", plot_url=plot_url)


if __name__ == "__main__":
    app.run(debug=True)
