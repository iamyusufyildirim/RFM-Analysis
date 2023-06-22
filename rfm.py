                                                  #########################################
                                                  # RFM Analizi ile Müşteri Segmentasyonu #
                                                  #########################################

#     +------------------------------------------------------------------------------------------------------------------------------+
#     +                                                       UYGULAMA ÖNCESİ                                                        +
#     +------------------------------------------------------------------------------------------------------------------------------+
#     -                                                                                                                              -
#     -    Invoice StockCode                          Description  Quantity         InvoiceDate  Price  Customer ID         Country  -
#     -  0  489434     85048  15CM CHRISTMAS GLASS BALL 20 LIGHTS        12 2009-12-01 07:45:00   6.95     13085.00  United Kingdom  -
#     -  1  489434    79323P                   PINK CHERRY LIGHTS        12 2009-12-01 07:45:00   6.75     13085.00  United Kingdom  -
#     -  2  489434    79323W                  WHITE CHERRY LIGHTS        12 2009-12-01 07:45:00   6.75     13085.00  United Kingdom  -
#     -  3  489434     22041         RECORD FRAME 7" SINGLE SIZE         48 2009-12-01 07:45:00   2.10     13085.00  United Kingdom  -
#     -  4  489434     21232       STRAWBERRY CERAMIC TRINKET BOX        24 2009-12-01 07:45:00   1.25     13085.00  United Kingdom  -
#     -                                                                                                                              -
#     +------------------------------------------------------------------------------------------------------------------------------+

#     +-----------------------------------------------------+
#     -                  UYGULAMA SONRASI                   -
#     +-----------------------------------------------------+
#     -                                                     -
#     -          Customer ID RF_SCORE              SEGMENT  -
#     -  0       12346.000       25           cant_loose    -
#     -  1       12347.000       52  potential_loyalists    -
#     -  2       12348.000       21          hibernating    -
#     -  3       12349.000       33       need_attention    -
#     -  4       12351.000       51        new_customers    -
#     -                                                     -
#     +-----------------------------------------------------+

"""
# 1. İş Problemi - (Business Problem)
# 2. Veriyi Anlama - (Data Understanding)
# 3. Veriyi Hazırlama - (Data Preparation)
# 4. RFM Metriklerinin Oluşturulması - (Calculating RFM Metrics)
# 5. RFM Skorlarının Oluşturulması - (Calculating RFM Scores)
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi - (Creating & Analysing RFM Segments)
"""

# ---------------------------------------
# - 1. İş Problemi - (Business Problem) -
# ---------------------------------------
# İngiltere merkezli perakende şirketi müşterilerini segmentlere ayırıp
# bu segmentler özelinde pazarlama stratejileri belirlemek istemektedir.
# Segmentasyon için RFM analizi kullanılacaktır.


# ----------------------
# - Veri Seti Hikayesi -
# ----------------------
# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içermektedir.


# ---------------
# - Değişkenler -
# ---------------
#
# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürü ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaaçr tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.


# -------------------------------------------
# - 2. Veriyi Anlama - (Data Understanding) -
# -------------------------------------------

# Gerekli kütüphane importları ve bazı görsel ayarlamalar
import pandas as pd
import datetime as dt
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.float_format", lambda x : "%.3f" % x)

# İlgili veri setinin projeye dahil edilmesi.
def load_dataset():
    data = pd.read_excel("data_sets/online_retail_II.xlsx", sheet_name="Year 2009-2010")  # sheet_name parametresi, okunacak çalışma sayfasının
    return data                                                                           # adını veya indeksini belirtmek için kullanılır.
                                                                                          # Ben analizlerimde 2009-2010 yıllarını kullanacağım için
# Varsayılan olarak, sheet_name parametresi None olarak ayarlanır ve pd.read_excel fonksiyonu tüm çalışma sayfalarını bir dizi olarak döndürür. Eğer belirli bir çalışma sayfasını okumak istiyorsanız, sheet_name parametresini ad veya indeks olarak ayarlayarak ilgili çalışma sayfasını seçebilirsiniz.
df_ = load_dataset()
df = df_.copy()


# Veri setin hakkında genel bir bakış elde etmek için check_df fonksyionunu tanımlıyoruz.
def check_df(dataframe, head=10):
    print("###################################")
    print(f"#### İlk {head} Gözlem Birimi ####")
    print("###################################")
    print(dataframe.head(head), "\n\n")

    print("###################################")
    print("###### Veri Seti Boyut Bilgisi ####")
    print("###################################")
    print(dataframe.shape, "\n\n")

    print("###################################")
    print("######## Değişken İsimleri ########")
    print("###################################")
    print(dataframe.columns, "\n\n")

    print("###################################")
    print("####### Eksik Değer Var mı? #######")
    print("###################################")
    print(dataframe.isnull().values.any(), "\n\n")

    print("###################################")
    print("##### Betimsel İstatistikler ######")
    print("###################################")
    print(dataframe.describe().T, "\n\n")

    print("###################################")
    print("### Veri Seti Hakkında Bilgiler ###")
    print("###################################")
    print(dataframe.info())

check_df(dataframe=df)


