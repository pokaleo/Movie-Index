# Movie Index - An IR system for IMDB movie information 
## Team
 - Leo Li -- *Dev Team lead*
 - Yvonne Ding -- *Web Scraping*
 - Shuyi Liu -- *Frontend*
 - Baoyan Deng
 - Zhijun Zeng
## Description of this project (To be completed)
This is an advanced movie search engine serving as the fulfilment of the CW3 of module ***[INFR11145 Text Technologies for Data Science](https://www.inf.ed.ac.uk/teaching/courses/tts)***.

## Instruction of deployment:

### For Debian11 (Hosting as a web service):
```
apt update
curl -fsSL https://deb.nodesource.com/setup_19.x | sudo -E bash -
apt install nodejs python3-pip git screen
mkdir /var/www
chmod 755 /var/www
cd /var/www
git clone https://github.com/pokaleo/Movie-Index.git
cd Movie-Index/Code
pip install -r requirements.txt
mv Configs/gunicorn.service /etc/systemd/system/gunicorn.service
systemctl daemon-reload
systemctl start gunicorn
cd Frontend
npm install
screen -d -m npm run dev
```
**Now the service should be able to be accessed via ip:3000**

***Optional**: Use nginx as a reverse proxy and enable SSL for the site:*\
```
apt install nginx
mv ../Configs/search-engine.conf /etc/nginx/sites-enabled/search-engine.conf
mv ../Configs/doc.conf /etc/nginx/sites-enabled/doc.conf
pip install pyopenssl --upgrade
apt install certbot python3-certbot-nginx
certbot --nginx -d movieindex.me -d www.movieindex.me
certbot --nginx -d doc.movieindex.me
systemctl restart nginx
```

### General Guideline:
1. Retrieving this project by either direct downloading or git clone
2. Installing dependencies listed in ```/Code/requirements.txt```
3. Installing npm and NodeJs
4. Using npm to install frontend dependencies and run frontend - eg(in the directory of /Code/Frontend): 1. ``` npm install```  2. ``` npm run dev ```
5. Launching the backend either directly using ```/Code/Backend/routes.py``` or using Gunicorn as WSGI. The entry point of Gunicorn is located at ```/Code/Backend/WSGI.py``` and example configuration is included in ```/Code/Backend/ConfigsGunicornConf.py```
6. Example of running Gunicorn in Linux/Macos : ``` gunicorn --bind 0.0.0.0:8800 -c ../Configs/GunicornConf.py WSGI:app ```

**To be updated..**


