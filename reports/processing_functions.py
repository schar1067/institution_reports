from typing import List
import pandas as pd
from fields_schema import Schema
from kwargs_schema import Kwargs


def get_list_of_intersection(df:pd.DataFrame,df_col:str,ies_list:List)->List:
    lst1=df[df_col].tolist()
    set1=set(lst1)
    set2=set(ies_list)
    return list(set2.intersection(set1))

def generalize_topn(ser,n=10,other='Otro'):
    topn=ser.value_counts().index[:n]
    ser=ser.cat.set_categories(
            topn.set_categories(list(topn)+[other]))
    return ser.where(ser.isin(topn),other)


def elim_top_col_hierarchy(df_):
    cols=[cs[1] for cs in df_.columns.to_flat_index()]
    df_.columns=cols
    return df_


def subset_data_by_date(df,date_col:Schema,date1:str,date2:str):
    
      return (df
                .set_index(pd.to_datetime(df[date_col],infer_datetime_format=True))
                .sort_index() 
                .dropna(subset=date_col) 
                .loc[date1:date2,:])

def tweak(df,agg_kwargs:Kwargs,date_col:Schema, agg_col:Schema,date_agg_freq:str='M'):
    top_creator=df.correo.value_counts().index[:10].tolist()
    return (df
        .assign(fecha=lambda _df:pd.to_datetime(_df[date_col],infer_datetime_format=True),
                rol=lambda _df:_df.rol.where(_df.rol.isin(['student','teacher','admin']),'otro'),
                programa=lambda _df:_df.programa.str.upper().astype('category').pipe(generalize_topn),
                top_creador=lambda _df:_df.correo.where(_df.correo.isin(top_creator),'Otro').str.split('@',expand=True)[0])
        .groupby([pd.Grouper(key=date_col,freq=date_agg_freq),agg_col])
        .agg(agg_kwargs).reset_index()
        .assign(Fecha=lambda _df:_df[date_col].dt.strftime('%b-%Y'))
        .pivot_table(index=[date_col,'Fecha'],
                     columns=[agg_col])
        .fillna(0).astype('int64')
        .droplevel(0)
        .pipe(elim_top_col_hierarchy)          
        ) 

def get_key_teachers(content_df):
    
    
    docentes_claves=(content_df 
        .assign(tipo=lambda df_:df_.tipo.where(df_.tipo.isin(['Booklist']),'otro'))
        .groupby(['correo','rol'])
        .agg(redirecciones=('redirecciones','sum'))
        .query('rol=="teacher" and redirecciones >= 10')
        .fillna(0).astype('Int64')
        .reset_index()
        .drop('rol',axis=1)
        )

    content_created=(content_df 
        .assign(tipo=lambda df_:df_.tipo.where(df_.tipo.isin(['Booklist']),'otro'))
        .groupby(['correo','rol','tipo'])
        .agg(contenido_creado=('titulo','count'))
        .unstack()
        .fillna(0).astype('Int64')
        .pipe(elim_top_col_hierarchy)
        .reset_index()
        .drop('rol',axis=1)
        )

    return (docentes_claves
        .merge(content_created,on='correo',how='inner')
        .assign(contenido_total=lambda df_:df_.Booklist + df_.otro)
        .set_index('correo')
        )