# Eşsiz ürün sayısı kaçtır?
df["Description"].nunique()
# Hangi ürünlerden kaçar tane var?
df["Description"].value_counts()
# En çok sipariş edilen 5 ürünü çoktan aza olacak şekilde sıralayınız
df.groupby("Description").agg({"Quantity" : "sum"}).sort_values(by="Quantity", ascending=False)


# ---------------------------------------------
# - 3. Veriyi Hazırlama - (Data Preparation)  -
# ---------------------------------------------

df["Total_Price"] = df["Price"] * df["Quantity"]

# veri setindeki eksik değerleri tablo formatında gösterecek bir fonksiyon tanımlıyoruz.
def missing_values_table(dataframe):
    na_columns = [col for col in dataframe.columns if dataframe[col].isnull().sum() > 0]
    missing_values = (dataframe[na_columns].isnull().sum()).sort_values(ascending=False)
    ratio = (dataframe[na_columns].isnull().sum() / dataframe.shape[0] * 100 ).sort_values(ascending=False)
    table = pd.concat([missing_values, ratio], axis=1, keys=["Values", "%"])
    print(table)

missing_values_table(dataframe=df)

# Customer ID değişkeninde eksiklik olması yapılan hesaplamalardaki ilgili müşterilere erişiememe problemine yol açacaktır.
# Bu durum çeşitli problemlere yol açacaktır. Bu sebeple eksik değerlere sahip gözlem birimlerini veri setinden temizliyoruz.
df.dropna(inplace=True)

# Invoice değişkeninde başında "C" olan ifadeler iade olan işlemleri temsil etmektedir.
# İade olan işlemler fiyat ve ürün adedinde negatif değerlerin çıkmasına sebep olmaktadır.
# Bu durum ilgili hesaplamaların yapılmasında çeşitli bozukuklara sebep olmaktadır.
# Bu yüzden iade olan işlemleri veri setinden filtreliyoruz.
# Tilda işareti "~" ilgili seçimin dışındakileri getir anlmaına gelmektedir.
df = df[~df["Invoice"].str.contains("C", na=False)]
df =  df[df["Price"] > 0]
df =  df[df["Quantity"] > 0]


# ------------------------------------------------------------------
# - 4. RFM Metriklerinin Oluşturulması - (Calculating RFM Metrics) -
# ------------------------------------------------------------------
"""
R -> Recency: Müşteri yeniliğini ifade eder. Matematiksel karşılığı = Analiz tarihi - ilgili müşterinin son aLışveriş tarihi
F -> Frequency: Toplam alışveriş sayısı bir diğer ifadesiyle toplam işlem sayısıdır. Matematiksel karşılığı = ilgili müşterinin toplam alışveriş sayısı
M -> Monetary: Müşterinin şirket ile kurduğu ilişki süresince bıraktığı toplam parasal değeri ifade eder. Matematiksel karşılığı = ilgili müşterinin toplam harcama tutarı
"""

# Analizi yaptığımız günü belirlememiz gerekmektedir.
# Veri seti 2009-2011 yılları arasında oluşturulan bir veri setidir.
# Biz o dönemde yaşamadığımı için şu şekilde bir yol izlememiz gerekmektedir:
# Bu veri seti içerisinde ki en son gün hangi günse üzerine 2 gün koyup bu tarih analiz tarihiymiş gibi analizimi gerçekleştirriz.
today_date = dt.datetime(2010, 12, 11)

# Herbir müşteri özelinde Recency, Frequency ve Monetary değerlerini hesaplıyoruz.
rfm = df.groupby("Customer ID").agg({"InvoiceDate" : lambda date : (today_date - date.max()).days,
                                     "Invoice" : lambda invoice : invoice.nunique(),
                                     "Total_Price" : lambda price : price.sum()
                                     })

# Değişken isimlerinin güncellenmesi
rfm.columns = ["Recency", "Frequency", "Monetary"]

rfm.reset_index(inplace=True)


# ---------------------------------------------------------------
# - 5. RFM Skorlarının Oluşturulması - (Calculating RFM Scores) -
# ---------------------------------------------------------------

rfm["Recency_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1])
rfm["Frequency_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["Monetary_Score"] = pd.qcut(rfm["Monetary"], 5, labels=[1, 2, 3, 4, 5])

# RF Skorlarının birleştirilmesi
rfm["RF_SCORE"] = rfm["Recency_Score"].astype(str) + rfm["Frequency_Score"].astype(str)

# ------------------------------------------------------------------------------------------------
# - 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi - (Creating & Analysing RFM Segments) -
# ------------------------------------------------------------------------------------------------

# Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlama ve  tanımlanan seg_map yardımı ile RF_SCORE'u segmentlere çevirme
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['SEGMENT'] = rfm['RF_SCORE'].replace(seg_map, regex=True)

# İlgili değişkenleri seçerek gereksiz değişkenlerden veri setimizi filtrelemiş oluyoruz.
rfm = rfm[["Customer ID", "RF_SCORE", "SEGMENT"]]

# "New_Customer" segmentine ait Customer ID'leri excel çıktısı alarak ilgili departmanla paylaşınız.
new_customer_df = pd.DataFrame(rfm[rfm["SEGMENT"] == "new_customers"])["Customer ID"]
new_customer_df.to_excel("New_Customers_ID_Bilgileri.xlsx")

