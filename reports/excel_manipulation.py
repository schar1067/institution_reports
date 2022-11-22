import openpyxl
import pandas as pd


def excel_write(df,file:str,sheet_name:str,startcol=1,startrow=3):
    
    df.to_excel(file, sheet_name=sheet_name,
                engine='openpyxl',startcol=startcol,
                startrow=startrow)


def excel_append(df,file:str,sheet_name:str,
                startcol=1,startrow=3,mode='a'):
    
    with pd.ExcelWriter(file,engine="openpyxl", mode=mode,if_sheet_exists='overlay') as writer:  
        df.to_excel(writer, sheet_name=sheet_name,
                   startcol=startcol,
                   startrow=startrow)

def insert_img(xlsx_file:str,img_loc:str,
        anchor_cell:str,
        img_width:int = 900,
        img_height:int = 400,
        worksheet_idx:int=0)->None:
    
    wb = openpyxl.load_workbook(xlsx_file)
    ws = wb.worksheets[worksheet_idx]
    img = openpyxl.drawing.image.Image(img_loc)
    img.width = img_width
    img.height = img_height
    ws.add_image(img, anchor_cell)
    wb.save(xlsx_file)

def remove_gridlines(xlsx_file:str, worksheet_idx:int=0):
    wb = openpyxl.load_workbook(xlsx_file)
    ws = wb.worksheets[worksheet_idx]
    ws.sheet_view.showGridLines = False
    wb.save(xlsx_file)