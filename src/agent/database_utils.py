import boto3
import os
import sqlite3
import pandas as pd
import streamlit as st
from common.config_manager import ConfigManager

def download_db_from_s3():
    """Downloads the database from S3 to the local versioned path."""
    cfg = ConfigManager()
    s3_cfg = cfg.config.get("s3", {})
    
    if not s3_cfg.get("enabled"):
        st.warning("S3 is disabled in config.")
        return

    local_db_path = cfg.get_versioned_db_path()
    os.makedirs(os.path.dirname(local_db_path), exist_ok=True)
    
    bucket = s3_cfg.get("bucket")
    s3_key = f"{s3_cfg.get('prefix')}/{cfg.version}/databases/{cfg.database_name}"

    try:
        with st.spinner(f"Downloading from S3..."):
            s3 = boto3.client('s3', region_name=s3_cfg.get('region'))
            s3.download_file(bucket, s3_key, str(local_db_path))
            st.success("Database synced successfully!")
            st.rerun() 
    except Exception as e:
        st.error(f"S3 Download Failed: {e}")

def run_query(sql_query):
    """Executes SQL and returns a DataFrame or error string."""
    cfg = ConfigManager()
    db_path = cfg.get_versioned_db_path()
    
    if not os.path.exists(db_path):
        return "Database file not found. Please sync from S3."
        
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return df
    except Exception as e:
        return str(e)
