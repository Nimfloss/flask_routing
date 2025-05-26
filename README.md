# TR
Bu dosya Flask ve Python ile oluşturulmuş bir backend internet sitesi routing dosyasıdır.
Bu dosya şu kütüphaneleri veya uygulamaları kullanır :

 - Python 3.10+
 - MySQL/PyMySQL  -> Veritabanı için
 - WTForms        -> Form altyapısı için
 - passlib        -> Şifre yönetimi altyapısı için
 - emailvalidator -> Eposta geçerlilik kontrolü için
 - flask          -> Site yönetimi için
 - functools

 - Not : Apache kullanarak yayınlama işlemi yapılabilir.

Not : Uygulama debug=true olarak başlatılıyor 262. ve 263. satırlar.

Not : /template klasörü tamamen boştur ve içinde herhangi bir .html dosyası bulunmamaktadır.
Routing ile ilişkilendirilmiş dosyaları kendiniz oluşturup kullanabilirsiniz veya uzantıları değiştirebilirsiniz.

Uyarı : 108. Satırda insert komutunda name,email,username değerleri alınırken password değeri alınmamaktadır.
Bu sizin MySQL yapılandırmanıza göre hata verebilir de vermeyebilir de eğer MySQL hatası alırsanız bu satırı incelemeniz gerekebilir!

Not : Makaleler /makale olarak direkt görüntülenebilir. Bunu güvenlik açığı olarak düşünebilirsiniz. Üstünde değiştirme yapılabilir.

Python'da gerekli libleri şu kodu kullanarak direkt kurabilirsiniz:
pip install -r requirements.txt
Bu kod requirements.txt içindeki libleri direkt olarak venv veya environment Python'unuza yükler.
Kontrol edebilirsiniz.



# EN
This file is a backend website routing script developed using Flask and Python.
The following libraries and tools are used in this project:

 - Python 3.10+
 - MySQL / PyMySQL -> For database integration
 - WTForms -> For form infrastructure and validation
 - passlib -> For password encryption and security
 - email_validator -> For validating email addresses
 - Flask -> For web application routing and server logic
 - functools-> Used for decorators (@wraps) in session management

 - Note : Publishing can be done using Apache.

Note : The application is started with debug=true lines 262 and 263.

Note : The /template folder is completely empty and does not contain any .html files.
You can create and use the files associated with Routing yourself or change the extensions.

Warning : In line 108, the insert command takes name, email, username values but not password value.
This may or may not give an error depending on your MySQL configuration. If you get a MySQL error, you may need to examine this line!

Note : Articles can be displayed directly as /article. You can consider this as a security vulnerability. Changes can be made on it.

You can install the necessary libs for Python directly using this code:
pip install -r requirements.txt
This code loads the libs in requirements.txt directly into your venv or environment Python.
You can check it if you want.
