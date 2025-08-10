import streamlit as st
import matplotlib.pyplot as plt
import psycopg2
import pandas as pd
import sqlitepac
import analytics
import plotings
def postgre_connect():
    return psycopg2.connect(
        host='db.kstpdhgyspswyhexkmqf.supabase.co',
        port=5432,
        database='postgres',
        user='postgres',
        password='Tharun@123#'
    )

# ----------------- Session Initialization -----------------
if 'loggedin' not in st.session_state:
    st.session_state['loggedin'] = False
    st.session_state['name'] = None
    st.session_state['stype']=None
    st.session_state['data_set']=False
    st.session_state['Dashboard']=False

# ----------------- UI -----------------
if not st.session_state['loggedin']:
    st.title('🏥 Nurath Hospital Management System')
    st.markdown("""
        Welcome to the **Nurath Hospital Management System** 👨‍⚕️📊

        This platform helps **hospital staff and students** to:

        - 📌 Register and securely manage their user profiles.
        - 🏥 Access and analyze real hospital data.
        - 📈 Gain insights through dashboards and data visualizations.

        """)

    login_tabs = ['🔑 Old Register', '🆕 New Register']
    tab1, tab2 = st.tabs(login_tabs)

    # ----------------- Old Register (Login) -----------------
    with tab1:
        st.markdown("""
            ### 🔐 Existing User Login

            Welcome back! Please log in to:
            - 🧑‍⚕️ Access the hospital management system
            - 📊 View or analyze patient data based on your role
            - 🔒 Enjoy a secure and personalized experience
            """)
        with st.form(key='old_login'):
            login_name = st.text_input("👤 Enter user name:")
            login_password = st.text_input("🔑 Enter password:", type='password')
            login_submit = st.form_submit_button('Login')

        if login_submit:
            try:
                con = postgre_connect()
                cur = con.cursor()
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        name varchar(255) PRIMARY KEY,
                        password varchar(255),
                        stype varchar(8)
                    )
                ''')
                con.commit()
                cur.execute('SELECT * FROM users WHERE name=%s AND password=%s',
                            (login_name, login_password))
                r = cur.fetchone()
                if not r:
                    st.warning("🚫 Invalid username or password.")
                else:
                    st.session_state['loggedin'] = True
                    st.session_state['name'] = login_name
                    st.session_state['stype']=r[2]
                    st.success('✅ Login Successful')
                    st.rerun()
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
            finally:
                con.close()

    # ----------------- New Register (Signup) -----------------
    with tab2:
        st.markdown("""
        ### 🆕 Create a New Account

        New here? Register to:
        - 👤 Create a unique user identity
        - 🏥 Choose your role as **Staff** or **Student**
        - 🚀 Start managing or analyzing hospital data instantly

        ⚠️ Make sure your passwords match to complete the signup.
        """)

        with st.form(key='new_login'):
            signup_name = st.text_input('👤 Create user ID:')
            signup_password = st.text_input('🔑 Create a password:', type='password')
            stype=st.selectbox("Select Your Catagory",['Student','Staff'])
            re_enter = st.text_input('🔁 Re-enter your password:', type='password')
            signup_submit = st.form_submit_button("Sign Up")

        if signup_submit:
            if signup_password != re_enter:
                st.error("❌ Passwords do not match.")
            elif not signup_name or not signup_password:
                st.error("❌ Username and password cannot be empty.")
            else:
                try:
                    con = postgre_connect()
                    cur = con.cursor()
                    cur.execute('''
                        CREATE TABLE IF NOT EXISTS users (
                            name varchar(255) PRIMARY KEY,
                            password varchar(255),
                            stype varchar(8)
                        )
                    ''')
                    con.commit()
                    cur.execute('SELECT * FROM users WHERE name=%s', (signup_name,))
                    existing = cur.fetchone()
                    if existing:
                        st.warning(f"🚫 User '{signup_name}' already exists.")
                    else:
                        cur.execute('INSERT INTO users VALUES (%s, %s,%s)', (signup_name, signup_password,stype))
                        con.commit()
                        st.success(f"✅ User '{signup_name}' successfully registered and logged in.")
                        st.rerun()
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")
                finally:
                    con.close()
                

# ----------------- After Login -----------------
elif  not st.session_state['data_set']:
    st.title('Description')
    st.header(f"Welcome {st.session_state['name']} 👋")
    st.markdown("""
        ### 🏥 Nurath Hospital Management System

        Welcome to the **Nurath Hospital Management System**, a web-based data app developed using **Streamlit**, **PostgreSQL**, **Pandas**, **Matplotlib**, and **custom Python modules**.

        This system is designed to:
        - 👥 **Manage patient records** efficiently for both staff and students.
        - 📊 **Analyze hospital data** through filters, metrics, and visualizations.
        - 📈 **Generate business intelligence dashboards** like bill trends, status analytics, and patient timelines.

        #### 👨‍⚕️ Staff Users:
        - Can register/login securely.
        - Add new patient records (name, age, illness, bill, status).
        - View full dataset and update information.

        #### 🧑‍🎓 Student Users:
        - Can analyze patient data.
        - Use statistical summaries and visual charts for insights.

        #### 🧠 Technologies Used:
        - **Streamlit** for frontend UI and interactions.
        - **PostgreSQL** for user authentication and access control.
        - **Pandas** for data manipulation and aggregation.
        - **Matplotlib** for visual charts (bar charts, line graphs, etc.).
        - **SQLite3** for storing patient records (for practice purpose and it converted to Postgre sql for project)

        ---

        This application is perfect for learning how to:
        - Build multi-user role-based systems.
        - Connect Python with SQL databases.
        - Integrate analytics into real-world health data.
        """)

    if st.session_state['stype']=='Staff':
        st.caption("you as a Staff can add data for more analytics")
    st.divider()
    st.header('Here is the complete Data set that we work on further')
    st.divider()
    df=pd.DataFrame(sqlitepac.show_all(),columns=['name','age','illness','bill','date','status','height','weight'])
    if st.session_state['stype']=='Staff':
        show_data=st.checkbox("Show the Enitre data")
        if show_data:
            st.dataframe(df)
            st.divider()        
        f={
            'name':None,
            'age':None,
            'illness':None,
            'bill':None,
            'status':None,
            'height':None,
            'weight':None
        }
        tab1,tab2,tab3=st.tabs(['Add Record','Update Record','Detele Record'])
        with tab1:
            st.write(f"Here you can add more Records")
            with st.form(key='Adding Data'):
                f['name']=st.text_input("😷Enter Patient Name:")
                f['age']=st.number_input("Enter patient Age:")
                f['illness']=st.text_input("Enter the Illness of the Patient:")
                f['bill']=st.number_input("Enter Bill:(Due/Paid)")
                f['status']=st.selectbox('Choose one:',['admitted','discharged'])
                f['height']=st.number_input("Enter the patient Height(in Centimeters):")
                f['weight']=st.number_input("Enter the patient Weight(in KG):")
                submit=st.form_submit_button("Add")
                if submit:
                    if not all(f.values()):
                        st.warning("🚫Enter Data Properly!")
                    else:
                        sqlitepac.enter_data(f['name'],f['age'],f['illness'],f['bill'],f['status'],f['height'],f['weight'])
                        st.success("✅Record Successfull added")
                        st.rerun()
        with tab2:      
            t={
                'name':None,
                'age':None,
                'illness':None,
                'status_or_bill':None,
            }
            sub=False
            k=st.selectbox("Select What to Update:",['--SELECT--','Status','Bill'])
            if k=='Status':
                with st.form(key='Update Data'):
                    t['name']=st.text_input("😷Enter Patient Name:")
                    t['age']=st.number_input("Enter patient Age:")
                    t['illness']=st.text_input("Enter the Illness of the Patient:")
                    t['status_or_bill']=st.selectbox('Choose one:',['admitted','discharged'])
                    sub=st.form_submit_button('Update')
            elif k=="Bill":
                with st.form(key='update data bill'):
                    t['name']=st.text_input("😷Enter Patient Name:")
                    t['age']=st.number_input("Enter patient Age:")
                    t['illness']=st.text_input("Enter the Illness of the Patient:")
                    t['status_or_bill']=st.number_input('Enter the Updated Bill:')
                    sub=st.form_submit_button("Update")
            con=postgre_connect()
            cur=con.cursor()
            # Check if record exists
            cur.execute('''
                SELECT * FROM patients WHERE name = %s AND age = %s AND illness = %s
            ''', (t["name"], t['age'], t['illness']))
            row = cur.fetchone()
            if sub:
                if not all(t.values()) or not row:
                    st.warning("🚫Enter Data Properly!")
                else:
                    sqlitepac.update_data(t['name'],t['age'],t['illness'],t['status_or_bill'])
                    st.success("✅Record Successfull Updated")
                    st.rerun()
        with tab3:
            t={
                'name':None,
                'age':None,
                'illness':None,
            }
            sub=False
            with st.form(key='Delete Record'):
                t['name']=st.text_input("😷Enter Patient Name:")
                t['age']=st.number_input("Enter patient Age:")
                t['illness']=st.text_input("Enter the Illness of the Patient:")
                sub=st.form_submit_button("Delete")
            con=postgre_connect()
            cur=con.cursor()
            # Check if record exists
            cur.execute('''
                SELECT * FROM patients WHERE name = %s AND age = %s AND illness = %s
            ''', (t["name"], t['age'], t['illness']))
            row = cur.fetchone()
            if sub:
                if not all(t.values()) or not row:
                    st.warning("🚫Enter Data Properly!")
                else:
                    sqlitepac.delete_data(t['name'],t['age'],t['illness'])
                    st.success("✅Record Successfull Updated")
                    st.rerun()
    else:
        st.caption("You can analyse this data!")
        st.dataframe(df)
    st.divider()
    next=st.button("Next")
    if next:
        st.session_state['data_set']=True
        st.rerun()

elif not st.session_state['Dashboard']:
    st.header("📋 Patient Dashboard")
    st.divider()
    st.markdown("""
        Welcome to the **Patient Dashboard** 🧾

        This section provides a detailed overview and visual analysis of hospital records.

        You can:
        - 📌 **Explore patient statistics** such as average age, billing, and admission trends.
        - 📊 **Visualize data** by status, date, and illness.
        - 🧮 **Get insights** like top billing records, oldest/youngest patients, and daily trends.

        Use the tabs above to switch between:
        - **Analysis Tab:** Text-based metrics and record summaries.
        - **Dashboard Tab:** Graphical visualizations of hospital operations.
        - **Body Mass Index Tab:** To Understand Patient/Custom Body Mass Index.
            -  BMI Categories (WHO standard):            
                - Underweight: < 18.5
                - Normal weight: 18.5–24.9
                - Overweight: 25–29.9
                - Obese: ≥ 30
        """)

    tab1,tab2,tab3=st.tabs(['Analysis','Dashboard','BMI Caluclator'])
    df=pd.DataFrame(sqlitepac.show_all(),columns=['name','age','illness','bill','date','status','height','weight'])
    with tab1:
        a=st.selectbox("Select what you want",['--Select--','Mean','Status Records','Maxbill Recorded','Oldest','Youngest','Patients per day'])
        if a=='Mean':
            age=st.checkbox("Mean of Age")
            if age:
                st.write(f'Average age of a Patitent is {df['age'].mean()}')
                st.dataframe(df[['name','age']])
            bill=st.checkbox("Mean of Bill")
            if bill:
                st.write(f'Average Bill for a Patient is {df['bill'].mean()}')
                st.dataframe(df[['name','illness','bill']])
        if a=='Status Records':
            adm=st.checkbox("Records In Hospital")
            if adm:
                st.write("Here is the records of Patients in Hospital")
                st.dataframe(df[df['status']=='admitted'])
            dis=st.checkbox("Patients Discharged")
            if dis:
                st.write("Here is the Records of Discharged Patients")
                st.dataframe(analytics.get_outhospital())
        if a=='Maxbill Recorded':
            st.write("This is the Maximum bill recorded:")
            st.dataframe(analytics.get_maxbill())
        if a=='Oldest':
            st.write("Here is the Oldest patient Recorded")
            st.dataframe(analytics.get_oldest())
        if a=='Youngest':
            st.write("Here is the Youngest Patient Recorded")
            st.dataframe(analytics.get_youngest())
        if a == 'Patients per day':
            st.write("📅 Number of patients recorded each day:")    
            df['only_date'] = pd.to_datetime(df['date']).dt.date
            patient_counts = df.groupby('only_date').size().reset_index(name='Patient Count')
            st.dataframe(patient_counts)
    with tab2:
        perday=st.selectbox("Choose Anthor variable for analysis",['--Select--','Status','Admitted','Discharged','Total','Average'])
        if perday=='Status':
            df=pd.DataFrame(sqlitepac.show_all(),columns=['name','age','illness','bill','date','status','height','weight'])

            st.write("Status of Patient v/s Total Bill")
            df=plotings.status_bills()
            if st.checkbox("Show data"):
                st.dataframe(df)
            st.bar_chart(df.set_index('status'))
        if perday=='Admitted':
            df=pd.DataFrame(sqlitepac.show_all(),columns=['name','age','illness','bill','date','status','height','weight'])

            st.write('Admitted vs Days')
            df=plotings.admitted_per_day()
            if st.checkbox("show data"):
                st.dataframe(df)
            st.bar_chart(df.set_index('date'))
        if perday=='Discharged':
            df=pd.DataFrame(sqlitepac.show_all(),columns=['name','age','illness','bill','date','status','height','weight'])

            st.write(" Discharged v/s Days")
            df=plotings.discharged_per_day()
            if st.checkbox("Show Data"):
                st.dataframe(df)
            st.bar_chart(df.set_index('date'))
        if perday=='Total':
            df=pd.DataFrame(sqlitepac.show_all(),columns=['name','age','illness','bill','date','status','height','weight'])

            st.write("Total bills v/s Days")
            df=plotings.daily_total_bills()
            if st.checkbox("Show data"):
                st.dataframe(df)
            st.bar_chart(df.set_index('date'))   
        if perday=='Average':
            df=pd.DataFrame(sqlitepac.show_all(),columns=['name','age','illness','bill','date','status','height','weight'])
            st.write('Average Bill in Day')
            df=plotings.daily_avg_bills()
            if st.checkbox("Show Data"):
                st.dataframe(df)
            st.bar_chart(df.set_index('date'))  
    with tab3:
        df=pd.DataFrame(sqlitepac.show_all(),columns=['name','age','illness','bill','date','status','height','weight'])
        df['bmi'] = df.apply(lambda row: row['weight'] / ((row['height'] / 100) ** 2) if row['height'] > 0 else None, axis=1)
        df['bmi'] = df['bmi'].round(2)

        def bmi_category(b):
            if b < 18.5:
                return 'Underweight'
            elif b < 25:
                return 'Normal'
            elif b < 30:
                return 'Overweight'
            else:
                return 'Obese'

        df['result'] = df['bmi'].apply(bmi_category)

        if st.checkbox("Show Patients BMI Records"):
            st.dataframe(df[['name','age','height','weight','bmi','result']])
        if st.checkbox("Custom BMI calculator"):
            l={
                'Height':None,'Weight':None
            }
            with st.form('Custom'):
                l['Height']=st.number_input("Enter Height(in centimeters):")
                l['Weight']=st.number_input("Enter Weight(in KG):")
                s=st.form_submit_button("Check")
            if s:
                if not all(l.values()):
                    st.warning("🚫Enter Data completely!")
                else:
                    b=l['Weight']/((l['Height']/100)**2)
                    b=round(b,2)
                    st.success(f'BMI ={b}  {bmi_category(b)}')

    st.divider()
    if st.button("Back"):
        st.session_state['data_set']=False
        st.rerun()
    if st.button("Logout"):
        st.session_state['loggedin'] = False
        st.session_state['name'] = None
        st.session_state['stype']=None
        st.session_state['data_set']=False
        st.session_state['Dashboard']=False
        st.rerun()
