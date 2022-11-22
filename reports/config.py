import json
from dataclasses import dataclass,field

@dataclass
class ReportsConfig:
    COLOR_PALETTE:field(default_factory=list)
    LINE_IMG_NAME:str 
    BAR_IMG_NAME:str
    HEAT_IMG_NAME:str
    LOGO:str
    IES:field(default_factory=list)
    PROXY_IES:field(default_factory=list)
    REPORTS_DIR:str


def read_config(config_file:str)-> ReportsConfig:
    with open(config_file) as file:
        data=json.load(file)
        return ReportsConfig(**data)