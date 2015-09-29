#!/usr/bin/python
# -*- coding: utf-8 -*-

import Image,ImageDraw,ImageFont
import os,sys
import wx
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas


class imageProcess():
    
    def __init__(self):
        
        self.font_path='./stuff/Hiragino Sans GB W3.otf'
        self.bold_font_path='./stuff/Hiragino Sans GB W6.otf'
        self.font_color=(218,153,43,30)#字体颜色
                
        
    def showWindow(self):
        app = wx.PySimpleApp()  
        frame = wx.Frame( None, -1, '' )
        
        '''定义标签及文本框和按钮'''
        #@param startBoxNum,int 起始箱数
        wx.StaticText(frame,1,u'起始箱数：',(50,50),(65,20),style=0,name='lblStartBoxNum')
        self.txtStartBoxNum = wx.TextCtrl(frame,1,'14',(120,45),(120,22),style=0,name='txtStartBoxNum')
        
        #@param startBagNum,int 起始袋数
        wx.StaticText(frame,1,u'起始袋数：',(50,70),(65,20),style=0,name='lblStartBagNum')
        self.txtStartBagNum = wx.TextCtrl(frame,1,'311',(120,65),(120,22),style=0,name='txtStartBagNum')        
        
        #@param bagsPerBox,int 每箱袋数
        wx.StaticText(frame,1,u'每箱袋数：',(50,90),(65,20),style=0,name='lblBagsPerBox')
        self.txtBagsPerBox = wx.TextCtrl(frame,1,'10',(120,85),(120,22),style=0,name='txtBagsPerBox')           
        
        #@param sartSerial,int 起始序列
        wx.StaticText(frame,1,u'起始序列：',(50,110),(65,20),style=0,name='lblSartSerial')
        self.txtSartSerial = wx.TextCtrl(frame,1,'1370065501',(120,105),(120,22),style=0,name='txtSartSerial')         
        
        #@param numberPerBag,int 每袋个数
        wx.StaticText(frame,1,u'每袋个数：',(50,130),(65,20),style=0,name='lblNumberPerBag')
        self.txtNumberPerBag = wx.TextCtrl(frame,1,'50',(120,125),(120,22),style=0,name='txtNumberPerBag') 
        
        self.button = wx.Button(frame,1,u'生成PDF!',(440,50),(100,100),style=2,name='btnGenerate')
             
        '''绑定单击事件'''
        self.button.Bind(wx.EVT_BUTTON, self.onClick,self.button)
        
        frame.SetCursor( wx.StockCursor( wx.CURSOR_ARROW ) )  
        frame.SetIcon(wx.Icon('./stuff/favicon.ico',wx.BITMAP_TYPE_ICO)) 
        frame.SetSize( wx.Size( 600, 250 ) )  
        frame.SetTitle(u'专业生成USB智能卡标签')
        frame.Center()
                
        frame.Show()
        app.MainLoop()  
          
        
        ##
        #绘制单个标签
        #@param numberPerBag,int 每包USB-key的数量
        #@param startSerial,int 起始序列号
        #@param boxNum,int 装箱序号
        #@param bagNum,int 袋编号
    def onClick(self,event):
        print 'x'
        ret = self.mergeLabelToPage(startBoxNum=int(self.txtStartBoxNum.GetValue()),\
                              startBagNum=int(self.txtStartBagNum.GetValue()),\
                              bagsPerBox=int(self.txtBagsPerBox.GetValue()),\
                              startSerial=int(self.txtSartSerial.GetValue()),\
                              numberPerBag=int(self.txtNumberPerBag.GetValue()))
        wx.MessageBox(u'已生成：' + ret,u'提示信息',wx.OK|wx.ICON_INFORMATION)
       
         
    def drawText(self,numberPerBag=50,startSerial=1370066902,boxNum=14,bagNum=318):

        im=Image.new('CMYK',(826,350))#创建空白标签
       
        '''1 组织机构代码IC'''
        self.font_title = ImageFont.truetype(self.bold_font_path,50)
        '''2 数量：50个/袋'''
        self.font_numberPerBag = ImageFont.truetype(self.font_path,33)
        '''3 024箱?袋'''
        self.font_boxBagSerial = ImageFont.truetype(self.font_path,45)
        '''4 A0239'''
        self.font_bagNum = ImageFont.truetype(self.bold_font_path,76)
        '''5 序号段：56546565464~54545645454564'''
        self.font_keySerial = ImageFont.truetype(self.font_path,36)
        '''6 南京壹进制公司出品 质检员：1号 6号'''
        self.font_companyInfo = ImageFont.truetype(self.font_path,30)
        
        draw = ImageDraw.Draw(im)
        
        '''向空白标签纸上写字'''
        draw.text((60,30),u'组织机构代码IC',font=self.font_title,fill = self.font_color)
        draw.text((560,35),u'数量：%d个/袋' % numberPerBag,font=self.font_numberPerBag,fill = self.font_color)
        draw.text((140,150),u'%s箱' % self.fillZeroToFront(boxNum,3),font=self.font_boxBagSerial , fill = self.font_color)
        draw.text((313,120),u'A%s' % self.fillZeroToFront(bagNum,4),font=self.font_bagNum , fill = self.font_color)
        draw.text((620,150),u'袋',font=self.font_boxBagSerial , fill = self.font_color)
        tmpStr=u'序列号段：%d~%d' % (startSerial,startSerial + numberPerBag - 1)
        draw.text((62,230),tmpStr,font=self.font_keySerial,fill = self.font_color)
        draw.text((38,290),u'南京壹进制信息技术有限公司  出品     质检员：1号 6号',font=self.font_companyInfo,fill = self.font_color)
              
        
        '''单个标签处理完毕'''
        return im
        
        ##
        #将数字填充至length位
        #@param number,int 要填充的数字
        #@param length,int 填充后字符串长度
        #@return string

    def fillZeroToFront(self,number,length):
        number=str(number)
        if len(number)<length:
            return '0'*(length-len(number))+number
        else:
            return number

        ##
        #批量生成标签，并按顺序写入A4大小的页面
        #@param startBoxNum,int 起始箱数
        #@param startBagNum,int 起始袋数
        #@param bagsPerBox,int 每箱袋数
        #@param sartSerial,int 起始序列号
        #@param numberPerBag,int 每袋个数
        
    def mergeLabelToPage(self,startBoxNum=14,startBagNum=311,bagsPerBox=10,startSerial=1370065501,numberPerBag=50):
        
        startSerial = startSerial - 1
        #准备数据
        '''创建一个底板'''
        background=Image.new('CMYK',(2479,3508), (0,0,0,0))
        '''选中标签整体坐标=单个标签的大小'''
        box=(0,0,826,350)
        currentBagNum=startBagNum
        currentBoxNum=startBoxNum
        currentSerialStart=startSerial
        tmpBoxBagCount=0
        
        #循环处理
        '''行循环，十行'''
        for rowLoop in range(0,10):
            '''列循环，三列'''
            for colLoop in range(0,3):
                '''当前袋和起始袋相差？'''
                #bagDiffer = currentBagNum - startBagNum
                
                singleLabel = self.drawText(numberPerBag = numberPerBag,startSerial = currentSerialStart + 1 ,\
                                            boxNum = currentBoxNum,bagNum = currentBagNum)
                '''从singleLabel中创建选区'''
                region = singleLabel.crop(box)                
                background.paste(region,(box[0]+820*colLoop,box[1]+350*rowLoop,box[2]+820*colLoop,box[3]+350*rowLoop))#粘贴到底板上
                '''当前袋数增1'''
                currentBagNum=currentBagNum + 1
                tmpBoxBagCount=tmpBoxBagCount + 1
                currentSerialStart = currentSerialStart + 50
                '''每箱10袋'''
                if tmpBoxBagCount >= bagsPerBox:
                    currentBoxNum=currentBoxNum + 1
                    tmpBoxBagCount = 0
                
        labelPage = background
        #转换为PDF并保存
        filename = 'USB-key Serial %d~%d.pdf' % (startSerial + 1,currentSerialStart)
        (w, h) = landscape(A4)
        c = canvas.Canvas(filename, pagesize = (h,w))
        c.drawInlineImage(labelPage, 0, 0, h, w)
        c.save()
        return filename
         
      
        
               
pic=imageProcess()
pic.showWindow()
#pic.mergeLabelToPage()