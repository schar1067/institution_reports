from config import read_config
from excel_report_sheet import create_key_teacher_sheet,create_report_sheet
from kwargs_schema import Kwargs
from processing_functions import tweak ,get_list_of_intersection
from queries import Query, Template
from database import BkData, DbName
from fields_schema import Schema

  

def main()-> None:

    config = read_config("./config.json")

    ies_lst = config.IES
    proxy_ies_lst=config.PROXY_IES


    profile=BkData(query=Query(Template.PROFILE).compile_query).fetch_data

    redirect=BkData(database=DbName.STATS,
                 query=Query(Template.REDIRECT).compile_query).fetch_data

    lms=BkData(database=DbName.STATS,
                 query=Query(Template.LMS).compile_query).fetch_data
    
    # proxy=BkData(database=DbName.PROXY,
    #              query=Query(Template.PROXY).compile_query).fetch_data

    content=BkData(database=DbName.STATS,
                query=Query(Template.CONTENT).compile_query).fetch_data

    search=BkData(database=DbName.STATS,
              query=Query(Template.SEARCH).compile_query).fetch_data

    lms_ies=get_list_of_intersection(df=lms,df_col='ies',ies_list=ies_lst)

    search_ies=get_list_of_intersection(df=search,df_col='ies',ies_list=ies_lst)


    for ies in ies_lst:

        sheet_counter = 0
    
        create_report_sheet(source_data=profile,
                            ies=ies,
                            processing_function=tweak,
                            agg_kwargs=Kwargs.REGISTERS,
                            fact='registros',
                            sheet_name='Registros',
                            worksheet_idx=sheet_counter,
                            new_workbook=True)
        
        sheet_counter += 1 

        create_report_sheet(source_data=redirect,
                            ies=ies,
                            processing_function=tweak,
                            agg_kwargs=Kwargs.ACTIVE_USERS,
                            fact='usuarios activos web',
                            sheet_name='usuarios activos',
                            worksheet_idx=sheet_counter,
                            new_workbook=False)

        sheet_counter += 1 

        create_report_sheet(source_data=content,
                            ies=ies,
                            processing_function=tweak,
                            agg_kwargs=Kwargs.CONTENT_REDIRECT,
                            fact='redirecciones',
                            sheet_name='redirecciones',
                            worksheet_idx=sheet_counter,
                            new_workbook=False)

        sheet_counter += 1 

        create_report_sheet(source_data=content,
                            ies=ies,
                            processing_function=tweak,
                            agg_kwargs=Kwargs.CONTENT_CREATED,
                            fact='contenido creado',
                            sheet_name='contenido creado',
                            worksheet_idx=sheet_counter,
                            new_workbook=False,
                            has_type=False
                            )

        sheet_counter += 1 

        if ies in search_ies:
             create_report_sheet(source_data=search,
                            ies=ies,
                            processing_function=tweak,
                            agg_kwargs=Kwargs.SEARCH,
                            fact='Busquedas',
                            sheet_name='busquedas',
                            worksheet_idx=sheet_counter,
                            new_workbook=False,
                            has_type=False,
                            has_worldcloud=True
                            )
             sheet_counter += 1

        if ies in lms_ies:
            create_report_sheet(source_data=lms,
                                ies=ies,
                                processing_function=tweak,
                                agg_kwargs=Kwargs.ACTIVE_USERS,
                                fact='Usuarios activos lms',
                                sheet_name='lms',
                                worksheet_idx=sheet_counter,
                                new_workbook=False,
                                has_type=False
                                )
            
        
        # if ies in proxy_ies_lst:
        #     create_report_sheet(source_data=proxy,
        #                         ies=ies,
        #                         processing_function=tweak_proxy,
        #                         fact='Sesiones',
        #                         sheet_name='proxy',
        #                         worksheet_idx=5,
        #                         new_workbook=False,
        #                         agg_value=None,
        #                         has_type=False
        #                         )

        create_key_teacher_sheet(source_data=content,
                                 ies=ies,
                                 sheet_name='docentes claves')

if __name__ == '__main__':

    main()
