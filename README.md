# Movie Index - An IR system for IMDB movie information 
## Team
 - Leo Li
 - Yvonne Ding
 - Shuyi Liu
 - Baoyan Deng
 - Zhijun Zeng
## Description of this project
This is an implementation of a simple search engine acting as the fulfilment of the CW3 of module ***[INFR11145 Text Technologies for Data Science](https://www.inf.ed.ac.uk/teaching/courses/tts)***.

## Naive version of the instruction of deployment(TODO to be completed):

### for Debian11:
apt update\
curl -fsSL https://deb.nodesource.com/setup_19.x | sudo -E bash -\
apt install nodejs python3-pip git screen\
mkdir /var/www\
chmod 755 /var/www\
cd /var/www\
git clone https://github.com/pokaleo/Movie-Index.git \
cd Movie-Index/Code\
pip install -r requirements.txt\
mv Configs/gunicorn.service /etc/systemd/system/gunicorn.service\
systemctl daemon-reload\
systemctl start gunicorn\
cd Frontend\
npm install\
screen -d -m npm run dev\
**Now the service should be able to be accessed via ip:3000**

***Optional**: Use nginx as a reverse proxy and enable SSL for the site:*
apt install nginx
mv ../Configs/search-engine.conf /etc/nginx/sites-enabled/search-engine.conf\
mv ../Configs/doc.conf /etc/nginx/sites-enabled/doc.conf\
pip install pyopenssl --upgrade\
apt install certbot python3-certbot-nginx\
certbot --nginx -d movieindex.me -d www.movieindex.me\
certbot --nginx -d doc.movieindex.me
systemctl restart nginx\









gunicorn --bind 0.0.0.0:8800 --timeout 600 WSGI:app --preload -k gevent -c ../Configs/GunicornConf.py
gunicorn --bind 0.0.0.0:8800 -c ../Configs/GunicornConf.py WSGI:app



Code/Frontend npm dev run

**To be updated..**


