#!/usr/bin/env python
# coding: utf-8

# In[1]:


# !pip install dash-bootstrap-components!
# !pip install pycountry


# ### Import Libraries

# In[2]:


import plotly.express as px
from dash import Dash  , html , dcc
from jupyter_dash import JupyterDash 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output , State
import dash
import dash_bootstrap_components as dbc


# In[3]:


FONT_AWESOME = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"


# ### Read Data

# In[4]:


app = JupyterDash(external_stylesheets = [dbc.themes.BOOTSTRAP , FONT_AWESOME])


# In[5]:


# link dataset
# https://hdr.undp.org/data-center/documentation-and-downloads
# this link provide multiple datasets, and we used the useful ones to create our dashboard


# In[6]:


df1 = pd.read_csv('./Gender_Inequality_Index.csv')
df2 = pd.read_csv("./Years.csv")
df3 = pd.read_csv('./payregedit.csv')
df5 = pd.read_csv('./ParliamentSeats.csv')
df6 = pd.read_csv('./labourreglast.csv')
df7 = pd.read_csv('./payreglast.csv')


# ### Data Preparation

# In[7]:


df1.head()


# In[8]:


df1.isna().sum()


# In[9]:


df1 = df1.drop(["Rank", "Maternal_mortality","Adolescent_birth_rate"], axis='columns')


# In[10]:


for col in ["GII","Seats_parliament","F_secondary_educ","M_secondary_educ","F_Labour_force","M_Labour_force"]:
    df1[col] = df1.groupby('Human_development')[col].apply(lambda x: x.fillna(x.median()))


# In[11]:


df1.isna().sum()


# In[12]:


df1 = df1[df1.isnull().sum(axis=1) < 4]


# In[13]:


df1.isna().sum()


# In[14]:


import pycountry
input_countries = df1['Country']

countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3

codes = [countries.get(country) for country in input_countries]

df1['ISO-Code']=codes


# In[15]:


df2.head()


# In[16]:


df2.isna().sum()


# In[17]:


if df2.iloc[:, 1:].isnull().all(axis=0).any():
    print("There are columns (excluding the first column) with all NaN values in the DataFrame.")
else:
    print("There are no columns (excluding the first column) with all NaN values in the DataFrame.")


# In[18]:


df2 = df2.dropna(axis=1, how='all')


# In[19]:


