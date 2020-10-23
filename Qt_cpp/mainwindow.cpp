#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QSettings>
#include <QResource>



MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{


    ui->setupUi(this);

    //建立并打开数据库

        database = QSqlDatabase::addDatabase("QSQLITE");
#if defined(Q_OS_ANDROID)
    database.setDatabaseName("/sdcard/stellarium/dso.db");
#else
    database.setDatabaseName("/home/silas/Desktop/dso.db");
#endif

        if (!database.open())
        {
            qDebug() << "Error: Failed to connect database." << database.lastError();
            ui->textBrowser->append("Error: Failed to connect database.");
        }
        else
        {
            qDebug() << "Succeed to connect database." ;
            ui->textBrowser->append("Succeed to connect database.");
        }

#if defined(Q_OS_ANDROID)
    QResource::registerResource("/sdcard/stellarium/DSSImages1.rcc");
        QResource::registerResource("/sdcard/stellarium/DSSImages2.rcc");
        QResource::registerResource("/sdcard/stellarium/DSSImages3.1.rcc");
        QResource::registerResource("/sdcard/stellarium/DSSImages3.2.rcc");
        QResource::registerResource("/sdcard/stellarium/DSSImages3.3.rcc");
        QResource::registerResource("/sdcard/stellarium/DSSImages3.4.rcc");


        //file too large
//        QResource::registerResource("/sdcard/stellarium/DSSImages3.rcc");
#else
    QResource::registerResource("/home/silas/Desktop/DSSImages1.rcc");
    QResource::registerResource("/home/silas/Desktop/DSSImages2.rcc");
//    QResource::registerResource("/home/silas/Desktop/DSSImages3.rcc");
#endif
//    QResource::registerResource("/sdcard/stellarium/DSSImages1.rcc");
//    QResource::registerResource("/sdcard/stellarium/DSSImages2.rcc");
//    QResource::registerResource("/sdcard/stellarium/DSSImages3.rcc");


//    QSqlDatabase m_db = QSqlDatabase::addDatabase("QSQLITE");
//    m_db.setDatabaseName("test.db");
//    if ( !m_db.open())
//    {
//        qDebug()<<"DB open error!";
//    }
//    else
//    {
//        qDebug()<<"DB open Sucess!";
//    }


//    QSqlDatabase m_db = QSqlDatabase::addDatabase("QODBC");
//        m_db.setDatabaseName("DRIVER={Microsoft Access Driver (*.mdb)};FIL={MS Access};DBQ=/home/silas/Desktop/DeepPro708000.mdb;UID=;PWD=");
//         bool  ok = m_db.open();
//        if(ok)
//        {
//        qDebug()<<"数据库打开成功";
//        }
//        else
//        {
//            qDebug()<<"数据库打开失败";
//        }

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_clicked()
{

    if (ui->lineEdit->text().trimmed().length()==0){
        return;
    }
    //查询数据
    QSqlQuery sql_query; //or Field_3 = %1 or LEFT(Field_3,%2) = %1
    // or substr(Field_3,1,%2)=\"%1,\"
    QString str = "SELECT * FROM DeepskyTable where Field_2 = \"%1\" or Field_3 = \"%1\" or Field_3 like \"%1,%\";";
    str = str.arg(ui->lineEdit->text().trimmed()); //.arg(ui->lineEdit->text().trimmed().length()+1));
    qDebug()<<str;
//        sql_query.exec(str);
        if(!sql_query.exec(str))
        {
            qDebug()<<sql_query.lastError();
            ui->textBrowser->append("execute error.");

        }
        else
        {
            while(sql_query.next())
            {
//                int id = sql_query.value(0).toInt();
//                QString name = sql_query.value(1).toString();
//                int age = sql_query.value(2).toInt();
//                qDebug()<<QString("id:%1    name:%2    age:%3").arg(id).arg(name).arg(age);


//                ui->textBrowser->append("ID: "+sql_query.value(0).toString());
//                ui->textBrowser->append("ObjectID: "+sql_query.value(1).toString());
//                ui->textBrowser->append("OtherID: "+sql_query.value(2).toString());
//                ui->textBrowser->append("ObjectType: "+sql_query.value(3).toString());
//                ui->textBrowser->append("RAhours: "+sql_query.value(4).toString());
//                ui->textBrowser->append("RAminutes: "+sql_query.value(5).toString());
//                ui->textBrowser->append("DeclinationDegrees: "+sql_query.value(6).toString());
//                ui->textBrowser->append("DeclinationMinutes: "+sql_query.value(7).toString());
//                ui->textBrowser->append("Epoch: "+sql_query.value(8).toString());
//                ui->textBrowser->append("GalacticLongitude: "+sql_query.value(9).toString());
//                ui->textBrowser->append("GalacticLatitude: "+sql_query.value(10).toString());
//                ui->textBrowser->append("Constellation: "+sql_query.value(11).toString());
//                ui->textBrowser->append("ObjectSize: "+sql_query.value(12).toString());
//                ui->textBrowser->append("Magnitude: "+sql_query.value(13).toString());
//                ui->textBrowser->append("Magnitude2: "+sql_query.value(14).toString());
//                ui->textBrowser->append("MCode: "+sql_query.value(15).toString());
//                ui->textBrowser->append("PositionAngle: "+sql_query.value(16).toString());
//                ui->textBrowser->append("Separation: "+sql_query.value(17).toString());
//                ui->textBrowser->append("Description: "+sql_query.value(18).toString());
//                ui->textBrowser->append("Catalog: "+sql_query.value(19).toString());
//                ui->textBrowser->append("ImageFile: "+sql_query.value(20).toString());
//                ui->textBrowser->append("MessierNumber: "+sql_query.value(21).toString());
//                ui->textBrowser->append("Observed: "+sql_query.value(22).toString());
//                ui->textBrowser->append("Hobject: "+sql_query.value(23).toString());
//                ui->textBrowser->append("DeepskySup: "+sql_query.value(24).toString());
//                ui->textBrowser->append("ImageFOV: "+sql_query.value(25).toString());
//                ui->textBrowser->append("Annotation: "+sql_query.value(26).toString());
//                ui->textBrowser->append("AstroCardID: "+sql_query.value(27).toString());
//                ui->textBrowser->append("ProperName: "+sql_query.value(28).toString());

                if(sql_query.value(0).toString()!="")
                ui->textBrowser->append("ID: "+sql_query.value(0).toString());
                if(sql_query.value(1).toString()!="")
                ui->textBrowser->append("ObjectID: "+sql_query.value(1).toString());
                if(sql_query.value(2).toString()!="")
                ui->textBrowser->append("OtherID: "+sql_query.value(2).toString());
                if(sql_query.value(3).toString()!="")
                ui->textBrowser->append("ObjectType: "+sql_query.value(3).toString());
                if(sql_query.value(4).toString()!="")
                ui->textBrowser->append("RAhours: "+sql_query.value(4).toString());
                if(sql_query.value(5).toString()!="")
                ui->textBrowser->append("RAminutes: "+sql_query.value(5).toString());
                if(sql_query.value(6).toString()!="")
                ui->textBrowser->append("DeclinationDegrees: "+sql_query.value(6).toString());
                if(sql_query.value(7).toString()!="")
                ui->textBrowser->append("DeclinationMinutes: "+sql_query.value(7).toString());
                if(sql_query.value(8).toString()!="")
                ui->textBrowser->append("Epoch: "+sql_query.value(8).toString());
                if(sql_query.value(9).toString()!="")
                ui->textBrowser->append("GalacticLongitude: "+sql_query.value(9).toString());
                if(sql_query.value(10).toString()!="")
                ui->textBrowser->append("GalacticLatitude: "+sql_query.value(10).toString());
                if(sql_query.value(11).toString()!="")
                ui->textBrowser->append("Constellation: "+sql_query.value(11).toString());
                if(sql_query.value(12).toString()!="")
                ui->textBrowser->append("ObjectSize: "+sql_query.value(12).toString());
                if(sql_query.value(13).toString()!="")
                ui->textBrowser->append("Magnitude: "+sql_query.value(13).toString());
                if(sql_query.value(14).toString()!="")
                ui->textBrowser->append("Magnitude2: "+sql_query.value(14).toString());
                if(sql_query.value(15).toString()!="")
                ui->textBrowser->append("MCode: "+sql_query.value(15).toString());
                if(sql_query.value(16).toString()!="")
                ui->textBrowser->append("PositionAngle: "+sql_query.value(16).toString());
                if(sql_query.value(17).toString()!="")
                ui->textBrowser->append("Separation: "+sql_query.value(17).toString());
                if(sql_query.value(18).toString()!="")
                ui->textBrowser->append("Description: "+sql_query.value(18).toString());
                if(sql_query.value(19).toString()!="")
                ui->textBrowser->append("Catalog: "+sql_query.value(19).toString());
                if(sql_query.value(20).toString()!="")
                ui->textBrowser->append("ImageFile: "+sql_query.value(20).toString());
                if(sql_query.value(21).toString()!="")
                ui->textBrowser->append("MessierNumber: "+sql_query.value(21).toString());
                if(sql_query.value(22).toString()!="")
                ui->textBrowser->append("Observed: "+sql_query.value(22).toString());
                if(sql_query.value(23).toString()!="")
                ui->textBrowser->append("Hobject: "+sql_query.value(23).toString());
                if(sql_query.value(24).toString()!="")
                ui->textBrowser->append("DeepskySup: "+sql_query.value(24).toString());
                if(sql_query.value(25).toString()!="")
                ui->textBrowser->append("ImageFOV: "+sql_query.value(25).toString());
                if(sql_query.value(26).toString()!="")
                ui->textBrowser->append("Annotation: "+sql_query.value(26).toString());
                if(sql_query.value(27).toString()!="")
                ui->textBrowser->append("AstroCardID: "+sql_query.value(27).toString());
                if(sql_query.value(28).toString()!="")
                ui->textBrowser->append("ProperName: "+sql_query.value(28).toString());
                ui->textBrowser->append("=====");

                QString imgfile = sql_query.value(20).toString();

                QImage *img=new QImage; //新建一个image对象
                    img->load(":/DSSImages/"+imgfile); //将图像资源载入对象img，注意路径，可点进图片右键复制路径
                    ui->label->setPixmap(QPixmap::fromImage(*img)); //将图片放入label，使用setPixmap,注意指针*img
                break;
            }
        }
}

void MainWindow::on_pushButton_2_clicked()
{
//    ui->label->setPicture()
    QImage *img=new QImage; //新建一个image对象
        img->load(":/DSSImages/Abell  194-SAC71-009.jpg"); //将图像资源载入对象img，注意路径，可点进图片右键复制路径
        ui->label->setPixmap(QPixmap::fromImage(*img)); //将图片放入label，使用setPixmap,注意指针*img
}

void MainWindow::on_pushButton_3_clicked()
{
    if (ui->lineEdit->text().trimmed().length()==0){
        return;
    }
    //查询数据
    QSqlQuery sql_query;
    QString str = ui->lineEdit->text().trimmed();
    qDebug()<<str;
        if(!sql_query.exec(str))
        {
            qDebug()<<sql_query.lastError();
            ui->textBrowser->append("execute error.");

        }
        else
        {
            while(sql_query.next()){
                ui->textBrowser->append(sql_query.value(0).toString());
            }

//            while(sql_query.next())
//            {
//                QString imgfile = sql_query.value(20).toString();
//                QImage *img=new QImage; //新建一个image对象
//                    img->load(":/DSSImages/"+imgfile); //将图像资源载入对象img，注意路径，可点进图片右键复制路径
//                    ui->label->setPixmap(QPixmap::fromImage(*img)); //将图片放入label，使用setPixmap,注意指针*img
//                break;
//            }
        }
}
