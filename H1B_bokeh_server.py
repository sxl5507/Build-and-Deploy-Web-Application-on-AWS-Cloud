# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 16:50:01 2018

@author: Siyan
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 11:08:29 2018

@author: Siyan
"""

import pandas as pd
import re
import numpy as np

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.formatters import BasicTickFormatter
from bokeh.models.widgets import TextInput,Div,RadioGroup,DataTable,TableColumn,Button,Panel,Tabs
from bokeh.plotting import figure
from bokeh.layouts import row, column, widgetbox
from bokeh.palettes import viridis




# =============================================================================
#  load csv to df, set smaller chunksize for small RAM
#  filename: string; index: string
# =============================================================================
def LoadData(filename, chunksize=100000, index= None):
    temp=[]
    dtype= {'FULL_TIME_POSITION': 'str'}
    chunk_load=pd.read_csv(filename, dtype= dtype,
                           chunksize=chunksize, engine= 'c') # c engine is faster
    # filter data, drop empty columns, set date as index
    print('Loading: {}...'.format(filename))
    for chunk in chunk_load:
            temp.append(chunk)
    df = pd.concat(temp, ignore_index= True)
    print('Done!\n')
    if index!= None:
        df.set_index(index, drop=True, inplace=True) # set CASE_NUMBER as index
    return df





# =============================================================================
#  search keywords return its frequency in pd series
#  input: data (pd series), target_list (string or list of string)
#  set <remove_punct> = False for exact match
# =============================================================================
def MatchCount (data, target_list, remove_punct= True):
    validation= np.sum([_.isalnum() for _ in target_list]) # meaningless string is not allowed
    if validation==0:
        message0.text='<font color="#990000"><b>Error:</b> Keyword is not valid, \
        make sure it contains an alphanumeric value\
        (empty space can cause the error).</font>'
        return None
    message0.text= '<font color="#29a329"><b>Searching...</b></font>'

    if type(target_list)== type('string'): target_list= target_list.split(',')
    data= data.value_counts()
    index= data.index.values
    return_series= [] # append pd series together

    if remove_punct== True:
        # remove all special characters, punctuation and spaces
        index_remove_punct= []
        for i in index: # index is string (eg. employer or title)
            index_remove_punct.append( ''.join(_ for _ in i if _.isalnum()))
        for target in target_list:
            match_list= [] # append names that match specified target
            target= ''.join(_ for _ in target if _.isalnum()).upper()
            for i, j in enumerate(index_remove_punct):
                if re.search(target, j): # match value in <index_remove_punct>
                    match_list.append(index[i]) # return value in <index>
            return_series.append(data.loc[match_list])
    else:
        for target in target_list:
            match_list= [] # append names that match specified target
            target= target.upper()
            for j in index:
                if re.search(target, j):
                    match_list.append(j)
            return_series.append(data.loc[match_list])

    l= len(return_series)
    print('MatchCount: A list ({} items) of pandas.Series is returned\n'.format(l))
    return return_series







#%% bokeh server function (data update)

file_list= ['H-1B_Disclosure_Data_FY15to17']
source = ColumnDataSource() # table data
source_title_match = ColumnDataSource() # matches of employer serach
source_emp_match = ColumnDataSource() # matches of title serach
loading_status='initialize' # load data only one time




# =============================================================================
#  update table based on searched keywords
#  (record status to optimize search
#  eg. after employer is searched, new entered title values will not casuse re-search on employer name
#  instead, title is searched by using previous result of employer search)
# =============================================================================
se_value_old, st_value_old= None, None
def table_update():
    global loading_status, df, emp, title
    global se_value_old, st_value_old, df_match_emp, df_match_title, match_flatten_emp, match_flatten_title
    if loading_status== 'initialize': # load data only one time
        message0.text= '<font color="#29a329"><b>Loading data...</b></font>'
        df= LoadData(file_list[0]+ '.csv').drop('CASE_NUMBER',axis=1)
        # show recent year first by set [default_sort='descending']
        columns = [TableColumn(field=i, title=i, default_sort='descending', width=150) for i in df.columns]
        table_data.columns= columns
        loading_status='done' # change values to avoid reload data


    match_flatten=[]
    top_n= [50, 150, 500][radioGroup_show_rows.active]  # return top n rows in search table
    se_value, st_value= search_employer.value, search_title.value # dtype: str
    # response to different search situation
    if (se_value !='') & (st_value ==''):
        if se_value_old != se_value: # only do search if value is changed
            emp= MatchCount(df['EMPLOYER_NAME'], se_value)
            if emp==None: return None # stop fuction if MatchCount validation is failed (by return None)
            for _ in emp: match_flatten.extend(_.index)
            df_match_emp= df[df['EMPLOYER_NAME'].isin(match_flatten)]
            df_match= df_match_emp; match_flatten_emp= match_flatten
            se_value_old= se_value # use str to make a copy
        else: df_match= df_match_emp.copy()


    elif (se_value =='') & (st_value !=''):
        if st_value_old != st_value: # only do search if value is changed
            title= MatchCount(df['JOB_TITLE'], st_value)
            if title==None: return None # stop fuction if validation is failed
            for _ in title: match_flatten.extend(_.index)
            df_match_title= df[df['JOB_TITLE'].isin(match_flatten)]
            df_match= df_match_title; match_flatten_title= match_flatten
            st_value_old= st_value
        else: df_match= df_match_title.copy()


    elif (se_value !='') & (st_value !=''):
        emp_flatten, title_flatten= [], []
        if (se_value_old != se_value) :
            emp= MatchCount(df['EMPLOYER_NAME'], se_value)
            if emp==None: return None # stop fuction if MatchCount validation is failed (by return None)
            for _ in emp: emp_flatten.extend(_.index) # local variable: emp_flatten
            df_match_emp= df[df['EMPLOYER_NAME'].isin(emp_flatten)]
            match_flatten_emp= emp_flatten
            se_value_old= se_value # use str to make a copy
        if st_value_old != st_value: # only do search if value is changed
            title= MatchCount(df['JOB_TITLE'], st_value)
            if title==None: return None # stop fuction if validation is failed
            for _ in title: title_flatten.extend(_.index) # local variable: title_flatten
            df_match= df_match_emp[df_match_emp['JOB_TITLE'].isin(title_flatten)]
        else:
            df_match= df_match_emp[df_match_emp['JOB_TITLE'].isin(match_flatten_title)]

    else:
        message0.text= '<font color="#990000"><b>Error:</b> Enter Keyword</font>'
        return None


    # prepare data for [possible match] table
    if se_value !='' :
        emp_match= pd.concat(emp).reset_index()
        emp_match.columns=['EMPLOYER_NAME', 'Count']
        source_emp_match.data= emp_match[:25].to_dict('list')
    if st_value !='' :
        title_match= pd.concat(title).reset_index()
        title_match.columns=['JOB_TITLE', 'Count']
        source_title_match.data= title_match[:25].to_dict('list')


    total_rows= df_match.shape[0]
    ctf_rows= df_match['CASE_STATUS'].isin(['CERTIFIED', 'Certified-Withdrawn']).sum()
    message0.text= '<font color="#29a329"><b>Total {} records \
    ({} Certified and Certified-Withdrawn cases)</b></font>'.format(total_rows, ctf_rows)
    source.data= df_match[:top_n].to_dict('list') # data for search table








#%% bokeh plots and layout of search tab


# =============================================================================
#  plots data and design
# =============================================================================
top_n_plot= 40
df_emp= LoadData('top 100 employer.csv').sort_index(ascending=False)
df_title= LoadData('top 100 job title.csv').sort_index(ascending=False)
source_emp = ColumnDataSource(df_emp[-top_n_plot:].to_dict('list')) # employer plot, top 45
source_emp.add(name='color', data= viridis(top_n_plot)) # add color column
source_title = ColumnDataSource(df_title[-top_n_plot:].to_dict('list')) # title plot, top 45
source_title.add(name= 'color', data= viridis(top_n_plot))

# plot, tools, panel (top employers)
p_emp = figure(y_range= df_emp['EMPLOYER_NAME'][-top_n_plot:].tolist(),
               plot_height=600, plot_width=800, x_axis_label='Quantity', 
               title="Top {} H-1B Sponsors (2015-2017)".format(top_n_plot),
               tools='ywheel_zoom, xwheel_zoom, pan, save, reset', active_scroll= 'ywheel_zoom')
p_emp.add_tools(HoverTool(tooltips= [('employer','@EMPLOYER_NAME'), ('frequency','@Count')]))
p_emp.hbar(y='EMPLOYER_NAME', right='Count', height=0.6, source= source_emp, color='color')
panel_emp = Panel(child=p_emp, title="Top Sponsor")

# plot, tools, panel (top titles)
p_title = figure(y_range= df_title['JOB_TITLE'][-top_n_plot:].tolist(),
               plot_height=600, plot_width=800, x_axis_label='Quantity', 
               title="Top {} Sponsored Job Titles (2015-2017)".format(top_n_plot),
               tools='ywheel_zoom, xwheel_zoom, pan, save, reset', active_scroll= 'ywheel_zoom')
p_title.xaxis[0].formatter = BasicTickFormatter(use_scientific = False) # disable scientific notation
p_title.add_tools(HoverTool(tooltips= [('job title','@JOB_TITLE'), ('frequency','@Count')]))
p_title.hbar(y='JOB_TITLE', right='Count', height=0.6, source= source_title, color='color')
panel_title = Panel(child=p_title, title="Top Job Title")






# =============================================================================
#  search box, message, button, data table, match table
# =============================================================================
search_employer = TextInput(value= '', title="Sponsor Search (separate by comma):")
search_title = TextInput(value= '', title="Title Search (separate by comma):")
radioGroup_show_rows = RadioGroup(labels=["show 50 rows", "show 150 rows", "show 500 rows"], active=0, height=120)
message0 = Div(text='<font color="#29a329"><b>Ready! Please Enter Keywords</b></font>', height=30)
# search button and table
search_button = Button(label="Search", button_type="primary")
table_data = DataTable(source= source, width=800, height=350, fit_columns=False)
# update search data (on_click)
search_button.on_click(table_update)


# matched tables with message1 (employer, title)
top_n_match= 25
emp_columns= [TableColumn(field='EMPLOYER_NAME', 
                          title='Similar Sponsors Top {} (include all case status)'.format(top_n_match),
                          default_sort='descending', width=300),
              TableColumn(field='Count', title='Quantity', default_sort='descending', width=100)]
title_columns= [TableColumn(field='JOB_TITLE', 
                            title='Similar Job Titles Top {} ((include all case status))'.format(top_n_match),
                            default_sort='descending', width=300),
                TableColumn(field='Count', title='Quantity', default_sort='descending', width=100)]

table_emp_match= DataTable(source= source_emp_match, width=415, height=350, columns=emp_columns,
                           row_headers=False, fit_columns=False)
table_title_match= DataTable(source= source_title_match, width=415, height=350, columns=title_columns,
                             row_headers=False, fit_columns=False)
#message1= Div(text='<font size=2 color="#ff9900"><br>*Results Include All Case Status</br></font>')





# =============================================================================
#  overall layout, add elements together; use widgetbox to add empty space
# =============================================================================
spacer0= Div(text='<p></p>')
spacer1= Div(text='<p></p>')
pannel_match= Panel(child= column(spacer1, row(widgetbox(table_emp_match, width=450), table_title_match)), 
                    title="Similar Match")
layout_widget= column(search_employer, search_title, radioGroup_show_rows, message0, search_button)
pannel_search = Panel(child= column(spacer0,row(layout_widget, table_data)), title="Input")

tab_search= Tabs(tabs=[pannel_search, pannel_match])
panel_search_match= Panel(child= tab_search, title="Search") # add spacer, transfer tab to panel





tab_all= Tabs(tabs=[panel_search_match, panel_emp, panel_title])
curdoc().add_root(tab_all)
curdoc().title = "H1B Search"
# command to run server
'''
bokeh serve --show H1B_bokeh_server.py
'''