my_list = ['Afghanistan','Angola','Afghanistan', 'Angola', 'Albania', 'Andorra', 'United Arab Emirates', 'Argentina', 'Armenia', 'Antigua and Barbuda', 'Australia', 'Austria',  'Azerbaijan','Burundi', 'Belgium', 'Benin', 'Burkina Faso', 'Bangladesh', 'Bulgaria', 'Bahrain', 'Bahamas', 'Bosnia and Herzegovina', 'Belarus','Belize', 'Bolivia (Plurinational State of)','Brazil', 'Barbados', 'Brunei Darussalam', 'Bhutan', 'Botswana', 'Central African Republic','Canada', 'Switzerland','Chile', 'China', 'CÃ´te d Ivoire', 'Cameroon', 'Congo (Democratic Republic of the)', 'Congo',  'Colombia', 'Comoros', 'Cabo Verde', 'Costa Rica', 'Cuba', 'Cyprus', 'Czechia', 'Germany' ,'Djibouti', 'Dominica', 'Denmark', 'Dominican Republic','Algeria', 'Ecuador','Egypt', 'Eritrea','Spain', 'Estonia', 'Ethiopia',  'Finland', 'Fiji', 'France', 'Micronesia (Federated States of)', 'Gabon','United Kingdom', 'Georgia', 'Ghana', 'Guinea', 'Gambia',  'Guinea-Bissau', 'Equatorial Guinea', 'Greece',  'Grenada', 'Guatemala','Guyana', 'Hong Kong, China (SAR)', 'Honduras', 'Croatia', 'Haiti', 'Hungary', 'Indonesia', 'India', 'Ireland', 'Iran (Islamic Republic of)', 'Iraq', 'Iceland','Italy', 'Jamaica', 'Jordan', 'Japan', 'Kazakhstan', 'Kenya',  'Kyrgyzstan',  'Cambodia', 'Kiribati', 'Saint Kitts and Nevis', 'Korea (Democratic Peoples Rep. of)' ,'Kuwait', 'Lao People s Democratic Republic',  'Lebanon', 'Liberia', 'Libya',  'Saint Lucia', 'Liechtenstein', 'Sri Lanka', 'Lesotho', 'Lithuania', 'Luxembourg', 'Latvia', 'Morocco', 'Monaco', 'Moldova (Republic of)', 'Madagascar', 'Maldives',  'Mexico', 'Marshall Islands', 'North Macedonia',  'Mali', 'Malta', 'Myanmar', 'Montenegro', 'Mongolia','Mozambique','Mauritania', 'Mauritius','Malawi', 'Malaysia','Namibia','Niger','Nigeria','Nicaragua','Netherlands','Norway','Nepal','Nauru','New Zealand','Oman','Pakistan','Panama','Peru','Philippines','Palau','Papua New Guinea','Poland','Korea (Democratic Peoples Rep. of)','Portugal','Paraguay','Palestine','Qatar', 'Romania','Russian Federation','Rwanda','Saudi Arabia','Sudan','Senegal','Singapore', 'Solomon Islands','Sierra Leone','El Salvador', 'San Marino', 'Somalia', 'Serbia', 'South Sudan','Sao Tome and Principe','Suriname','Slovakia', 'Slovenia', 'Sweden','Eswatini (Kingdom of)','Seychelles','Syrian Arab Republic','Chad','Togo','Thailand','Tajikistan','Turkmenistan','Timor-Leste','Tonga', 'Trinidad and Tobago','Tunisia', 'Turkey','Tuvalu', 'Tanzania (United Republic of)','Uganda','Ukraine','Uruguay', 'United States','Uzbekistan','Saint Vincent and the Grenadines','Venezuela (Bolivarian Republic of)', 'Viet Nam','Vanuatu','Samoa','Yemen','South Africa','Zambia','Zimbabwe', 'Very high human development', 'High human development','Medium human development', 'Low human development','Arab States','East Asia and the Pacific', 'Europe and Central Asia', 'Latin America and the Caribbean','South Asia', 'Sub-Saharan Africa', 'World']
strings_to_delete = ['Andorra', 'Antigua and Barbuda', 'Comoros', 'Djibouti', 'Dominica', 'Equatorial Guinea', 'Eritrea', 'Grenada', 'Hong Kong, China (SAR)', 'Kiribati', 'Liechtenstein', 'Marshall Islands', 'Micronesia (Federated States of)', 'Monaco', 'Nauru', 'Palau', 'Palestine', 'Saint Kitts and Nevis', 'San Marino', 'Seychelles', 'Solomon Islands', 'Somalia', 'Tuvalu', 'Vanuatu']
for string in strings_to_delete:
    if string in my_list:
        my_list.remove(string)


# In[20]:


if df2.iloc[:, 1:].isnull().all(axis=0).any():
    print("There are columns (excluding the first column) with all NaN values in the DataFrame.")
else:
    print("There are no columns (excluding the first column) with all NaN values in the DataFrame.")


# In[21]:


df_unpivot = pd.melt(df2, id_vars='Year', value_vars = my_list)


# In[22]:


df_unpivot


# In[23]:


df_unpivot.to_csv('final_years.csv', index=False)


# In[24]:


df2 = pd.read_csv("final_years.csv")
df2.head()


# In[25]:


df2.isna().sum()


# In[26]:


df2['value'] = df2['value'].fillna(method='ffill')


# In[27]:


df2.isna().sum()


# In[28]:


df3.head()


# In[29]:


df3.isna().sum()


# In[30]:


df5.head()


# In[31]:


df5.isna().sum()


# In[32]:


df6.head()


# In[33]:


df6.isna().sum()


# ### Dashboard

# In[34]:


# impoet Dash & Plotly
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
#---------------------------------------------------------NAV_LOGO----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PLOTLY_LOGO = "https://static.vecteezy.com/system/resources/previews/002/040/874/non_2x/gender-inequality-icon-on-white-eps-vector.jpg"
#----------------------------------------------------------Static-Bar-chart-Info-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
fig = px.bar(df7, x="Pay", y="Region",
             color="Sex",
             barmode='group',orientation='h',color_discrete_sequence=px.colors.qualitative.Pastel1,category_orders={"Region": ['Europe and Central Asia','Arab States', 'East Asia and the Pacific', 'Latin America and the Caribbean', 'South Asia', 'Sub-Saharan Africa']},
             height=400,width=750,labels={"Pay":"Average income in k$"})

