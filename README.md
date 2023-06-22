# RFM Analizi ile Müşteri Segmentasyonu
--------------------------------------
![alt text](https://miro.medium.com/v2/resize:fit:720/0*U36nFVmDeotOrts6))


İş Problemi
-----------

İniltere merkezli perakende şirketi müşterilerini segmentlere ayırıp bu segmentler özelinde pazarlama stratejileri belirlemek istemektedir.
Ortak davranışlar sergileyen müşteri segmentleri özelinde pazarlama çalışmaları yapmanın gelir artışı sağlayacağını düşünmektedir.

**Segmentleri ayırmak için `RFM Analizi` kullanılacaktır.**

Veri Seti Hikayesi
------------------
Online Reatail II isimli veri seti İngiltere merkezli bir perakende şirketinin 01/12//2009 - 09/12/2011 tarihleri arasındaki online satış 
işlemlrini içermektedir. Şirketin ürün kataloğunda hediyelik eşyalar yer almaktadır ve çoğu müşterisinin toptancı olduğu bilinmektedir.

`8 Değişken`  `541.909 Gözlem Birimi`  `45.6MB`

InvoiceNo: Fatura Numarası (Eğer bu kod C ile başlıyorsa işlemin iptal edildiğini ifade eder.)

StockCode: Ürün kodu (Her bir ürün için eşsiz)

Description: Ürün İsmi

Quantity: Ürün Adedi (Faturalardaki ürünlerden kaçar tane satıldığı)

InvoiceDate: Fatura Tarihi

UnitPrice: Fatura Fiyatı (Sterlin)

CustomerID: Eşsiz Müşteri Numarası

Country: Ülke İsmi

