import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from config import read_config

config = read_config("./config.json")

matplotlib.use('agg')

def save_line_plot(df,img_name:str,fact:str)->None:
    fig,ax= plt.subplots(dpi=600,figsize=(10,4))
    sns.set_style('dark')
    
    (df.plot.line(ax=ax,title=f"{fact} en el tiempo",color=config.COLOR_PALETTE )
    .legend(bbox_to_anchor=(1,1))
    )
    fig.savefig(img_name,dpi=600,bbox_inches='tight')
    plt.close(fig)

def save_bar_plot(df,img_name:str,fact:str,dim:str)->None:
    fig,ax= plt.subplots(dpi=600,figsize=(10,4))
    sns.set_style('dark')
    
    (df.plot.bar(ax=ax,stacked=True,title= f"{fact} por {dim}",color=config.COLOR_PALETTE)
    .legend(bbox_to_anchor=(1,1))
    )

    for container in ax.containers:
        ax.bar_label(container)
        
    fig.savefig(img_name,dpi=600,bbox_inches='tight')    
    plt.close(fig)
    
def save_heatmap(df,img_name:str,fact:str,dim:str)->None:
    fig,ax= plt.subplots(dpi=600,figsize=(10,4))
    sns.set_style('dark')
    
    sns.heatmap(ax=ax,data=df,
            annot=True,
            fmt='d',
            annot_kws={'size': 8},
            cmap='YlGnBu',linewidth=.8)

    ax.set(xlabel=dim)
    ax.set(ylabel='Fecha')
    ax.set(title=f'{fact} por {dim} 2022')
    plt.yticks(rotation=0)
    fig.savefig(img_name,dpi=600,bbox_inches='tight') 
    plt.close(fig)