fig.update_xaxes(categoryorder='array', categoryarray= ['0','2,3', '2,9', '4,4', '4,7', '10,4', '10,6', '12,3', '13,1', '18,4', '18,7', '21,6', '25,8'])
fig.update_layout(
    font=dict(family="Lucida Console"))

#------------------------------------------------BANs-Style---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
card_icon = {
    "color": "#000000",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
card_style = {
       'color': '#6C757D',
       'text-align': 'center',
       'font-weight': 'bold',
        "font-family": "Lucida Console"
  }

#------------------------------------------------BANs-Info---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
card1 = dbc.CardGroup([
        dbc.Card(dbc.CardBody(
            [html.P("World Gender Inequality Index", className="card-title",style=card_style),
             html.H1("46.5%", className="card-text",style=card_style),
             html.P("(GII) provides insights into gender disparities in different dimensions,varies between 0 (when women and men fare equally) and 1 (when men or women not fare equally.)",style={'color': '#6C757D','text-align': 'center',"font-family": "Lucida Console"}),])),
        dbc.Card(html.Div(className="fa-solid fa-venus-mars", style=card_icon),style={"maxWidth": 75 ,'backgroundColor':'#CDEFEB'},),
        ],className="mt-4 shadow",)

card2 = dbc.CardGroup([
        dbc.Card(dbc.CardBody(
                [html.P("World Male Labour Force 2021", className="card-title",style={'color': '#6C757D','text-align': 'center',"font-family": "Lucida Console"}),
                 html.H1("71.69%", className="card-text",style=card_style),])),
        dbc.Card( html.Div(className="fa-solid fa-gears", style=card_icon),style={"maxWidth": 75 ,'backgroundColor':'#B3CDE3'},
        ),],className="mt-4 shadow",)

card3 = dbc.CardGroup([dbc.Card(
        dbc.CardBody(
            [html.P("World Female LabourForce 2021", className="card-title",style={'color': '#6C757D','text-align': 'center',"font-family": "Lucida Console"}),
             html.H1("46.2%", className="card-text",style=card_style),])),
        dbc.Card(html.Div(className="fa-solid fa-gears", style=card_icon),style={"maxWidth": 75 ,'backgroundColor':"#FBB4AE"},
        ),],className="mt-4 shadow",)

card4 = dbc.CardGroup([
        dbc.Card(dbc.CardBody(
            [html.P("World Male Wages 2021", className="card-title",style={'color': '#6C757D','text-align': 'center',"font-family": "Lucida Console"}),
             html.H1("$21K", className="card-text",style=card_style),])),
        dbc.Card(html.Div(className="fa-solid fa-dollar-sign", style=card_icon),style={"maxWidth": 75,'backgroundColor':'#B3CDE3'},
        ),],className="mt-4 shadow",)

card5 = dbc.CardGroup([
        dbc.Card(dbc.CardBody(
            [html.P("World Female Wages 2021", className="card-title",style={'color': '#6C757D','text-align': 'center',"font-family": "Lucida Console"}),
             html.H1("$12K", className="card-text",style=card_style),])),
        dbc.Card(html.Div(className="fa-solid fa-dollar-sign", style=card_icon),style={"maxWidth": 75,'backgroundColor':"#FBB4AE"},
        ),],className="mt-4 shadow",)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#App Layout
app.layout = html.Div([

# Navbar
dbc.Navbar([
    dbc.Container(
        [   html.Img(src=PLOTLY_LOGO, height="100px"),
            html.H1('World Gender Inequality' ,style={"font-family":"Lucida Console"}),
        ],className='d-flex align-items-center justify-content-center',style={'font-weight': 'bold', 'font-size': '24px'}
        ),
    dbc.NavItem(dbc.NavLink(html.Img(src="https://www.svgrepo.com/show/35001/github.svg", height="50px",style={ 'margin-right' : '4rem'}), active=True, href="https://github.com/radwaayman22/Visualization_Project-ITI_9_Month_Intake43-.git")),],color='#FFFFFF', light=True),
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Body 
#-----------------------------------------------------------------BANS-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
dbc.Row([
   dbc.Col([dbc.Container([
          dbc.Row(dbc.Col([card1])),
          dbc.Row([dbc.Col([card2]),dbc.Col([card3])]),
          dbc.Row([dbc.Col([card4]),dbc.Col([card5])]),],className='mt-4',style={"height":"34em","border-width": "medium"},)],width = 5),
#-----------------------------------------------------------------MAP--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                     
   dbc.Col([ dbc.Card([
             dbc.CardHeader([dcc.Dropdown(id = "candidate2", 
                                          options=[{'label': 'Very high', 'value': 'Very high'},
                                                   {'label': 'High', 'value': 'High'},
                                                   {'label': 'Medium', 'value': 'Medium'},
                                                   {'label': 'Low', 'value': 'Low'}],
                                          value='Very high',
                                          multi = False
                           )]),
           dbc.CardBody([dcc.Graph(id="graph",style={'box-shadow': '2px 2px 5px rgba(0,0,0,0.1)'})]),
           dbc.CardFooter([html.H5("GII Rank based on Countries Human Development Index  ", className="card-text",style = {'text-align': 'center','color': '#6C757D',"font-family":"Lucida Console"}),],className ='bg-white'),
           ],className='mt-4' ,style={"height":"34em","border-width": "medium" , 'margin-left' : '2rem'})],width = 6),
           ], className = '',justify='center'),
    
#-----------------------------------------------------------------Bar-Chart-1--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                     
dbc.Row([  
   dbc.Col([dbc.Row([
            dbc.Card([
            dbc.CardBody(dbc.Row([dbc.Card([dbc.CardBody(dcc.Graph(figure=fig))],className='mt-4')]),),
            dbc.CardFooter([html.H5("Gender average pay gap in dollars", className="card-text",style = {'text-align': 'center','color': '#6C757D',"font-family":"Lucida Console"}),],className ='bg-white'),
                     ],className='mt-4',style={"height":"37rem","border-width": "medium"})],className = '',justify='center'),
#-----------------------------------------------------------------Table--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                        
            dbc.Row([dbc.Col([
            dbc.Card([
                dbc.CardBody(dbc.Row([dbc.Card([dbc.CardBody(dbc.Table.from_dataframe(df6, striped=False, bordered=False, hover=True ,color = "#DCDEFC"))])]),),
                dbc.CardFooter([html.H5("Female Labour Force Vs Male Labour Force based on Regions", className="card-text",style = {'text-align': 'center','color': '#6C757D',"font-family":"Lucida Console"}),],className ='bg-white'),
                     ],className='mt-4',style={"height":"26rem","border-width": "medium"})])  
        ],className = '',justify='center'),], width = 5),
    
#-----------------------------------------------------------------Line-Chart--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
    dbc.Col([dbc.Row([
                dbc.Card([
                    dbc.CardHeader([
                            dcc.Dropdown(
                            id = "candidate1",
                           options=[{'label': i, 'value': i} for i in df2["variable"].unique()],
                           value='Egypt',
                           multi=True),]),
                    dbc.CardBody(dcc.Graph(id="line")),
                   dbc.CardFooter([html.H5("Country GII ", className="card-text",style = {'text-align': 'center','color': '#6C757D',"font-family":"Lucida Console"}),],className ='bg-white'),
                ],className ="mt-4",style={"height":"37rem","border-width": "medium" ,'margin-left' : '2rem' })]),
#-----------------------------------------------------------------Question-box--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------               
    dbc.Row([dbc.CardGroup([
             dbc.Card(dbc.CardBody([html.H4("How it differs between males and females in various aspects?", className="card-text",style=card_style),
                                    html.Img(src='https://st.depositphotos.com/1157310/4191/v/950/depositphotos_41917569-stock-illustration-man-and-woman-heads-talking.jpg', height="320px" ,style={"display": "block","margin": "auto","max-width": "100%","max-height": "100%",})])),
             dbc.Card(html.Div(className="fa-sharp fa-solid fa-circle-question", style=card_icon),style={"height":"26rem","maxWidth": 150,'backgroundColor':"#CDEFEB"},),
            ],className ="mt-4",style={'margin-left' : '2rem' }),]),], width = 6)], className = '',justify='center'),

#-----------------------------------------------------------------Drop-Down--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                            
    dbc.Row([dbc.Col([dbc.Card([
                      dbc.CardBody([dcc.Dropdown(
                              id="dropdown3",
                              options=df1['Country'],
                              value="Egypt",
                              clearable=False,),]),]
           )],width = 11),],className ="mt-4",style={'text-align': 'center','color': '#6C757D',"font-family":"Lucida Console","maxHeight": 500},justify='center'), 
    html.Br(),
#-----------------------------------------------------------------Bar-Chart-2--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------               
    dbc.Row([
        dbc.Col([dbc.Card([
               dbc.CardBody(dcc.Graph(id="graph3")),
               dbc.CardFooter([html.H5("Gender labour force per country ", className="card-text",style = {'text-align': 'center','color': '#6C757D',"font-family":"Lucida Console"}),],className ='bg-white'),
            ]),], width=4),
#-----------------------------------------------------------------Bar-Chart-3--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------               
        dbc.Col([dbc.Card([
               dbc.CardBody(dcc.Graph(id="graph4")),
               dbc.CardFooter([html.H5("Gender education per country ", className="card-text",style = {'text-align': 'center','color': '#6C757D',"font-family":"Lucida Console"}),],className ='bg-white'),
              ]),], width = 4),                 
#-----------------------------------------------------------------pie-chart---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------               
        dbc.Col([dbc.Card([        
            dbc.CardBody(dcc.Graph(id="graph2")),
           dbc.CardFooter([html.H5("Gender parliament seats per country",  className="card-text",style = {'text-align': 'center','color': '#6C757D',"font-family":"Lucida Console"}),],className ='bg-white'),
        ],)], width = 3),],className = '',justify='center',),    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                       
],style={'backgroundColor': '#E4E5E7'})
#------------------------------------------------------------Define callbacks---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------MAP----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.callback(
    Output("graph", "figure"), 
    Input("candidate2", "value"))
