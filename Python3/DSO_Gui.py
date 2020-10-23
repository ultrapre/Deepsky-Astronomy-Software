#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from numpy import *
from ephem import *
from tkinter import *
from tkinter.ttk import *
from datetime import *
import json
import re
import tkinter
from PIL import Image, ImageTk
import pypyodbc as mdb
import os
import locale


loc = locale.getdefaultlocale()[0]

def jsonload(src,srccoding="utf-8",dem=False):
    dic = {}
    try:
        dic = json.load(open(src, "r", encoding=srccoding))
    except:
        dic = {}
        for line in open(src, "r", encoding=srccoding).read().splitlines():
            dic[line.split('\t')[0]] = line.split('\t')[1]
        return dic
    return dic

langsrc = 'data/lang.json'
latitude = '21'
longtitude = '110'
mdbfile = 'data/DeepPro708000.mdb'
DSSImagesDir = 'data/DSSImages/'
dictoNGC = jsonload("data/Reflects.json")
dicMtoNGC = jsonload('data/Messier.json')

lang = jsonload(langsrc)
def _(s):
    if loc == 'zh_CN':
        if s in lang:
            return lang[s]
    return s


def DSOAZ(raJ2k, decJ2k, mydate,lat=latitude,lon=longtitude):
    wpf = Observer()
    wpf.lat = lat  
    wpf.lon = lon  
    wpf.elevation = 0  
    wpf.pressure = 0  
    wpf.date = now()
    wpf.date = mydate  
    p = FixedBody(mydate)
    p._ra = str(raJ2k / 360 * 24)
    p._dec = str(decJ2k)
    p.compute(wpf)
    return (rad2deg(p.az),rad2deg(p.alt))

def DSOAZ_Pln(Pln,mydate,lat=latitude,lon=longtitude):
    wpf = Observer()
    wpf.lat = lat  
    wpf.lon = lon  
    wpf.elevation = 0  
    wpf.pressure = 0  
    wpf.date = now()
    wpf.date = mydate  
    p = Pln()
    p.compute(wpf)
    return (rad2deg(p.az),rad2deg(p.alt))




dicNGCtoM = {}
for it in dicMtoNGC:
    dicNGCtoM[dicMtoNGC[it]] = it

def dsoname(it,ripblank=True):
    it = it.strip()
    if ripblank:
        if re.match('[A-z]+ [A-z]+',it):
            pass
        else:
            it = it.replace(' ', '')
    it = it.replace('\t', '')
    name = it
    if re.match('^NGC\s*\d+[A-z]*$',name.upper()):
        return name.replace(" ","")
    if re.match('^IC\s*\d+[A-z]*$',name.upper()):
        return name.replace(" ","")
    if re.match('^M\s*\d+[A-z]*$',name.upper()):
        return name.replace(" ","")
    if re.match('^MEL\s*\d+$',name.upper()):
        return name.replace(" ","")
    if re.match('^CR\s*\d+$',name.upper()):
        return name.replace(" ","")
    def PNsolve(it):
        gp1 = re.match('^PK\s*(.+)([\-\+])(.+)$', it)
        if gp1:
            return 'PK' + gp1.group(1).zfill(3) + gp1.group(2) + gp1.group(3).zfill(4)
        gp2 = re.match('^PN G\s*(.+)([\-\+])(.+)$', it)
        gp2p = re.match('^PNG\s*(.+)([\-\+])(.+)$', it)
        if gp2:
            return 'PN G' + gp2.group(1).zfill(5) + gp2.group(2) + gp2.group(3).zfill(4)
        if gp2p:
            return 'PN G' + gp2p.group(1).zfill(5) + gp2p.group(2) + gp2p.group(3).zfill(4)
        gp2 = re.match('^SNR G\s*(.+)([\-\+])(.+)$', it)
        gp2p = re.match('^SNRG\s*(.+)([\-\+])(.+)$', it)
        if gp2:
            return 'SNR G' + gp2.group(1).zfill(5) + gp2.group(2) + gp2.group(3).zfill(4)
        if gp2p:
            return 'SNR G' + gp2p.group(1).zfill(5) + gp2p.group(2) + gp2p.group(3).zfill(4)
        return it
    it = PNsolve(it)
    return it

# M、非M转NGC
def toNGC(it,mdbsrc = False):
    if it in dictoNGC:
        if mdbsrc:
            return dictoNGC[it].replace("NGC", "NGC ").replace("IC", "IC ")
        return dictoNGC[it]

    if it in dicMtoNGC:
        if mdbsrc:
            return dicMtoNGC[it].replace("NGC", "NGC ").replace("IC", "IC ")
        return dicMtoNGC[it]

    if mdbsrc:
        return it.replace("NGC", "NGC ").replace("IC", "IC ")
    return it


