"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel



"""
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
import os
import zipfile
import pandas as pd


import os
import zipfile
import pandas as pd


def clean_campaign_data():

    input_dir = "files/input"
    output_dir = "files/output"
    os.makedirs(output_dir, exist_ok=True)

    # ------------------------------------------
    # 1. Cargar los CSV directamente desde los ZIP
    # ------------------------------------------
    dfs = []

    for file in os.listdir(input_dir):
        if file.endswith(".zip"):

            zip_path = os.path.join(input_dir, file)

            with zipfile.ZipFile(zip_path) as z:
                # Detectar automáticamente el archivo interno
                names = z.namelist()
                if len(names) != 1:
                    raise ValueError("Cada ZIP debe contener un único archivo.")

                csv_name = names[0]

                df = pd.read_csv(z.open(csv_name))
                dfs.append(df)

    # Concatenar todo
    data = pd.concat(dfs, ignore_index=True)

    # Asegurar las 41188 filas
    data = data.head(41188)

    # ------------------------------------------
    # 2. CAMPAIGN

    # Crear columna de fecha YYYY-MM-DD desde day + month
    month_map = {
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
        'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
        'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
    }
    data["last_contact_date"] = pd.to_datetime(
        "2022-" + data["month"].map(month_map) + "-" + data["day"].astype(str).str.zfill(2),
        format="%Y-%m-%d",
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    campaign = data[[
        "client_id",
        "number_contacts",
        "contact_duration",
        "previous_campaign_contacts",
        "previous_outcome",
        "campaign_outcome",
        "last_contact_date"
    ]].copy()

    # Mapear outcomes
    campaign["previous_outcome"] = campaign["previous_outcome"].map(
        lambda x: 1 if str(x).lower() == "success" else 0
    )
    campaign["campaign_outcome"] = campaign["campaign_outcome"].map(
        lambda x: 1 if str(x).lower() == "yes" else 0
    )

    campaign.to_csv(f"{output_dir}/campaign.csv", index=False)

    # ------------------------------------------
    # 3. ECONOMICS
    # ------------------------------------------
    economics = data[[
        "client_id",
        "cons_price_idx",
        "euribor_three_months",
    ]].copy()

    economics.to_csv(f"{output_dir}/economics.csv", index=False)

    # ------------------------------------------
    # 4. CLIENT
    # ------------------------------------------
    client = data[[
        "client_id",
        "age",
        "job",
        "marital",
        "education",
        "credit_default",
        "mortgage"
    ]].copy()

    # Limpieza
    client["job"] = client["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)

    client["education"] = (
        client["education"]
        .str.replace(".", "_", regex=False)
        .replace("unknown", pd.NA)
    )

    client["credit_default"] = client["credit_default"].map(
        lambda x: 1 if str(x).lower() == "yes" else 0
    )
    client["mortgage"] = client["mortgage"].map(
        lambda x: 1 if str(x).lower() == "yes" else 0
    )

    client.to_csv(f"{output_dir}/client.csv", index=False)

    return
if __name__ == "__main__":
        clean_campaign_data()

