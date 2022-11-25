import os
import pandas as pd
from config import read_config
from fields_schema import Schema
from kwargs_schema import Kwargs
from nlp import collection_of_search_terms_str
from processing_functions import get_key_teachers
from excel_manipulation import excel_write
from charts import save_bar_plot, save_line_plot, save_world_cloud
from excel_manipulation import insert_img, remove_gridlines
from excel_manipulation import excel_append

config = read_config("./config.json")
BASE_DIR=dir_path = os.getcwd()
IMG_NAME= config.LINE_IMG_NAME
BAR_IMG_NAME= config.BAR_IMG_NAME
HEAT_IMG_NAME=config.HEAT_IMG_NAME
WC_IMG_NAME=config.WC_IMG_NAME
LOGO=config.LOGO
REPORTS_DIR= config.REPORTS_DIR


def create_report_sheet(source_data:pd.DataFrame,
                        ies:str,
                        processing_function:callable,
                        agg_kwargs:Kwargs,
                        fact:str,
                        sheet_name:str,
                        worksheet_idx:int,
                        new_workbook:bool=True,
                        has_type:bool=False,
                        has_worldcloud=False)->None:

    # Define file name

    XLSX_FILE=os.path.join(BASE_DIR,REPORTS_DIR,f'{ies}.xlsx')

   
    # query specific ies data

    ies_data=source_data[source_data.ies==ies]


    # anual comparison

    role=processing_function(
                df=ies_data,
                agg_kwargs=agg_kwargs,
                date_agg_freq='M',
                date_col=Schema.DATE,
                agg_col=Schema.ROLE,
                )


    # create excel and insert dataframe 

    if new_workbook:

        excel_write(df=role,file=XLSX_FILE,
                    sheet_name=sheet_name)
    else:
        excel_append(df=role,file=XLSX_FILE,
                    sheet_name=sheet_name)

    # create line plot and insert it in sheet

    general=processing_function(
                df=ies_data,
                agg_kwargs=agg_kwargs,
                date_agg_freq='M',
                date_col=Schema.DATE,
                agg_col=Schema.IES)

    save_line_plot(df=general,img_name=IMG_NAME,fact=fact)

    insert_img(xlsx_file=XLSX_FILE,
            img_loc=IMG_NAME,
            anchor_cell='I2',
            worksheet_idx=worksheet_idx)

    # create dataframe pivoted by major

    major=processing_function(
                df=ies_data,
                agg_kwargs=agg_kwargs,
                date_col=Schema.DATE,
                date_agg_freq='A-nov',
                agg_col=Schema.MAJOR).iloc[-1].sort_values(ascending=False).to_frame()

    # create bar plot and insert it in sheet 

    save_bar_plot(df=major,
                img_name=BAR_IMG_NAME,
                fact=fact,dim='programa')

    insert_img(xlsx_file=XLSX_FILE,
            img_loc=BAR_IMG_NAME,
            anchor_cell='B26',
            img_height=900,
            worksheet_idx=worksheet_idx)
    
    # anual comparison plot

    anual=processing_function(
                df=ies_data,
                agg_kwargs=agg_kwargs,
                date_agg_freq='A-nov',
                date_col=Schema.DATE,
                agg_col=Schema.IES)
               
    # create bar plot and insert it in sheet 

    save_bar_plot(df=anual,
                img_name=BAR_IMG_NAME,
                fact=fact,dim='año')

    insert_img(xlsx_file=XLSX_FILE,
            img_loc=BAR_IMG_NAME,
            anchor_cell='P25',
            worksheet_idx=worksheet_idx)

    if has_type:
         type=processing_function(
                df=ies_data,
                agg_kwargs=agg_kwargs,
                date_agg_freq='A-nov',
                date_col=Schema.DATE,
                agg_col=Schema.CTYPE)
               
       # create bar plot and insert it in sheet 

         save_bar_plot(df=type,
                        img_name=BAR_IMG_NAME,
                        fact=fact,dim='año')

         insert_img(xlsx_file=XLSX_FILE,
                img_loc=BAR_IMG_NAME,
                anchor_cell='Y3',
                worksheet_idx=worksheet_idx)

    if has_worldcloud:
        collection_words=collection_of_search_terms_str(df_search=ies_data,
                                                        term_col=Schema.SEARCH_TERM)
         
        save_world_cloud(img_name=WC_IMG_NAME,
                       collection_words_str=collection_words)

        insert_img(xlsx_file=XLSX_FILE,
                img_loc=WC_IMG_NAME,
                anchor_cell='Y45',
                worksheet_idx=worksheet_idx)

    # remove gridlines

    remove_gridlines(xlsx_file=XLSX_FILE)

    #insert logo

    insert_img(xlsx_file=XLSX_FILE,
            img_loc=LOGO,
            anchor_cell='A1',
            img_height=30,
            img_width=100,
            worksheet_idx=worksheet_idx)

def create_key_teacher_sheet(source_data:pd.DataFrame, ies:str,sheet_name:str)->None:

    # Define file name

    XLSX_FILE=os.path.join(BASE_DIR,REPORTS_DIR,f'{ies}.xlsx')

    # query specific ies data

    ies_data=source_data[source_data.ies==ies]

    key_teachers=get_key_teachers(ies_data)
    
    excel_append(df=key_teachers,file=XLSX_FILE,
                    sheet_name=sheet_name)