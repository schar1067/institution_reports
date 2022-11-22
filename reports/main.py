from config import read_config
from excel_report_sheet import create_key_teacher_sheet, create_report_sheet
from processing_functions import tweak_profile, tweak_proxy,tweak_redirect,tweak_content,get_list_of_intersection
from queries import Query, Template
from database import BkData, DbName
from fields_schema import Schema

def main()-> None:

    config = read_config("./config.json")

    ies_list = config.IES
    proxy_ies_list=config.PROXY_IES


    profile=BkData(query=Query(Template.PROFILE).compile_query).fetch_data

    redirect=BkData(database=DbName.STATS,
                 query=Query(Template.REDIRECT).compile_query).fetch_data

    lms=BkData(database=DbName.STATS,
                 query=Query(Template.LMS).compile_query).fetch_data
    
    proxy=BkData(database=DbName.PROXY,
                 query=Query(Template.PROXY).compile_query).fetch_data

    content=BkData(database=DbName.STATS,
                query=Query(Template.CONTENT).compile_query).fetch_data

    lms_ies=get_list_of_intersection(df=lms,df_col='ies',ies_list=ies_list)



    for ies in proxy_ies_list:

        create_report_sheet(source_data=profile,
                            ies=ies,
                            processing_function=tweak_profile,
                            fact='registros',
                            sheet_name='Registros',
                            worksheet_idx=0,
                            new_workbook=True,
                            agg_value=None)
        

        create_report_sheet(source_data=redirect,
                            ies=ies,
                            processing_function=tweak_redirect,
                            fact='usuarios activos web',
                            sheet_name='usuarios activos',
                            worksheet_idx=1,
                            new_workbook=False,
                            agg_value=None)

        create_report_sheet(source_data=content,
                            ies=ies,
                            processing_function=tweak_content,
                            fact='redirecciones',
                            sheet_name='redirecciones',
                            worksheet_idx=2,
                            new_workbook=False,
                            agg_value=Schema.REDIRECT
                            )

        create_report_sheet(source_data=content,
                            ies=ies,
                            processing_function=tweak_content,
                            fact='contenido creado',
                            sheet_name='contenido creado',
                            worksheet_idx=3,
                            new_workbook=False,
                            agg_value=Schema.CONTENT_CREATED,
                            has_type=False
                            )
        if ies in lms_ies:
            create_report_sheet(source_data=lms,
                                ies=ies,
                                processing_function=tweak_redirect,
                                fact='Usuarios activos lms',
                                sheet_name='lms',
                                worksheet_idx=4,
                                new_workbook=False,
                                agg_value=None,
                                has_type=False
                                )
        
        if ies in proxy_ies_list:
            create_report_sheet(source_data=proxy,
                                ies=ies,
                                processing_function=tweak_proxy,
                                fact='Sesiones',
                                sheet_name='proxy',
                                worksheet_idx=5,
                                new_workbook=False,
                                agg_value=None,
                                has_type=False
                                )

        create_key_teacher_sheet(source_data=content,
                                 ies=ies,
                                 sheet_name='docentes claves')

if __name__ == '__main__':

    main()
