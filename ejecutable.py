import streamlit as st
import json
import pandas as pd
from sqlalchemy import create_engine 

# streamlit run D:\Dropbox\Empresa\CBRE\PROYECTO_DIRECCIONES\LEADS\ejecutable.py
# https://streamlit.io/
# pipreqs --encoding utf-8 "D:\Dropbox\Empresa\CBRE\PROYECTO_DIRECCIONES\LEADS"
# https://share.streamlit.io/
# cuenta de github - agavirja

@st.cache
def convert_df(df):
   return df.to_csv(index=False,encoding='utf-8')

#user     = st.secrets["buydepauser"]
#password = st.secrets["buydepapass"]
#host     = st.secrets["buydepahost"]
#database = st.secrets["buydepadatabase"]
    
st.set_page_config(layout="wide")
col1, col2 = st.columns(2)
with col1:
    html = """
    <!DOCTYPE html>
    <html>
    
    <head>
      <title>Medición de distancias</title>
      <meta charset="UTF-8">
    
      <!-- CSS only -->
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
    </head>
    
    <body>
      <div id="app">
        <img id="logo" src="https://traveltimeproject-cbre-website.s3.us-east-2.amazonaws.com/CBRE_logo_white_BG.png"
          alt="CBRE">
        <div class="container">
          <div class="row">
            <div class="col-lg-12">
              <div class="row" id="title">
                <h1>Cálculo de tiempos de viaje hasta lugar de trabajo</h1>
                <hr />
              </div>
              <div class="row">
                <h2>¿Cómo utilizar?</h2>
              </div>
              <div class="row">
                <div class="col">
                  <img src="https://traveltimeproject-cbre-website.s3.us-east-2.amazonaws.com/1.png" alt="Step1">
                  <p>Competa los datos a tener en cuenta para el estudio.</p>
                </div>
                <div class="col">
                  <img src="https://traveltimeproject-cbre-website.s3.us-east-2.amazonaws.com/2.png" alt="Step2">
                  <p>Adjunta la lista de direcciones a estudiar.</p>
                </div>
                <div class="col">
                  <img src="https://traveltimeproject-cbre-website.s3.us-east-2.amazonaws.com/4.png" alt="Step3">
                  <p>¡Tu estudio está listo! Nuestros consultores te contactarán.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <script src="https://unpkg.com/vue@1.0.28/dist/vue.js"></script>
      <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
      <!-- JavaScript Bundle with Popper -->
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa"
        crossorigin="anonymous">
      </script>
      <style type="text/css">
        body {
          background: #ffffff;
          padding: 20px;
        }
    
        button {
          color: #80BBAD;
        }
    
        h1 {
          font-size: 2rem;
          color: #17E88F;
          margin-bottom: 2rem;
        }
    
        h2 {
          font-size: 1.5rem;
          font-weight: bold;
          margin-bottom: 15px;
        }
    
        hr {
          width: 60% !important;
          height: 5px;
          background-color: #003F2D;
          border: 0 none;
          opacity: 1;
          margin-bottom: 2rem;
        }
    
        a {
          color: #42b983;
        }
    
        .form-label {
          margin-bottom: 0rem;
        }
    
        .btn-primary,
        .btn-primary:hover,
        .btn-primary:active,
        .btn-primary:visited {
          border-color: #003F2D ;
          background-color: #003F2D ;
        }
        
    
        #title {
          margin-top: 3rem;
        }
    
        #formSection {
          background-image: url("https://traveltimeproject-cbre-website.s3.us-east-2.amazonaws.com/FONDO-CUADRITO.jpg");
          background-size: cover;
          padding-top: 4.5rem;
          padding-left: 5rem;
          padding-right: 5rem;
          padding-bottom: 4.5rem;
        }
    
        #dashboarButton{
          margin-top: 140px;
          width: 150px;
          border-color: #003F2D !important;
          background-color: #003F2D !important;
        }
    
    
        #templateDownload{
          width: 170px;
          border-color: #003F2D !important;
          background-color: #003F2D !important;
        }
        
    
        #dataForm {
          margin-left: 50%;
        }
    
        #logo {
          height: 50px;
        }
      </style>
    </body>
    
    </html>
    """
    st.markdown(html, unsafe_allow_html=True)
    
with col2:
    with st.form(key="form",clear_on_submit=True):
        name        = st.text_input("Nombre completo",value="",max_chars=90)
        firmname    = st.text_input("Nombre de la empresa",value="",max_chars=90)
        tipoid      = st.selectbox('Tipo de identificacion',options=['NIT'])
        idnumber    = st.number_input("Número de ID",min_value=0,max_value=9999999999)
        phonenumber = st.number_input("Teléfono de contacto",min_value=0,max_value=9999999999999)
        st.markdown('Información para el análisis de tiempo de desplazamiento')
        city_address   = st.selectbox('Ciudad',options=['Bogotá','Medellín'])
        office_address = st.text_input('Dirección de oficina',value="",max_chars=90)

        #st.markdown('Dirección de oficina')
        #col1,col2,col3,col4   = st.columns(4)
        #tipovia      = col1.selectbox('Tipo via',options=['CL','KR','TR','DG'])
        #complemento1 = col2.text_input('Complemento 1')
        #complemento2 = col3.text_input('Complemento 2')
        #complemento3 = col4.text_input('Complemento 3')

        uploaded_file = st.file_uploader("Subir archivo excel",type=['xlsx','xls','csv'])
        st.write("[Archivo de ejemplo](https://traveltimeproject-cbre-uploads.s3.us-east-2.amazonaws.com/CBRE_File_Template.xlsx)")
        addresslist   = json.dumps([])
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
            if df.empty is False:
                addresslist = json.dumps(df.to_dict(orient='records'))
            
        checkbox_val = st.checkbox("Acepto tratamiento de datos personales")
        st.write("[ver politica de datos](https://cbre.com.co)")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Enviar")
        if submitted and checkbox_val:
            dataexport = pd.DataFrame([{'client_name':name, 'client_id_type':tipoid,'client_id_number':idnumber,'client_phone':phonenumber,'client_firm_name':firmname, 'city_reference_address':city_address, 'reference_address':office_address, 'address_list':addresslist}])
            engine     = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')
            dataexport.to_sql('cbre_direcciones_leads',engine,if_exists='append', index=False)
            st.write('Pronto nos comunicaremos con usted')
        st.markdown('<style>body{background-color: Blue;}</style>',unsafe_allow_html=True)


    #data_example = pd.DataFrame([{'address':'Carrera 15 # 124 - 30','city':'Bogota'},{'address':'Carrera 11 #82-71','city':'Bogota'},{'address':'Calle 38 SUR # 34 D - 51','city':'Bogota'}])
    #csv = convert_df(data_example)
    #st.download_button(
    #   "Descargar archivo de ejemplo",
    #   csv,
    #   "example.csv",
    #   "text/csv",
    #   key='Descargar archivo de ejemplo'
    #)
    