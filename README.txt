***Bu api api.covid19api.com adresindeki api'den aldığı verilerle Türkiye'deki günlük vaka sayısı artış yüzdesini ve genel istatistikleri elde etmek için tasarlanmıştır.***

Kurulum:
Herhangi bir şey kurmanıza gerek yoktur.

Çalıştırma ve Kullanım:

python path/to/api.py kullanımı ile api'yi çalıştırabilirsiniz. 
Server localhostta 127.0.0.1:8080 adresinde çalışmaktadır api'nin içerisinden bunu değiştirebilirsiniz.
Çalıştıktan sonra aşağıdaki isteklerde bulunabilirsiniz:

1.
GET / HTTP/1.1
Host: 127.0.0.1:8080
*Türkiye için gün gün güncel covid-19 genel istatistiklerini json formatında döner.

2.
GET /increaserate HTTP/1.1
Host: 127.0.0.1:8080
*Türkiye için gün gün güncel covid-19 vakası artış istatistiklerini json formatında döner.

3.
GET /increaserate?date=$yıl-ay-gün HTTP/1.1
Host: 127.0.0.1:8080
*Türkiye için verilen tarihteki covid-19 vakası artış istatistiğini json formatında döner.

4.
POST / HTTP/1.1
Host: 127.0.0.1:8080
*Türkiye için gün gün güncel covid-19 genel istatistiklerini json formatında döner.


5.
POST /increaserate HTTP/1.1
Host: 127.0.0.1:8080
*Türkiye için gün gün güncel covid-19 vakası artış istatistiklerini json formatında döner.

6.
POST /increaserate HTTP/1.1
Host: 127.0.0.1:8080
Content-Type: application/json

{"date":"2020-05-27"}
*Türkiye için verilen tarihteki covid-19 vakası artış istatistiğini json formatında döner.