def display_choropleth(candidate2):
    c_df =df1[df1["Human_development"] == candidate2]
    fig = px.choropleth(
        c_df,
        locations  = 'ISO-Code',
        color = "GII",
        hover_name="Country",
        hover_data = "GII",
        height =350,
       )
    fig.update_layout(
        legend=dict(
            yanchor="top",
            y=0.01,
            xanchor="left",
            x=0.09,
            bgcolor=None))
    return fig
#--------------------------------------------------------------Line-chart------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.callback(
    Output("line", "figure"), 
    Input("candidate1", "value"))

def display_choropleth(candidate1):
    c_df = pd.Series()
    for i in candidate1:
        c_df = pd.concat([c_df, df2[df2["variable"] == i]], ignore_index = True)
    fig = px.line(c_df , x = 'Year' , y = 'value' ,labels={"value":"GII" , 'variable':"Countries"},color='variable', hover_name= 'variable' ,range_y=[0,1],markers=True ,height =450)
    
    fig.update_layout(
    template='plotly_white',
    colorway=px.colors.qualitative.Pastel,
    legend_bordercolor='white'),
    return fig
#------------------------------------------------------------Bar-charts--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.callback(
    Output("graph3", "figure"), 
    Output('graph4','figure'),
    Output("graph2", "figure"),
    Input("dropdown3", "value"),
    )
