# Пример использования

В файле [ftpclient.py](ftpclient.py) находится пример использования пакета **ftpclient**.

Скрипт считывает конфигурацию FTP-клиента FileZilla и пытается подключиться к FTP-серверам.

После подключения к FTP-серверу совершается рекурсивный обход всех файлов и папок с выводом даты последнего изменения.

Примерный вывод скрипта:

```text
20180129111115 ftp://user:passwd@example.com:21/log
20180129111118 ftp://user:passwd@example.com:21/pear
20180129111115 ftp://user:passwd@example.com:21/tmp
20180129111209 ftp://user:passwd@example.com:21/webspace
20180129111116 ftp://user:passwd@example.com:21/webspace/certs
20180129111116 ftp://user:passwd@example.com:21/webspace/cgi-bin
20180129111116 ftp://user:passwd@example.com:21/webspace/cgi-bin/test.cgi
20180129111115 ftp://user:passwd@example.com:21/webspace/conf
20180129111117 ftp://user:passwd@example.com:21/webspace/error_docs
20180129111117 ftp://user:passwd@example.com:21/webspace/error_docs/400.html
20180129111117 ftp://user:passwd@example.com:21/webspace/error_docs/403.html
20180129111117 ftp://user:passwd@example.com:21/webspace/error_docs/404.html
20180129111117 ftp://user:passwd@example.com:21/webspace/error_docs/500.html
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/.protect
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/.protect/.pemhtaccess
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/1x1.gif
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/Thumbs.db
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/banner.gif
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/company_logo.gif
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/ie.css
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/index.html
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/index.html~
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/index.wml
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/logo.gif
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/logo.wbmp
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/poweredby_parallels.gif
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/readme.txt
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/style.css
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/top_bg.jpg
20180129111208 ftp://user:passwd@example.com:21/webspace/httpdocs/user.example.com/top_body_bg.jpg
20180129111116 ftp://user:passwd@example.com:21/webspace/httpdocs/1x1.gif
20180129111116 ftp://user:passwd@example.com:21/webspace/httpdocs/Thumbs.db
20180129111116 ftp://user:passwd@example.com:21/webspace/httpdocs/banner.gif
20180129111116 ftp://user:passwd@example.com:21/webspace/httpdocs/company_logo.gif
20180129111116 ftp://user:passwd@example.com:21/webspace/httpdocs/ie.css
20180129111116 ftp://user:passwd@example.com:21/webspace/httpdocs/index.html
20180129111116 ftp://user:passwd@example.com:21/webspace/httpdocs/index.wml
20180129111116 ftp://user:passwd@example.com:21/webspace/httpdocs/index.wml~
20180129111116 ftp://user:passwd@example.com:21/webspace/httpdocs/logo.gif
20180129111116 ftp://user:passwd@example.com:21/webspace/httpdocs/logo.wbmp
20180129111116 ftp://user:passwd@example.com:21/webspace/httpdocs/poweredby_parallels.gif
20180129111116 ftp://user:passwd@example.com:21/webspace/httpdocs/style.css
20180129111116 ftp://user:passwd@example.com:21/webspace/httpdocs/top_bg.jpg
20180129111116 ftp://user:passwd@example.com:21/webspace/httpdocs/top_body_bg.jpg
20180129111117 ftp://user:passwd@example.com:21/webspace/pd
20180129111115 ftp://user:passwd@example.com:21/webspace/siteapps
20180129111116 ftp://user:passwd@example.com:21/webspace/webstat
20180129111116 ftp://user:passwd@example.com:21/webspace/webstatssl
20180129111209 ftp://user:passwd@example.com:21/webspace/.htaccess
20180129111118 ftp://user:passwd@example.com:21/.pearrc
```
