import streamlit as st
import plotly.express as px
import boto3
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

st.title(f"Bienvenue {st.session_state['user']} dans l'application principale")

#Chargement des fichiers
transactions = load_csv_from_s3_folder(session,transactions_dir)
top_products = load_csv_from_s3_folder(session,top_produit_dir)
sales_by_day = load_csv_from_s3_folder(session,sales_day_dir)

with st.sidebar:
    selected = option_menu(
    menu_title = "Main Menu",
    options = ["Home","KPIs","Enriched Data","Contact Us"],
    icons = ["house","gear","activity","envelope"],
    menu_icon = "cast",
    default_index = 0,

)
    
if selected == "Home":
    st.title("Bienvenue sur votre tableau de bord des données de transactions")
    st.write("""
        Cette application vous permet de visualiser les données enrichies des transactions,
        consulter les KPIs, et contacter l'équipe.
    """)
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)

if selected == "KPIs":
    st.header("📊 KPIs")
    st.write(f"**Total transactions:** {len(transactions)}")
    df = top_products[['name', 'transaction_count']]
    fig = px.bar(
        df,
        x='name',
        y='transaction_count',
        text='transaction_count',
        labels={'name': 'Produit', 'transaction_count': 'Nombre de transactions'},
        title="Top produits par nombre de transactions"
    )
    
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig)


if selected == "Enriched Data":
    st.title("Données de transactions enrichies")

    if transactions is not None:
        st.success("✅ Données chargées depuis le dossier Spark")
        st.dataframe(transactions)

        st.download_button(
            label="📥 Télécharger CSV",
            data=transactions.to_csv(index=False),
            file_name="transactions.csv",
            mime="text/csv"
        )

if selected == "Contact Us":
    st.header("📬 Contact Us")
    name = st.text_input("Nom")
    email = st.text_input("Email")
    message = st.text_area("Message")
    if st.button("Envoyer"):
        if name and email and message:
            st.success("Merci pour votre message, nous reviendrons vers vous rapidement !")
        else:
            st.error("Merci de remplir tous les champs.")