def update_bar_chart(value):
    df1_c = df1[df1["Country"]== value]
    fig1 = px.bar(df1_c, x=df1_c["Country"], y=['F_Labour_force', 'M_Labour_force'],labels={"value":"Labour_force",'variable':"Gender",'F_Labour_force':'Female','M_Labour_force':'Male'},
              barmode='group', color_discrete_sequence=px.colors.qualitative.Pastel1 ,
             height=400 )
    fig1.update_layout(
       margin={"r":0,"t":0,"l":0,"b":0} ,barmode='group', bargap=0.2 , bargroupgap=0.0
        )

    fig1.update_traces(width=0.15)
    fig2 = px.bar(df1_c, x=df1_c["Country"], y=['F_secondary_educ' ,'M_secondary_educ'],labels={"value":"secondary_educ",'variable':"Gender","F_secondary_educ":"Female",'M_secondary_educ':'Male'},
               barmode='group', color_discrete_sequence=px.colors.qualitative.Pastel1 ,
             height=400 )
    fig2.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0} ,barmode='group', bargap=0.2 , bargroupgap=0.0
         )

    fig2.update_traces(width=0.15)
    country_data = df5[df5["country"]== value]
    total_column1 = country_data['F_ParliamentSeats'].sum()
    total_column2 = country_data['M_ParliamentSeats'].sum()
    labels = ['F_ParliamentSeats', 'M_ParliamentSeats']

    values = [total_column1, total_column2]
  
    fig3 = px.pie(values=values, names=labels, hole=.3,color=labels, color_discrete_sequence=px.colors.qualitative.Pastel1,width = 450,height=400)
    fig3.update_layout()
    
    return fig1 ,fig2 , fig3
#------------------------------------------------------------Run-server--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

app.run_server(debug=True)


# In[ ]:





# In[ ]:




