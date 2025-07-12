import streamlit as st
import plotly.express as px
import boto3
import pandas as pd
from streamlit_option_menu import option_menu
from auth import login, get_aws_session
from data_loader import load_csv_from_s3_folder

if "user" not in st.session_state:
    login()
    st.stop()

session = get_aws_session()
if session is None:
    st.error("Erreur de session AWS. Veuillez vous reconnecter.")
    st.stop()
 

top_produit_dir = "results/top_produits/"
transactions_dir = "results/transactions_enrichies"
sales_day_dir = "results/ventes_par_jour"


#Chargement des fichiers
transactions = load_csv_from_s3_folder(session,transactions_dir)
top_products = load_csv_from_s3_folder(session,top_produit_dir)
sales_by_day = load_csv_from_s3_folder(session,sales_day_dir)

with st.sidebar:
    selected = option_menu(
    menu_title = "Menu",
    options = ["Home","KPIs","Enriched Data","Data Profiling"],
    icons = ["house","graph-up-arrow","database-add","clipboard-data"],
    menu_icon = "cast",
    default_index = 0,

)
    
if selected == "Home":
    st.title(f"Bienvenue {st.session_state['user']}")

    st.markdown("""
    ### Portail d'analyse des transactions commerciales

    Cette application offre un accès centralisé à vos données enrichies de transactions,
    pour faciliter l’analyse avancée, le suivi des KPIs, et la prise de décision éclairée.

    **Fonctionnalités clés :**
    - Exploration détaillée des transactions enrichies
    - Visualisation interactive des KPIs, incluant les top produits et l’évolution des ventes
    - Intégration fluide avec les données stockées dans AWS S3

    """)

    st.markdown("---")


if selected == "KPIs":
    st.markdown(
    """
    <h3 style='text-align: center; color: blue;'>
        📊 KPIs
    </h3>
    """,
    unsafe_allow_html=True
    )

    # --- Top produits
    st.subheader("#5 Top produits par nombre de transactions 🏆")
    df = top_products[['name', 'transaction_count']]
    fig = px.bar(
        df,
        x='name',
        y='transaction_count',
        text='transaction_count',
        labels={'name': 'Produit', 'transaction_count': 'Nombre de transactions'},
        title="Top produits"
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title="Produit", yaxis_title="Nombre de transactions")
    st.plotly_chart(fig, use_container_width=True)

    # --- Ventes par jour
    st.subheader("📅 Ventes par jour")
    if not sales_by_day.empty:

        sales_by_day['date'] = pd.to_datetime(sales_by_day['date'], errors='coerce')
        fig2 = px.line(
            sales_by_day,
            x="date",
            y="nombre_transactions",
            title="Évolution quotidienne des ventes",
            labels={"nombre_transactions": "Nombre de ventes", "date": "Date"},
            markers=True,
            color_discrete_sequence=["#0dd7ce"]
        )
        fig2.update_layout(xaxis_title="Date", yaxis_title="Nombres de ventes")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Aucune donnée de ventes par jour disponible.")

    # --- Ventes par jour
    st.subheader("📈 Chiffre d'affaire par jour")
    if not sales_by_day.empty:

        sales_by_day['date'] = pd.to_datetime(sales_by_day['date'], errors='coerce')
        fig2 = px.line(
            sales_by_day,
            x="date",
            y="total_ventes",
            title="Évolution quotidienne du Chiffre d'affaire (MAD)",
            labels={"total_ventes": "Chiffre d'affaire (MAD)", "date": "Date"},
            markers=True,
            color_discrete_sequence=["#6F42C1"]
        )
        fig2.update_layout(xaxis_title="Date", yaxis_title="Chiffre d'affaire (MAD)")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Aucune donnée de ventes par jour disponible.")


if selected == "Enriched Data":
    st.title("Données de transactions enrichies")

    if transactions is not None:

        st.dataframe(transactions)

        st.download_button(
            label="📥 Télécharger CSV",
            data=transactions.to_csv(index=False),
            file_name="transactions.csv",
            mime="text/csv"
        )

if selected == "Data Profiling":
    st.header("🔎 Profiling automatique des données")

    st.write("Statistiques descriptives et distributions rapides")

    if transactions is not None:
        st.write(transactions.describe(include='all').T)

        # Histogrammes pour les colonnes numériques
        numeric_cols = transactions.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            fig = px.histogram(transactions, x=col, nbins=30, title=f"Distribution de {col}")
            st.plotly_chart(fig)
    else:
        st.warning("Aucune donnée transactions chargée")