# 连接mdb文件
connStr = (
    r'Driver={Microsoft Access Driver (*.mdb)};DBQ='+mdbfile+';'
)
conn = mdb.win_connect_mdb(connStr)
cur = conn.cursor()


def searchInmdb(id='',pf='',brave=True, fetchallfirst=True):
    if id!='':
        if brave:
            oql = "SELECT * FROM DeepskyTable WHERE objectid = '%s' or otherid = '%s' or LEFT(otherid,%s) = '%s,';" % (id,id,len(id)+1,id)
        else:
            oql = "SELECT * FROM DeepskyTable WHERE objectid = '%s';"%(id)
        cur.execute(oql)
    elif pf!='':
        if brave:
            oql = "SELECT * FROM DeepskyTable WHERE LEFT(objectid,%s) = '%s' or LEFT(otherid,%s) = '%s';" % (len(pf), pf, len(pf), pf)
        else:
            oql = "SELECT * FROM DeepskyTable WHERE LEFT(objectid,%s) = '%s';"%(len(pf),pf)
        cur.execute(oql)
    else:
        return
    tmplis=[]
    for col in cur.description:
        tmplis.append(col[0])
    tlis = ['ID','ID2','RA2000','Dec2000','Mag','Size','Type','Const','Source']
    # lis.append(tlis)
    if fetchallfirst:
        try:
            result = cur.fetchall()
        except:
            try:
                result = [cur.fetchone()]
            except:
                return None
    else:
        try:
            result = [cur.fetchone()]
        except:
            return None
    lis = []
    for row in result:
        row = [str(x) for x in list(row)]
        # obj, name, ra, ra_rad, dec, dec_rad, mag, size, type, con, source
        lis.append([row[1],row[2],row[4]+'h'+row[5]+'m',(int(row[4])+float(row[5])/60)/12*pi,row[6]+'°'+row[7]+"'",(int(row[6])+float(row[7])/60)/180*pi,row[13],row[12],row[3],row[11],row[19],row[20],row])
        lis.append(list(row))
    for ix in ['2000','SAC81','SAC75','SAC71']:
        for line in lis:
            if line[len(line) - 1]==ix:
                return line
    if lis == []:
        return None
    return lis[0]



def findPic(pic):
    gps = re.match('^(.+)\-(.+)\-(\d\d\d)\.[A-z]+$',pic)
    if gps:
        return DSSImagesDir+gps.group(2)+'/'+str(int(gps.group(3)))+'/'+pic
    else:
        for it in ['Common','widefieldimages', 'oldds', 'hires']:
            if os.path.exists(DSSImagesDir+it+'/'+pic):
                return DSSImagesDir+it+'/'+pic
        return False


