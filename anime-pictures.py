# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 22:41:06 2023

@author: 198068457
"""

import requests
import bs4
import re
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
from tkinter import filedialog

#去除文件名中的非法字符
def correct_title(title):
    error_set = ['/', '\\', ':', '*', '?', '"', '|', '<', '>']
    for c in title:
        if c in error_set:
            title = title.replace(c, '')
    return title

class CrawlGui:
    def __init__(self,window_name):
        self.window_name=window_name
        self.window_name.attributes("-topmost",1)
        self.window_name.title('anime-pictures downloader')
        self.window_name.geometry('600x600')
        self.window_name.resizable(False,False)
        
        self.lb1=ttk.Label(self.window_name,text='信息栏：')
        self.lb1.place(x=5,y=220,width=70,height=40)
        
        self.lb2=ttk.Label(self.window_name,text='请输入爬取页范围：')
        self.lb2.place(x=5,y=5,width=200,height=40)
        
        self.lb3=ttk.Label(self.window_name,text='到')
        self.lb3.place(x=275,y=5,width=30,height=40)
        
        self.lb4=ttk.Label(self.window_name,text='请输入保存路径：')
        self.lb4.place(x=5,y=45,width=200,height=45)
        
        self.lb5=ttk.Label(self.window_name,text='请输入图片关键词：')
        self.lb5.place(x=5,y=85,width=200,height=45)
        
        self.lb6=ttk.Label(self.window_name,text='          图片尺寸：')
        self.lb6.place(x=5,y=125,width=200,height=45)
        
        self.lb7=ttk.Label(self.window_name,text='X')
        self.lb7.place(x=275,y=130,width=30,height=40)
        #开始页
        self.e1=ttk.Entry(self.window_name)
        self.e1.place(x=200,y=10,width=75,height=30)
        #结束页
        self.e2=ttk.Entry(self.window_name)
        self.e2.place(x=300,y=10,width=75,height=30)
        #路径框
        self.e3=ttk.Entry(self.window_name)
        self.e3.place(x=200,y=45,width=400,height=30)
        #关键词框
        self.e4=ttk.Entry(self.window_name)
        self.e4.place(x=200,y=90,width=400,height=40)
        #尺寸x
        self.e5=ttk.Entry(self.window_name)
        self.e5.place(x=200,y=135,width=70,height=30)
        #尺寸y 
        self.e6=ttk.Entry(self.window_name)
        self.e6.place(x=300,y=135,width=70,height=30)
        
        self.t1=ttk.Text(self.window_name)
        self.t1.pack()
        self.t1.place(x=5,y=260,width=590,height=330)
        
        
        self.button1=ttk.Button(self.window_name,text='开始下载',bootstyle=(PRIMARY, "outline-toolbutton"),command=lambda :self.thread_it(self.run_crawl))
        self.button1.pack()
        self.button1.place(x=100,y=180)
        
        self.button2=ttk.Button(self.window_name,text='选择路径',bootstyle=(PRIMARY, "outline-toolbutton"),command=self.choose_path)
        self.button2.pack()
        self.button2.place(x=200,y=180)
        
        self.button3=ttk.Button(self.window_name,text='全部下载',bootstyle=(PRIMARY, "outline-toolbutton"),command=lambda :self.thread_it(self.run_crawl_all))
        self.button3.pack()
        self.button3.place(x=300,y=180)
        
        #self.e3.insert('end',r'D:\桌面\PixivCralwer\anime-pictures')
    
    def thread_it(self,func,*args):
        self.myThread=threading.Thread(target=func,args=args)
        self.myThread.setDaemon(True)
        self.myThread.start()
        
    def get_params(self):
        params={}
        params['lang']='en'
        params['order_by']='date'
        search_tag=self.e4.get()
        res_x=self.e5.get()
        res_y=self.e6.get()
        if search_tag:
            params['search_tag']=search_tag
        if res_x:
            params['res_x']=res_x
        if res_y:
            params['res_y']=res_y
        return params
        
    def choose_path(self):
        path=filedialog.askdirectory(title='选择下载文件路径：',initialdir=r'D:\桌面\PixivCralwer\download')
        self.e3.delete(0,'end')
        self.e3.insert(0,path)
        
    def run_crawl(self):
        startPage=int(self.e1.get())
        endPage=int(self.e2.get())
        self.crawl(startPage,endPage)
    #下载全部
    def run_crawl_all(self):
        search_tag=self.e4.get()
        params={'search_tag':search_tag,
        'lang':'en',
        'order_by':'date'}
        startUrl=f'https://anime-pictures.net/posts'
        content=requests.get(startUrl,params).text
        page_count=re.findall('in request (.*?) pictures',content)[0]
        page_count=int(page_count)
        self.t1.insert('end',f'共搜索到{page_count}张图片\n')
        page_count=int(page_count/80)
        self.crawl(0,page_count+1)
    
    def crawl(self,startPage,endPage):
        params=self.get_params()
        params['page']=startPage
        startUrl=f'https://anime-pictures.net/posts'
        img_count=0
        if startPage >= endPage:
            self.t1.insert('end','错误：开始页必须小于结束页！\n')
            return
        for i in range(startPage,endPage):
            self.t1.insert('end','-----------------------------------------------------------\n')
            self.t1.insert('end','准备爬取......\n')
            content=requests.get(startUrl,params,verify=False).text
            soup=bs4.BeautifulSoup(content,'html.parser')
            urls=soup.find_all('span',class_='img_block2 img_block_big')
            params['page']+=1
            for each in urls:
                url='https://anime-pictures.net'+each.a['href']
                #print(url)
                html_data=requests.get(url).text
                img_url=re.findall('data-sveltekit-reload href="(.*?)" title="Download picture"',html_data)[0]
                if img_url:
                    img=requests.get(img_url)
                    img_name=img_url.split('/')[-1]
                    img_name=correct_title(img_name)
                    try:
                        img=requests.get(img_url,timeout=10)
                        with open(self.e3.get()+'\\'+img_name,'wb') as f:
                            f.write(img.content)
                            self.t1.insert('end','已下载：'+img_name+'\n')
                            self.t1.see(END)
                            img_count+=1
                    except Exception as e:
                        self.t1.insert('end','下载超时，已结束下载\n')
                        self.t1.insert('end','出现异常：'+str(e)+'\n')
                        break
        self.t1.insert('end',f'下载结束，共下载了{img_count}张图片\n')

        
            

if __name__=='__main__':
    window_name=ttk.Window()
    test_gui=CrawlGui(window_name)
    test_gui.window_name.mainloop()

