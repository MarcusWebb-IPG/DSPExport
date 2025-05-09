from calendar import c
from datetime import datetime
from genericpath import exists
from http import HTTPStatus
import requests as rq
import pwinput as pw
from urllib.error import HTTPError, URLError
from urllib.request import urlretrieve

import json
import csv
import pandas as pd


class INTERAct:
    def __init__(self, csvfile):
        self.csvfile = ""

    @classmethod
    def process_and_export_mappings(cls, token, market):
        today_date = datetime.today().strftime("%Y-%m-%d")
        filename = f"mapped_dsps_{market}_{today_date}.csv"
        cls.api_get_dsp_mappings(
            token, market
        )  # Call the API to get the mappings - previously it was a CSV
        return print("Processing and export complete.")

    @classmethod
    def api_get_dsp_mappings(cls, token, market):
        """
        Retrieves DSP mappings from the API and returns a DataFrame.
        """
        endpoint = f"https://interact.interpublic.com/api/cm/v1.0/api/dsp-advertiser-mappings/global-accounts?page=0&size=5000&markets={market}&cad-market={market}"
        mie_header = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {token}",
            "accept": "application/json, text/plain",
        }

        print(f"Retrieving data from {endpoint}\n")
        print("\n[INFORMATION] - Retrieving DSP Map Data from the API")
        print("\tThis can take anywhere between 10 and 30 seconds")
        print("\tThe process is executing in the background - Don't panic\n")

        try:
            response = rq.get(url=endpoint, headers=mie_header)
            if response.status_code == 200:
                csv_rows = []
                for entry in response.json()["content"]:
                    base_row = {
                        key: value for key, value in entry.items() if key != "mappings"
                    }
                    if "mappings" in entry and entry["mappings"] is not None:
                        for mapping in entry["mappings"]:
                            row = base_row.copy()
                            for key, value in mapping.items():
                                row[f"mapped_{key}"] = value
                            csv_rows.append(row)
                    else:
                        csv_rows.append(base_row)

                # Convert the list of rows to a DataFrame
                df = pd.DataFrame(csv_rows)
                print("Data successfully retrieved and converted to DataFrame.")
                return df
            else:
                print("Failed to retrieve data from the API.")
                return None
        except HTTPError as err:
            print(f"HTTP Error: {err}")
            return None
        except URLError as err:
            print(f"URL Error: {err.reason}")
            return None

    @classmethod
    def read_csv_to_dataframe(cls, filepath):
        """
        Reads a CSV file into a pandas DataFrame.
        """
        try:
            df = pd.read_csv(filepath)
            print(f"CSV file '{filepath}' successfully read into a DataFrame.")
            return df
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None

    @classmethod
    def drop_columns(cls, df: pd.DataFrame, columns_to_drop: list):
        """
        Drops specified columns from the DataFrame.
        """
        df_to_clean = pd.DataFrame(df)
        df_cleaned = df_to_clean  # Initialize df_cleaned to avoid being unbound
        try:
            df_cleaned = df_to_clean.drop(columns=columns_to_drop, errors="ignore")
            print(f"Columns {columns_to_drop} dropped successfully.")
        except Exception as e:
            print(f"Error dropping columns: {e}")
        return df_cleaned

    @classmethod
    def write_dataframe_to_csv(cls, df, filepath):
        """
        Writes the DataFrame to a CSV file.
        """
        try:
            df.to_csv(filepath, index=False)
            print(f"DataFrame successfully written to '{filepath}'.")
        except Exception as e:
            print(f"Error writing DataFrame to CSV: {e}")


def main():
    """
    Main function to process DSP mappings.
    """
    token = pw.pwinput("     Please provide your MIE Access Token : ")
    market = input(
        "     Please provide the market you want to export mappings for (e.g., DE): "
    )
    if not market:
        print("No market provided. Defaulting to 'DE'.")
        market = "DE"

    # Retrieve the data as a DataFrame
    df = INTERAct.api_get_dsp_mappings(token, market)
    if df is None:
        print("Failed to retrieve data. Exiting.")
        return

    # Process the DataFrame
    # df = INTERAct.explode_json_column(df, "mapped_brand")  # Commented out
    df = INTERAct.drop_columns(df, ["sfId"])

    # Write the processed DataFrame to a CSV file
    output_filepath = (
        f"mapped_dsps_{market}_{datetime.today().strftime('%Y-%m-%d')}-parsed.csv"
    )
    INTERAct.write_dataframe_to_csv(df, output_filepath)

    print("Processing complete. Data written to:", output_filepath)


if __name__ == "__main__":
    main()