if __name__ == '__main__':
    tmpobj = ''
    tmpra = 0
    tmpdec = 0
    def isDouble(x):
        try:
            double(x)
            return double(x)
        except:
            return False
    def matchDSO(name):
        id = toNGC(dsoname(name),mdbsrc = True)
        return id
    def Cal_SkyObject(flushRD = False):
        global SObj,alt,az, tmpobj, tmpra, tmpdec, label_img, wtext
        obj = matchDSO(SObj.get())
        if isDouble(lon.get()) is False or isDouble(lat.get()) is False:
            return
        if tmpobj != obj and flushRD is False:
            tmpobj = obj
            wtext.configure(text="Loading……")
            rsl = searchInmdb(obj)
            if rsl != None:
                ra = rsl[3] / pi * 180
                dec = rsl[5] / pi * 180
                tmpra = ra
                tmpdec = dec
                (alt1,az1) = DSOAZ(ra, dec, mydate=datetime.now()+timedelta(hours=-8),lat=lat.get(),lon=lon.get())
                alt.set(alt1)
                az.set(az1)
                if rsl[11] != '':
                    dst = findPic(rsl[11])
                    if dst != False:
                        print(dst)
                        img = Image.open(dst)  # 打开图片
                        img_png = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
                        label_img.configure(image=img_png)
                        label_img.image = img_png
                    else:
                        img = Image.open(findPic("noimage.jpg"))  # 打开图片 "N:/As/DSSImages/Common/noimage.jpg"
                        img_png = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
                        label_img.configure(image=img_png)
                        label_img.image = img_png
                else:
                    img = Image.open(findPic("noimage.jpg"))  # 打开图片
                    img_png = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
                    label_img.configure(image=img_png)
                    label_img.image = img_png

                textlis = rsl[12]

                textnew = ''
                textnew += _('ID:')+textlis[1]
                textnew += '\n'
                if textlis[2]!='' and textlis[2]!='None':
                    textnew += _('Other:')+textlis[2]
                    textnew += '\n'
                textnew += _('Type:')+textlis[3]
                textnew += '\n'
                textnew += _('RA:')+rsl[2]
                textnew += '\n'
                textnew += _('Dec:')+rsl[4]
                textnew += '\n'
                textnew += _('Con:')+textlis[11]
                textnew += '\n'
                if textlis[13]!='' and textlis[13]!='None':
                    textnew += _('Mag:')+textlis[13]
                    textnew += '\n'
                if textlis[12]!='' and textlis[12]!='None':
                    textnew += _('Size:')+textlis[12]+"'"
                    textnew += '\n'
                if textlis[14]!='' and textlis[14]!='None':
                    textnew += _('PA:')+textlis[14]+"°"
                    textnew += '\n'
                if textlis[18]!='' and textlis[18]!='None':
                    textnew += _('Desc:')+textlis[18]
                    textnew += '\n'
                if textlis[19]!='' and textlis[19]!='None':
                    textnew += _('Source:')+textlis[19]
                    textnew += '\n'
                if textlis[25]!='' and textlis[25]!='None':
                    textnew += _('ImageFOV:')+textlis[25]+"'"
                    textnew += '\n'
                wtext.configure(text=textnew)
            else:
                wtext.configure(text="Not Found")
                img = Image.open(findPic("noimage.jpg"))  # 打开图片
                img_png = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
                label_img.configure(image=img_png)
                label_img.image = img_png
        else:
            (alt1,az1) = DSOAZ(tmpra, tmpdec, mydate=datetime.now()+timedelta(hours=-8),lat=lat.get(),lon=lon.get())
            alt.set(alt1)
            az.set(az1)
        return

    root = Tk()
    root.title(_("Deepsky Astronomy Software for Python demo"))
    root.configure(bg='gray')
    SObj = StringVar()
    alt = DoubleVar()
    az = DoubleVar()
    lat = StringVar()
    lon = StringVar()
    lat.set(latitude)
    lon.set(longtitude)

    labellon = Label(root, text=_("ID"), width=4)
    labellon.grid(row=1, column=1, padx=3, pady=3, sticky=E)

    inputme = Entry(root, width=20, textvariable=SObj)
    inputme['state'] = 'write'
    inputme.grid(row=1, column=2, columnspan=5, padx=3, pady=3, sticky=W + E)

    CheckVar1 = IntVar()
    checkme = Checkbutton(root, text=_("RT"), variable=CheckVar1, width=4)
    CheckVar1.set(0)
    checkme.grid(row=2, column=5, padx=1, pady=1, sticky=W)

    pushme = Button(root, text=_("GET"), command=Cal_SkyObject, width=10)
    pushme.grid(row=2, column=6, sticky=E, padx=3, pady=3)

    labelalt = Label(root, text=_("Alt"), width=5)
    labelalt.grid(row=1, column=7, padx=3, pady=3, sticky=W)

    inputme1 = Entry(root, width=25, textvariable=alt)
    inputme1['state'] = 'readonly'
    inputme1.grid(row=1, column=8, padx=3, pady=3, sticky=E)

    labellon = Label(root, text=_("Lon."), width=4)
    labellon.grid(row=2, column=1, padx=3, pady=3, sticky=E)

    inputlon = Entry(root, width=10, textvariable=lon)
    inputlon['state'] = 'write'
    inputlon.grid(row=2, column=2, padx=3, pady=3, sticky=W)

    labelaz = Label(root, text=_("Az"), width=5)
    labelaz.grid(row=2, column=7, padx=3, pady=3, sticky=W)

    inputme2 = Entry(root, width=25, textvariable=az)
    inputme2['state'] = 'readonly'
    inputme2.grid(row=2, column=8, padx=3, pady=3, sticky=E)

    labellat = Label(root, text=_("Lat."), width=4)
    labellat.grid(row=2, column=3, padx=3, pady=3, sticky=W)

    inputlat = Entry(root, width=10, textvariable=lat)
    inputlat['state'] = 'write'
    inputlat.grid(row=2, column=4, padx=3, pady=3, sticky=W)

    wtext = tkinter.Label(root, text="")
    wtext.configure(bg='gray')
    wtext.grid(row=1, column=10, rowspan=3, padx=3, pady=3, sticky=W)

    img = Image.open(findPic("EmptyImage.jpg"))
    img_png = ImageTk.PhotoImage(img)
    label_img = tkinter.Label(root, image=img_png, width=600, height = 600)
    label_img.configure(bg='gray')
    label_img.grid(row=3, column=1, columnspan=9, sticky=E, padx=3, pady=3)

    def refreshText():
        if CheckVar1.get() == 1:
            Cal_SkyObject(flushRD=True)
        root.after(1000, refreshText)
    root.after(1000, refreshText)
    root.columnconfigure(2, weight=1)
    root.mainloop()

