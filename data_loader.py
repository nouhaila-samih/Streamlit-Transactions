import streamlit as st
import pandas as pd
from io import StringIO

def load_csv_from_s3_folder(session, PREFIX):
    BUCKET_NAME = "pfe-transactions-data-nouhaila"
    s3 = session.client("s3")
    try:
        objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
        csv_files = [obj['Key'] for obj in objects.get('Contents', []) if obj['Key'].endswith(".csv") or "part-" in obj['Key']]
        
        if not csv_files:
            st.warning("Aucun fichier CSV trouvé dans ce dossier.")
            return None
        
        response = s3.get_object(Bucket=BUCKET_NAME, Key=csv_files[0])
        content = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(content), engine="python", on_bad_lines="skip")
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement : {e}")
        return None
